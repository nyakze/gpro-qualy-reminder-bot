import json
import logging
import re
import os
import asyncio
import tempfile
from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo
import aiohttp
from config import GPRO_API_TOKEN, CALENDAR_FILE, GPRO_API_LANG, NEXT_SEASON_FILE

logger = logging.getLogger(__name__)

# Module-level globals
race_calendar: dict = {}
next_season_calendar: dict = {}

# Date parsing formats (in order of priority)
DATE_FORMATS = [
    "%d.%m %Y",  # 05.12 2025
    "%b %d, %Y",
    "%b %d %Y",
    "%d %b %Y",
    "%Y-%m-%d",
    "%d.%m.%Y",
]

# Race timing constants
# GPRO races are at 20:00 CET/CEST (Europe/Paris timezone)
# CET (winter, UTC+1): 20:00 CET = 19:00 UTC
# CEST (summer, UTC+2): 20:00 CEST = 18:00 UTC
RACE_START_HOUR_CET = 20  # Races start at 20:00 CET/CEST
RACE_START_MINUTE_CET = 0
QUALI_CLOSES_BEFORE_RACE_HOURS = 1.5  # Quali closes 1.5 hours before race
GPRO_TIMEZONE = ZoneInfo("Europe/Paris")  # CET/CEST timezone

# Season transition constants
PREFETCH_DAYS_BEFORE_SEASON = 4  # Fetch next season calendar 4 days before first race
# CRITICAL: Wait until AFTER all notifications are sent
# Replay/results notifications: sent immediately after race
# We transition at 4h to ensure everything is complete and avoid conflicts
SEASON_TRANSITION_HOURS_AFTER_RACE = 4.0  # Transition 4 hours after last race


def get_race_time_in_utc(race_date: datetime) -> datetime:
    """Convert race time from CET/CEST to UTC based on DST.

    Args:
        race_date: Naive datetime with just the date (time will be set)

    Returns:
        datetime: Race time in UTC timezone-aware format
    """
    # Create race time in CET/CEST timezone
    race_time_cet = race_date.replace(
        hour=RACE_START_HOUR_CET, minute=RACE_START_MINUTE_CET, second=0, microsecond=0
    )

    # Localize to CET/CEST (handles DST automatically)
    race_time_cet = race_time_cet.replace(tzinfo=GPRO_TIMEZONE)

    # Convert to UTC and return as timezone-aware datetime
    race_time_utc = race_time_cet.astimezone(ZoneInfo("UTC"))
    return race_time_utc


def _load_calendar_from_file(filepath: str) -> dict:
    """Generic calendar loader from JSON file

    Returns:
        dict: Calendar data with datetime objects, or empty dict on error
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            calendar = {}
            for race_id_str, race_data in data.items():
                race_id = int(race_id_str)
                race_entry = {
                    "quali_close": datetime.fromisoformat(
                        race_data["quali_close"]
                    ).replace(tzinfo=UTC),
                    "track": race_data["track"],
                    "date": datetime.fromisoformat(race_data["date"]).replace(
                        tzinfo=UTC
                    ),
                    "group": race_data.get("group", "Pro"),
                }

                # Load weather data if available
                if "weather" in race_data:
                    race_entry["weather"] = race_data["weather"]

                calendar[race_id] = race_entry
            return calendar
    except FileNotFoundError:
        logger.warning(f"No cache file: {filepath}")
        return {}
    except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
        logger.error(f"Cache load error from {filepath}: {e}")
        return {}


def _save_calendar_to_file(calendar: dict, filepath: str):
    """Generic calendar saver to JSON file with atomic write

    Args:
        calendar: Calendar dict with datetime objects
        filepath: Target file path

    Raises:
        Exception: If save fails
    """
    serializable = {}
    for k, v in calendar.items():
        race_data = {
            "quali_close": v["quali_close"].isoformat(),
            "track": v["track"],
            "date": v["date"].isoformat(),
            "group": v["group"],
        }

        # Include weather data if available
        if "weather" in v:
            race_data["weather"] = v["weather"]

        serializable[str(k)] = race_data

    temp_file = None
    try:
        # Use unique temp file to avoid race conditions
        fd, temp_file = tempfile.mkstemp(dir=os.path.dirname(filepath), suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(serializable, f, indent=2)
                f.flush()
                os.fsync(f.fileno())

            os.replace(temp_file, filepath)
            logger.debug(f"💾 Saved calendar to {filepath}")
        except Exception:
            # Close the fd if it wasn't closed by os.fdopen
            try:
                os.close(fd)
            except (OSError, ValueError):
                pass
            raise
    except Exception as e:
        logger.error(f"Failed to save calendar to {filepath}: {e}")
        raise
    finally:
        # Clean up temp file if it still exists
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


async def load_calendar_silent() -> bool:
    """Load from cache ONLY - no API calls"""
    calendar = _load_calendar_from_file(CALENDAR_FILE)
    if calendar:
        global race_calendar
        race_calendar.clear()
        race_calendar.update(calendar)
        logger.debug(f"✅ Loaded {len(calendar)} races from cache")
        return True
    return False


async def load_next_season_silent() -> bool:
    """Load next season from cache ONLY"""
    if not os.path.exists(NEXT_SEASON_FILE):
        return False

    calendar = _load_calendar_from_file(NEXT_SEASON_FILE)
    if calendar:
        global next_season_calendar
        next_season_calendar.clear()
        next_season_calendar.update(calendar)
        logger.debug(f"✅ Loaded {len(calendar)} next season races from cache")
        return True
    return False


async def update_calendar() -> bool:
    """Update calendar from GPRO API - /update command"""
    if not GPRO_API_TOKEN:
        logger.error("❌ GPRO_API_TOKEN missing")
        return False

    url = f"https://gpro.net/{GPRO_API_LANG}/backend/api/v2/Calendar"
    headers = {
        "Authorization": f"Bearer {GPRO_API_TOKEN}",
        "User-Agent": "GPRO-QualiBot/1.0",
    }

    try:
        logger.info("🔄 Updating calendar from GPRO API...")
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    raw_response = await resp.json()

                    # CURRENT SEASON
                    data = raw_response.get("events", [])
                    calendar = parse_gpro_events(data, is_next_season=False)

                    if calendar:
                        save_calendar(calendar)
                        global race_calendar
                        race_calendar.clear()
                        race_calendar.update(calendar)
                        logger.info(f"✅ CURRENT SEASON: {len(calendar)} races!")
                    else:
                        logger.warning("No valid race events found")

                    # NEXT SEASON LOGIC
                    next_season_published = raw_response.get(
                        "nextSeasonPublished", False
                    )
                    logger.info(f"📊 API nextSeasonPublished: {next_season_published}")

                    if next_season_published:
                        next_events = raw_response.get("nextSeasonEvents", [])
                        logger.info(f"📊 Found {len(next_events)} nextSeasonEvents")

                        if next_events:
                            next_calendar = parse_gpro_events(
                                next_events, is_next_season=True
                            )
                            if next_calendar:
                                save_next_season_calendar(next_calendar)
                                global next_season_calendar
                                next_season_calendar.clear()
                                next_season_calendar.update(next_calendar)
                                logger.info(
                                    f"🌟 NEXT SEASON: {len(next_calendar)} races populated!"
                                )
                            else:
                                logger.warning("No valid next season events")
                        else:
                            logger.warning(
                                "nextSeasonPublished=true but no nextSeasonEvents"
                            )
                    else:
                        # FORCE CLEANUP
                        next_season_calendar.clear()

                        if os.path.exists(NEXT_SEASON_FILE):
                            os.remove(NEXT_SEASON_FILE)
                            logger.info(
                                "🗑️ Next season file REMOVED - API says not published"
                            )
                        else:
                            logger.info("ℹ️ No next season file (already clean)")

                    return True
                else:
                    logger.error(f"API {resp.status}")
    except asyncio.TimeoutError:
        logger.warning("Calendar API timeout")
    except aiohttp.ClientError as e:
        logger.error(f"Calendar API client error: {e}")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"Calendar API response error: {e}")

    return False


def parse_gpro_events(events: list, is_next_season: bool = False) -> dict:
    """Parse GPRO events - SEQUENTIAL RACE NUMBERS 1,2,3...!"""
    calendar = {}
    valid_races = []
    season_type = "🌟 NEXT" if is_next_season else "✅ CURRENT"

    # **1. COLLECT ALL valid races first**
    for event in events:
        if event.get("eventType") != "R":  # Race only
            continue

        idx = event.get("idxReal") or event.get("idx")
        if not idx:
            continue

        date_str = event.get("dateEvent")
        track = event.get("trackName", f"Race {idx}")

        try:
            race_date = parse_gpro_date_fixed(date_str)
            if not race_date:
                continue

            # Set race start time (convert from CET/CEST to UTC)
            race_date = get_race_time_in_utc(race_date)
            quali_close = race_date - timedelta(hours=QUALI_CLOSES_BEFORE_RACE_HOURS)

            valid_races.append(
                {
                    "orig_id": int(idx),
                    "quali_close": quali_close,
                    "track": track[:30],
                    "date": race_date,
                    "group": event.get("group", "Pro"),
                }
            )
        except (ValueError, TypeError, AttributeError) as e:
            logger.debug(f"Parse event {idx} error: {e}")
            continue

    # **2. SORT by date + RE-NUMBER 1,2,3...**
    valid_races.sort(key=lambda x: x["date"])

    for seq_num, race_data in enumerate(valid_races, 1):
        calendar[seq_num] = {
            "quali_close": race_data["quali_close"],
            "track": race_data["track"],
            "date": race_data["date"],
            "group": race_data["group"],
        }
        # Log with actual UTC time (varies by CET/CEST)
        utc_time_str = race_data["date"].strftime("%d.%m %Y %H:%M UTC")
        logger.info(
            f"{season_type} Race {seq_num}: {race_data['track']} → {utc_time_str} (20:00 CET/CEST)"
        )

    logger.info(
        f"{season_type} Parsed {len(calendar)} sequential race events at 20:00 CET/CEST"
    )
    return calendar


def parse_gpro_date_fixed(date_str: str) -> datetime | None:
    """Parse GPRO dates - Simple 'Today' handler!"""
    if not date_str:
        return None

    # Skip obvious placeholder values (e.g., "-", "TBD", "N/A")
    if date_str.strip() in ["-", "TBD", "N/A", ""]:
        return None

    # **SIMPLE "Today" = CURRENT DAY 00:00**
    if "Today" in date_str or "<font" in date_str or "<b>" in date_str:
        now = datetime.now(UTC)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.info(f"⏰ 'Today' → {today.strftime('%d.%m.%Y')} 20:00 CET/CEST")
        return today

    # **CLEAN HTML + ordinals**
    day_str = re.sub(r"<[^>]*>", "", date_str)
    day_str = re.sub(r"(?i)(st|nd|rd|th)\b", "", day_str)
    day_str = day_str.strip()

    now = datetime.now(UTC)

    # Try all standard date formats
    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(day_str, fmt)
            if dt.year < 2025:
                dt = dt.replace(year=now.year)
            return dt.replace(tzinfo=UTC)
        except ValueError:
            continue

    # Month/day only
    if not re.search(r"\d{4}", day_str):
        try:
            dt = datetime.strptime(day_str, "%b %d")
            dt = dt.replace(year=now.year)
            if dt.date() < now.date():
                dt = dt.replace(year=now.year + 1)
            return dt.replace(tzinfo=UTC)
        except (ValueError, AttributeError) as e:
            logger.debug(f"Failed to parse date format '{day_str}': {e}")
            pass

    logger.warning(f"Cannot parse date: '{date_str}'")
    return None


def save_calendar(calendar: dict):
    """Save current season calendar with atomic write to prevent corruption"""
    _save_calendar_to_file(calendar, CALENDAR_FILE)


def save_next_season_calendar(calendar: dict):
    """Save next season calendar with atomic write to prevent corruption"""
    _save_calendar_to_file(calendar, NEXT_SEASON_FILE)


async def check_quali_status_from_api() -> dict:
    """Check real-time qualification status from GPRO /office endpoint

    Returns:
        dict: {race_id: seconds_left_quali} for races with active quali, empty dict on error
    """
    if not GPRO_API_TOKEN:
        return {}

    url = f"https://gpro.net/{GPRO_API_LANG}/backend/api/v2/office"
    headers = {
        "Authorization": f"Bearer {GPRO_API_TOKEN}",
        "User-Agent": "GPRO-QualiBot/1.0",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    seconds_left = data.get("secondsLeftQual")

                    if seconds_left and int(seconds_left) > 0:
                        # Figure out which race this quali is for
                        # by matching quali close time
                        seconds = int(seconds_left)
                        now = datetime.now(UTC)
                        expected_close = now + timedelta(seconds=seconds)

                        # Find matching race (within 1 hour tolerance)
                        for race_id, race_data in race_calendar.items():
                            time_diff = abs(
                                (
                                    race_data["quali_close"] - expected_close
                                ).total_seconds()
                            )
                            if time_diff < 7200:  # Within 2 hours
                                logger.info(
                                    f"✅ API: Race {race_id} quali open, {seconds//3600}h remaining"
                                )
                                return {race_id: seconds}

                        logger.debug(
                            f"API returned secondsLeftQual={seconds} but no matching race found"
                        )
                    else:
                        logger.debug("API: No active qualification")
                    return {}
                else:
                    logger.warning(f"Office API returned {resp.status}")
                    return {}
    except asyncio.TimeoutError:
        logger.warning("Office API timeout")
        return {}
    except aiohttp.ClientError as e:
        logger.error(f"Office API client error: {e}")
        return {}
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        logger.error(f"Office API response error: {e}")
        return {}


async def fetch_weather_from_api(race_id: int) -> dict:
    """Fetch weather data from GPRO Practice API for a specific race

    Args:
        race_id: Race ID to fetch weather for

    Returns:
        dict: Weather data with parsed info, or empty dict on error
    """
    if not GPRO_API_TOKEN:
        logger.warning("Cannot fetch weather: GPRO_API_TOKEN missing")
        return {}

    url = f"https://gpro.net/{GPRO_API_LANG}/backend/api/v2/Practice"
    headers = {
        "Authorization": f"Bearer {GPRO_API_TOKEN}",
        "User-Agent": "GPRO-QualiBot/1.0",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    # Extract just the weather data from the response
                    weather_data = data.get("weather", {})

                    if weather_data:
                        logger.info(
                            f"🌤️ Weather API: Successfully fetched data for race {race_id}"
                        )
                        # Store weather data in race_calendar
                        if race_id in race_calendar:
                            race_calendar[race_id]["weather"] = weather_data
                            # Save to file to persist weather across restarts
                            save_calendar(race_calendar)
                            logger.debug(
                                f"Weather data persisted to file for race {race_id}"
                            )
                    else:
                        logger.warning(
                            f"Weather API returned data but no 'weather' key found for race {race_id}"
                        )

                    return weather_data
                else:
                    logger.warning(f"Weather API returned {resp.status}")
                    return {}
    except asyncio.TimeoutError:
        logger.warning("Weather API timeout")
        return {}
    except aiohttp.ClientError as e:
        logger.error(f"Weather API client error: {e}")
        return {}
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"Weather API response error: {e}")
        return {}


async def check_race_replay_api(race_id: int) -> bool:
    """Check if a specific race has been calculated using RaceReplay API

    This is especially important for the last race (race 17) where qualification
    doesn't open afterwards due to season break, so we can't rely on the /office
    endpoint to detect when the race is complete.

    Args:
        race_id: Race ID to check (1-17)

    Returns:
        bool: True if API returns the requested race number (race is calculated)
    """
    if not GPRO_API_TOKEN:
        logger.warning("Cannot check race replay: GPRO_API_TOKEN missing")
        return False

    url = f"https://gpro.net/{GPRO_API_LANG}/backend/api/v2/RaceReplay"
    headers = {
        "Authorization": f"Bearer {GPRO_API_TOKEN}",
        "User-Agent": "GPRO-QualiBot/1.0",
    }

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    api_race_nb = data.get("raceNb")

                    if api_race_nb:
                        try:
                            api_race_id = int(api_race_nb)
                            if api_race_id == race_id:
                                logger.info(
                                    f"✅ RaceReplay API: Race {race_id} is calculated and available"
                                )
                                return True
                            else:
                                logger.debug(
                                    f"RaceReplay API: Expected race {race_id}, got race {api_race_id}"
                                )
                                return False
                        except (ValueError, TypeError):
                            logger.warning(
                                f"RaceReplay API returned non-integer raceNb: {api_race_nb}"
                            )
                            return False
                    else:
                        logger.debug("RaceReplay API: No raceNb in response")
                        return False
                else:
                    logger.warning(f"RaceReplay API returned {resp.status}")
                    return False
    except asyncio.TimeoutError:
        logger.warning("RaceReplay API timeout")
        return False
    except aiohttp.ClientError as e:
        logger.error(f"RaceReplay API client error: {e}")
        return False
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.error(f"RaceReplay API response error: {e}")
        return False


def get_races_closing_soon(hours_before: float = 720) -> list:
    """Get races closing within 30 days - SORTED by time!"""
    now = datetime.now(UTC)
    upcoming = {}

    for race_id, data in race_calendar.items():
        time_to_close = (data["quali_close"] - now).total_seconds() / 3600
        if 0 < time_to_close <= hours_before:
            data_copy = data.copy()
            data_copy["hours_left"] = time_to_close
            upcoming[race_id] = data_copy

    # Sort by closest first and convert to list of tuples
    sorted_items = sorted(upcoming.items(), key=lambda x: x[1]["hours_left"])
    sorted_upcoming = [
        (data["hours_left"], race_id, data) for race_id, data in sorted_items
    ]
    if sorted_upcoming:
        race_ids = [race_id for _, race_id, _ in sorted_upcoming]
        logger.debug(f"Tracking quali deadlines: {race_ids}")
    else:
        # Find when next race enters the tracking window
        future_races = [
            (rid, d) for rid, d in race_calendar.items() if d["quali_close"] > now
        ]
        if future_races:
            next_race_id, next_race_data = min(
                future_races, key=lambda x: x[1]["quali_close"]
            )
            hours_until_close = (
                next_race_data["quali_close"] - now
            ).total_seconds() / 3600
            tracking_starts_in = hours_until_close - hours_before
            logger.debug(
                f"No races in {hours_before:.0f}h window. "
                f"Race {next_race_id} enters tracking in {tracking_starts_in:.1f}h"
            )
    return sorted_upcoming


def get_last_race_id() -> int:
    """Get the ID of the last race in the current season

    Returns:
        int: Last race ID, or 0 if no races
    """
    if not race_calendar:
        return 0
    return max(race_calendar.keys())


def get_first_race_date() -> datetime:
    """Get the date of the first race in the current season

    Returns:
        datetime: First race date, or None if no races
    """
    if not race_calendar:
        return None

    first_race_id = min(race_calendar.keys())
    return race_calendar[first_race_id]["date"]


def should_trigger_season_transition(now: datetime) -> bool:
    """Check if we should trigger season transition (last race concluded + ALL notifications sent)

    CRITICAL: This waits until 4 hours after the last race to ensure:
    - Race replay/results notifications sent (immediately after race)
    - All notification windows complete before transitioning
    - No conflicts with any race-related notifications

    Timeline example for Race 17 (last race) at 20:00:
    - 20:00: Race 17 finishes
    - 20:05: Replay/results notifications sent
    - 00:00: Season transition occurs (4.0h) ✓ SAFE

    Note: Race 1 quali does NOT open after Race 17 - there's a season break

    Args:
        now: Current datetime

    Returns:
        bool: True once at least 4h have passed after the last race and we have
        next season data
    """
    if not race_calendar or not next_season_calendar:
        return False

    last_race_id = get_last_race_id()
    last_race_time = race_calendar[last_race_id]["date"]

    # Calculate hours since last race ended
    hours_since_race = (now - last_race_time).total_seconds() / 3600

    # Target: 4 hours after race (ensures all notifications sent)
    # We wait until 4 hours to ensure everything is done
    target_hours = SEASON_TRANSITION_HOURS_AFTER_RACE
    # Keep returning True after the threshold so a restart or temporary outage
    # cannot permanently miss the transition.
    if hours_since_race >= target_hours:
        logger.info(
            f"🔄 Season transition conditions met: {hours_since_race:.2f}h after last race "
            f"(all notifications sent)"
        )
        return True

    return False


def should_prefetch_next_season(now: datetime) -> bool:
    """Check if we should poll for the next season calendar.

    GPRO does not expose the next season's first-race date until the next-season
    calendar is published. Start polling shortly before the current season's
    final race and continue until the API supplies next-season data.

    Args:
        now: Current datetime

    Returns:
        bool: True if we should fetch next season calendar
    """
    if not race_calendar:
        return False

    # Don't prefetch if we already have next season data
    if next_season_calendar:
        logger.debug("Next season calendar already exists, skipping prefetch")
        return False

    last_race_id = get_last_race_id()
    if not last_race_id:
        return False

    last_race_date = race_calendar[last_race_id]["date"]
    days_until_last_race = (last_race_date - now).total_seconds() / (24 * 3600)

    if days_until_last_race <= PREFETCH_DAYS_BEFORE_SEASON:
        logger.info(
            f"📅 Next-season polling active: {days_until_last_race:.2f} days "
            "until current season's final race"
        )
        return True

    return False


async def transition_to_next_season() -> bool:
    """Transition from current season to next season

    This function:
    1. Replaces gpro_calendar.json with next_season_calendar.json
    2. Deletes next_season_calendar.json
    3. Updates in-memory race_calendar

    Returns:
        bool: True if transition successful, False otherwise
    """
    global race_calendar, next_season_calendar

    if not next_season_calendar:
        logger.error("❌ Cannot transition: no next season calendar available")
        return False

    try:
        logger.info("🔄 Starting season transition...")

        # Save next season as current season
        save_calendar(next_season_calendar)
        logger.info(
            f"✅ Saved next season as current season ({len(next_season_calendar)} races)"
        )

        # Update in-memory calendar
        race_calendar.clear()
        race_calendar.update(next_season_calendar)

        # Clear next season
        next_season_calendar.clear()

        # Delete next season file
        if os.path.exists(NEXT_SEASON_FILE):
            os.remove(NEXT_SEASON_FILE)
            logger.info("🗑️ Deleted next_season_calendar.json")

        logger.info("🎉 Season transition completed successfully!")
        return True

    except (OSError, IOError, json.JSONDecodeError) as e:
        logger.error(f"❌ Season transition failed: {e}")
        return False

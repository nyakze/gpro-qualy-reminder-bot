"""Main notification checking loop and helper functions"""

import asyncio
import json
import logging
import os
import tempfile
from datetime import datetime, timedelta, UTC
from typing import Dict, Tuple

from aiogram import Bot

from gpro_calendar import (
    get_races_closing_soon,
    race_calendar,
    check_quali_status_from_api,
    fetch_weather_from_api,
    should_trigger_season_transition,
    should_prefetch_next_season,
    transition_to_next_season,
    update_calendar,
)
from .user_data import (
    users_data,
    is_notification_enabled,
    is_user_blocked,
    load_users_data,
)
from .sender import (
    send_notification_to_user,
)
from infra.logging import log_structured

logger = logging.getLogger(__name__)

# Check intervals (adaptive based on race proximity)
CHECK_INTERVAL_NORMAL_SECONDS = 5 * 60  # 5 minutes
CHECK_INTERVAL_FAST_SECONDS = 60  # 1 minute (when approaching race time)
CHECK_INTERVAL_CLOSING_HOURS = 3  # Switch to fast mode when within this many hours

# API check constants for quali open notifications
API_CHECK_START_HOURS = 2.0  # Start checking API 2 hours after race
API_CHECK_END_HOURS = 3.5  # Fallback after 3.5 hours if API doesn't detect
API_CHECK_INTERVAL_MINUTES = 10  # Rate limit: check API every 10 minutes max
FALLBACK_TOLERANCE_MINUTES = 10  # Allow fallback within 10 minutes of window end

# Season transition tracking
last_season_transition_check = None
SEASON_CHECK_INTERVAL_HOURS = 1  # Check season transition conditions every hour
last_prefetch_check = None

# Notification history retention
NOTIFICATION_HISTORY_RETENTION_HOURS = 24 * 30  # 30 days
MAX_HISTORY_SIZE = 10000  # Maximum entries to prevent unbounded growth

# Module-level in-memory caches (lazy loaded)
notify_history: Dict[Tuple[int, str], datetime] = {}
notification_lock = asyncio.Lock()


def _enforce_history_size_limit(
    history: Dict[Tuple[int, str], datetime],
) -> Dict[Tuple[int, str], datetime]:
    """Enforce size limit on notification history to prevent memory leaks

    If history exceeds MAX_HISTORY_SIZE, remove oldest entries.
    """
    if len(history) <= MAX_HISTORY_SIZE:
        return history

    # Sort by timestamp and keep most recent entries
    sorted_items = sorted(history.items(), key=lambda x: x[1], reverse=True)
    trimmed_history = dict(sorted_items[:MAX_HISTORY_SIZE])

    removed_count = len(history) - len(trimmed_history)
    logger.warning(
        f"Notification history exceeded limit ({len(history)} > {MAX_HISTORY_SIZE}), "
        f"removed {removed_count} oldest entries"
    )

    return trimmed_history


def _get_history_file_path() -> str:
    """Get the path for the notification history file"""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notification_history.json",
    )


def load_notify_history() -> Dict[Tuple[int, str], datetime]:
    """Load notification history from file"""
    history_file = _get_history_file_path()
    history: Dict[Tuple[int, str], datetime] = {}

    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert from JSON format: list of [race_id, label, timestamp]
                for item in data:
                    if len(item) == 3:
                        race_id, label, timestamp_str = item
                        try:
                            history[(int(race_id), label)] = datetime.fromisoformat(
                                timestamp_str
                            )
                        except (ValueError, TypeError):
                            continue
            logger.info(f"✅ Loaded {len(history)} notification history entries")
        except (json.JSONDecodeError, IOError, OSError) as e:
            logger.error(f"Failed to load notification history: {e}")

    return history


def save_notify_history() -> None:
    """Save notification history to file"""
    history_file = _get_history_file_path()

    try:
        # Convert to JSON-serializable format: list of [race_id, label, timestamp]
        data = [
            [race_id, label, timestamp.isoformat()]
            for (race_id, label), timestamp in notify_history.items()
        ]

        # Atomic write
        fd, temp_path = tempfile.mkstemp(
            dir=os.path.dirname(history_file), suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, history_file)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

        logger.debug(f"Saved {len(data)} notification history entries")
    except (IOError, OSError) as e:
        logger.error(f"Failed to save notification history: {e}")


def _is_already_notified(race_id: int, label: str) -> bool:
    """Check if a notification was already sent (with history cleanup)"""
    global notify_history

    history_key = (race_id, label)
    if history_key not in notify_history:
        return False

    # Check if entry is older than retention period
    cutoff = datetime.now(UTC) - timedelta(hours=NOTIFICATION_HISTORY_RETENTION_HOURS)
    if notify_history[history_key] < cutoff:
        # Clean up old entry
        del notify_history[history_key]
        return False

    return True


def _mark_notified(race_id: int, label: str) -> None:
    """Mark a notification as sent with current timestamp"""
    global notify_history
    notify_history[(race_id, label)] = datetime.now(UTC)

    # Enforce size limit
    notify_history = _enforce_history_size_limit(notify_history)


async def _fetch_weather_with_retry(race_id: int) -> None:
    """Fetch weather data for a race with retry logic

    Args:
        race_id: The race ID to fetch weather for
    """
    # Skip if already fetched
    if "weather" in race_calendar[race_id]:
        return

    # First attempt
    weather_data = await fetch_weather_from_api(race_id)

    # Retry once if failed
    if not weather_data:
        logger.warning(f"First weather fetch failed for race {race_id}, retrying...")
        await asyncio.sleep(2)
        weather_data = await fetch_weather_from_api(race_id)

        if not weather_data:
            logger.warning(f"Weather fetch failed for race {race_id} after retry")


def _check_quali_closing_notifications(now: datetime, races_closing: list) -> list:
    """Check for qualification deadlines approaching

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for hours_remaining, race_id, race_data in races_closing:
        # Determine notification label based on time remaining
        if hours_remaining <= 0.17:  # ~10 minutes
            label = "10min"
        elif hours_remaining <= 2:
            label = "2h"
        elif hours_remaining <= 24:
            label = "24h"
        elif hours_remaining <= 48:
            label = "48h"
        elif hours_remaining <= 72:
            label = "72h"
        else:
            continue

        # Check already notified
        if _is_already_notified(race_id, label):
            continue

        history_key = (race_id, label)
        notifications.append(("closing", race_id, race_data, label, history_key))

    return notifications


def _get_next_check_interval(now: datetime) -> int:
    """Determine the next check interval based on race proximity

    Uses fast mode (60s) when approaching race time, normal mode (5min) otherwise.

    Args:
        now: Current datetime

    Returns:
        int: Seconds to wait before next check
    """
    from notifications.user_data import get_all_active_snoozes

    # Check if any snoozes are within 10 minutes of firing
    active_snoozes = get_all_active_snoozes()
    for snooze in active_snoozes:
        snooze_time = datetime.fromisoformat(snooze["snooze_time"])
        minutes_until = (snooze_time - now).total_seconds() / 60

        # If snooze is within 10 minutes (and hasn't passed), use fast mode
        if 0 < minutes_until <= 10:
            return CHECK_INTERVAL_FAST_SECONDS

    # Check if any race is closing within the threshold
    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]
        hours_until = (quali_close - now).total_seconds() / 3600

        if 0 < hours_until <= CHECK_INTERVAL_CLOSING_HOURS:
            return CHECK_INTERVAL_FAST_SECONDS

    # Check if any qualification just opened (within last 4 hours)
    for race_id, race_data in race_calendar.items():
        # Skip race 1 - no previous race
        if race_id == 1:
            continue

        # Get previous race end time
        prev_race_id = race_id - 1
        if prev_race_id not in race_calendar:
            continue

        prev_race_time = race_calendar[prev_race_id]["date"]
        hours_since = (now - prev_race_time).total_seconds() / 3600

        # If within 4 hours of previous race ending, we're in quali open window
        if 0 <= hours_since <= 4:
            return CHECK_INTERVAL_FAST_SECONDS

    return CHECK_INTERVAL_NORMAL_SECONDS


def _get_races_for_polling(now: datetime) -> list:
    """Get races that are in the API polling window (2-3.5 hours after previous race)

    IMPORTANT: Skips race_id=1 because Race 1 quali doesn't open after the
    last race of previous season - there's a season break.

    Args:
        now: Current datetime

    Returns:
        list: Races to check via API [(race_id, race_data, prev_race_id, hours_since), ...]
    """
    races = []

    for race_id, race_data in race_calendar.items():
        # Skip race 1 - no previous race in same season (season break)
        if race_id == 1:
            continue

        # Check if already notified
        history_key = (race_id, "opens_soon")
        if history_key in notify_history:
            continue

        # Find previous race
        prev_race_id = race_id - 1
        if prev_race_id not in race_calendar:
            continue

        prev_race_time = race_calendar[prev_race_id]["date"]
        hours_since_race = (now - prev_race_time).total_seconds() / 3600

        # Check if we're in the API polling window
        if API_CHECK_START_HOURS <= hours_since_race <= API_CHECK_END_HOURS:
            races.append((race_id, race_data, prev_race_id, hours_since_race))

    return races


def _get_races_for_fallback(now: datetime) -> list:
    """Get races that have reached fallback time (3.5 hours after previous race)

    IMPORTANT: Skips race_id=1 because Race 1 quali doesn't open after the
    last race of previous season - there's a season break.

    Args:
        now: Current datetime

    Returns:
        list: Races for fallback notification [(race_id, race_data, prev_race_id, hours_since), ...]
    """
    races = []

    for race_id, race_data in race_calendar.items():
        # Skip race 1 - no previous race in same season (season break)
        if race_id == 1:
            continue

        # Check if already notified
        history_key = (race_id, "opens_soon")
        if history_key in notify_history:
            continue

        # Find previous race
        prev_race_id = race_id - 1
        if prev_race_id not in race_calendar:
            continue

        prev_race_time = race_calendar[prev_race_id]["date"]
        hours_since_race = (now - prev_race_time).total_seconds() / 3600

        # Check if we've reached fallback time (within tolerance)
        if hours_since_race > API_CHECK_END_HOURS:
            minutes_since_fallback = (hours_since_race - API_CHECK_END_HOURS) * 60
            if minutes_since_fallback <= FALLBACK_TOLERANCE_MINUTES:
                races.append((race_id, race_data, prev_race_id, hours_since_race))

    return races


async def _check_quali_open_notifications(now: datetime) -> list:
    """Check for qualifications that just opened using API when appropriate

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    global last_api_check_time
    notifications = []

    # Get races to check via API and races for fallback
    races_in_polling_window = _get_races_for_polling(now)
    races_for_fallback = _get_races_for_fallback(now)

    # Check API if we have races in polling window (rate limited to every 10 minutes)
    api_result = {}
    if races_in_polling_window:
        if (
            last_api_check_time is None
            or (now - last_api_check_time).total_seconds()
            >= API_CHECK_INTERVAL_MINUTES * 60
        ):
            logger.info(
                f"🔍 Checking API for quali open status ({len(races_in_polling_window)} races in window)"
            )
            api_result = await check_quali_status_from_api()
            last_api_check_time = now
        else:
            time_until_next = (
                API_CHECK_INTERVAL_MINUTES * 60
                - (now - last_api_check_time).total_seconds()
            )
            logger.debug(f"API check skipped (next in {int(time_until_next)}s)")

    # Process API-confirmed races
    for race_id, race_data, prev_race_id, hours_since in races_in_polling_window:
        if race_id in api_result:
            logger.info(f"🆕 API confirmed: Race {race_id} quali opened!")

            # Fetch weather data with retry
            await _fetch_weather_with_retry(race_id)

            # Add replay and results notifications for previous race FIRST
            _add_replay_and_results_notifications(notifications, prev_race_id)

            # Add quali open notification AFTER replay and results
            history_key = (race_id, "opens_soon")
            notifications.append(
                ("opens", race_id, race_data, "opens_soon", history_key)
            )

    # Process fallback races (3.5h without API detection)
    for race_id, race_data, prev_race_id, hours_since in races_for_fallback:
        logger.info(
            f"⏰ Fallback: Sending quali open for race {race_id} at {hours_since:.1f}h (API didn't detect)"
        )

        # Fetch weather data with retry
        await _fetch_weather_with_retry(race_id)

        # Add replay and results notifications for previous race FIRST
        _add_replay_and_results_notifications(notifications, prev_race_id)

        # Add quali open notification AFTER replay and results
        history_key = (race_id, "opens_soon")
        notifications.append(("opens", race_id, race_data, "opens_soon", history_key))

    return notifications


def _add_replay_and_results_notifications(
    notifications: list, prev_race_id: int
) -> None:
    """Add replay and results notifications for the previous race if not already sent

    These are time-independent - they should be sent once when the next quali opens,
    regardless of when the previous race finished.

    Args:
        notifications: List to append notifications to
        prev_race_id: The previous race ID
    """
    if prev_race_id in race_calendar:
        prev_race_data = race_calendar[prev_race_id]

        # Add race replay notification
        replay_history_key = (prev_race_id, "race_replay")
        if replay_history_key not in notify_history:
            notifications.append(
                (
                    "replay",
                    prev_race_id,
                    prev_race_data,
                    "race_replay",
                    replay_history_key,
                )
            )

        # Add race results notification
        results_history_key = (prev_race_id, "race_results")
        if results_history_key not in notify_history:
            notifications.append(
                (
                    "results",
                    prev_race_id,
                    prev_race_data,
                    "race_results",
                    results_history_key,
                )
            )


def _check_quali_results_notifications(now: datetime) -> list:
    """Check for qualification results notifications

    Sends when 5 minutes have passed since quali close (time for GPRO to process results).

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]
        history_key = (race_id, "race_results")

        # Skip if already notified
        if history_key in notify_history:
            continue

        # Check if quali closed 5+ minutes ago (time for GPRO to process results)
        minutes_since_close = (now - quali_close).total_seconds() / 60

        # Only notify if quali has been closed for at least 5 minutes
        if minutes_since_close >= 5:
            notifications.append(
                ("results", race_id, race_data, "race_results", history_key)
            )

    return notifications


def _check_race_live_notifications(now: datetime) -> list:
    """Check for race live notifications

    Sends at race start time.

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for race_id, race_data in race_calendar.items():
        race_time = race_data["date"]
        history_key = (race_id, "race_live")

        # Skip if already notified
        if history_key in notify_history:
            continue

        # Check if race is starting now (within 1 minute window)
        seconds_until = (race_time - now).total_seconds()

        # Race starts when seconds_until is around 0 (within 60s tolerance)
        if -60 <= seconds_until <= 60:
            notifications.append(("live", race_id, race_data, "race_live", history_key))

    return notifications


def _check_custom_notifications(now: datetime, races_closing: list) -> list:
    """Check for custom user-defined notifications

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for hours_remaining, race_id, race_data in races_closing:
        # Check custom_1 (8h)
        custom_1_key = (race_id, "custom_1")
        if custom_1_key not in notify_history and hours_remaining <= 8:
            notifications.append(
                ("closing", race_id, race_data, "custom_1", custom_1_key)
            )

        # Check custom_2 (12h)
        custom_2_key = (race_id, "custom_2")
        if custom_2_key not in notify_history and hours_remaining <= 12:
            notifications.append(
                ("closing", race_id, race_data, "custom_2", custom_2_key)
            )

    return notifications


def _check_snooze_reminders(now: datetime, races_closing: list) -> list:
    """Check for snooze reminders that need to be sent

    Snoozes fire up to 2 minutes late (within tolerance window).

    Args:
        now: Current datetime
        races_closing: List of races closing soon (to associate with snoozes)

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key, user_id), ...]
    """
    from notifications.user_data import get_all_active_snoozes, SNOOZE_TOLERANCE_SECONDS

    notifications = []
    active_snoozes = get_all_active_snoozes()

    # Build lookup for race data
    race_lookup = {race_id: race_data for _, race_id, race_data in races_closing}
    # Also include all races in calendar for complete lookup
    race_lookup.update(race_calendar)

    for snooze in active_snoozes:
        snooze_time = datetime.fromisoformat(snooze["snooze_time"])
        seconds_until = (snooze_time - now).total_seconds()

        # Snooze fires if we're within tolerance window (slightly early or up to 2 min late)
        if -SNOOZE_TOLERANCE_SECONDS <= seconds_until <= SNOOZE_TOLERANCE_SECONDS:
            race_id = snooze["race_id"]
            snooze_id = snooze["id"]
            user_id = snooze["user_id"]
            original_label = snooze.get("original_label", "deadline")

            # Get race data
            race_data = race_lookup.get(race_id)
            if not race_data:
                continue

            # Unique history key for this specific snooze instance
            history_key = (race_id, f"snooze_{snooze_id}")

            # Only send if not already notified for this snooze
            if history_key not in notify_history:
                # Convert original label to user-friendly format
                if original_label == "deadline":
                    display_label = "⏰ Deadline snooze"
                else:
                    display_label = f"⏰ {original_label} snooze"

                # Include user_id as 6th element for targeted delivery
                # Use original_label (not display_label) so sender can parse notification type
                notifications.append(
                    ("snooze", race_id, race_data, original_label, history_key, user_id)
                )
                logger.info(
                    f"Snooze reminder firing: user {user_id}, race {race_id}, snooze {snooze_id} "
                    f"(scheduled: {snooze_time}, now: {now})"
                )

    return notifications


def _reset_snooze_counts_for_past_deadlines(now: datetime) -> None:
    """Reset snooze counts for races whose deadlines have passed

    This allows snoozes to work again for the next occurrence of similar notifications.
    """
    from notifications.user_data import (
        users_data,
        SNOOZE_MAX_COUNTS,
        reset_snooze_count,
    )

    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]

        # If quali closed more than 1 hour ago, reset snooze counts
        if now > quali_close + timedelta(hours=1):
            for user_id_str in users_data:
                user_data = users_data[user_id_str]
                if "snooze_counts" not in user_data:
                    continue

                snooze_counts = user_data["snooze_counts"]
                for label in SNOOZE_MAX_COUNTS.keys():
                    count_key = f"{race_id}_{label}"
                    if count_key in snooze_counts and snooze_counts[count_key] > 0:
                        reset_snooze_count(int(user_id_str), race_id, label)


def _cleanup_completed_quali_for_all_users() -> None:
    """Clean up completed quali data for all users after season transition.

    This is called during season transition to clean up old quali data.
    """
    from notifications.user_data import users_data, save_users_data

    cleaned_count = 0
    for user_id, user_data in users_data.items():
        if "completed_quali" in user_data:
            del user_data["completed_quali"]
            cleaned_count += 1

    if cleaned_count > 0:
        save_users_data()
        logger.info(f"Cleaned up completed_quali data for {cleaned_count} users")


async def _check_season_transition(now: datetime) -> None:
    """Check and handle season transition conditions

    Args:
        now: Current datetime
    """
    global last_season_transition_check, last_prefetch_check

    # Season transition check (after last race concludes)
    if should_trigger_season_transition(now):
        logger.info("🔄 Season transition triggered!")

        # Perform transition
        success = await transition_to_next_season()

        if success:
            # Clean up user data
            _cleanup_completed_quali_for_all_users()

            # Mark as checked to avoid repeated transitions
            last_season_transition_check = now
            logger.info("🎉 Season transition completed successfully!")
        else:
            logger.error("❌ Season transition failed")

    # Prefetch check (4 days before first race)
    # Only check every hour to avoid excessive checks
    if (
        last_prefetch_check is None
        or (now - last_prefetch_check).total_seconds()
        >= SEASON_CHECK_INTERVAL_HOURS * 3600
    ):
        if should_prefetch_next_season(now):
            logger.info("📅 Pre-fetching next season calendar...")

            # Fetch calendar from API
            success = await update_calendar()

            if success:
                logger.info("✅ Next season calendar pre-fetched successfully!")

                # Also fetch weather for Race 1 (it won't be auto-fetched later)
                if 1 in race_calendar:
                    logger.info("🌤️ Fetching weather for Race 1...")
                    weather_data = await fetch_weather_from_api(1)
                    if weather_data:
                        logger.info("✅ Race 1 weather fetched successfully")
                    else:
                        logger.warning(
                            "⚠️ Race 1 weather not available yet (may need retry later)"
                        )
            else:
                logger.error("❌ Failed to pre-fetch next season calendar")

        last_prefetch_check = now


async def check_notifications(bot: Bot):
    """Continuous notification loop - adaptive check interval based on race proximity"""
    global notify_history
    logger.info(
        f"🔔 Starting notification checker (adaptive: {CHECK_INTERVAL_NORMAL_SECONDS//60}min normal, {CHECK_INTERVAL_FAST_SECONDS}s when race approaching)"
    )
    load_users_data()
    notify_history = load_notify_history()

    while True:
        try:
            # Determine what notifications to send (quick check under lock)
            async with notification_lock:
                now = datetime.now(UTC)

                # Check season transition conditions
                await _check_season_transition(now)

                # Fetch upcoming races once for efficiency (used by multiple checks)
                races_closing = get_races_closing_soon(
                    72
                )  # Extended to 72h for Tuesday races

                # Check all notification types
                notifications_to_send = []
                notifications_to_send.extend(
                    _check_quali_closing_notifications(now, races_closing)
                )
                notifications_to_send.extend(await _check_quali_open_notifications(now))
                notifications_to_send.extend(_check_quali_results_notifications(now))
                notifications_to_send.extend(_check_race_live_notifications(now))
                notifications_to_send.extend(
                    _check_custom_notifications(now, races_closing)
                )
                notifications_to_send.extend(
                    _check_new_season_reminder_notifications(now)
                )
                notifications_to_send.extend(
                    _check_snooze_reminders(now, races_closing)
                )

                # Reset snooze counts for past deadlines
                _reset_snooze_counts_for_past_deadlines(now)

                # Clean old history entries
                cutoff = now - timedelta(hours=NOTIFICATION_HISTORY_RETENTION_HOURS)
                notify_history = {k: v for k, v in notify_history.items() if v > cutoff}

                # Enforce size limit to prevent unbounded growth
                notify_history = _enforce_history_size_limit(notify_history)

                # Determine next check interval based on race proximity
                next_interval = _get_next_check_interval(now)

            # Send notifications outside the lock (slow operation)
            await _send_notifications_to_users(bot, notifications_to_send)

        except Exception as e:
            logger.error(f"❌ Notification check error: {e}")
            next_interval = CHECK_INTERVAL_NORMAL_SECONDS  # Fallback on error

        # Wait before next check (adaptive interval)
        await asyncio.sleep(next_interval)


async def _send_notifications_to_users(bot: Bot, notifications: list) -> None:
    """Send notifications to all eligible users

    Args:
        bot: Bot instance
        notifications: List of (type, race_id, race_data, label, history_key, [user_id]) tuples.
                      For snooze notifications, user_id is included as the 6th element for targeted delivery.
    """
    from notifications.user_data import remove_active_snooze

    for notification in notifications:
        try:
            # Handle both formats: regular (5 items) and snooze (6 items with user_id)
            if len(notification) == 6:
                ntype, race_id, race_data, label, history_key, target_user_id = (
                    notification
                )
                is_targeted = True
            else:
                ntype, race_id, race_data, label, history_key = notification
                target_user_id = None
                is_targeted = False

            race_name = race_data.get("track", f"Race {race_id}")

            # Log notification type
            if ntype == "closing":
                log_structured(
                    logging.INFO,
                    f"🔔 Quali {label} notification: Race {race_id} - {race_name}",
                    race_id=race_id,
                    race_name=race_name,
                    hours_remaining=(
                        race_data["quali_close"] - datetime.now(UTC)
                    ).total_seconds()
                    / 3600,
                )
            elif ntype == "opens":
                logger.info(f"🆕 Quali opened: Race {race_id} - {race_name}")
            elif ntype == "replay":
                logger.info(f"📺 Race replay available: Race {race_id} - {race_name}")
            elif ntype == "results":
                logger.info(f"📊 Race results available: Race {race_id} - {race_name}")
            elif ntype == "live":
                logger.info(f"🏁 Race is LIVE: Race {race_id} - {race_name}")
            elif ntype == "custom":
                logger.info(
                    f"🔔 Custom notification {label}: Race {race_id} - {race_name}"
                )
            elif ntype == "snooze":
                logger.info(
                    f"⏰ Snooze reminder: user {target_user_id}, race {race_id} - {race_name}"
                )
            elif ntype == "new_season":
                logger.info(f"🎉 New season reminder: {label}")

            # For targeted notifications (snoozes), only send to the specific user
            if is_targeted and target_user_id is not None:
                try:
                    user_id_int = int(target_user_id)

                    # Skip blocked users
                    if is_user_blocked(user_id_int):
                        continue

                    await send_notification_to_user(
                        bot, user_id_int, ntype, race_id, race_data, label
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending targeted {ntype} to user {target_user_id}: {e}"
                    )
                continue

            # Send to all users (for non-targeted notifications)
            for user_id, user_data in list(users_data.items()):
                try:
                    user_id_int = int(user_id)

                    # Skip blocked users
                    if is_user_blocked(user_id_int):
                        continue

                    # Check notification type and settings
                    should_send = False

                    if ntype == "new_season":
                        # New season reminder uses race_live setting
                        should_send = is_notification_enabled(user_id_int, "race_live")
                    elif ntype == "closing":
                        # Map labels to settings
                        label_map = {
                            "72h": "custom_1",
                            "48h": "custom_1",
                            "24h": "24h",
                            "2h": "2h",
                            "10min": "10min",
                            "custom_1": "custom_1",
                            "custom_2": "custom_2",
                        }
                        setting = label_map.get(label, label)
                        should_send = is_notification_enabled(user_id_int, setting)
                    elif ntype in ["opens", "replay", "results", "live", "custom"]:
                        should_send = is_notification_enabled(user_id_int, ntype)

                    if should_send:
                        await send_notification_to_user(
                            bot, user_id_int, ntype, race_id, race_data, label
                        )

                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")

            # Mark as notified (snoozes are marked in both user_data AND notify_history)
            if ntype == "snooze":
                # For snoozes, extract the snooze_id from history_key
                # history_key format: (race_id, f"snooze_{snooze_id}")
                _, snooze_key = history_key
                if snooze_key.startswith("snooze_"):
                    snooze_id = snooze_key.replace("snooze_", "")
                    # Find and remove the active snooze
                    from notifications.user_data import get_all_active_snoozes

                    for snooze in get_all_active_snoozes():
                        if snooze["id"] == snooze_id:
                            remove_active_snooze(snooze["user_id"], snooze_id)
                            break
                # ALSO mark in notify_history to prevent duplicate firing
                # (in case checker runs again before active_snoozes is saved)
                _mark_notified(race_id, snooze_key)
            else:
                _mark_notified(race_id, label)

        except Exception as e:
            logger.error(f"Error processing notification {notification}: {e}")

    # Persist history after processing all notifications
    save_notify_history()


def _check_new_season_reminder_notifications(now: datetime) -> list:
    """Check for new season reminder notifications (1-2 days before first race)

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    from gpro_calendar import get_first_race_date

    notifications = []

    # Check if we have a next season calendar (meaning new season is coming)
    from gpro_calendar import next_season_calendar

    if not next_season_calendar:
        return notifications

    first_race_date = get_first_race_date()
    if not first_race_date:
        return notifications

    days_until = (first_race_date - now).total_seconds() / (24 * 3600)

    # Send single reminder at 30 hours before (1.25 days)
    # Window: 28.8-30 hours before (1.20-1.25 days with tolerance)
    reminder_label = "new_season_reminder"
    target_days = 1.25  # 30 hours
    min_days = 1.20  # 28.8 hours (30 min tolerance)

    history_key = (0, reminder_label)  # race_id=0 for season-level reminders

    # Skip if already notified
    if not _is_already_notified(0, reminder_label):
        # Check if we're within the notification window
        if min_days <= days_until <= target_days:
            # Use race_id=1 data for track name, but label indicates season reminder
            if 1 in next_season_calendar:
                race_data = next_season_calendar[1].copy()
                race_data["days_until"] = days_until
                notifications.append(
                    ("new_season", 1, race_data, reminder_label, history_key)
                )

    return notifications


# Track last API check time for rate limiting
last_api_check_time: datetime = None

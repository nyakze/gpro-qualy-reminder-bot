"""Qualification-related notification checks

Handles quali closing, quali opening, and quali results notifications.
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Tuple

from gpro_calendar import (
    race_calendar,
    check_quali_status_from_api,
    fetch_weather_from_api,
)
from notifications.history import is_already_notified
from notifications.timing import (
    API_CHECK_START_HOURS,
    API_CHECK_END_HOURS,
    API_CHECK_INTERVAL_MINUTES,
    FALLBACK_TOLERANCE_MINUTES,
    EARLY_CHECK_MINUTES,
)

logger = logging.getLogger(__name__)

# Track last API check time for rate limiting
last_api_check_time: datetime = None


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


def check_quali_closing(now: datetime, races_closing: list) -> List[Tuple]:
    """Check for qualification deadlines approaching

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    # Convert early check minutes to hours for comparison
    early_check_hours = EARLY_CHECK_MINUTES / 60.0

    for hours_remaining, race_id, race_data in races_closing:
        # Determine notification label based on time remaining (with early check offset)
        if hours_remaining <= 0.17 + early_check_hours:  # ~10 minutes + early
            label = "10min"
        elif hours_remaining <= 2 + early_check_hours:
            label = "2h"
        elif hours_remaining <= 24 + early_check_hours:
            label = "24h"
        elif hours_remaining <= 48 + early_check_hours:
            label = "48h"
        elif hours_remaining <= 72 + early_check_hours:
            # 72h notification only for Tuesday races (quali closes on Tuesday)
            quali_close = race_data["quali_close"]
            if quali_close.weekday() == 1:  # Tuesday = 1
                label = "72h"
            else:
                continue  # Skip 72h for non-Tuesday races
        else:
            continue

        # Check already notified
        if is_already_notified(race_id, label):
            continue

        history_key = (race_id, label)
        notifications.append(("closing", race_id, race_data, label, history_key))

    return notifications


def _get_races_for_polling(now: datetime) -> list:
    """Get races that are in the API polling window (2-3.5 hours after previous race)

    IMPORTANT: Skips race_id=1 because Race 1 quali doesn't open after the
    last race of previous season - there's a season break.

    Args:
        now: Current datetime

    Returns:
        list: Races to check via API [(race_id, race_data, prev_race_id, hours_since), ...]
    """
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

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
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

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
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

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


async def check_quali_open(now: datetime) -> List[Tuple]:
    """Check for qualifications that just opened using API when appropriate

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    global last_api_check_time
    notifications: list = []

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


def check_quali_results(now: datetime) -> List[Tuple]:
    """Check for qualification results notifications

    Sends when 5 minutes have passed since quali close (time for GPRO to process results).

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

    notifications = []

    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]
        history_key = (race_id, "quali_results")

        # Skip if already notified
        if history_key in notify_history:
            continue

        # Check if quali closed 5+ minutes ago (time for GPRO to process results)
        minutes_since_close = (now - quali_close).total_seconds() / 60

        # Only notify if quali has been closed for at least 5 minutes
        if minutes_since_close >= 5:
            notifications.append(
                ("results", race_id, race_data, "quali_results", history_key)
            )

    return notifications

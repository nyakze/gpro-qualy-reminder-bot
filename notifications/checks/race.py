"""Race-related notification checks

Handles race live, replay, and results notifications.
"""

import logging
from datetime import datetime
from typing import List, Tuple

from gpro_calendar import (
    race_calendar,
    get_last_race_id,
    check_race_replay_api,
)

logger = logging.getLogger(__name__)


def check_race_live_notifications(now: datetime) -> List[Tuple]:
    """Check for race live notifications

    Sends at race start time.

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

    notifications = []

    for race_id, race_data in race_calendar.items():
        race_time = race_data["date"]
        history_key = (race_id, "race_live")

        # Skip if already notified
        if history_key in notify_history:
            continue

        # Check if race is starting now (within 6 minute window: 1min before to 5min after)
        seconds_until = (race_time - now).total_seconds()

        # Race starts when seconds_until is around 0 (within tolerance)
        # -60s (1 min before) to +300s (5 min after) to catch late checks
        if -60 <= seconds_until <= 300:
            notifications.append(("live", race_id, race_data, "race_live", history_key))

    return notifications


async def check_last_race_results(now: datetime) -> List[Tuple]:
    """Check if last race (race 17) results are available using RaceReplay API

    For the last race of the season, we can't rely on the next quali opening
    to detect when the race is complete (season break). Instead, we check the
    RaceReplay API which returns the race number when results are calculated.

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    from notifications.history import get_notify_history

    notify_history = get_notify_history()

    notifications = []

    # Only check for the last race of the season (race 17)
    last_race_id = get_last_race_id()
    if last_race_id == 0:
        return notifications

    # This function is specifically for the last race only
    # Other races use the standard quali open detection via check_quali_open
    # which is more reliable when the next quali opens after a race

    # Skip if already notified for this race
    replay_history_key = (last_race_id, "race_replay")
    results_history_key = (last_race_id, "race_results")

    if replay_history_key in notify_history and results_history_key in notify_history:
        return notifications

    # Check if last race has finished (at least 90 minutes ago to allow processing)
    last_race_time = race_calendar[last_race_id]["date"]
    minutes_since_race = (now - last_race_time).total_seconds() / 60

    if minutes_since_race < 90:
        # Race just finished, give GPRO time to calculate results
        return notifications

    # Stop checking after 3.5 hours (210 minutes) - if results aren't calculated by then,
    # something is wrong with GPRO or the API, no point in wasting tokens
    if minutes_since_race > 210:
        logger.warning(
            f"⚠️ Stopping RaceReplay API checks for race {last_race_id}: "
            f"{minutes_since_race:.0f} minutes elapsed without results"
        )
        return notifications

    # Check RaceReplay API to see if race 17 results are calculated
    race_is_calculated = await check_race_replay_api(last_race_id)

    if race_is_calculated:
        last_race_data = race_calendar[last_race_id]

        # Add race replay notification if not sent yet
        if replay_history_key not in notify_history:
            notifications.append(
                (
                    "replay",
                    last_race_id,
                    last_race_data,
                    "race_replay",
                    replay_history_key,
                )
            )

        # Add race results notification if not sent yet
        if results_history_key not in notify_history:
            notifications.append(
                (
                    "results",
                    last_race_id,
                    last_race_data,
                    "race_results",
                    results_history_key,
                )
            )

        if notifications:
            logger.info(
                f"🎯 RaceReplay API confirmed race {last_race_id} is calculated, "
                f"sending {len(notifications)} notifications"
            )

    return notifications

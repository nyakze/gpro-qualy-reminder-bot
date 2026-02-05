"""Timing utilities for notification checking

Handles check intervals, timing calculations, and scheduling.
"""

import logging
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

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


def get_next_check_interval(now: datetime, race_calendar: dict) -> int:
    """Determine the next check interval based on race proximity

    Uses fast mode (60s) when approaching race time, normal mode (5min) otherwise.

    Args:
        now: Current datetime
        race_calendar: Race calendar dictionary

    Returns:
        int: Seconds to wait before next check
    """
    from notifications.users import get_all_active_snoozes

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

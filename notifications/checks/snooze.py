"""Snooze and custom notification checks"""

import logging
from datetime import datetime, timedelta
from typing import List, Tuple

from gpro_calendar import race_calendar
from notifications.users import (
    get_all_active_snoozes,
    SNOOZE_TOLERANCE_SECONDS,
    SNOOZE_MAX_COUNTS,
    reset_snooze_count,
)
from notifications.history import (
    get_notify_history,
)

logger = logging.getLogger(__name__)


def check_snooze_reminders(now: datetime, races_closing: list) -> List[Tuple]:
    """Check for snooze reminders that need to be sent

    Snoozes fire up to 2 minutes late (within tolerance window).

    Args:
        now: Current datetime
        races_closing: List of races closing soon (to associate with snoozes)

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key, user_id), ...]
    """
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
            if history_key not in get_notify_history():
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


def check_custom_notifications(now: datetime, races_closing: list) -> List[Tuple]:
    """Check for custom user-defined notifications

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for hours_remaining, race_id, race_data in races_closing:
        # Check custom_1 (8h)
        custom_1_key = (race_id, "custom_1")
        if custom_1_key not in get_notify_history() and hours_remaining <= 8:
            notifications.append(
                ("closing", race_id, race_data, "custom_1", custom_1_key)
            )

        # Check custom_2 (12h)
        custom_2_key = (race_id, "custom_2")
        if custom_2_key not in get_notify_history() and hours_remaining <= 12:
            notifications.append(
                ("closing", race_id, race_data, "custom_2", custom_2_key)
            )

    return notifications


def reset_snooze_counts_for_past_deadlines(now: datetime) -> None:
    """Reset snooze counts for races whose deadlines have passed

    This allows snoozes to work again for the next occurrence of similar notifications.
    """
    from notifications.users import users_data

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

"""Snooze and custom notification checks"""

import logging
from datetime import datetime, timedelta
from typing import List, Tuple

from gpro_calendar import race_calendar
from notifications.users import (
    get_all_active_snoozes,
    remove_active_snooze,
    is_user_blocked,
    users_data,
    SNOOZE_TOLERANCE_SECONDS,
    reset_snooze_counts_for_deadline_passed,
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
        if seconds_until <= SNOOZE_TOLERANCE_SECONDS:
            race_id = snooze["race_id"]
            snooze_id = snooze["id"]
            user_id = snooze["user_id"]
            original_label = snooze.get("original_label", "deadline")

            # Get race data
            race_data = race_lookup.get(race_id)
            if not race_data:
                continue
            if now >= race_data["quali_close"]:
                remove_active_snooze(user_id, snooze_id)
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
    """Build targeted notifications using each user's configured interval."""
    notifications = []
    history = get_notify_history()

    for hours_remaining, race_id, race_data in races_closing:
        for user_id, user_status in list(users_data.items()):
            if is_user_blocked(int(user_id)):
                continue

            custom_notifs = user_status.get("custom_notifications", [])
            for slot_idx, custom_notif in enumerate(custom_notifs[:2]):
                if not custom_notif.get("enabled", False):
                    continue

                hours_before = custom_notif.get("hours_before")
                if hours_before is None or hours_remaining > float(hours_before):
                    continue

                label = f"custom_{slot_idx + 1}"
                history_label = f"{label}:user:{int(user_id)}"
                history_key = (race_id, history_label)
                if history_key in history:
                    continue

                notifications.append(
                    (
                        "custom",
                        race_id,
                        race_data,
                        label,
                        history_key,
                        int(user_id),
                    )
                )

    return notifications


def reset_snooze_counts_for_past_deadlines(now: datetime) -> None:
    """Clear race-specific snooze counters after each deadline."""
    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]
        if now > quali_close + timedelta(hours=1):
            reset_snooze_counts_for_deadline_passed(race_id, quali_close)

"""Snooze management utilities for notifications"""

import logging
from datetime import datetime, timedelta, UTC
from typing import Tuple, Optional, List

from aiogram.types import InlineKeyboardButton

from gpro_calendar import race_calendar
from notifications.users import get_snooze_count

logger = logging.getLogger(__name__)

SNOOZE_OPTIONS = [
    (5, "5m"),
    (15, "15m"),
    (30, "30m"),
    (60, "1h"),
    (120, "2h"),
    (240, "4h"),
    (480, "8h"),
]

SNOOZE_TOLERANCE_MINUTES = 2
MAX_SNOOZES = 3

QUALI_NOTIFICATION_TYPES = [
    "72h",
    "48h",
    "24h",
    "2h",
    "10min",
    "opens_soon",
    "deadline",
]


def get_next_notification_time(
    race_id: int, current_label: str, now: datetime
) -> Optional[datetime]:
    """Get the next notification time after current_label for a race

    Args:
        race_id: Race ID
        current_label: Current notification label (e.g., "48h", "2h")
        now: Current datetime

    Returns:
        datetime: Next notification time, or None if no more notifications
    """
    if race_id not in race_calendar:
        return None

    race_data = race_calendar[race_id]
    quali_close = race_data.get("quali_close")
    if not quali_close:
        return None

    notification_labels = ["72h", "48h", "24h", "2h", "10min"]

    try:
        current_idx = notification_labels.index(current_label)
    except ValueError:
        return None

    for label in notification_labels[current_idx + 1 :]:
        hours_map = {
            "72h": 72,
            "48h": 48,
            "24h": 24,
            "2h": 2,
            "10min": 10 / 60,
        }
        hours_before = hours_map.get(label)
        if hours_before is None:
            continue

        next_time = quali_close - timedelta(hours=hours_before)
        if next_time > now:
            return next_time

    return None


def can_snooze(
    user_id: int, race_id: int, notification_label: str, snooze_minutes: int
) -> Tuple[bool, str]:
    """Check if a snooze action is valid

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        notification_label: Current notification label (e.g., "48h", "2h")
        snooze_minutes: Minutes to snooze

    Returns:
        Tuple of (is_valid, error_message)
    """
    if race_id not in race_calendar:
        return False, "Race not found"

    race_data = race_calendar[race_id]
    quali_close = race_data.get("quali_close")
    now = datetime.now(UTC)

    if not quali_close:
        return False, "Qualifying deadline not set"

    snooze_until = now + timedelta(minutes=snooze_minutes)

    snooze_count = get_snooze_count(user_id, notification_label)
    if snooze_count >= MAX_SNOOZES:
        return False, "max_reached"

    if snooze_until >= quali_close:
        return False, "past_deadline"

    next_notification = get_next_notification_time(race_id, notification_label, now)
    if next_notification and snooze_until >= next_notification - timedelta(
        minutes=SNOOZE_TOLERANCE_MINUTES
    ):
        minutes_until_next = int((next_notification - now).total_seconds() / 60)
        return False, f"next_{minutes_until_next}"

    return True, ""


def get_snooze_buttons(
    user_id: int,
    race_id: int,
    notification_label: str,
    i18n_get_text,
) -> List[List[InlineKeyboardButton]]:
    """Generate dynamic snooze buttons based on available time

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        notification_label: Current notification label (e.g., "48h", "2h")
        i18n_get_text: Function to get translated text

    Returns:
        List of button rows for inline keyboard
    """
    if race_id not in race_calendar:
        return []

    race_data = race_calendar[race_id]
    quali_close = race_data.get("quali_close")
    now = datetime.now(UTC)

    if not quali_close:
        return []

    time_until_deadline = (quali_close - now).total_seconds() / 60
    next_notification = get_next_notification_time(race_id, notification_label, now)

    if next_notification:
        time_until_next = (next_notification - now).total_seconds() / 60
        available_minutes = min(
            time_until_deadline, time_until_next - SNOOZE_TOLERANCE_MINUTES
        )
    else:
        available_minutes = time_until_deadline

    if available_minutes < 5:
        return []

    snooze_count = get_snooze_count(user_id, notification_label)
    if snooze_count >= MAX_SNOOZES:
        return []

    buttons = []
    current_row = []

    for minutes, label in SNOOZE_OPTIONS:
        if minutes > available_minutes:
            continue

        if snooze_count >= MAX_SNOOZES:
            break

        button = InlineKeyboardButton(
            text=i18n_get_text(f"button-snooze-{label}"),
            callback_data=f"snooze_{race_id}_{notification_label}_{minutes}",
        )

        current_row.append(button)

        if len(current_row) == 2:
            buttons.append(current_row)
            current_row = []

    if current_row:
        buttons.append(current_row)

    return buttons

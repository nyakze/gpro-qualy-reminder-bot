"""Validation and parsing functions for custom notifications"""

import logging
import re

logger = logging.getLogger(__name__)

# Custom notification constraints
CUSTOM_NOTIF_MIN_HOURS = 20 / 60  # 20 minutes minimum
CUSTOM_NOTIF_MAX_HOURS = 70  # 70 hours maximum
CUSTOM_NOTIF_MAX_SLOTS = 2  # Maximum 2 custom notifications per user


def validate_custom_notification_hours(hours: float, i18n=None) -> tuple[bool, str]:
    """Validate custom notification time

    Args:
        hours: Hours before quali closes
        i18n: I18n context for translations (optional)

    Returns:
        (is_valid, error_message)
    """
    # Import i18n context if not provided
    if i18n is None:
        from aiogram_i18n import I18nContext

        try:
            i18n = I18nContext.get_current(no_error=True)
        except:
            i18n = None

    # Use i18n if available, fallback to English
    def get_text(key, **kwargs):
        if i18n:
            return i18n.get(key, **kwargs)
        return key

    if hours is None:
        return False, get_text("validation-time-empty")

    if hours < CUSTOM_NOTIF_MIN_HOURS:
        return False, get_text("validation-time-min")

    if hours > CUSTOM_NOTIF_MAX_HOURS:
        return False, get_text("validation-time-max")

    return True, ""


def parse_time_input(time_str: str, i18n=None) -> tuple[float, str]:
    """Parse user time input into hours

    Supported formats:
    - "20m", "30min", "45 minutes" -> minutes
    - "2h", "12 hours" -> hours
    - "2d", "2 days" -> days (converted to hours)
    - "1h 30m", "2h30m" -> hours + minutes
    - "2d 12h", "2d12h" -> days + hours
    - "2d 12h 30m", "2d12h30m" -> days + hours + minutes

    Supports multiple languages:
    - English: d, day, days, h, hours, m, min, minutes
    - Russian: д, день, дня, дней, ч, час, часа, часов, м, мин, минут, минуты, минута
    - Portuguese: d, dia, dias, h, hora, horas, m, min, minuto, minutos
    - Spanish: d, día, días, h, hora, horas, m, min, minuto, minutos
    - French: d, j, jour, jours, h, heure, heures, m, min, minute, minutes
    - Italian: d, g, giorno, giorni, h, ora, ore, m, min, minuto, minuti

    Args:
        time_str: User input time string
        i18n: I18n context for translations (optional)

    Returns:
        (hours_float, error_message)
    """
    # Import i18n context if not provided
    if i18n is None:
        from aiogram_i18n import I18nContext

        try:
            i18n = I18nContext.get_current(no_error=True)
        except:
            i18n = None

    # Use i18n if available, fallback to English
    def get_text(key, **kwargs):
        if i18n:
            return i18n.get(key, **kwargs)
        return key

    if not time_str:
        return None, get_text("validation-enter-time")

    time_str = time_str.strip().lower()

    # Day patterns (multi-language support)
    # English: d, day, days
    # Russian: д, день, дня, дней
    # Portuguese: d, dia, dias
    # Spanish: d, día, días
    # French: d, j, jour, jours
    # Italian: d, g, giorno, giorni
    day_pattern = r"(?:d(?:ay|ays|ia|ias|ía|ías)?|j(?:our|ours)?|g(?:iorno|iorni)?|д(?:ень|ня|ней)?)"

    # Hour patterns (multi-language support)
    # English: h, hour, hours
    # Russian: ч, час, часа, часов
    # Portuguese: h, hora, horas
    # Spanish: h, hora, horas
    # French: h, heure, heures
    # Italian: h, ora, ore (note: "ore" standalone is also common)
    hour_pattern = r"(?:h(?:our|ours|ora|oras|eure|eures)?|ore|ч(?:ас(?:а|ов)?)?)"

    # Minute patterns (multi-language support)
    # English: m, min, minute, minutes
    # Russian: м, мин, минут, минуты, минута
    # Portuguese: m, min, minuto, minutos
    # Spanish: m, min, minuto, minutos
    # French: m, min, minute, minutes
    # Italian: m, min, minuto, minuti
    minute_pattern = r"(?:m(?:in(?:ute|utes|uto|utos|uti)?)?|м(?:ин(?:ут(?:а|ы)?)?)?)"

    # Try to match "Xd Yh Zm" or "XdYhZm" format (days + hours + minutes)
    match = re.match(
        rf"^(\d+)\s*{day_pattern}\s*(\d+)\s*{hour_pattern}\s*(\d+)\s*{minute_pattern}$",
        time_str,
    )
    if match:
        days = int(match.group(1))
        hours = int(match.group(2))
        minutes = int(match.group(3))
        total_hours = days * 24 + hours + minutes / 60
        return float(total_hours), ""

    # Try to match "Xd Yh" or "XdYh" format (days + hours)
    match = re.match(rf"^(\d+)\s*{day_pattern}\s*(\d+)\s*{hour_pattern}$", time_str)
    if match:
        days = int(match.group(1))
        hours = int(match.group(2))
        total_hours = days * 24 + hours
        return float(total_hours), ""

    # Try to match "Xh Ym" or "XhYm" format (hours + minutes)
    match = re.match(rf"^(\d+)\s*{hour_pattern}\s*(\d+)\s*{minute_pattern}$", time_str)
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        total_hours = hours + minutes / 60
        return total_hours, ""

    # Try to match days only: "Xd" or "X days" or "Xд" or "X дней"
    match = re.match(rf"^(\d+)\s*{day_pattern}$", time_str)
    if match:
        days = int(match.group(1))
        return float(days * 24), ""

    # Try to match hours only: "Xh" or "X hours" or "Xч" or "X часа"
    match = re.match(rf"^(\d+)\s*{hour_pattern}$", time_str)
    if match:
        hours = int(match.group(1))
        return float(hours), ""

    # Try to match minutes only: "Xm" or "X minutes" or "Xм" or "X минут"
    match = re.match(rf"^(\d+)\s*{minute_pattern}$", time_str)
    if match:
        minutes = int(match.group(1))
        return minutes / 60, ""

    return None, get_text("validation-invalid-format")


def format_custom_notification_time(hours: float, i18n=None) -> str:
    """Format hours into human-readable string

    Args:
        hours: Hours before quali closes
        i18n: I18n context for translations (optional)

    Examples:
        0.333 -> "20 minutes" (or "20м" in Russian)
        1.5 -> "1 hour 30 minutes" (or "1 час 30 минут" in Russian)
        12 -> "12 hours" (or "12 часов" in Russian)

    Returns:
        Formatted time string
    """
    if hours is None:
        return "Not set"

    # Import i18n context if not provided
    if i18n is None:
        from aiogram_i18n import I18nContext

        try:
            i18n = I18nContext.get_current(no_error=True)
        except:
            i18n = None

    # Helper to get i18n text or fallback to abbreviations
    def get_text(key, **kwargs):
        if i18n:
            try:
                return i18n.get(key, **kwargs)
            except:
                pass
        return None

    total_minutes = hours * 60
    h = int(hours)
    m = int(total_minutes % 60)

    if h > 0 and m > 0:
        text = get_text("time-hours-minutes", hours=h, minutes=m)
        return text if text else f"{h}h {m}m"
    elif h > 0:
        text = get_text("time-hours", hours=h)
        return text if text else f"{h}h"
    else:
        text = get_text("time-minutes", minutes=m)
        return text if text else f"{m}m"


def get_custom_notifications(user_id: int) -> list:
    """Get user's custom notifications

    Returns:
        List of custom notification dicts
    """
    from .user_data import get_user_status, get_default_custom_notifications

    user_status = get_user_status(user_id)
    return user_status.get("custom_notifications", get_default_custom_notifications())


def set_custom_notification(
    user_id: int, slot: int, hours_before: float, i18n=None
) -> tuple[bool, str]:
    """Set or update a custom notification slot

    Args:
        user_id: User ID
        slot: Slot index (0 or 1)
        hours_before: Hours before quali closes (None to disable)
        i18n: I18n context for translations (optional)

    Returns:
        (success, message)
    """
    # Import i18n context if not provided
    if i18n is None:
        from aiogram_i18n import I18nContext

        try:
            i18n = I18nContext.get_current(no_error=True)
        except:
            i18n = None

    # Use i18n if available, fallback to English
    def get_text(key, **kwargs):
        if i18n:
            return i18n.get(key, **kwargs)
        return key

    if slot < 0 or slot >= CUSTOM_NOTIF_MAX_SLOTS:
        return False, get_text(
            "validation-invalid-slot", maxSlots=CUSTOM_NOTIF_MAX_SLOTS - 1
        )

    # Validate hours if provided
    if hours_before is not None:
        is_valid, error_msg = validate_custom_notification_hours(hours_before, i18n)
        if not is_valid:
            return False, error_msg

    from .user_data import (
        get_user_status,
        get_default_custom_notifications,
        save_users_data,
    )

    user_status = get_user_status(user_id)
    custom_notifs = user_status.get(
        "custom_notifications", get_default_custom_notifications()
    )

    # Ensure list has correct size
    while len(custom_notifs) < CUSTOM_NOTIF_MAX_SLOTS:
        custom_notifs.append({"enabled": False, "hours_before": None})

    # Update slot
    if hours_before is None:
        custom_notifs[slot] = {"enabled": False, "hours_before": None}
    else:
        custom_notifs[slot] = {"enabled": True, "hours_before": hours_before}

    user_status["custom_notifications"] = custom_notifs
    save_users_data()

    time_str = format_custom_notification_time(hours_before, i18n)
    logger.info(f"User {user_id} set custom notification {slot+1} to: {time_str}")
    return True, get_text("custom-notif-set", slot=slot + 1, time=time_str)

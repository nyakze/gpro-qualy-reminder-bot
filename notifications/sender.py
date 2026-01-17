"""Functions for sending notifications to users"""

import logging
import re
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from gpro_calendar import race_calendar
from utils import add_flag_to_track
from .user_data import (
    get_user_status,
    DEFAULT_USER_LANG,
    get_snooze_count,
)

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

QUALI_NOTIFICATION_TYPES = ["72h", "48h", "24h", "2h", "10min", "deadline"]


def generate_gpro_link(
    group: str, gpro_lang: str = "gb", link_type: str = "live"
) -> str:
    """Generate GPRO race link based on group format and type

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')
        link_type: 'live' for live race, 'replay' for replay

    Examples: E → Elite, M3 → Master - 3, A42 → Amateur - 42, R11 → Rookie - 11"""
    from .user_data import is_valid_language

    # GPRO URL endpoints
    GPRO_LIVE_ENDPOINT = "racescreenlive.asp"
    GPRO_REPLAY_ENDPOINT = "racescreen.asp"

    # Validate and fallback for language
    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        gpro_lang = "gb"

    # Determine endpoint based on link type
    endpoint = GPRO_LIVE_ENDPOINT if link_type == "live" else GPRO_REPLAY_ENDPOINT
    base_url = f"https://gpro.net/{gpro_lang}/{endpoint}?Group="

    if not group:
        return base_url

    group = group.strip().upper()

    # Elite has no number
    if group == "E":
        return f"{base_url}Elite"

    # Parse group letter and number (e.g., M3, R11, P15, A42)
    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        # Invalid format, return default
        return base_url

    letter, number = match.groups()
    group_names = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}

    group_name = group_names[letter]
    # URL encode: "Rookie - 11" → "Rookie%20-%2011"
    encoded = f"{group_name}%20-%20{number}"
    return f"{base_url}{encoded}"


def generate_race_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate race live link - wrapper for backwards compatibility"""
    return generate_gpro_link(group, gpro_lang, "live")


def generate_replay_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate race replay link - wrapper for backwards compatibility"""
    return generate_gpro_link(group, gpro_lang, "replay")


def generate_starting_grid_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate Starting Grid link with user's group

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Starting Grid page
    """
    from .user_data import is_valid_language

    # Validate and fallback for language
    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        gpro_lang = "gb"

    base_url = f"https://gpro.net/{gpro_lang}/StartingGrid.asp?Group="

    if not group:
        return base_url

    group = group.strip().upper()

    # Elite has no number
    if group == "E":
        return f"{base_url}Elite"

    # Parse group letter and number (e.g., M3, R11, P15, A42)
    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        # Invalid format, return default
        return base_url

    letter, number = match.groups()
    group_names = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}

    group_name = group_names[letter]
    # URL encode: "Rookie - 11" → "Rookie%20-%2011"
    encoded = f"{group_name}%20-%20{number}"
    return f"{base_url}{encoded}"


def generate_quali_link(gpro_lang: str = "gb") -> str:
    """Generate Qualifying page link

    Args:
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Qualifying page
    """
    from .user_data import is_valid_language

    # Validate and fallback for language
    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        gpro_lang = "gb"

    return f"https://gpro.net/{gpro_lang}/Qualify.asp"


def generate_race_analysis_link(gpro_lang: str = "gb") -> str:
    """Generate Race Analysis page link

    Args:
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Race Analysis page
    """
    from .user_data import is_valid_language

    # Validate and fallback for language
    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        gpro_lang = "gb"

    return f"https://gpro.net/{gpro_lang}/RaceAnalysis.asp"


def is_qualifying_closed(race_id: int, race_data: dict) -> bool:
    """Check if qualifying is currently closed (between deadline and opens_soon)

    Qualifying is closed when:
    - Current time is after the quali_close deadline
    - AND the "opens_soon" notification hasn't been sent yet for this race

    Args:
        race_id: The race ID to check
        race_data: The race data dict

    Returns:
        bool: True if qualifying is closed and waiting for race to be calculated
    """
    from .checker import notify_history

    now = datetime.utcnow()
    quali_close = race_data.get("quali_close")

    if not quali_close:
        return False

    # Check if qualifying deadline has passed
    if now <= quali_close:
        return False

    # Check if "opens_soon" notification was already sent (meaning quali is open)
    history_key = (race_id, "opens_soon")
    if history_key in notify_history:
        return False

    # Qualifying is closed if deadline passed and opens_soon not sent yet
    return True


# ==========================================
# APP Website URL Generators
# ==========================================


def format_group_for_app_url(group: str) -> str:
    """Convert group code to APP URL format

    Examples:
        E → Elite
        M3 → Master%20-%203
        R11 → Rookie%20-%2011

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL-encoded group string for APP URLs
    """
    if not group:
        return ""

    group = group.strip().upper()

    if group == "E":
        return "Elite"

    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        return ""

    letter, number = match.groups()
    group_names = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}
    group_name = group_names[letter]

    return f"{group_name}%20-%20{number}"


def generate_app_quali_link() -> str:
    """Generate APP qualifying page link (office page)

    Returns:
        str: URL to APP office page (no language or group support)
    """
    return "https://app.gpro.net/office"


def generate_app_starting_grid_link(group: str = None) -> str:
    """Generate APP starting grid link

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL to APP starting grid page
    """
    base_url = "https://app.gpro.net/qstandings/startgrid"

    if not group:
        return base_url

    formatted_group = format_group_for_app_url(group)
    if formatted_group:
        return f"{base_url}/{formatted_group}"
    else:
        return base_url


def generate_app_race_live_link() -> str:
    """Generate APP race live link

    Returns:
        str: URL to APP race live page (no group or language support)
    """
    return "https://app.gpro.net/liverace"


def generate_app_race_replay_link() -> str:
    """Generate APP race replay link

    Returns:
        str: URL to APP race replay page (no group or language support)
    """
    return "https://app.gpro.net/pastrace/racereplay"


def generate_app_race_analysis_link() -> str:
    """Generate APP race analysis link

    Returns:
        str: URL to APP race analysis page (no group or language support)
    """
    return "https://app.gpro.net/pastrace/analysis"


def generate_app_race_summary_link(group: str = None) -> str:
    """Generate APP race summary link

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL to APP race summary page
    """
    base_url = "https://app.gpro.net/pastrace/summary"

    if not group:
        return base_url

    formatted_group = format_group_for_app_url(group)
    if formatted_group:
        return f"{base_url}/{formatted_group}"
    else:
        return base_url


WEATHER_CONDITIONS = {
    "Sunny": "☀️",
    "Partially Cloudy": "⛅",
    "Cloudy": "🌥️",
    "Very Cloudy": "☁️",
    "Rain": "🌧️",
}


def get_temp_icon(temp: int) -> str:
    """Return temperature icon based on value
    
    Args:
        temp: Temperature value in Celsius
        
    Returns:
        Icon based on temperature (🔥 for hot, 🧊 for cold, 🌡️ for normal)
    """
    if isinstance(temp, int):
        if temp > 38:
            return "🔥"
        if temp < 12:
            return "🧊"
    return "🌡️"


def get_hum_icon() -> str:
    """Return static humidity icon"""
    return "💧"


def get_rain_icon(rain_prob: int) -> str:
    """Return rain icon based on probability
    
    Args:
        rain_prob: Rain probability percentage (0-100)
        
    Returns:
        Icon based on rain probability (💨 for none, ⛈️ for heavy, 🌧️ for moderate, ☔ for light)
    """
    if isinstance(rain_prob, int):
        if rain_prob == 0:
            return "💨"
        if rain_prob >= 80:
            return "⛈️"
        if rain_prob >= 50:
            return "🌧️"
    return "☔"


def get_time_interval_icon() -> str:
    """Return static time interval icon"""
    return "🕐"


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
    now = datetime.utcnow()

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
    now = datetime.utcnow()

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


def translate_weather_condition(weather_condition: str, get_text_func) -> str:
    """Translate weather condition from English to user's language

    Args:
        weather_condition: Weather condition in English (e.g., "Sunny", "Rain")
        get_text_func: Function to get translated text

    Returns:
        str: Translated weather condition with icon
    """
    normalized_condition = weather_condition.strip().title()

    weather_map = {
        "Sunny": "weather-condition-sunny",
        "Partially Cloudy": "weather-condition-partially-cloudy",
        "Cloudy": "weather-condition-cloudy",
        "Very Cloudy": "weather-condition-very-cloudy",
        "Rain": "weather-condition-rain",
    }

    translation_key = weather_map.get(normalized_condition)
    if translation_key:
        translated = get_text_func(translation_key)
        icon = WEATHER_CONDITIONS.get(normalized_condition, "")
        return f"{icon} {translated}" if icon else translated
    else:
        return weather_condition


def format_weather_data(weather: dict, i18n=None, user_id: int = None) -> str:
    """Format weather data into human-readable text

    Args:
        weather: Weather data from Practice API
        i18n: I18n context for translations (optional)
        user_id: User ID for getting user's UI language (optional)

    Returns:
        str: Formatted weather message
    """
    # Import i18n context if not provided
    if i18n is None:
        # Get user's UI language if user_id is provided
        ui_lang = "gb"
        if user_id is not None:
            user_status = get_user_status(user_id)
            ui_lang = user_status.get("ui_lang", "gb")

        # Use the global translation function with user's UI language
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:
        # Use i18n if available
        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    if not weather:
        return get_text("weather-unavailable")

    # Practice / Qualify 1
    q1_weather_raw = weather.get("q1WeatherTransl", "Unknown")
    q1_weather = translate_weather_condition(q1_weather_raw, get_text)
    q1_temp = weather.get("q1Temp", "?")
    q1_hum = weather.get("q1Hum", "?")

    # Qualify 2 / Race Start
    q2_weather_raw = weather.get("q2WeatherTransl", "Unknown")
    q2_weather = translate_weather_condition(q2_weather_raw, get_text)
    q2_temp = weather.get("q2Temp", "?")
    q2_hum = weather.get("q2Hum", "?")

    message = get_text("weather-title") + "\n\n"
    message += get_text("weather-practice-q1", weather=q1_weather) + "\n"
    message += get_text(
        "weather-temp-hum",
        temp=f"{get_temp_icon(q1_temp) if isinstance(q1_temp, int) else ''} {q1_temp}",
        hum=f"{get_hum_icon()} {q1_hum}",
    ) + "\n\n"
    message += get_text("weather-q2-race-start", weather=q2_weather) + "\n"
    message += get_text(
        "weather-temp-hum",
        temp=f"{get_temp_icon(q2_temp) if isinstance(q2_temp, int) else ''} {q2_temp}",
        hum=f"{get_hum_icon()} {q2_hum}",
    ) + "\n\n"

    # Race Quarters
    message += get_text("weather-race-conditions") + "\n"

    quarters = [
        ("weather-start-0h30m", "raceQ1"),
        ("weather-0h30m-1h00m", "raceQ2"),
        ("weather-1h00m-1h30m", "raceQ3"),
        ("weather-1h30m-2h00m", "raceQ4"),
    ]

    for label_key, prefix in quarters:
        temp_low = weather.get(f"{prefix}TempLow", "?")
        temp_high = weather.get(f"{prefix}TempHigh", "?")
        hum_low = weather.get(f"{prefix}HumLow", "?")
        hum_high = weather.get(f"{prefix}HumHigh", "?")
        rain_low = weather.get(f"{prefix}RainPLow", "?")
        rain_high = weather.get(f"{prefix}RainPHigh", "?")

        # Format ranges - show single value if min == max
        temp_str = (
            f"{temp_low}°" if temp_low == temp_high else f"{temp_low}°-{temp_high}°"
        )
        hum_str = f"{hum_low}%" if hum_low == hum_high else f"{hum_low}%-{hum_high}%"
        rain_str = (
            f"{rain_low}%" if rain_low == rain_high else f"{rain_low}%-{rain_high}%"
        )

        # Get icons for temp (use higher value for range), humidity, and rain
        temp_icon = (
            get_temp_icon(temp_high)
            if isinstance(temp_high, int)
            else ""
        )
        rain_icon = (
            get_rain_icon(rain_high)
            if isinstance(rain_high, int)
            else ""
        )

        message += f"\n{get_time_interval_icon()} {get_text(label_key)}\n"
        message += get_text(
            "weather-temp-hum-range",
            temp=f"{temp_icon} {temp_str}",
            hum=f"{get_hum_icon()} {hum_str}",
        ) + "\n"
        message += get_text("weather-rain-prob", rain=f"{rain_icon} {rain_str}") + "\n"

    return message


async def send_race_live_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    """Send notification when race goes live"""
    from timezone_utils import format_datetime_for_user

    user_status = get_user_status(user_id)
    group = user_status.get("group")
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")  # Get user's UI language
    website_mode = user_status.get("website_mode", "classic")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate race live link based on website mode
    if website_mode == "app":
        race_link = generate_app_race_live_link()
        # APP live doesn't support group, always use no-group message
        logger.debug(
            f"User {user_id} using APP mode - Live: {race_link} (no group support)"
        )
    else:
        race_link = generate_race_link(group, gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Live: {race_link}")

    # Import i18n context if not provided
    if i18n is None:
        # Use the global translation function with user's UI language
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:
        # Use i18n context from handler
        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    # Build message based on website mode and group
    # APP mode: always use simple message (no group warning needed)
    # Classic mode: show warning only if group not set
    if website_mode == "app" or group:
        message = get_text(
            "notif-race-live",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            raceLink=race_link,
        )
    else:
        message = get_text(
            "notif-race-live-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            raceLink=race_link,
        )

    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        logger.info(f"🏁 Sent race live notification to {user_id} for race {race_id}")
    except Exception as e:
        logger.error(f"Race live notify {user_id} failed: {e}")


async def send_race_replay_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    """Send race replay notification when next quali opens"""
    from timezone_utils import format_datetime_for_user

    user_status = get_user_status(user_id)
    group = user_status.get("group")
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")  # Get user's UI language
    website_mode = user_status.get("website_mode", "classic")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate replay link based on website mode
    if website_mode == "app":
        replay_link = generate_app_race_replay_link()
        # APP replay doesn't support group, always use no-group message
        logger.debug(
            f"User {user_id} using APP mode - Replay: {replay_link} (no group support)"
        )
    else:
        replay_link = generate_replay_link(group, gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Replay: {replay_link}")

    # Import i18n context if not provided
    if i18n is None:
        # Use the global translation function with user's UI language
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:
        # Use i18n context from handler
        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    # Build message based on website mode and group
    # APP mode: always use simple message (no group warning needed)
    # Classic mode: show warning only if group not set
    if website_mode == "app" or group:
        message = get_text(
            "notif-race-replay",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            replayLink=replay_link,
        )
    else:
        message = get_text(
            "notif-race-replay-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            replayLink=replay_link,
        )

    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        logger.info(f"📺 Sent race replay notification to {user_id} for race {race_id}")
    except Exception as e:
        logger.error(f"Race replay notify {user_id} failed: {e}")


async def send_race_results_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    """Send race results notification when next quali opens"""
    from timezone_utils import format_datetime_for_user

    user_status = get_user_status(user_id)
    group = user_status.get("group")
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")  # Get user's UI language
    website_mode = user_status.get("website_mode", "classic")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate analysis and summary links based on website mode
    if website_mode == "app":
        analysis_link = generate_app_race_analysis_link()
        summary_link = generate_app_race_summary_link(group)
        logger.debug(
            f"User {user_id} using APP mode - Analysis: {analysis_link}, Summary: {summary_link}"
        )
    else:
        # Race Analysis link (same for everyone, just language)
        analysis_link = generate_race_analysis_link(gpro_lang)
        # Race Summary link (group-dependent)
        summary_link = generate_gpro_link(
            group, gpro_lang, "replay"
        )  # Use same format as replay
        summary_link = summary_link.replace("racescreen.asp", "RaceSummary.asp")
        logger.debug(
            f"User {user_id} using Classic mode - Analysis: {analysis_link}, Summary: {summary_link}"
        )

    # Import i18n context if not provided
    if i18n is None:
        # Use the global translation function with user's UI language
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:
        # Use i18n context from handler
        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    # Build message based on whether group is set
    if group:
        message = get_text(
            "notif-race-results",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            analysisLink=analysis_link,
            summaryLink=summary_link,
        )
    else:
        message = get_text(
            "notif-race-results-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            analysisLink=analysis_link,
        )

    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        logger.info(
            f"📊 Sent race results notification to {user_id} for race {race_id}"
        )
    except Exception as e:
        logger.error(f"Race results notify {user_id} failed: {e}")


async def send_quali_results_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    """Send qualifying results notification after quali deadline"""
    from timezone_utils import format_datetime_for_user

    user_status = get_user_status(user_id)
    group = user_status.get("group")
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")
    website_mode = user_status.get("website_mode", "classic")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    quali_close = race_data["quali_close"]
    quali_close_time = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    if website_mode == "app":
        starting_grid_link = generate_app_starting_grid_link(group)
        logger.debug(
            f"User {user_id} using APP mode - Starting grid: {starting_grid_link}"
        )
    else:
        starting_grid_link = generate_starting_grid_link(group, gpro_lang)
        logger.debug(
            f"User {user_id} using Classic mode - Starting grid: {starting_grid_link}"
        )

    if i18n is None:
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:

        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    if group:
        message = get_text(
            "notif-quali-results",
            raceId=race_id,
            track=track,
            qualiClose=quali_close_time,
            raceTime=race_time,
            gridLink=starting_grid_link,
        )
    else:
        message = get_text(
            "notif-quali-results-no-group",
            raceId=race_id,
            track=track,
            qualiClose=quali_close_time,
            raceTime=race_time,
            gridLink=starting_grid_link,
        )

    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        logger.info(
            f"🏁 Sent quali results notification to {user_id} for race {race_id}"
        )
    except Exception as e:
        logger.error(f"Quali results notify {user_id} failed: {e}")


async def send_new_season_reminder_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    """Send new season reminder notification before race 1"""
    from timezone_utils import format_datetime_for_user
    from utils import format_group_display

    user_status = get_user_status(user_id)
    group = user_status.get("group")
    ui_lang = user_status.get("ui_lang", "gb")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    if i18n is None:
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:

        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    if group:
        group_display = format_group_display(group)
        message = get_text(
            "notif-new-season-reminder",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            group=group_display,
        )
    else:
        message = get_text(
            "notif-new-season-reminder-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
        )

    try:
        await bot.send_message(user_id, message, parse_mode="HTML")
        logger.info(f"🌟 Sent new season reminder to {user_id} for race {race_id}")
    except Exception as e:
        logger.error(f"New season reminder to {user_id} failed: {e}")


async def send_quali_notification(
    bot: Bot,
    user_id: int,
    race_id: int,
    race_data: Dict,
    notification_type: str = "deadline",
    i18n=None,
):
    from timezone_utils import format_datetime_for_user

    user_status = get_user_status(user_id)

    # Skip automatic notifications if user marked quali done
    if user_status.get("completed_quali") == race_id and notification_type != "manual":
        return

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    quali_close = race_data["quali_close"]
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")  # Get user's UI language
    website_mode = user_status.get("website_mode", "classic")

    # Generate qualifying link based on website mode
    if website_mode == "app":
        quali_link = generate_app_quali_link()
        logger.debug(f"User {user_id} using APP mode - Quali link: {quali_link}")
    else:
        quali_link = generate_quali_link(gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Quali link: {quali_link}")

    # Import i18n context if not provided
    if i18n is None:
        # Use the global translation function with user's UI language
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:
        # Use i18n context from handler
        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    # Check if this is a snoozed notification
    is_snoozed = notification_type.startswith("snooze_")
    if is_snoozed:
        original_type = notification_type.replace("snooze_", "")
    else:
        original_type = notification_type

    # Check if qualifying is currently closed (between deadline and opens_soon)
    quali_is_closed = is_qualifying_closed(race_id, race_data)

    if quali_is_closed and not is_snoozed:
        # Qualifying is closed, waiting for race to be calculated
        emoji = "🔒"
        title = get_text("notif-quali-closed-title")
        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
    elif notification_type == "opens_soon":
        emoji = "🆕"
        title = get_text("notif-quali-opens")
        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
    else:
        now = datetime.utcnow()
        if "hours_left" not in race_data:
            hours_left = (quali_close - now).total_seconds() / 3600
        else:
            hours_left = race_data["hours_left"]

        if hours_left >= 24:
            days = int(hours_left / 24)
            remaining_hours = int(hours_left % 24)
            if remaining_hours > 0:
                time_text = get_text(
                    "time-days-hours", days=days, hours=remaining_hours
                )
            else:
                time_text = get_text("time-days", days=days)
            emoji = "🔔"
        elif hours_left >= 2:
            hours = int(hours_left)
            minutes = int((hours_left - hours) * 60)
            if minutes > 0:
                time_text = get_text("time-hours-minutes", hours=hours, minutes=minutes)
            else:
                time_text = get_text("time-hours", hours=hours)
            emoji = "⏰"
        else:
            # For anything under 2 hours, just show minutes
            minutes = int(hours_left * 60)
            time_text = get_text("time-minutes", minutes=minutes)
            if hours_left >= 0.333:
                emoji = "⚠️"
            else:
                emoji = "🚨"

        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
        title = get_text("notif-quali-closes", time=time_text)

    # Add 🔁 prefix for snoozed notifications
    if is_snoozed:
        title = f"🔁 {title}"

    # Check if user already marked this race done
    is_marked_done = user_status.get("completed_quali") == race_id

    # Check if weather data is available
    has_weather = race_id in race_calendar and "weather" in race_calendar[race_id]

    # Special message format when qualifying is closed
    if quali_is_closed:
        # Only show weather button if available (no "Done" button when closed)
        keyboard_buttons = []
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )

        keyboard = (
            InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            if keyboard_buttons
            else None
        )
        message = get_text(
            "notif-quali-closed-message",
            emoji=emoji,
            title=title,
            raceId=race_id,
            track=track,
            qualiDeadline=deadline,
            raceTime=race_time,
        )
    elif is_marked_done:
        keyboard_buttons = [
            [
                InlineKeyboardButton(
                    text=get_text("button-reenable-race", raceId=race_id),
                    callback_data=f"reset_{race_id}",
                )
            ]
        ]
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        message = get_text(
            "notif-quali-message-disabled",
            emoji=emoji,
            title=title,
            raceId=race_id,
            track=track,
            qualiDeadline=deadline,
            raceTime=race_time,
            qualiLink=quali_link,
        )
    else:
        keyboard_buttons = [
            [
                InlineKeyboardButton(
                    text=get_text("button-quali-done"), callback_data=f"done_{race_id}"
                )
            ]
        ]
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )

        # Add snooze buttons for qualifying deadline notifications
        if (
            original_type in QUALI_NOTIFICATION_TYPES
            and original_type != "manual"
            and not quali_is_closed
        ):
            snooze_buttons = get_snooze_buttons(
                user_id, race_id, original_type, get_text
            )
            if snooze_buttons:
                keyboard_buttons.extend(snooze_buttons)

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

        # Use snooze-specific message template if snoozed
        if is_snoozed:
            message = get_text(
                "notif-snooze-message",
                emoji=emoji,
                title=title,
                raceId=race_id,
                track=track,
                qualiDeadline=deadline,
                raceTime=race_time,
                qualiLink=quali_link,
            )
        else:
            message = get_text(
                "notif-quali-message",
                emoji=emoji,
                title=title,
                raceId=race_id,
                track=track,
                qualiDeadline=deadline,
                raceTime=race_time,
                qualiLink=quali_link,
            )

    try:
        await bot.send_message(
            user_id, message, reply_markup=keyboard, parse_mode="HTML"
        )
        logger.info(f"✅ Sent {notification_type} to {user_id} for race {race_id}")
    except Exception as e:
        logger.error(f"Notify {user_id} failed: {e}")

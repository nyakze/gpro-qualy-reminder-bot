"""Functions for sending notifications to users"""

import logging
import re
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from typing import Dict

from gpro_calendar import race_calendar
from utils import add_flag_to_track
from .user_data import get_user_status, DEFAULT_USER_LANG

logger = logging.getLogger(__name__)


def generate_gpro_link(group: str, gpro_lang: str = "gb", link_type: str = "live") -> str:
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


def generate_quali_standings_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate Q1 Q2 Standings link with user's group

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Q1 Q2 Standings page
    """
    from .user_data import is_valid_language

    # Validate and fallback for language
    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        gpro_lang = "gb"

    base_url = f"https://gpro.net/{gpro_lang}/Qualify12Standings.asp?Group="

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


def generate_app_race_live_link(group: str = None, gpro_lang: str = "gb") -> str:
    """Generate APP race live link

    NOTE: APP live race link not found yet, using classic fallback

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for fallback classic URL

    Returns:
        str: URL to race live page (currently returns classic URL)
    """
    # TODO: Replace with APP link when found
    # For now, use classic link as fallback
    return generate_race_link(group, gpro_lang)


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


def translate_weather_condition(weather_condition: str, get_text_func) -> str:
    """Translate weather condition from English to user's language

    Args:
        weather_condition: Weather condition in English (e.g., "Sunny", "Rain")
        get_text_func: Function to get translated text

    Returns:
        str: Translated weather condition
    """
    # Normalize the weather condition (title case for consistent lookup)
    normalized_condition = weather_condition.strip().title()

    # Map English weather conditions to translation keys
    weather_map = {
        "Sunny": "weather-condition-sunny",
        "Partially Cloudy": "weather-condition-partially-cloudy",
        "Cloudy": "weather-condition-cloudy",
        "Very Cloudy": "weather-condition-very-cloudy",
        "Rain": "weather-condition-rain",
    }

    # Get translation key, fallback to original if not found
    translation_key = weather_map.get(normalized_condition)
    if translation_key:
        return get_text_func(translation_key)
    else:
        # Return original if no translation found (for unknown conditions)
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
    message += get_text("weather-temp-hum", temp=q1_temp, hum=q1_hum) + "\n\n"
    message += get_text("weather-q2-race-start", weather=q2_weather) + "\n"
    message += get_text("weather-temp-hum", temp=q2_temp, hum=q2_hum) + "\n\n"

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

        message += f"\n{get_text(label_key)}\n"
        message += get_text("weather-temp-hum-range", temp=temp_str, hum=hum_str) + "\n"
        message += get_text("weather-rain-prob", rain=rain_str) + "\n"

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
        race_link = generate_app_race_live_link(group, gpro_lang)
        logger.debug(f"User {user_id} using APP mode - Race live: {race_link} (classic fallback)")
    else:
        race_link = generate_race_link(group, gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Race live: {race_link}")

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
        has_group_support = False
        logger.debug(f"User {user_id} using APP mode - Replay: {replay_link} (no group support)")
    else:
        replay_link = generate_replay_link(group, gpro_lang)
        has_group_support = True
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

    # Build message based on whether group is set AND mode supports group
    if group and has_group_support:
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
        logger.debug(f"User {user_id} using APP mode - Analysis: {analysis_link}, Summary: {summary_link}")
    else:
        # Race Analysis link (same for everyone, just language)
        analysis_link = generate_race_analysis_link(gpro_lang)
        # Race Summary link (group-dependent)
        summary_link = generate_gpro_link(
            group, gpro_lang, "replay"
        )  # Use same format as replay
        summary_link = summary_link.replace("racescreen.asp", "RaceSummary.asp")
        logger.debug(f"User {user_id} using Classic mode - Analysis: {analysis_link}, Summary: {summary_link}")

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
    ui_lang = user_status.get("ui_lang", "gb")  # Get user's UI language
    website_mode = user_status.get("website_mode", "classic")

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    quali_close = race_data["quali_close"]
    quali_close_time = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate starting grid link based on website mode (Q1/Q2 links removed)
    if website_mode == "app":
        starting_grid_link = generate_app_starting_grid_link(group)
        logger.debug(f"User {user_id} using APP mode - Starting grid: {starting_grid_link}")
    else:
        starting_grid_link = generate_starting_grid_link(group, gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Starting grid: {starting_grid_link}")

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

    # Build message based on whether group is set (only starting grid link)
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

    if notification_type == "opens_soon":
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
                time_text = get_text("time-days-hours", days=days, hours=remaining_hours)
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
        elif hours_left >= 0.333:
            time_text = get_text("time-minutes", minutes=10)
            emoji = "⚠️"
        else:
            minutes = int(hours_left * 60)
            time_text = get_text("time-minutes", minutes=minutes)
            emoji = "🚨"

        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
        title = get_text("notif-quali-closes", time=time_text)

    # Check if user already marked this race done
    is_marked_done = user_status.get("completed_quali") == race_id

    # Check if weather data is available
    has_weather = race_id in race_calendar and "weather" in race_calendar[race_id]

    if is_marked_done:
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

        keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
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

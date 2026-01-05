"""Shared utility functions for GPRO Bot"""

import pycountry
import math
import re
from datetime import datetime

# UI Language Display Names
UI_LANGUAGE_DISPLAY = {
    "en": "🇬🇧 English",
    "ru": "🇷🇺 Русский",
    "br": "🇧🇷 Português",
    "it": "🇮🇹 Italiano",
    "es": "🇪🇸 Español",
    "fr": "🇫🇷 Français",
}


def get_ui_language_display(lang_code: str) -> str:
    """Get display name for a UI language code

    Args:
        lang_code: Language code (e.g., 'en', 'ru', 'br')

    Returns:
        str: Display name with flag (e.g., '🇬🇧 English')
    """
    return UI_LANGUAGE_DISPLAY.get(lang_code, "🇬🇧 English")


def country_code_to_flag(country_code: str) -> str:
    """Convert ISO 2-letter country code to flag emoji

    Flag emojis are composed of regional indicator symbols.
    Each letter is converted to a regional indicator symbol.

    Examples:
        "US" -> "🇺🇸"
        "GB" -> "🇬🇧"
        "FR" -> "🇫🇷"
    """
    if not country_code or len(country_code) != 2:
        return ""

    # Regional indicator symbols start at 0x1F1E6 (for 'A')
    REGIONAL_INDICATOR_A = 0x1F1E6
    country_code = country_code.upper()

    try:
        flag = "".join(
            chr(REGIONAL_INDICATOR_A + ord(char) - ord("A")) for char in country_code
        )
        return flag
    except (ValueError, TypeError):
        return ""


def get_country_iso_code(country_name: str) -> str:
    """Automatically get ISO code for any country name using pycountry

    Handles variations and common names automatically.
    Returns empty string if country not found.
    """
    if not country_name:
        return ""

    # Try exact match first
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_2
    except (KeyError, AttributeError):
        pass

    # Try fuzzy search
    try:
        results = pycountry.countries.search_fuzzy(country_name)
        if results:
            return results[0].alpha_2
    except (KeyError, LookupError, AttributeError):
        pass

    return ""


def add_flag_to_track(track: str) -> str:
    """Replace country name in parentheses with flag emoji

    Automatically detects country and converts to flag emoji.
    Works for any country without needing manual mapping.

    Examples:
        "Yas Marina GP (United Arab Emirates)" -> "Yas Marina GP 🇦🇪"
        "Sakhir GP (Bahrain)" -> "Sakhir GP 🇧🇭"
        "Silverstone GP (United Kingdom)" -> "Silverstone GP 🇬🇧"
    """
    if not track or "(" not in track:
        return track

    try:
        track_name = track.split("(")[0].strip()
        country = track.split("(")[1].split(")")[0].strip()

        # Get ISO code automatically
        iso_code = get_country_iso_code(country)
        if iso_code:
            flag = country_code_to_flag(iso_code)
            return f"{track_name} {flag}"
        else:
            # If country not found, keep original format
            return track
    except (IndexError, AttributeError):
        return track


def format_group_display(group: str) -> str:
    """Convert group code to human-readable format

    Examples:
        E -> Elite
        M3 -> Master - 3
        P15 -> Pro - 15
        A42 -> Amateur - 42
        R11 -> Rookie - 11
    """
    if not group:
        return "Not set"

    group = group.strip().upper()
    if group == "E":
        return "Elite"

    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        return group  # Return as-is if invalid format

    letter, number = match.groups()
    group_names = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}

    return f"{group_names[letter]} - {number}"


def format_time_until_quali(quali_close: datetime, i18n=None) -> str:
    """Time remaining until quali deadline - human friendly

    Args:
        quali_close: Qualification close datetime
        i18n: Optional i18n context for translations

    Returns:
        Formatted time string (e.g., "2 hours 45 minutes" or "2h45m" if no i18n)
    """
    now = datetime.utcnow()
    delta = quali_close - now

    total_minutes = delta.total_seconds() / 60
    if total_minutes <= 0:
        return ""

    total_hours = total_minutes / 60
    total_days = total_hours / 24

    # Helper to get i18n text or fallback to abbreviations
    def get_text(key, **kwargs):
        if i18n:
            try:
                return i18n.get(key, **kwargs)
            except:
                pass
        # Fallback to abbreviations if no i18n
        return None

    if total_minutes < 100:  # Less than 100 minutes → show minutes or H:M
        hours = math.floor(total_minutes / 60)
        minutes = math.floor(total_minutes % 60)
        if hours > 0:
            text = get_text("time-hours-minutes", hours=hours, minutes=minutes)
            return text if text else f"{hours}h{minutes}m"
        else:
            text = get_text("time-minutes", minutes=minutes)
            return text if text else f"{minutes}m"
    elif total_days >= 30:  # 30+ days → months + days
        months = math.floor(total_days / 30)
        remaining_days = math.floor(total_days % 30)
        if remaining_days > 0:
            text = get_text("time-months-days", months=months, days=remaining_days)
            return text if text else f"{months}mo {remaining_days}d"
        else:
            text = get_text("time-months", months=months)
            return text if text else f"{months}mo"
    elif total_hours >= 120:  # 5+ days → just days
        days = math.floor(total_hours / 24)
        text = get_text("time-days", days=days)
        return text if text else f"{days}d"
    elif total_hours >= 24:  # 1+ day → "1d 14h"
        days = math.floor(total_hours / 24)
        remaining_hours = math.floor(total_hours % 24)
        if remaining_hours > 0:
            text = get_text("time-days-hours", days=days, hours=remaining_hours)
            return text if text else f"{days}d {remaining_hours}h"
        else:
            text = get_text("time-days", days=days)
            return text if text else f"{days}d"
    else:
        hours = math.floor(total_hours)
        text = get_text("time-hours", hours=hours)
        return text if text else f"{hours}h"


def format_race_beautiful(race_data: dict) -> str:
    """Format race data for display"""
    if not race_data:
        return "None"

    track = race_data.get("track", "Unknown")
    track = add_flag_to_track(track)
    hours_left = race_data.get("hours_left", 0)
    quali_close = race_data.get("quali_close", datetime.utcnow())

    hours_display = math.floor(hours_left)
    deadline = quali_close.strftime("%d.%m %H:%M")

    return f"Qualification closes in {hours_display}h\n**({deadline})** - {track}"


def get_localized_weekday(date: datetime, i18n=None) -> str:
    """Get 2-letter weekday abbreviation in the user's language

    Args:
        date: Date to get weekday for
        i18n: Optional i18n context for translations

    Returns:
        2-letter weekday abbreviation (e.g., "Mo", "Tu", "Пн", "Вт")
    """
    weekday_map = {
        0: "weekday-mon",
        1: "weekday-tue",
        2: "weekday-wed",
        3: "weekday-thu",
        4: "weekday-fri",
        5: "weekday-sat",
        6: "weekday-sun",
    }

    weekday_key = weekday_map[date.weekday()]

    if i18n:
        return i18n.get(weekday_key)
    else:
        # Fallback to English 3-letter abbreviation if no i18n
        return date.strftime("%a")


def format_full_calendar(
    calendar_data: dict,
    title: str = "Full Season",
    is_current_season: bool = True,
    user_id: int = None,
    i18n=None,
) -> str:
    """Generic formatter for current/next season

    Args:
        calendar_data: Dictionary of race data
        title: Title for the calendar
        is_current_season: Whether this is the current season
        user_id: Optional user ID for timezone conversion
        i18n: Optional i18n context for translations

    Returns:
        Formatted calendar text
    """
    if not calendar_data:
        return "No races scheduled"

    now = datetime.utcnow()
    race_list = []

    # Collect races 1-17 in sequential order
    if isinstance(calendar_data, dict):
        for race_id in range(1, 18):
            if race_id in calendar_data and isinstance(calendar_data[race_id], dict):
                race_data = calendar_data[race_id].copy()
                race_data["race_id"] = race_id
                race_list.append(race_data)

    # 🔥 Next race ТОЛЬКО для current season
    next_race_id = None
    if is_current_season:
        for race in race_list:
            if race.get("quali_close", now) > now:
                next_race_id = race["race_id"]
                break

    text = ""
    for race in race_list:
        track = race.get("track", f'Race {race["race_id"]}')
        track = add_flag_to_track(track)
        race_date = race.get("date", now)
        quali_close = race.get("quali_close", now)
        race_id = race["race_id"]

        # Format datetime with timezone if user_id provided
        if user_id is not None:
            from timezone_utils import format_datetime_for_user, convert_to_user_tz

            # Get localized datetime with timezone abbreviation
            date_time_tz = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
            # Also convert race_date for weekday calculation
            race_date = convert_to_user_tz(race_date, user_id) or race_date
        else:
            # Fallback to UTC if no user_id
            date_time_tz = race_date.strftime("%d.%m %H:%M UTC")

        # Get localized 2-letter weekday abbreviation
        weekday = get_localized_weekday(race_date, i18n)
        time_text = format_time_until_quali(quali_close, i18n)

        # Build time info with weekday, date, time, and timezone
        time_info = f"{weekday} {date_time_tz}"
        if time_text:
            time_info += f" • {time_text}"

        # 🔥 ONLY для current season next race
        if next_race_id and race_id == next_race_id:
            text += f"🔥 #{race_id} **{track}**\n{time_info}\n"
        else:
            text += f"#{race_id} **{track}**\n{time_info}\n"

    return text.rstrip()

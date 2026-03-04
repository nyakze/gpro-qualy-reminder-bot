"""Weather formatting utilities for notifications"""

from typing import Callable

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
        if temp < 12:
            return "🧊"
        if temp > 31:
            return "🔥"
    return "🌡️"


def get_temp_icon_for_range(temp_low: int, temp_high: int) -> str:
    """Return temperature icon based on range values

    Args:
        temp_low: Low temperature value in Celsius
        temp_high: High temperature value in Celsius

    Returns:
        Icon based on temperature (🔥 if any value >38, 🧊 if any value <12, 🌡️ otherwise)
    """
    if isinstance(temp_low, int) and isinstance(temp_high, int):
        if temp_low < 12 or temp_high < 12:
            return "🧊"
        if temp_low > 31 or temp_high > 31:
            return "🔥"
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


def translate_weather_condition(weather_condition: str, get_text_func: Callable) -> str:
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


def format_weather_data(weather: dict, i18n=None, user_id: int | None = None) -> str:
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
            from notifications.users import get_user_status

            user_status, _ = get_user_status(user_id)
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
    message += (
        get_text(
            "weather-temp-hum",
            temp=f"{get_temp_icon(q1_temp) if isinstance(q1_temp, int) else ''} {q1_temp}",
            hum=f"{get_hum_icon()} {q1_hum}",
        )
        + "\n\n"
    )
    message += get_text("weather-q2-race-start", weather=q2_weather) + "\n"
    message += (
        get_text(
            "weather-temp-hum",
            temp=f"{get_temp_icon(q2_temp) if isinstance(q2_temp, int) else ''} {q2_temp}",
            hum=f"{get_hum_icon()} {q2_hum}",
        )
        + "\n\n"
    )

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

        # Get icons for temp (check range), humidity, and rain
        temp_icon = (
            get_temp_icon_for_range(temp_low, temp_high)
            if isinstance(temp_low, int) and isinstance(temp_high, int)
            else ""
        )
        rain_icon = get_rain_icon(rain_high) if isinstance(rain_high, int) else ""

        message += f"\n{get_time_interval_icon()} {get_text(label_key)}\n"
        message += (
            get_text(
                "weather-temp-hum-range",
                temp=f"{temp_icon} {temp_str}",
                hum=f"{get_hum_icon()} {hum_str}",
            )
            + "\n"
        )
        message += get_text("weather-rain-prob", rain=f"{rain_icon} {rain_str}") + "\n"

    return message

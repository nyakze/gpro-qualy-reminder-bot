"""Notification utilities package

This package contains utility modules for notifications:
- link_generators: URL generation for Classic and APP websites
- weather_formatter: Weather data formatting and icons
- snooze_manager: Snooze functionality and button generation
"""

from notifications.utils.link_generators import (
    generate_gpro_link,
    generate_race_link,
    generate_replay_link,
    generate_starting_grid_link,
    generate_quali_link,
    generate_race_analysis_link,
    generate_app_quali_link,
    generate_app_starting_grid_link,
    generate_app_race_live_link,
    generate_app_race_replay_link,
    generate_app_race_analysis_link,
    generate_app_race_summary_link,
)
from notifications.utils.weather_formatter import (
    format_weather_data,
    translate_weather_condition,
    get_temp_icon,
    get_hum_icon,
    get_rain_icon,
    get_time_interval_icon,
)
from notifications.utils.snooze_manager import (
    can_snooze,
    get_snooze_buttons,
    get_next_notification_time,
    SNOOZE_OPTIONS,
    MAX_SNOOZES,
)

__all__ = [
    # Link generators
    "generate_gpro_link",
    "generate_race_link",
    "generate_replay_link",
    "generate_starting_grid_link",
    "generate_quali_link",
    "generate_race_analysis_link",
    "generate_app_quali_link",
    "generate_app_starting_grid_link",
    "generate_app_race_live_link",
    "generate_app_race_replay_link",
    "generate_app_race_analysis_link",
    "generate_app_race_summary_link",
    # Weather
    "format_weather_data",
    "translate_weather_condition",
    "get_temp_icon",
    "get_hum_icon",
    "get_rain_icon",
    "get_time_interval_icon",
    # Snooze
    "can_snooze",
    "get_snooze_buttons",
    "get_next_notification_time",
    "SNOOZE_OPTIONS",
    "MAX_SNOOZES",
]

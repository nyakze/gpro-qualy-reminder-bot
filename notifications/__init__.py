"""Notifications module - handles user notifications and data management"""

import logging

logger = logging.getLogger(__name__)

# Import and expose all public functions
from .user_data import (
    users_data,
    load_users_data,
    save_users_data,
    get_user_status,
    set_user_group,
    toggle_notification,
    is_notification_enabled,
    set_user_language,
    get_user_language,
    set_user_ui_language,
    get_user_ui_language,
    get_user_timezone,
    set_user_timezone,
    set_user_website_mode,
    get_user_website_mode,
    mark_quali_done,
    reset_user_status,
    update_user_profile,
    get_user_profile,
    LANGUAGE_OPTIONS,
    DEFAULT_USER_LANG,
)

from .validation import (
    parse_time_input,
    validate_custom_notification_hours,
    format_custom_notification_time,
    get_custom_notifications,
    set_custom_notification,
    CUSTOM_NOTIF_MIN_HOURS,
    CUSTOM_NOTIF_MAX_HOURS,
)

from .sender import (
    send_quali_notification,
    send_race_live_notification,
    send_race_replay_notification,
    send_race_results_notification,
    send_quali_results_notification,
    send_new_season_reminder_notification,
    format_weather_data,
)

from .checker import check_notifications

logger.debug("✅ notifications module loaded")

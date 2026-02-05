"""Users package - User data management

This package handles all user-related data:
- storage: File I/O operations
- constants: Default values and configuration
- core: Core user management (groups, notifications, languages, timezone, etc.)
- snooze: Snooze tracking and management
- blocked: Blocked user management
"""

from notifications.users.storage import (
    users_data,
    load_users_data,
    save_users_data,
)
from notifications.users.constants import (
    LANGUAGE_OPTIONS,
    DEFAULT_USER_LANG,
    SNOOZE_TOLERANCE_SECONDS,
    SNOOZE_MAX_COUNTS,
    get_default_notification_preferences,
    get_default_custom_notifications,
    get_default_snooze_tracking,
)
from notifications.users.core import (
    get_user_status,
    set_user_group,
    toggle_notification,
    is_notification_enabled,
    is_valid_language,
    set_user_language,
    get_user_language,
    set_user_ui_language,
    get_user_ui_language,
    get_user_timezone,
    set_user_timezone,
    mark_quali_done,
    reset_user_status,
    set_user_website_mode,
    get_user_website_mode,
    update_user_profile,
    get_user_profile,
)
from notifications.users.snooze import (
    add_snooze_reminder,
    remove_snooze_reminder,
    remove_snooze_reminder_by_time,
    get_all_snooze_reminders,
    get_all_active_snoozes,
    remove_active_snooze,
    get_snooze_count,
    increment_snooze_count,
    reset_snooze_count,
    reset_snooze_counts_for_deadline_passed,
)
from notifications.users.blocked import (
    mark_user_blocked,
    is_user_blocked,
    unblock_user,
)

__all__ = [
    # Storage
    "users_data",
    "load_users_data",
    "save_users_data",
    # Constants
    "LANGUAGE_OPTIONS",
    "DEFAULT_USER_LANG",
    "SNOOZE_TOLERANCE_SECONDS",
    "SNOOZE_MAX_COUNTS",
    "get_default_notification_preferences",
    "get_default_custom_notifications",
    "get_default_snooze_tracking",
    # Core
    "get_user_status",
    "set_user_group",
    "toggle_notification",
    "is_notification_enabled",
    "is_valid_language",
    "set_user_language",
    "get_user_language",
    "set_user_ui_language",
    "get_user_ui_language",
    "get_user_timezone",
    "set_user_timezone",
    "mark_quali_done",
    "reset_user_status",
    "set_user_website_mode",
    "get_user_website_mode",
    "update_user_profile",
    "get_user_profile",
    # Snooze
    "add_snooze_reminder",
    "remove_snooze_reminder",
    "remove_snooze_reminder_by_time",
    "get_all_snooze_reminders",
    "get_all_active_snoozes",
    "remove_active_snooze",
    "get_snooze_count",
    "increment_snooze_count",
    "reset_snooze_count",
    "reset_snooze_counts_for_deadline_passed",
    # Blocked
    "mark_user_blocked",
    "is_user_blocked",
    "unblock_user",
]

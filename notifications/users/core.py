"""Core user data management"""

import logging
from typing import Dict, Tuple

from notifications.users.storage import users_data, save_users_data
from notifications.users.constants import (
    DEFAULT_USER_LANG,
    UI_LANGUAGE_DISPLAY,
    get_default_notification_preferences,
    get_default_custom_notifications,
    get_default_snooze_tracking,
)

logger = logging.getLogger(__name__)


def get_user_status(user_id: int) -> Tuple[Dict, bool]:
    """Get or create user status, with field migrations
    
    Returns:
        Tuple of (user_data_dict, was_new_user)
    """
    logger.debug(f"get_user_status({user_id}): {len(users_data)} users in cache")

    if not users_data:
        from notifications.users.storage import load_users_data
        load_users_data()
        logger.debug(f"Loaded {len(users_data)} users from file")

    was_new = False
    if user_id not in users_data:
        was_new = True
        logger.info(f"🆕 New user {user_id} registered")
        users_data[user_id] = {
            "completed_quali": None,
            "group": None,
            "notifications": get_default_notification_preferences(),
            "custom_notifications": get_default_custom_notifications(),
            "gpro_lang": DEFAULT_USER_LANG,
            "ui_lang": "gb",
            "timezone": "UTC",
            "website_mode": "classic",
            "tg_language_code": None,
            "username": None,
            "first_name": None,
        }
        save_users_data()
    else:
        needs_save = False
        # Migration: Add missing fields
        if "group" not in users_data[user_id]:
            users_data[user_id]["group"] = None
            logger.debug(f"Added 'group' field to user {user_id}")
            needs_save = True
        if "notifications" not in users_data[user_id]:
            users_data[user_id]["notifications"] = get_default_notification_preferences()
            logger.debug(f"Added 'notifications' field to user {user_id}")
            needs_save = True
        if "custom_notifications" not in users_data[user_id]:
            users_data[user_id]["custom_notifications"] = get_default_custom_notifications()
            logger.debug(f"Added 'custom_notifications' field to user {user_id}")
            needs_save = True
        if "gpro_lang" not in users_data[user_id]:
            users_data[user_id]["gpro_lang"] = DEFAULT_USER_LANG
            logger.debug(f"Added 'gpro_lang' field to user {user_id}")
            needs_save = True
        if "ui_lang" not in users_data[user_id]:
            users_data[user_id]["ui_lang"] = "gb"
            logger.debug(f"Added 'ui_lang' field to user {user_id}")
            needs_save = True
        elif users_data[user_id]["ui_lang"] == "en":
            users_data[user_id]["ui_lang"] = "gb"
            logger.debug(f"Migrated user {user_id} from 'en' to 'gb'")
            needs_save = True
        if "72h" not in users_data[user_id]["notifications"]:
            users_data[user_id]["notifications"]["72h"] = True
            logger.debug(f"Added '72h' notification to user {user_id}")
            needs_save = True
        if "new_season_reminder" not in users_data[user_id]["notifications"]:
            users_data[user_id]["notifications"]["new_season_reminder"] = True
            logger.debug(f"Added 'new_season_reminder' notification to user {user_id}")
            needs_save = True
        if "timezone" not in users_data[user_id]:
            users_data[user_id]["timezone"] = "UTC"
            logger.debug(f"Added 'timezone' field to user {user_id}")
            needs_save = True
        if "website_mode" not in users_data[user_id]:
            users_data[user_id]["website_mode"] = "classic"
            logger.debug(f"Added 'website_mode' field to user {user_id}")
            needs_save = True
        if "tg_language_code" not in users_data[user_id]:
            users_data[user_id]["tg_language_code"] = None
            logger.debug(f"Added 'tg_language_code' field to user {user_id}")
            needs_save = True
        if "username" not in users_data[user_id]:
            users_data[user_id]["username"] = None
            logger.debug(f"Added 'username' field to user {user_id}")
            needs_save = True
        if "first_name" not in users_data[user_id]:
            users_data[user_id]["first_name"] = None
            logger.debug(f"Added 'first_name' field to user {user_id}")
            needs_save = True
        if "snooze_tracking" not in users_data[user_id]:
            users_data[user_id]["snooze_tracking"] = get_default_snooze_tracking()
            logger.debug(f"Added 'snooze_tracking' field to user {user_id}")
            needs_save = True
        if "active_snoozes" not in users_data[user_id]:
            users_data[user_id]["active_snoozes"] = {}
            logger.debug(f"Added 'active_snoozes' field to user {user_id}")
            needs_save = True
        if "blocked_at" not in users_data[user_id]:
            users_data[user_id]["blocked_at"] = None
            logger.debug(f"Added 'blocked_at' field to user {user_id}")
            needs_save = True
        if needs_save:
            save_users_data()

    return users_data[user_id], was_new


def set_user_group(user_id: int, group: str):
    """Set user's GPRO group for race links"""
    get_user_status(user_id)
    users_data[user_id]["group"] = group
    save_users_data()
    logger.info(f"User {user_id} set group to: {group}")


def toggle_notification(user_id: int, notification_type: str):
    """Toggle a specific notification type for a user"""
    user_status = get_user_status(user_id)[0]
    current_state = user_status["notifications"].get(notification_type, True)
    user_status["notifications"][notification_type] = not current_state
    save_users_data()
    new_state = "enabled" if not current_state else "disabled"
    logger.info(f"User {user_id} {new_state} '{notification_type}' notifications")
    return not current_state


def is_notification_enabled(user_id: int, notification_type: str) -> bool:
    """Check if a notification type is enabled for a user"""
    user_status = get_user_status(user_id)[0]
    return user_status["notifications"].get(notification_type, True)


def is_valid_language(lang_code: str) -> bool:
    """Validate language code against supported languages"""
    from notifications.users.constants import LANGUAGE_OPTIONS
    return lang_code in LANGUAGE_OPTIONS


def set_user_language(user_id: int, lang: str) -> bool:
    """Set user's preferred language for GPRO URLs"""
    lang = lang.strip().lower()
    if not is_valid_language(lang):
        logger.warning(f"Invalid language code: {lang}")
        return False

    get_user_status(user_id)
    users_data[user_id]["gpro_lang"] = lang
    save_users_data()
    logger.info(f"User {user_id} set language to: {lang}")
    return True


def get_user_language(user_id: int) -> str:
    """Get user's preferred language for GPRO URLs"""
    user_status = get_user_status(user_id)[0]
    return user_status.get("gpro_lang", DEFAULT_USER_LANG)


def set_user_ui_language(user_id: int, lang: str) -> bool:
    """Set user's preferred UI language for bot interface"""
    lang = lang.strip().lower()

    # Validate against available UI languages
    if lang not in UI_LANGUAGE_DISPLAY:
        logger.warning(f"Invalid UI language code: {lang}")
        return False

    get_user_status(user_id)
    users_data[user_id]["ui_lang"] = lang
    save_users_data()
    logger.info(f"User {user_id} set UI language to: {lang}")
    return True


def get_user_ui_language(user_id: int) -> str:
    """Get user's preferred UI language for bot interface"""
    user_status = get_user_status(user_id)[0]
    return user_status.get("ui_lang", "gb")


def get_user_timezone(user_id: int) -> str:
    """Get user's timezone IANA name"""
    user_status = get_user_status(user_id)[0]
    return user_status.get("timezone", "UTC")


def set_user_timezone(user_id: int, timezone: str) -> bool:
    """Set user's timezone"""
    # Validate timezone exists
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo(timezone)
    except Exception as e:
        logger.warning(f"Invalid timezone '{timezone}': {e}")
        return False

    get_user_status(user_id)
    users_data[user_id]["timezone"] = timezone
    save_users_data()
    logger.info(f"User {user_id} set timezone to: {timezone}")
    return True


def mark_quali_done(user_id: int, race_id: int):
    """Mark qualifying as done for a race"""
    get_user_status(user_id)
    users_data[user_id]["completed_quali"] = race_id
    save_users_data()
    logger.info(f"User {user_id} marked race {race_id} done")


def reset_user_status(user_id: int):
    """Reset user's completed quali status"""
    if user_id in users_data:
        users_data[user_id]["completed_quali"] = None
        save_users_data()
        logger.info(f"User {user_id} reset")


def set_user_website_mode(user_id: int, mode: str) -> bool:
    """Set user's website mode (classic or app)"""
    if mode not in ["classic", "app"]:
        logger.warning(f"Invalid website mode: {mode}")
        return False

    get_user_status(user_id)
    users_data[user_id]["website_mode"] = mode
    save_users_data()
    logger.info(f"User {user_id} switched to {mode} mode")
    return True


def get_user_website_mode(user_id: int) -> str:
    """Get user's website mode"""
    user_status = get_user_status(user_id)[0]
    return user_status.get("website_mode", "classic")


def update_user_profile(
    user_id: int,
    tg_language_code: str = None,
    username: str = None,
    first_name: str = None,
) -> bool:
    """Update user's profile data from Telegram message"""
    if user_id not in users_data:
        return False

    needs_save = False

    if tg_language_code is not None:
        current_lang = users_data[user_id].get("tg_language_code")
        if current_lang != tg_language_code:
            users_data[user_id]["tg_language_code"] = tg_language_code
            needs_save = True
            logger.debug(f"Updated tg_language_code for user {user_id}: {tg_language_code}")

    current_username = users_data[user_id].get("username")
    if current_username != username:
        users_data[user_id]["username"] = username
        needs_save = True
        logger.debug(f"Updated username for user {user_id}: {username}")

    if first_name is not None:
        current_name = users_data[user_id].get("first_name")
        if current_name != first_name:
            users_data[user_id]["first_name"] = first_name
            needs_save = True
            logger.debug(f"Updated first_name for user {user_id}: {first_name}")

    if needs_save:
        save_users_data()

    return needs_save


def get_user_profile(user_id: int) -> Dict:
    """Get user's profile data"""
    user_status = get_user_status(user_id)[0]
    return {
        "tg_language_code": user_status.get("tg_language_code"),
        "username": user_status.get("username"),
        "first_name": user_status.get("first_name"),
    }

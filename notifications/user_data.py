"""User data persistence and management"""

import logging
import json
import os
from typing import Dict

logger = logging.getLogger(__name__)

# Import UI language list for validation
try:
    from utils import UI_LANGUAGE_DISPLAY
except ImportError:
    # Fallback if import fails (shouldn't happen in normal operation)
    UI_LANGUAGE_DISPLAY = {
        "gb": "English",
        "ru": "Русский",
        "br": "Português",
        "it": "Italiano",
        "es": "Español",
        "fr": "Français",
        "nl": "Nederlands",
        "bg": "Български",
        "cz": "Čeština",
        "in": "हिन्दी",
        "ua": "Українська",
        "pt": "Português",
    }

users_data: Dict[int, Dict] = {}

# Language options for URL generation (user-facing)
LANGUAGE_OPTIONS = {
    "gb": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "es": "🇪🇸 Español",
    "ro": "🇷🇴 Română",
    "it": "🇮🇹 Italiano",
    "fr": "🇫🇷 Français",
    "pl": "🇵🇱 Polski",
    "bg": "🇧🇬 Български",
    "mk": "🇲🇰 Македонски",
    "nl": "🇳🇱 Nederlands",
    "fi": "🇫🇮 Suomi",
    "hu": "🇭🇺 Magyar",
    "tr": "🇹🇷 Türkçe",
    "gr": "🇬🇷 Ελληνικά",
    "dk": "🇩🇰 Dansk",
    "pt": "🇵🇹 Português",
    "ru": "🇷🇺 Русский",
    "rs": "🇷🇸 Српски",
    "se": "🇸🇪 Svenska",
    "lt": "🇱🇹 Lietuvių",
    "ee": "🇪🇪 Eesti",
    "al": "🇦🇱 Shqip",
    "hr": "🇭🇷 Hrvatski",
    "cn": "🇨🇳 中文",
    "my": "🇲🇾 Bahasa Melayu",
    "in": "🇮🇳 हिन्दी",
    "pi": "🏴‍☠️ Pirate",
    "be": "🇧🇪 Vlaams",
    "br": "🇧🇷 Português (BR)",
    "cz": "🇨🇿 Čeština",
    "sk": "🇸🇰 Slovenčina",
}
DEFAULT_USER_LANG = "gb"

# Use absolute path based on script location for robustness
_SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(_SCRIPT_DIR, "users_data.json")


def get_default_notification_preferences():
    """Default notification settings - all enabled by default"""
    return {
        "72h": True,
        "48h": True,
        "24h": True,
        "2h": True,
        "10min": True,
        "opens_soon": True,
        "quali_results": True,
        "race_replay": True,
        "race_live": True,
        "race_results": True,
    }


def get_default_custom_notifications():
    """Default custom notification settings - empty slots"""
    return [
        {"enabled": False, "hours_before": None},
        {"enabled": False, "hours_before": None},
    ]


def load_users_data():
    global users_data
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                raw_data = json.load(f)
                # TYPE FIX: Convert string keys → int keys
                clean_data = {int(k_str): status for k_str, status in raw_data.items()}
                users_data.update(clean_data)
                logger.debug(f"✅ Loaded {len(users_data)} users (int keys)")
        except Exception as e:
            logger.error(f"Load failed: {e}")


def save_users_data():
    """Save user data with atomic write to prevent corruption"""
    try:
        # Write to temporary file first
        temp_file = USERS_FILE + ".tmp"
        with open(temp_file, "w") as f:
            # TYPE FIX: Convert int keys → string for JSON
            save_data = {str(k): v for k, v in users_data.items()}
            json.dump(save_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is written to disk

        # Atomic rename (overwrites USERS_FILE)
        os.replace(temp_file, USERS_FILE)
        logger.debug(f"Saved {len(users_data)} users")
    except Exception as e:
        logger.error(f"Save failed: {e}")
        # Clean up temp file if it exists
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass


def get_user_status(user_id: int) -> Dict:
    global users_data
    logger.debug(f"get_user_status({user_id}): {len(users_data)} users in cache")

    if not users_data:
        load_users_data()
        logger.debug(f"Loaded {len(users_data)} users from file")

    if user_id not in users_data:
        logger.info(f"🆕 New user {user_id} registered")
        users_data[user_id] = {
            "completed_quali": None,
            "group": None,
            "notifications": get_default_notification_preferences(),
            "custom_notifications": get_default_custom_notifications(),
            "gpro_lang": DEFAULT_USER_LANG,
            "ui_lang": "gb",  # Default UI language (separate from GPRO links language)
            "timezone": "UTC",  # Default timezone
            "website_mode": "classic",  # Website mode: "classic" or "app"
        }
        save_users_data()
    else:
        # Ensure existing users have required fields (migration)
        # Batch migrations to avoid multiple saves
        needs_save = False
        if "group" not in users_data[user_id]:
            users_data[user_id]["group"] = None
            logger.debug(f"Added 'group' field to user {user_id}")
            needs_save = True
        if "notifications" not in users_data[user_id]:
            users_data[user_id][
                "notifications"
            ] = get_default_notification_preferences()
            logger.debug(f"Added 'notifications' field to user {user_id}")
            needs_save = True
        if "custom_notifications" not in users_data[user_id]:
            users_data[user_id][
                "custom_notifications"
            ] = get_default_custom_notifications()
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
        # Migration: Convert old "en" to "gb" for GPRO consistency
        elif users_data[user_id]["ui_lang"] == "en":
            users_data[user_id]["ui_lang"] = "gb"
            logger.debug(f"Migrated user {user_id} from 'en' to 'gb'")
            needs_save = True
        # Migration: Add 72h notification preference for existing users
        if "72h" not in users_data[user_id]["notifications"]:
            users_data[user_id]["notifications"]["72h"] = True
            logger.debug(f"Added '72h' notification to user {user_id}")
            needs_save = True
        # Migration: Add timezone field for existing users
        if "timezone" not in users_data[user_id]:
            users_data[user_id]["timezone"] = "UTC"
            logger.debug(f"Added 'timezone' field to user {user_id}")
            needs_save = True
        # Migration: Add website_mode field for existing users
        if "website_mode" not in users_data[user_id]:
            users_data[user_id]["website_mode"] = "classic"
            logger.debug(f"Added 'website_mode' field to user {user_id}")
            needs_save = True

        # Save only once if any migrations were applied
        if needs_save:
            save_users_data()

    return users_data[user_id]


def set_user_group(user_id: int, group: str):
    """Set user's GPRO group for race links"""
    get_user_status(user_id)
    users_data[user_id]["group"] = group
    save_users_data()
    logger.info(f"User {user_id} set group to: {group}")


def toggle_notification(user_id: int, notification_type: str):
    """Toggle a specific notification type for a user"""
    user_status = get_user_status(user_id)
    current_state = user_status["notifications"].get(notification_type, True)
    user_status["notifications"][notification_type] = not current_state
    save_users_data()
    new_state = "enabled" if not current_state else "disabled"
    logger.info(f"User {user_id} {new_state} '{notification_type}' notifications")
    return not current_state


def is_notification_enabled(user_id: int, notification_type: str) -> bool:
    """Check if a notification type is enabled for a user"""
    user_status = get_user_status(user_id)
    return user_status["notifications"].get(notification_type, True)


def is_valid_language(lang_code: str) -> bool:
    """Validate language code against supported languages"""
    return lang_code in LANGUAGE_OPTIONS


def set_user_language(user_id: int, lang: str) -> bool:
    """Set user's preferred language for GPRO URLs

    Args:
        user_id: Telegram user ID
        lang: Language code (e.g., 'gb', 'de', 'fr')

    Returns:
        bool: True if language was set successfully, False if invalid
    """
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
    """Get user's preferred language for GPRO URLs

    Args:
        user_id: Telegram user ID

    Returns:
        str: Language code (defaults to 'gb' if not set)
    """
    user_status = get_user_status(user_id)
    return user_status.get("gpro_lang", DEFAULT_USER_LANG)


def set_user_ui_language(user_id: int, lang: str) -> bool:
    """Set user's preferred UI language for bot interface

    Args:
        user_id: Telegram user ID
        lang: Language code (e.g., 'en', 'ru')

    Returns:
        bool: True if language was set successfully, False if invalid
    """
    lang = lang.strip().lower()

    # Validate against available UI languages (dynamically from UI_LANGUAGE_DISPLAY)
    if lang not in UI_LANGUAGE_DISPLAY:
        logger.warning(f"Invalid UI language code: {lang}")
        return False

    get_user_status(user_id)
    users_data[user_id]["ui_lang"] = lang
    save_users_data()
    logger.info(f"User {user_id} set UI language to: {lang}")
    return True


def get_user_ui_language(user_id: int) -> str:
    """Get user's preferred UI language for bot interface

    Args:
        user_id: Telegram user ID

    Returns:
        str: Language code (defaults to 'gb' if not set)
    """
    user_status = get_user_status(user_id)
    return user_status.get("ui_lang", "gb")


def get_user_timezone(user_id: int) -> str:
    """Get user's timezone IANA name

    Args:
        user_id: Telegram user ID

    Returns:
        str: IANA timezone name (e.g., 'America/New_York', defaults to 'UTC')
    """
    user_status = get_user_status(user_id)
    return user_status.get("timezone", "UTC")


def set_user_timezone(user_id: int, timezone: str) -> bool:
    """Set user's timezone

    Args:
        user_id: Telegram user ID
        timezone: IANA timezone name (e.g., 'America/New_York')

    Returns:
        bool: True if timezone was set successfully, False if invalid
    """
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
    get_user_status(user_id)
    users_data[user_id]["completed_quali"] = race_id
    save_users_data()
    logger.info(f"User {user_id} marked race {race_id} done")


def reset_user_status(user_id: int):
    if user_id in users_data:
        users_data[user_id]["completed_quali"] = None
        save_users_data()
        logger.info(f"User {user_id} reset")


def set_user_website_mode(user_id: int, mode: str) -> bool:
    """Set user's website mode (classic or app)

    Args:
        user_id: Telegram user ID
        mode: "classic" or "app"

    Returns:
        bool: True if successful, False otherwise
    """
    if mode not in ["classic", "app"]:
        logger.warning(f"Invalid website mode: {mode}")
        return False

    get_user_status(user_id)
    users_data[user_id]["website_mode"] = mode
    save_users_data()
    logger.info(f"User {user_id} switched to {mode} mode")
    return True


def get_user_website_mode(user_id: int) -> str:
    """Get user's website mode

    Args:
        user_id: Telegram user ID

    Returns:
        str: "classic" or "app" (defaults to "classic")
    """
    user_status = get_user_status(user_id)
    return user_status.get("website_mode", "classic")


load_users_data()

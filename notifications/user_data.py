"""User data persistence and management"""

import logging
import json
import os
from datetime import datetime, UTC
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
        "new_season_reminder": True,
    }


def get_default_custom_notifications():
    """Default custom notification settings - empty slots"""
    return [
        {"enabled": False, "hours_before": None},
        {"enabled": False, "hours_before": None},
    ]


def get_default_snooze_tracking():
    """Default snooze tracking - 0 snoozes per notification type"""
    return {
        "72h": 0,
        "48h": 0,
        "24h": 0,
        "2h": 0,
        "10min": 0,
    }


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
    temp_file = USERS_FILE + ".tmp"
    try:
        with open(temp_file, "w") as f:
            save_data = {str(k): v for k, v in users_data.items()}
            json.dump(save_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_file, USERS_FILE)
        logger.debug(f"Saved {len(users_data)} users")
    except Exception as e:
        logger.error(f"Save failed: {e}")
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


def get_user_status(user_id: int):
    global users_data
    logger.debug(f"get_user_status({user_id}): {len(users_data)} users in cache")

    if not users_data:
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
    user_status = get_user_status(user_id)[0]
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
    user_status = get_user_status(user_id)[0]
    return user_status.get("ui_lang", "gb")


def get_user_timezone(user_id: int) -> str:
    """Get user's timezone IANA name

    Args:
        user_id: Telegram user ID

    Returns:
        str: IANA timezone name (e.g., 'America/New_York', defaults to 'UTC')
    """
    user_status = get_user_status(user_id)[0]
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
    user_status = get_user_status(user_id)[0]
    return user_status.get("website_mode", "classic")


def update_user_profile(
    user_id: int,
    tg_language_code: str = None,
    username: str = None,
    first_name: str = None,
) -> bool:
    """Update user's profile data from Telegram message

    Args:
        user_id: Telegram user ID
        tg_language_code: Telegram's language_code from message.from_user (e.g., 'en', 'ru')
        username: Telegram username from message.from_user (can be None)
        first_name: Display name from message.from_user

    Returns:
        bool: True if any data was updated and saved
    """
    if user_id not in users_data:
        return False

    needs_save = False

    if tg_language_code is not None:
        current_lang = users_data[user_id].get("tg_language_code")
        if current_lang != tg_language_code:
            users_data[user_id]["tg_language_code"] = tg_language_code
            needs_save = True
            logger.debug(
                f"Updated tg_language_code for user {user_id}: {tg_language_code}"
            )

    if username is not None:
        current_user = users_data[user_id].get("username")
        if current_user != username:
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
    """Get user's profile data

    Args:
        user_id: Telegram user ID

    Returns:
        Dict with tg_language_code, username, and first_name fields
    """
    user_status = get_user_status(user_id)[0]
    return {
        "tg_language_code": user_status.get("tg_language_code"),
        "username": user_status.get("username"),
        "first_name": user_status.get("first_name"),
    }


def add_snooze_reminder(
    user_id: int, race_id: int, until: datetime, notification_type: str
) -> None:
    """Add an active snooze reminder to user data

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        until: Datetime when snooze should fire
        notification_type: Original notification type (e.g., "2h")
    """
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        user_status["active_snoozes"] = {}

    # Use unique key based on race, type, and until time to allow multiple snoozes
    key = f"{race_id}_{notification_type}_{until.strftime('%Y%m%d%H%M%S')}"
    user_status["active_snoozes"][key] = {
        "until": until.isoformat(),
        "notification_type": notification_type,
        "race_id": race_id,
    }
    save_users_data()
    logger.debug(
        f"Added snooze reminder for user {user_id}, race {race_id}, type {notification_type}, key={key}"
    )


def remove_snooze_reminder(user_id: int, race_id: int, notification_type: str) -> None:
    """Remove a snooze reminder from user data

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        notification_type: Notification type
    """
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        return

    # Find and remove snooze by race_id and notification_type (removes ALL matching)
    keys_to_remove = []
    for key, data in user_status["active_snoozes"].items():
        if (
            data.get("race_id") == race_id
            and data.get("notification_type") == notification_type
        ):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del user_status["active_snoozes"][key]
        logger.debug(
            f"Removed snooze reminder for user {user_id}, race {race_id}, type {notification_type}, key={key}"
        )

    if keys_to_remove:
        save_users_data()


def remove_snooze_reminder_by_time(
    user_id: int, race_id: int, notification_type: str, until: datetime
) -> None:
    """Remove a specific snooze reminder by its exact until time

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        notification_type: Notification type
        until: Exact datetime of the snooze to remove
    """
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        return

    until_str = until.isoformat()
    keys_to_remove = []
    for key, data in user_status["active_snoozes"].items():
        if (
            data.get("race_id") == race_id
            and data.get("notification_type") == notification_type
            and data.get("until") == until_str
        ):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del user_status["active_snoozes"][key]
        logger.debug(
            f"Removed snooze by time for user {user_id}, race {race_id}, type {notification_type}, until={until_str}"
        )

    if keys_to_remove:
        save_users_data()


def get_all_snooze_reminders() -> list:
    """Get all active snooze reminders from all users

    Returns:
        list: [(user_id, race_id, until, notification_type), ...]
    """
    reminders = []

    for user_id, user_status in users_data.items():
        active_snoozes = user_status.get("active_snoozes", {})

        for key, data in active_snoozes.items():
            try:
                # Get data from dict (new format stores race_id and notification_type)
                race_id = data.get("race_id")
                notification_type = data.get("notification_type")
                until = datetime.fromisoformat(data["until"]).replace(tzinfo=UTC)

                if race_id is None or notification_type is None:
                    continue

                # Return ALL snoozes (past and future) - checker will handle timing
                reminders.append((user_id, race_id, until, notification_type))
            except (ValueError, IndexError, TypeError):
                continue

    return reminders


def get_snooze_count(user_id: int, notification_label: str) -> int:
    """Get snooze count for a notification type

    Args:
        user_id: Telegram user ID
        notification_label: Notification label (e.g., "48h", "2h", "10min")

    Returns:
        int: Number of times user has snoozed this notification type
    """
    user_status = get_user_status(user_id)[0]
    tracking = user_status.get("snooze_tracking", get_default_snooze_tracking())
    return tracking.get(notification_label, 0)


def increment_snooze_count(user_id: int, notification_label: str) -> None:
    """Increment snooze count for a notification type

    Args:
        user_id: Telegram user ID
        notification_label: Notification label (e.g., "48h", "2h", "10min")
    """
    user_status = get_user_status(user_id)[0]
    if "snooze_tracking" not in user_status:
        user_status["snooze_tracking"] = get_default_snooze_tracking()
    user_status["snooze_tracking"][notification_label] = (
        user_status["snooze_tracking"].get(notification_label, 0) + 1
    )
    save_users_data()
    logger.debug(f"User {user_id} snooze count for '{notification_label}' incremented")


def reset_snooze_counts_for_deadline_passed(race_id: int, quali_close) -> None:
    """Reset snooze counts for notification types where deadline has passed

    Called after quali_close to reset counts for that race's notifications

    Args:
        race_id: Race ID
        quali_close: Datetime when qualifying closes
    """
    now = datetime.now(UTC)
    if now < quali_close:
        return

    for user_id in users_data:
        if "snooze_tracking" not in users_data[user_id]:
            continue
        users_data[user_id]["snooze_tracking"] = get_default_snooze_tracking()

    save_users_data()
    logger.info(f"🔄 Reset snooze counts for all users after race {race_id} deadline")


def mark_user_blocked(user_id: int) -> bool:
    """Mark user as blocked by the bot

    Called when TelegramForbiddenError is raised when sending a message.
    Once blocked, user won't receive notifications until they unblock and
    send /start again.

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if user was marked as blocked, False if already blocked or user not found
    """
    if user_id not in users_data:
        return False

    # Check if already blocked
    if users_data[user_id].get("blocked_at") is not None:
        return False

    users_data[user_id]["blocked_at"] = datetime.now(UTC).isoformat()
    save_users_data()
    logger.info(f"🚫 User {user_id} marked as blocked (bot was blocked by user)")
    return True


def is_user_blocked(user_id: int) -> bool:
    """Check if user has blocked the bot

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if user has blocked the bot, False otherwise
    """
    if user_id not in users_data:
        return False

    return users_data[user_id].get("blocked_at") is not None


def unblock_user(user_id: int) -> bool:
    """Unblock a user when they interact with the bot again

    Called when user sends /start or any command after unblocking the bot.

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if user was unblocked, False if not blocked or user not found
    """
    if user_id not in users_data:
        return False

    # Check if actually blocked
    if users_data[user_id].get("blocked_at") is None:
        return False

    users_data[user_id]["blocked_at"] = None
    save_users_data()
    logger.info(f"✅ User {user_id} unblocked (user interacted with bot again)")
    return True

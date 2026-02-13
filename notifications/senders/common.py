"""Common utilities for notification senders"""

import logging
from typing import Callable

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from notifications.users import (
    get_user_status,
    mark_user_blocked,
    DEFAULT_USER_LANG,
)

logger = logging.getLogger(__name__)


def get_user_info(user_id: int) -> dict:
    """Get user status and extract commonly used fields

    Returns:
        dict with user info including group, gpro_lang, ui_lang, website_mode
    """
    user_status, _ = get_user_status(user_id)
    return {
        "status": user_status,
        "group": user_status.get("group"),
        "gpro_lang": user_status.get("gpro_lang", DEFAULT_USER_LANG),
        "ui_lang": user_status.get("ui_lang", "gb"),
        "website_mode": user_status.get("website_mode", "classic"),
    }


def get_text_getter(i18n=None, ui_lang: str = "gb") -> Callable:
    """Get a text getter function

    Args:
        i18n: Optional i18n context
        ui_lang: UI language code (used if i18n not provided)

    Returns:
        Function that takes key and kwargs and returns translated text
    """
    if i18n is None:
        from i18n_setup import get_translation

        def get_text(key, **kwargs):
            return get_translation(key, locale=ui_lang, **kwargs)

    else:

        def get_text(key, **kwargs):
            return i18n.get(key, **kwargs)

    return get_text


async def send_notification(
    bot: Bot,
    user_id: int,
    message: str,
    notification_type: str,
    race_id: int,
    reply_markup=None,
) -> bool:
    """Send a notification with proper error handling

    Args:
        bot: Aiogram Bot instance
        user_id: Telegram user ID
        message: Message text to send
        notification_type: Type of notification (for logging)
        race_id: Race ID (for logging)
        reply_markup: Optional inline keyboard markup

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        await bot.send_message(
            user_id, message, reply_markup=reply_markup, parse_mode="HTML"
        )
        return True
    except TelegramForbiddenError:
        mark_user_blocked(user_id)
        logger.warning(f"🚫 User {user_id} blocked the bot ({notification_type})")
        return False
    except Exception as e:
        logger.error(f"{notification_type} notify {user_id} failed: {e}")
        return False

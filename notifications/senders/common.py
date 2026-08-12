"""Common utilities for notification senders"""

import logging
from enum import Enum
from typing import Callable

from aiogram import Bot
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramNotFound,
    TelegramRetryAfter,
    TelegramServerError,
)

from notifications.users import (
    get_user_status,
    mark_user_blocked,
    DEFAULT_USER_LANG,
)

logger = logging.getLogger(__name__)


class DeliveryStatus(str, Enum):
    """Outcome of one Telegram delivery attempt."""

    SENT = "sent"
    SKIPPED = "skipped"
    PERMANENT_FAILURE = "permanent_failure"
    RETRYABLE_FAILURE = "retryable_failure"

    @property
    def is_terminal(self) -> bool:
        """Return whether retrying cannot improve this delivery."""
        return self is not DeliveryStatus.RETRYABLE_FAILURE


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
) -> DeliveryStatus:
    """Send a notification with proper error handling

    Args:
        bot: Aiogram Bot instance
        user_id: Telegram user ID
        message: Message text to send
        notification_type: Type of notification (for logging)
        race_id: Race ID (for logging)
        reply_markup: Optional inline keyboard markup

    Returns:
        DeliveryStatus describing whether the attempt is terminal or retryable.
    """
    try:
        await bot.send_message(
            user_id, message, reply_markup=reply_markup, parse_mode="HTML"
        )
        return DeliveryStatus.SENT
    except TelegramForbiddenError:
        mark_user_blocked(user_id)
        logger.warning(f"🚫 User {user_id} blocked the bot ({notification_type})")
        return DeliveryStatus.PERMANENT_FAILURE
    except TelegramNotFound:
        logger.warning(
            f"📍 Chat not found for user {user_id} ({notification_type}) - removing user"
        )
        mark_user_blocked(user_id)
        return DeliveryStatus.PERMANENT_FAILURE
    except TelegramRetryAfter as e:
        logger.warning(
            f"Telegram rate limited {notification_type} for user {user_id}; "
            f"retry after {e.retry_after}s"
        )
        return DeliveryStatus.RETRYABLE_FAILURE
    except (TelegramNetworkError, TelegramServerError) as e:
        logger.warning(f"Temporary {notification_type} failure for {user_id}: {e}")
        return DeliveryStatus.RETRYABLE_FAILURE
    except TelegramBadRequest as e:
        if "chat not found" in str(e.message).lower():
            logger.warning(
                f"📍 Chat not found for user {user_id} ({notification_type}) - removing user"
            )
            mark_user_blocked(user_id)
            return DeliveryStatus.PERMANENT_FAILURE
        logger.error(f"{notification_type} notify {user_id} failed: {e}")
        return DeliveryStatus.PERMANENT_FAILURE
    except Exception as e:
        logger.error(f"{notification_type} notify {user_id} failed: {e}")
        return DeliveryStatus.RETRYABLE_FAILURE

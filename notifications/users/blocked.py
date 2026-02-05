"""Blocked user management"""

import logging
from datetime import datetime, UTC

from notifications.users.storage import users_data, save_users_data

logger = logging.getLogger(__name__)


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

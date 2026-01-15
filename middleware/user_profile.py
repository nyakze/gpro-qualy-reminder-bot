"""Middleware to update user profile data from Telegram on every interaction"""

import logging
from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Update

from notifications import update_user_profile

logger = logging.getLogger(__name__)


class UserProfileMiddleware(BaseMiddleware):
    """Middleware that updates user profile data (username, first_name, tg_language_code)
    on every incoming update.
    """

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user = None

        if event.message and event.message.from_user:
            user = event.message.from_user
        elif event.callback_query and event.callback_query.from_user:
            user = event.callback_query.from_user
        elif event.inline_query and event.inline_query.from_user:
            user = event.inline_query.from_user
        elif event.chosen_inline_result and event.chosen_inline_result.from_user:
            user = event.chosen_inline_result.from_user

        if user:
            update_user_profile(
                user_id=user.id,
                tg_language_code=user.language_code,
                username=user.username,
                first_name=user.first_name,
            )

        return await handler(event, data)

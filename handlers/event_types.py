"""Narrow event types guaranteed by the bot's router filters."""

from aiogram.types import CallbackQuery, Message, User


class AccessibleCallbackQuery(CallbackQuery):
    """Callback query with accessible source message and callback payload."""

    data: str
    message: Message


class UserTextMessage(Message):
    """Private user message containing text."""

    from_user: User
    text: str

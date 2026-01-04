"""i18n setup for GPRO Bot using aiogram-i18n"""
import os
from pathlib import Path
from typing import Any
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore
from aiogram_i18n.managers import BaseManager

# Supported UI languages
SUPPORTED_UI_LANGUAGES = ['en', 'ru', 'br', 'it', 'es', 'fr']
DEFAULT_UI_LANGUAGE = 'en'

# Get absolute path to locales directory
_SCRIPT_DIR = Path(__file__).parent
LOCALES_DIR = _SCRIPT_DIR / 'locales'


class UserLanguageManager(BaseManager):
    """Manager for determining user's UI language"""

    async def get_locale(self, event_from_user: Any = None, data: dict = None) -> str:
        """Get user's UI language preference from user data

        Args:
            event_from_user: Telegram user object from event
            data: Additional event data

        Returns:
            str: Language code ('en' or 'ru')
        """
        # Import here to avoid circular dependency
        from notifications import get_user_status

        if not event_from_user:
            return DEFAULT_UI_LANGUAGE

        user_id = event_from_user.id
        user_status = get_user_status(user_id)

        # Get UI language (separate from GPRO language)
        ui_lang = user_status.get('ui_lang', DEFAULT_UI_LANGUAGE)

        # Validate language
        if ui_lang not in SUPPORTED_UI_LANGUAGES:
            ui_lang = DEFAULT_UI_LANGUAGE

        return ui_lang

    async def set_locale(self, locale: str, event_from_user: Any = None, data: dict = None) -> None:
        """Set user's UI language preference

        Args:
            locale: Language code to set
            event_from_user: Telegram user object from event
            data: Additional event data
        """
        # Import here to avoid circular dependency
        from notifications import set_user_ui_language

        if event_from_user:
            user_id = event_from_user.id
            set_user_ui_language(user_id, locale)


def setup_i18n() -> I18nMiddleware:
    """Setup and configure i18n middleware

    Returns:
        I18nMiddleware: Configured middleware instance
    """
    import logging
    logger = logging.getLogger(__name__)

    # Create i18n middleware with Fluent core
    # Note: path must be a string, not a Path object
    locales_path = str(LOCALES_DIR)
    logger.info(f"Loading i18n from path: {locales_path}")
    logger.info(f"Path exists: {LOCALES_DIR.exists()}")
    logger.info(f"Path contents: {list(LOCALES_DIR.glob('*.ftl'))}")

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path=locales_path,
            raise_key_error=False  # Gracefully handle missing keys, fall back to default locale
        ),
        manager=UserLanguageManager(),
        default_locale=DEFAULT_UI_LANGUAGE
    )

    return i18n_middleware

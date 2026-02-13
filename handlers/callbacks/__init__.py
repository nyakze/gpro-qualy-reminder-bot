"""Callback handlers package

Contains:
- main_menu: Main menu navigation callbacks
- settings: Language, UI language, group, timezone settings
- notifications: Notification toggles and custom notifications
- race_status: Race done/reset/weather callbacks
"""

from aiogram import Router

__all__ = [
    "router",
    "main_menu",
    "settings",
    "notifications",
    "race_status",
    "build_ui_language_keyboard",
    "build_settings_keyboard",
]

router: Router = Router()

from . import main_menu  # noqa: F401, E402
from . import settings  # noqa: F401, E402
from . import notifications  # noqa: F401, E402
from . import race_status  # noqa: F401, E402

from .settings import build_ui_language_keyboard  # noqa: F401, E402
from .settings import build_settings_keyboard  # noqa: F401, E402

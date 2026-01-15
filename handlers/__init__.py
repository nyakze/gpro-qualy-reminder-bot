"""Handlers module - combines all command, callback, and state handlers"""

import logging
from aiogram import Router

__all__ = ["router", "commands", "callbacks", "states", "onboarding", "admin_commands"]

router = Router()

from . import commands
from . import callbacks
from . import states
from . import onboarding
from . import admin_commands

router.include_router(callbacks.router)

logger = logging.getLogger(__name__)

logger.debug("✅ handlers module loaded - Aiogram 3.x Router ready")

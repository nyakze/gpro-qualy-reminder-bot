"""Handlers module - combines all command, callback, and state handlers"""

import logging
from aiogram import Router

__all__ = ["router", "commands", "callbacks", "states", "onboarding", "admin_commands"]

router = Router()

# Import all handler modules to register them with the router
# ruff: noqa: E402
from . import commands
from . import callbacks
from . import states
from . import onboarding
from . import admin_commands

logger = logging.getLogger(__name__)

logger.debug("✅ handlers module loaded - Aiogram 3.x Router ready")

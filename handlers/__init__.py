"""Handlers module - combines all command, callback, and state handlers"""

import logging
from aiogram import Router

logger = logging.getLogger(__name__)

# Create main router
router = Router()

# Import all handler modules to register them with the router
from . import commands
from . import callbacks
from . import states
from . import onboarding

logger.debug("✅ handlers module loaded - Aiogram 3.x Router ready")

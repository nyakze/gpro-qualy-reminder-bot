import asyncio
import logging
import sys
import os
from logging.handlers import RotatingFileHandler

sys.path.insert(0, ".")

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from gpro_calendar import load_calendar_silent
from notifications import check_notifications, load_users_data  # ADD load_users_data
from i18n_setup import setup_i18n

# Configure production-ready logging
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_FILE = os.path.join(_SCRIPT_DIR, "gpro_bot.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # Console handler
        logging.StreamHandler(),
        # File handler with rotation (10MB max, keep 5 backups)
        RotatingFileHandler(_LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5),
    ],
)

# Reduce verbosity for aiogram event logs (they spam on every interaction)
logging.getLogger("aiogram.event").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN not found!")
        return

    # CRITICAL: Load users BEFORE anything
    load_users_data()
    logger.debug("✅ users_data loaded at startup")

    # Load timezone search index (if available)
    from timezone_utils import load_timezone_search_index

    if load_timezone_search_index():
        logger.debug("✅ Timezone search index loaded")
    else:
        logger.warning(
            "⚠️ Timezone search index not available, using fallback. Run /updatetz to download."
        )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Setup i18n middleware
    i18n = setup_i18n()
    await i18n.core.startup()  # Manually start the i18n core to load translations
    dp.update.middleware(i18n)
    logger.debug("✅ i18n middleware loaded")

    from handlers import router

    dp.include_router(router)
    logger.debug("✅ Handlers router loaded")

    await load_calendar_silent()
    asyncio.create_task(check_notifications(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

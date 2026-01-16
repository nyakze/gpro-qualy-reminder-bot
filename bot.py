import asyncio
import logging
import os
import sys
import time

sys.path.insert(0, ".")

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from gpro_calendar import load_calendar_silent, race_calendar
from notifications import load_users_data
from notifications.checker import load_notify_history, notify_history
from i18n_setup import setup_i18n
from middleware.user_profile import UserProfileMiddleware
from infra.logging import init_logging_paths, setup_logging, log_structured
from infra.signals import setup_signal_handlers
from infra.runner import run_with_recovery

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_STARTUP_TIME = time.time()

init_logging_paths(_SCRIPT_DIR)
logger = setup_logging()


async def main():
    log_structured(logging.INFO, "Starting GPRO Bot", version="3.0")

    if not BOT_TOKEN:
        log_structured(logging.ERROR, "BOT_TOKEN not found")
        return

    load_users_data()
    log_structured(logging.INFO, "Users data loaded", count=len({}))

    from timezone_utils import load_timezone_search_index

    if load_timezone_search_index():
        log_structured(logging.INFO, "Timezone search index loaded")
    else:
        log_structured(logging.WARNING, "Timezone search index not available")

    try:
        loaded_history = load_notify_history()
        notify_history.update(loaded_history)
        log_structured(
            logging.INFO, "Notification history loaded", count=len(notify_history)
        )
    except Exception as e:
        log_structured(
            logging.WARNING, "Failed to load notification history", error=str(e)
        )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    await load_calendar_silent()

    if not race_calendar:
        log_structured(logging.WARNING, "No calendar loaded, alerting admins")
        from infra.signals import alert_admin

        await alert_admin(
            bot, "⚠️ Calendar failed to load! Bot is running but has no race data."
        )
    else:
        log_structured(logging.INFO, "Calendar loaded", races=len(race_calendar))

    dp.update.middleware(UserProfileMiddleware())
    log_structured(logging.INFO, "UserProfileMiddleware loaded")

    i18n = setup_i18n()
    await i18n.core.startup()
    dp.update.middleware(i18n)
    log_structured(logging.INFO, "i18n middleware loaded")

    from handlers import router

    dp.include_router(router)
    log_structured(logging.INFO, "Handlers router loaded")

    setup_signal_handlers(bot)

    uptime_seconds = time.time() - _STARTUP_TIME
    log_structured(
        logging.INFO, "Bot startup complete", uptime_seconds=round(uptime_seconds, 2)
    )

    asyncio.create_task(run_with_recovery(bot))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

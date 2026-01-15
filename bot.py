import asyncio
import logging
import sys
import os
import signal
import json
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any, Dict

sys.path.insert(0, ".")

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN, ADMIN_USER_IDS
from gpro_calendar import load_calendar_silent, race_calendar
from notifications import check_notifications, load_users_data, save_users_data
from notifications.checker import load_notify_history, save_notify_history, notify_history
from i18n_setup import setup_i18n
from middleware.user_profile import UserProfileMiddleware

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_LOG_FILE = os.path.join(_SCRIPT_DIR, "gpro_bot.log")

# Track startup time for uptime calculation
_STARTUP_TIME = time.time()


class StructuredLogFormatter(logging.Formatter):
    """Log formatter that outputs structured JSON format"""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra") and record.extra:
            for key, value in record.extra.items():
                if not key.startswith("_"):
                    try:
                        log_data[key] = json.dumps(value)
                    except (TypeError, ValueError):
                        log_data[key] = str(value)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    """Configure structured JSON logging"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    logger.handlers.clear()

    # JSON formatter for both handlers
    json_formatter = StructuredLogFormatter()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # File handler with rotation (10MB max, keep 5 backups)
    file_handler = RotatingFileHandler(
        _LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    # Reduce aiogram verbosity
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

    return logger


logger = setup_logging()


def log_structured(level: int, message: str, **extra) -> None:
    """Log with structured extra data"""
    logger.log(level, message, extra=extra)


async def alert_admin(bot: Bot, message: str) -> None:
    """Send alert message to all admins"""
    for admin_id in ADMIN_USER_IDS:
        try:
            await bot.send_message(admin_id, f"⚠️ {message}")
            logger.info(f"Alert sent to admin {admin_id}", extra={"admin_id": admin_id})
        except Exception as e:
            logger.error(f"Failed to alert admin {admin_id}", extra={"error": str(e)})


async def shutdown(bot: Bot, reason: str) -> None:
    """Graceful shutdown - save state and close connections"""
    log_structured(logging.INFO, "Shutting down", reason=reason)

    # Save state
    try:
        save_notify_history(notify_history)
        save_users_data()
        log_structured(logging.INFO, "State saved successfully")
    except Exception as e:
        log_structured(logging.ERROR, "Failed to save state", error=str(e))

    # Close bot session
    try:
        await bot.session.close()
    except Exception as e:
        log_structured(logging.ERROR, "Failed to close bot session", error=str(e))

    log_structured(logging.INFO, "Shutdown complete")
    sys.exit(0)


def setup_signal_handlers(bot: Bot) -> None:
    """Setup graceful shutdown on SIGTERM/SIGINT"""

    def signal_handler(sig):
        sig_name = signal.Signals(sig).name
        log_structured(logging.INFO, "Received shutdown signal", signal=sig_name)
        asyncio.create_task(shutdown(bot, f"Signal {sig_name}"))

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


async def run_with_recovery(bot: Bot) -> None:
    """Run notification checker with error recovery"""
    while True:
        try:
            log_structured(logging.INFO, "Starting notification checker")
            await check_notifications(bot)
        except asyncio.CancelledError:
            log_structured(logging.INFO, "Notification checker cancelled")
            raise
        except Exception as e:
            log_structured(logging.ERROR, "Notification checker crashed, restarting in 10s", error=str(e))
            await asyncio.sleep(10)


async def main():
    log_structured(logging.INFO, "Starting GPRO Bot", version="3.0")

    if not BOT_TOKEN:
        log_structured(logging.ERROR, "BOT_TOKEN not found")
        return

    # Load users data
    load_users_data()
    log_structured(logging.INFO, "Users data loaded", count=len({}))

    # Load timezone search index
    from timezone_utils import load_timezone_search_index

    if load_timezone_search_index():
        log_structured(logging.INFO, "Timezone search index loaded")
    else:
        log_structured(logging.WARNING, "Timezone search index not available")

    # Load notification history
    try:
        loaded_history = load_notify_history()
        notify_history.update(loaded_history)
        log_structured(logging.INFO, "Notification history loaded", count=len(notify_history))
    except Exception as e:
        log_structured(logging.WARNING, "Failed to load notification history", error=str(e))

    # Setup bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Load calendar and validate
    await load_calendar_silent()

    if not race_calendar:
        log_structured(logging.WARNING, "No calendar loaded, alerting admins")
        await alert_admin(bot, "⚠️ Calendar failed to load! Bot is running but has no race data.")
    else:
        log_structured(logging.INFO, "Calendar loaded", races=len(race_calendar))

    # Setup middleware
    dp.update.middleware(UserProfileMiddleware())
    log_structured(logging.INFO, "UserProfileMiddleware loaded")

    i18n = setup_i18n()
    await i18n.core.startup()
    dp.update.middleware(i18n)
    log_structured(logging.INFO, "i18n middleware loaded")

    # Setup handlers
    from handlers import router

    dp.include_router(router)
    log_structured(logging.INFO, "Handlers router loaded")

    # Setup graceful shutdown
    setup_signal_handlers(bot)

    # Calculate uptime
    uptime_seconds = time.time() - _STARTUP_TIME
    log_structured(logging.INFO, "Bot startup complete", uptime_seconds=round(uptime_seconds, 2))

    # Start notification checker with error recovery
    asyncio.create_task(run_with_recovery(bot))

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

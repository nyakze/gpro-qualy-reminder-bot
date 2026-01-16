import asyncio
import logging
import signal
import sys
from types import FrameType

from config import ADMIN_USER_IDS
from notifications.checker import save_notify_history, notify_history
from notifications import save_users_data

from .logging import log_structured


async def alert_admin(bot, message: str) -> None:
    """Send alert message to all admins"""
    for admin_id in ADMIN_USER_IDS:
        try:
            await bot.send_message(admin_id, f"⚠️ {message}")
            log_structured(
                logging.INFO, f"Alert sent to admin {admin_id}", admin_id=admin_id
            )
        except Exception as e:
            log_structured(
                logging.ERROR, f"Failed to alert admin {admin_id}", error=str(e)
            )


async def shutdown(bot, reason: str) -> None:
    """Graceful shutdown - save state and close connections"""
    log_structured(logging.INFO, "Shutting down", reason=reason)

    try:
        save_notify_history(notify_history)
        save_users_data()
        log_structured(logging.INFO, "State saved successfully")
    except Exception as e:
        log_structured(logging.ERROR, "Failed to save state", error=str(e))

    try:
        await bot.session.close()
    except Exception as e:
        log_structured(logging.ERROR, "Failed to close bot session", error=str(e))

    log_structured(logging.INFO, "Shutdown complete")
    sys.exit(0)


def setup_signal_handlers(bot) -> None:
    """Setup graceful shutdown on SIGTERM/SIGINT"""

    def signal_handler(sig: int, frame: FrameType | None) -> None:
        sig_name = signal.Signals(sig).name
        log_structured(logging.INFO, "Received shutdown signal", signal=sig_name)
        asyncio.create_task(shutdown(bot, f"Signal {sig_name}"))

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

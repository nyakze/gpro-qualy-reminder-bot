import asyncio
import logging

from notifications import check_notifications

from .logging import log_structured


async def run_with_recovery(bot) -> None:
    """Run notification checker with error recovery"""
    while True:
        try:
            log_structured(logging.INFO, "Starting notification checker")
            await check_notifications(bot)
        except asyncio.CancelledError:
            log_structured(logging.INFO, "Notification checker cancelled")
            raise
        except Exception as e:
            log_structured(
                logging.ERROR,
                "Notification checker crashed, restarting in 10s",
                error=str(e),
            )
            await asyncio.sleep(10)

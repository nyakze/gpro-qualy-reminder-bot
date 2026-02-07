"""Simple backup system: Telegram + Classic file backup

Telegram Backup (Sunday 2AM UTC):
- Sends users_data.json file directly to admin Telegram IDs who enabled it
- Each admin can enable/disable independently (default: OFF)
- Triggered weekly + on-demand via /backup menu

Classic Backup (Thursday 2AM UTC):
- Copies only users_data.json to backup/ folder with timestamp
- Always enabled, runs regardless of Telegram settings
- Keeps last 4 backups

Both backups only handle users_data.json (other files can be restored from API)
"""

import asyncio
import logging
import os
import shutil
from datetime import datetime, UTC, timedelta
from typing import Optional

from aiogram import Bot
from aiogram.types import FSInputFile

from config import ADMIN_USER_IDS, CLASSIC_BACKUP_ENABLED
from notifications.users.storage import USERS_FILE

logger = logging.getLogger(__name__)

_SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(_SCRIPT_DIR, "backup")

# Backup configuration
CLASSIC_BACKUP_RETENTION_COUNT = 4
CLASSIC_BACKUP_DAY = 3  # Thursday (0=Monday, 3=Thursday)
TELEGRAM_BACKUP_DAY = 6  # Sunday (0=Monday, 6=Sunday)
BACKUP_HOUR = 2  # 2:00 AM UTC

# Per-admin Telegram backup settings (default: OFF for each admin)
_telegram_backup_enabled: dict[int, bool] = {}
_backup_scheduler_task: Optional[asyncio.Task] = None


def _ensure_backup_dir():
    """Ensure classic backup directory exists"""
    os.makedirs(BACKUP_DIR, exist_ok=True)


def _get_timestamp() -> str:
    """Generate timestamp string for backup filenames"""
    return datetime.now(UTC).strftime("%Y%m%d_%H%M%S")


def _cleanup_old_classic_backups():
    """Remove old classic backups, keeping only the most recent N"""
    _ensure_backup_dir()

    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("users_data_") and filename.endswith(".json"):
            filepath = os.path.join(BACKUP_DIR, filename)
            try:
                stat = os.stat(filepath)
                backups.append((filepath, stat.st_mtime))
            except OSError:
                continue

    # Sort by modification time (newest first)
    backups.sort(key=lambda x: x[1], reverse=True)

    # Remove old backups beyond retention count
    for filepath, _ in backups[CLASSIC_BACKUP_RETENTION_COUNT:]:
        try:
            os.remove(filepath)
            logger.info(f"Removed old classic backup: {os.path.basename(filepath)}")
        except OSError as e:
            logger.warning(f"Failed to remove old backup {filepath}: {e}")


def is_classic_backup_enabled() -> bool:
    """Check if classic backups are enabled via config"""
    return CLASSIC_BACKUP_ENABLED


def create_classic_backup() -> Optional[str]:
    """Create a classic file backup of users_data.json

    Returns:
        Path to the created backup file, or None if failed/disabled
    """
    if not CLASSIC_BACKUP_ENABLED:
        logger.debug("Classic backup skipped (disabled in config)")
        return None

    try:
        _ensure_backup_dir()

        if not os.path.exists(USERS_FILE):
            logger.error(f"Cannot create backup: {USERS_FILE} not found")
            return None

        timestamp = _get_timestamp()
        backup_filename = f"users_data_{timestamp}.json"
        backup_path = os.path.join(BACKUP_DIR, backup_filename)

        shutil.copy2(USERS_FILE, backup_path)
        # Update mtime to now so new backup is always considered "newest"
        # (copy2 preserves source mtime, causing all backups to have same timestamp)
        os.utime(backup_path, None)
        _cleanup_old_classic_backups()

        file_size = os.path.getsize(backup_path)
        logger.info(
            "Classic backup created",
            extra={
                "backup_path": backup_path,
                "file_size_bytes": file_size,
            },
        )

        return backup_path

    except Exception as e:
        logger.error(f"Failed to create classic backup: {e}")
        return None


def is_telegram_backup_enabled(admin_id: int) -> bool:
    """Check if Telegram backup is enabled for specific admin (default: False)"""
    return _telegram_backup_enabled.get(admin_id, False)


def set_telegram_backup_enabled(admin_id: int, enabled: bool):
    """Enable or disable Telegram backup for specific admin"""
    _telegram_backup_enabled[admin_id] = enabled
    logger.info(
        f"Telegram backup {'enabled' if enabled else 'disabled'} for admin {admin_id}"
    )


def get_enabled_telegram_admins() -> set[int]:
    """Get set of admin IDs who have Telegram backup enabled"""
    return {
        admin_id
        for admin_id in ADMIN_USER_IDS
        if _telegram_backup_enabled.get(admin_id, False)
    }


async def send_telegram_backup_to_admin(bot: Bot, admin_id: int) -> bool:
    """Send users_data.json to a specific admin

    Args:
        bot: Aiogram Bot instance
        admin_id: Telegram user ID of admin

    Returns:
        True if backup was sent successfully, False otherwise
    """
    if not os.path.exists(USERS_FILE):
        logger.error(f"Cannot send backup: {USERS_FILE} not found")
        return False

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    caption = f"📦 <b>Users Data Backup</b>\n🕐 {timestamp}"

    try:
        input_file = FSInputFile(USERS_FILE, filename="users_data.json")

        await bot.send_document(
            chat_id=admin_id,
            document=input_file,
            caption=caption,
            parse_mode="HTML",
        )
        logger.info(f"Backup sent to admin {admin_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send backup to admin {admin_id}: {e}")
        return False


async def send_telegram_backup(bot: Bot | None) -> bool:
    """Send users_data.json to all admins who have it enabled

    Args:
        bot: Aiogram Bot instance

    Returns:
        True if backup was sent to at least one admin, False otherwise
    """
    if bot is None:
        logger.error("Cannot send Telegram backup: Bot instance is None")
        return False

    enabled_admins = get_enabled_telegram_admins()

    if not enabled_admins:
        logger.info("No admins have Telegram backup enabled, skipping")
        return True  # Not a failure, just nobody wants it

    success_count = 0
    failed_admins = []

    for admin_id in enabled_admins:
        if await send_telegram_backup_to_admin(bot, admin_id):
            success_count += 1
        else:
            failed_admins.append(admin_id)

    if success_count > 0:
        logger.info(
            "Telegram backup completed",
            extra={
                "success_count": success_count,
                "failed_count": len(failed_admins),
                "enabled_count": len(enabled_admins),
            },
        )
        return True
    else:
        logger.error("Failed to send backup to any admin")
        return False


def get_classic_backup_info() -> list:
    """Get list of existing classic backups with metadata

    Returns:
        List of dicts with filename, size_bytes, modified
    """
    _ensure_backup_dir()

    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("users_data_") and filename.endswith(".json"):
            filepath = os.path.join(BACKUP_DIR, filename)
            try:
                stat = os.stat(filepath)
                backups.append(
                    {
                        "filename": filename,
                        "size_bytes": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime, UTC),
                    }
                )
            except OSError:
                continue

    backups.sort(key=lambda x: x["modified"], reverse=True)
    return backups


async def run_backup_now(
    bot: Bot | None, admin_id: Optional[int] = None
) -> tuple[bool, str]:
    """Run both backups immediately

    Args:
        bot: Aiogram Bot instance
        admin_id: If provided, send Telegram backup only to this admin (for manual trigger)

    Returns:
        Tuple of (success: bool, message: str)
    """
    results = []

    # Classic backup
    if not CLASSIC_BACKUP_ENABLED:
        results.append("⚪️ Classic: Disabled in config")
        classic_success = True  # Not a failure, just disabled
    else:
        classic_path = create_classic_backup()
        if classic_path:
            filename = os.path.basename(classic_path)
            size_kb = os.path.getsize(classic_path) / 1024
            results.append(f"✅ Classic: {filename} ({size_kb:.1f} KB)")
            classic_success = True
        else:
            results.append("❌ Classic backup failed")
            classic_success = False

    # Telegram backup
    if bot is None:
        results.append("❌ Telegram backup: Bot not initialized")
        telegram_success = False
    elif admin_id is not None:
        # Manual trigger - send only to the requesting admin
        if await send_telegram_backup_to_admin(bot, admin_id):
            results.append("✅ Telegram: Sent to you")
            telegram_success = True
        else:
            results.append("❌ Telegram backup failed")
            telegram_success = False
    else:
        # Scheduled trigger - send to all enabled admins
        telegram_success = await send_telegram_backup(bot)
        if telegram_success:
            enabled_count = len(get_enabled_telegram_admins())
            results.append(f"✅ Telegram: Sent to {enabled_count} enabled admin(s)")
        else:
            results.append("❌ Telegram backup failed")

    success = classic_success and telegram_success
    return success, "\n".join(results)


def _seconds_until_next_day(target_day: int | None, target_hour: int) -> float:
    """Calculate seconds until next occurrence of target day/hour (UTC)

    Args:
        target_day: Day of week (0=Monday, 6=Sunday) or None for daily
        target_hour: Hour of day (0-23)

    Returns:
        Seconds until the target time
    """
    now = datetime.now(UTC)

    if target_day is None:
        next_run = now.replace(hour=target_hour, minute=0, second=0, microsecond=0)
        if now.hour >= target_hour:
            next_run += timedelta(days=1)
        return (next_run - now).total_seconds()

    days_ahead = target_day - now.weekday()

    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7

    next_run = now.replace(hour=target_hour, minute=0, second=0, microsecond=0)
    next_run += timedelta(days=days_ahead)

    if days_ahead == 0 and now.hour >= target_hour:
        next_run += timedelta(days=7)

    return (next_run - now).total_seconds()


async def _backup_scheduler_loop(bot: Bot):
    """Main backup scheduler loop using asyncio"""
    logger.info("Backup scheduler started")

    while True:
        now_weekday = datetime.now(UTC).weekday()

        classic_day_is_today = (
            CLASSIC_BACKUP_DAY is None or now_weekday == CLASSIC_BACKUP_DAY
        )
        telegram_day_is_today = (
            TELEGRAM_BACKUP_DAY is None or now_weekday == TELEGRAM_BACKUP_DAY
        )

        if classic_day_is_today and CLASSIC_BACKUP_ENABLED:
            seconds_until = _seconds_until_next_day(CLASSIC_BACKUP_DAY, BACKUP_HOUR)
            backup_type = "classic"
        elif telegram_day_is_today:
            seconds_until = _seconds_until_next_day(TELEGRAM_BACKUP_DAY, BACKUP_HOUR)
            backup_type = "telegram"
        else:
            classic_seconds = (
                _seconds_until_next_day(CLASSIC_BACKUP_DAY, BACKUP_HOUR)
                if CLASSIC_BACKUP_ENABLED
                else float("inf")
            )
            telegram_seconds = _seconds_until_next_day(TELEGRAM_BACKUP_DAY, BACKUP_HOUR)

            if classic_seconds < telegram_seconds:
                seconds_until = classic_seconds
                backup_type = "classic"
            else:
                seconds_until = telegram_seconds
                backup_type = "telegram"

        logger.info(
            f"Next backup scheduled: {backup_type} in {seconds_until/3600:.1f} hours"
        )

        await asyncio.sleep(seconds_until)

        try:
            if backup_type == "classic":
                success = create_classic_backup()
                if success:
                    logger.info("Scheduled classic backup completed")
                else:
                    logger.error("Scheduled classic backup failed")
            else:
                enabled_admins = get_enabled_telegram_admins()
                if enabled_admins:
                    success = await send_telegram_backup(bot)
                    if success:
                        logger.info("Scheduled telegram backup completed")
                    else:
                        logger.error("Scheduled telegram backup failed")
                else:
                    logger.info("Scheduled telegram backup skipped (no admins enabled)")
        except Exception as e:
            logger.error(f"Scheduled backup crashed: {e}")


def start_backup_scheduler(bot: Bot):
    """Start the backup scheduler task

    Args:
        bot: Aiogram Bot instance
    """
    global _backup_scheduler_task

    if _backup_scheduler_task is not None:
        logger.warning("Backup scheduler already running")
        return

    _backup_scheduler_task = asyncio.create_task(_backup_scheduler_loop(bot))
    logger.info("Backup scheduler task created")


def stop_backup_scheduler():
    """Stop the backup scheduler task"""
    global _backup_scheduler_task

    if _backup_scheduler_task is not None:
        _backup_scheduler_task.cancel()
        _backup_scheduler_task = None
        logger.info("Backup scheduler stopped")

"""Notification history management

Handles tracking of sent notifications to prevent duplicates.
"""

import json
import logging
import os
import tempfile
from datetime import datetime, timedelta, UTC
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Constants
NOTIFICATION_HISTORY_RETENTION_HOURS = 24 * 30  # 30 days
MAX_HISTORY_SIZE = 10000  # Maximum entries to prevent unbounded growth

# In-memory cache (lazy loaded)
_notify_history: Dict[Tuple[int, str], datetime] = {}

# Public reference for backwards compatibility
notify_history = _notify_history


def _enforce_history_size_limit(
    history: Dict[Tuple[int, str], datetime],
) -> Dict[Tuple[int, str], datetime]:
    """Enforce size limit on notification history to prevent memory leaks

    If history exceeds MAX_HISTORY_SIZE, remove oldest entries.
    """
    if len(history) <= MAX_HISTORY_SIZE:
        return history

    # Sort by timestamp and keep most recent entries
    sorted_items = sorted(history.items(), key=lambda x: x[1], reverse=True)
    trimmed_history = dict(sorted_items[:MAX_HISTORY_SIZE])

    removed_count = len(history) - len(trimmed_history)
    logger.warning(
        f"Notification history exceeded limit ({len(history)} > {MAX_HISTORY_SIZE}), "
        f"removed {removed_count} oldest entries"
    )

    return trimmed_history


def _get_history_file_path() -> str:
    """Get the path for the notification history file"""
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notification_history.json",
    )


def load_notify_history() -> Dict[Tuple[int, str], datetime]:
    """Load notification history from file"""
    global _notify_history
    history_file = _get_history_file_path()

    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Convert from JSON format: list of [race_id, label, timestamp]
                for item in data:
                    if len(item) == 3:
                        race_id, label, timestamp_str = item
                        try:
                            _notify_history[(int(race_id), label)] = (
                                datetime.fromisoformat(timestamp_str)
                            )
                        except (ValueError, TypeError):
                            continue
            logger.info(
                f"✅ Loaded {len(_notify_history)} notification history entries"
            )
        except (json.JSONDecodeError, IOError, OSError) as e:
            logger.error(f"Failed to load notification history: {e}")

    return _notify_history


def save_notify_history() -> None:
    """Save notification history to file"""
    global _notify_history
    history_file = _get_history_file_path()

    try:
        # Convert to JSON-serializable format: list of [race_id, label, timestamp]
        data = [
            [race_id, label, timestamp.isoformat()]
            for (race_id, label), timestamp in _notify_history.items()
        ]

        # Atomic write
        fd, temp_path = tempfile.mkstemp(
            dir=os.path.dirname(history_file), suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_path, history_file)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise

        logger.debug(f"Saved {len(data)} notification history entries")
    except (IOError, OSError) as e:
        logger.error(f"Failed to save notification history: {e}")


def is_already_notified(race_id: int, label: str) -> bool:
    """Check if a notification was already sent (with history cleanup)"""
    global _notify_history

    history_key = (race_id, label)
    if history_key not in _notify_history:
        return False

    # Check if entry is older than retention period
    cutoff = datetime.now(UTC) - timedelta(hours=NOTIFICATION_HISTORY_RETENTION_HOURS)
    if _notify_history[history_key] < cutoff:
        # Clean up old entry
        del _notify_history[history_key]
        return False

    return True


def mark_notified(race_id: int, label: str) -> None:
    """Mark a notification as sent with current timestamp"""
    global _notify_history
    _notify_history[(race_id, label)] = datetime.now(UTC)

    # Enforce size limit
    _notify_history = _enforce_history_size_limit(_notify_history)


def get_notify_history() -> Dict[Tuple[int, str], datetime]:
    """Get the current notification history"""
    global _notify_history
    return _notify_history


def set_notify_history(history: Dict[Tuple[int, str], datetime]) -> None:
    """Set the notification history (used during initialization)"""
    global _notify_history
    _notify_history = history


def cleanup_old_entries() -> None:
    """Remove old entries from notification history"""
    global _notify_history
    cutoff = datetime.now(UTC) - timedelta(hours=NOTIFICATION_HISTORY_RETENTION_HOURS)
    _notify_history = {k: v for k, v in _notify_history.items() if v > cutoff}
    _notify_history = _enforce_history_size_limit(_notify_history)

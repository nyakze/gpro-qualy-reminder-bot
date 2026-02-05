"""Snooze tracking and management"""

import logging
from datetime import datetime, UTC

from notifications.users.storage import users_data, save_users_data
from notifications.users.core import get_user_status
from notifications.users.constants import get_default_snooze_tracking

logger = logging.getLogger(__name__)


def add_snooze_reminder(
    user_id: int, race_id: int, until: datetime, notification_type: str
) -> None:
    """Add an active snooze reminder to user data

    Args:
        user_id: Telegram user ID
        race_id: Race ID
        until: Datetime when snooze should fire
        notification_type: Original notification type (e.g., "2h")
    """
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        user_status["active_snoozes"] = {}

    # Use unique key based on race, type, and until time to allow multiple snoozes
    key = f"{race_id}_{notification_type}_{until.strftime('%Y%m%d%H%M%S')}"
    user_status["active_snoozes"][key] = {
        "until": until.isoformat(),
        "notification_type": notification_type,
        "race_id": race_id,
    }
    save_users_data()
    logger.debug(
        f"Added snooze reminder for user {user_id}, race {race_id}, type {notification_type}, key={key}"
    )


def remove_snooze_reminder(user_id: int, race_id: int, notification_type: str) -> None:
    """Remove a snooze reminder from user data"""
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        return

    # Find and remove snooze by race_id and notification_type (removes ALL matching)
    keys_to_remove = []
    for key, data in user_status["active_snoozes"].items():
        if (
            data.get("race_id") == race_id
            and data.get("notification_type") == notification_type
        ):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del user_status["active_snoozes"][key]
        logger.debug(
            f"Removed snooze reminder for user {user_id}, race {race_id}, type {notification_type}, key={key}"
        )

    if keys_to_remove:
        save_users_data()


def remove_snooze_reminder_by_time(
    user_id: int, race_id: int, notification_type: str, until: datetime
) -> None:
    """Remove a specific snooze reminder by its exact until time"""
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        return

    until_str = until.isoformat()
    keys_to_remove = []
    for key, data in user_status["active_snoozes"].items():
        if (
            data.get("race_id") == race_id
            and data.get("notification_type") == notification_type
            and data.get("until") == until_str
        ):
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del user_status["active_snoozes"][key]
        logger.debug(
            f"Removed snooze by time for user {user_id}, race {race_id}, type {notification_type}, until={until_str}"
        )

    if keys_to_remove:
        save_users_data()


def get_all_snooze_reminders() -> list:
    """Get all active snooze reminders from all users

    Returns:
        list: [(user_id, race_id, until, notification_type), ...]
    """
    reminders = []

    for user_id, user_status in users_data.items():
        active_snoozes = user_status.get("active_snoozes", {})

        for key, data in active_snoozes.items():
            try:
                # Get data from dict (new format stores race_id and notification_type)
                race_id = data.get("race_id")
                notification_type = data.get("notification_type")
                until = datetime.fromisoformat(data["until"]).replace(tzinfo=UTC)

                if race_id is None or notification_type is None:
                    continue

                # Return ALL snoozes (past and future) - checker will handle timing
                reminders.append((user_id, race_id, until, notification_type))
            except (ValueError, IndexError, TypeError):
                continue

    return reminders


def get_all_active_snoozes() -> list:
    """Get all active snooze reminders as dict objects

    Returns:
        list: [{"id": snooze_id, "user_id": user_id, "race_id": race_id,
                "snooze_time": iso_timestamp, "original_label": label}, ...]
    """
    snoozes = []

    for user_id_str, user_status in users_data.items():
        active_snoozes = user_status.get("active_snoozes", {})

        for key, data in active_snoozes.items():
            try:
                race_id = data.get("race_id")
                notification_type = data.get("notification_type")
                until = data.get("until")

                if race_id is None or notification_type is None or until is None:
                    continue

                snoozes.append(
                    {
                        "id": key,
                        "user_id": int(user_id_str),
                        "race_id": race_id,
                        "snooze_time": until,
                        "original_label": notification_type,
                    }
                )
            except (ValueError, TypeError):
                continue

    return snoozes


def remove_active_snooze(user_id: int, snooze_id: str) -> bool:
    """Remove a specific snooze by its ID

    Args:
        user_id: Telegram user ID
        snooze_id: The unique snooze key/ID

    Returns:
        bool: True if removed, False if not found
    """
    user_status = get_user_status(user_id)[0]

    if "active_snoozes" not in user_status:
        return False

    if snooze_id in user_status["active_snoozes"]:
        del user_status["active_snoozes"][snooze_id]
        save_users_data()
        logger.debug(f"Removed active snooze {snooze_id} for user {user_id}")
        return True

    return False


def get_snooze_count(user_id: int, notification_label: str) -> int:
    """Get snooze count for a notification type"""
    user_status = get_user_status(user_id)[0]
    tracking = user_status.get("snooze_tracking", get_default_snooze_tracking())
    return tracking.get(notification_label, 0)


def increment_snooze_count(user_id: int, notification_label: str) -> None:
    """Increment snooze count for a notification type"""
    user_status = get_user_status(user_id)[0]
    if "snooze_tracking" not in user_status:
        user_status["snooze_tracking"] = get_default_snooze_tracking()
    user_status["snooze_tracking"][notification_label] = (
        user_status["snooze_tracking"].get(notification_label, 0) + 1
    )
    save_users_data()
    logger.debug(f"User {user_id} snooze count for '{notification_label}' incremented")


def reset_snooze_count(user_id: int, race_id: int, notification_label: str) -> None:
    """Reset snooze count for a specific race and notification type"""
    user_status = get_user_status(user_id)[0]

    if "snooze_counts" not in user_status:
        return

    count_key = f"{race_id}_{notification_label}"
    if count_key in user_status["snooze_counts"]:
        user_status["snooze_counts"][count_key] = 0
        save_users_data()
        logger.debug(
            f"Reset snooze count for user {user_id}, race {race_id}, label {notification_label}"
        )


def reset_snooze_counts_for_deadline_passed(race_id: int, quali_close) -> None:
    """Reset snooze counts for notification types where deadline has passed"""
    now = datetime.now(UTC)
    if now < quali_close:
        return

    for user_id in users_data:
        if "snooze_tracking" not in users_data[user_id]:
            continue
        users_data[user_id]["snooze_tracking"] = get_default_snooze_tracking()

    save_users_data()
    logger.info(f"🔄 Reset snooze counts for all users after race {race_id} deadline")

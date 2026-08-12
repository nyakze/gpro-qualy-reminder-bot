"""Notification dispatcher - routes to appropriate sender"""

import logging
from typing import Dict

from aiogram import Bot

from notifications.senders.quali import send_quali_notification
from notifications.senders.common import DeliveryStatus
from notifications.senders.quali_results import send_quali_results_notification
from notifications.senders.race_live import send_race_live_notification
from notifications.senders.race_replay import send_race_replay_notification
from notifications.senders.race_results import send_race_results_notification
from notifications.senders.new_season import send_new_season_reminder_notification

logger = logging.getLogger(__name__)


async def send_notification_to_user(
    bot: Bot,
    user_id: int,
    ntype: str,
    race_id: int,
    race_data: Dict,
    label: str,
) -> DeliveryStatus:
    """Dispatcher function to send the appropriate notification type to a user.

    Args:
        bot: Aiogram Bot instance
        user_id: Telegram user ID
        ntype: Notification type ("closing", "opens", "live", "replay", "results", "snooze", "new_season", "custom")
        race_id: Race ID
        race_data: Race data dictionary
        label: Notification label for mapping to specific types
    """
    if ntype == "closing":
        # Map labels to quali notification types
        quali_type_map = {
            "72h": "72h",
            "48h": "48h",
            "24h": "24h",
            "2h": "2h",
            "10min": "10min",
            "custom_1": "custom_1",
            "custom_2": "custom_2",
        }
        quali_type = quali_type_map.get(label, label)
        return await send_quali_notification(
            bot, user_id, race_id, race_data, quali_type
        )
    elif ntype == "opens":
        return await send_quali_notification(
            bot, user_id, race_id, race_data, "opens_soon"
        )
    elif ntype == "live":
        return await send_race_live_notification(bot, user_id, race_id, race_data)
    elif ntype == "replay":
        return await send_race_replay_notification(bot, user_id, race_id, race_data)
    elif ntype == "results":
        if label == "quali_results":
            return await send_quali_results_notification(
                bot, user_id, race_id, race_data
            )
        else:
            return await send_race_results_notification(
                bot, user_id, race_id, race_data
            )
    elif ntype == "new_season":
        return await send_new_season_reminder_notification(
            bot, user_id, race_id, race_data
        )
    elif ntype == "snooze":
        # Snooze notifications use the snooze_ prefix with original type
        return await send_quali_notification(
            bot, user_id, race_id, race_data, f"snooze_{label}"
        )
    elif ntype == "custom":
        return await send_quali_notification(bot, user_id, race_id, race_data, label)
    else:
        logger.warning(f"Unknown notification type '{ntype}' for user {user_id}")
        return DeliveryStatus.SKIPPED

"""Qualifying results notification sender"""

import logging

from aiogram import Bot

from utils import add_flag_to_track
from timezone_utils import format_datetime_for_user
from notifications.utils.link_generators import (
    generate_starting_grid_link,
    generate_app_starting_grid_link,
)
from notifications.senders.common import (
    DeliveryStatus,
    get_user_info,
    get_text_getter,
    send_notification,
)

logger = logging.getLogger(__name__)


async def send_quali_results_notification(
    bot: Bot, user_id: int, race_id: int, race_data: dict, i18n=None
) -> DeliveryStatus:
    """Send qualifying results notification after quali deadline"""
    user_info = get_user_info(user_id)
    group = user_info["group"]
    gpro_lang = user_info["gpro_lang"]
    ui_lang = user_info["ui_lang"]
    website_mode = user_info["website_mode"]

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    quali_close = race_data["quali_close"]
    quali_close_time = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    if website_mode == "app":
        starting_grid_link = generate_app_starting_grid_link(group)
        logger.debug(
            f"User {user_id} using APP mode - Starting grid: {starting_grid_link}"
        )
    else:
        starting_grid_link = generate_starting_grid_link(group, gpro_lang)
        logger.debug(
            f"User {user_id} using Classic mode - Starting grid: {starting_grid_link}"
        )

    get_text = get_text_getter(i18n, ui_lang)

    if group:
        message = get_text(
            "notif-quali-results",
            raceId=race_id,
            track=track,
            qualiClose=quali_close_time,
            raceTime=race_time,
            gridLink=starting_grid_link,
        )
    else:
        message = get_text(
            "notif-quali-results-no-group",
            raceId=race_id,
            track=track,
            qualiClose=quali_close_time,
            raceTime=race_time,
            gridLink=starting_grid_link,
        )

    success = await send_notification(
        bot, user_id, message, "quali results notification", race_id
    )
    if success is DeliveryStatus.SENT:
        logger.info(
            f"🏁 Sent quali results notification to {user_id} for race {race_id}"
        )
    return success

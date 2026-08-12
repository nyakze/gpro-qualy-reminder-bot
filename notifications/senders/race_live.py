"""Race live notification sender"""

import logging

from aiogram import Bot

from utils import add_flag_to_track
from timezone_utils import format_datetime_for_user
from notifications.utils.link_generators import (
    generate_race_link,
    generate_app_race_live_link,
)
from notifications.senders.common import (
    DeliveryStatus,
    DeliveryOutcome,
    get_user_info,
    get_text_getter,
    send_notification,
)

logger = logging.getLogger(__name__)


async def send_race_live_notification(
    bot: Bot, user_id: int, race_id: int, race_data: dict, i18n=None
) -> DeliveryOutcome:
    """Send notification when race goes live"""
    user_info = get_user_info(user_id)
    group = user_info["group"]
    gpro_lang = user_info["gpro_lang"]
    ui_lang = user_info["ui_lang"]
    website_mode = user_info["website_mode"]

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate race live link based on website mode
    if website_mode == "app":
        race_link = generate_app_race_live_link()
        logger.debug(
            f"User {user_id} using APP mode - Live: {race_link} (no group support)"
        )
    else:
        race_link = generate_race_link(group, gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Live: {race_link}")

    get_text = get_text_getter(i18n, ui_lang)

    # Build message based on website mode and group
    # APP mode: always use simple message (no group warning needed)
    # Classic mode: show warning only if group not set
    if website_mode == "app" or group:
        message = get_text(
            "notif-race-live",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            raceLink=race_link,
        )
    else:
        message = get_text(
            "notif-race-live-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            raceLink=race_link,
        )

    success = await send_notification(
        bot, user_id, message, "race live notification", race_id
    )
    if success is DeliveryStatus.SENT:
        logger.info(f"🏁 Sent race live notification to {user_id} for race {race_id}")
    return success

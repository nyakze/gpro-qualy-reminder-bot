"""New season reminder notification sender"""

import logging

from aiogram import Bot

from utils import add_flag_to_track, format_group_display
from timezone_utils import format_datetime_for_user
from notifications.senders.common import get_user_info, get_text_getter, send_notification

logger = logging.getLogger(__name__)


async def send_new_season_reminder_notification(
    bot: Bot, user_id: int, race_id: int, race_data: dict, i18n=None
):
    """Send new season reminder notification before race 1"""
    user_info = get_user_info(user_id)
    group = user_info["group"]
    ui_lang = user_info["ui_lang"]

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    get_text = get_text_getter(i18n, ui_lang)

    if group:
        group_display = format_group_display(group)
        message = get_text(
            "notif-new-season-reminder",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            group=group_display,
        )
    else:
        message = get_text(
            "notif-new-season-reminder-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
        )

    success = await send_notification(
        bot, user_id, message, "new season reminder", race_id
    )
    if success:
        logger.info(f"🌟 Sent new season reminder to {user_id} for race {race_id}")

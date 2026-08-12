"""Race results notification sender"""

import logging

from aiogram import Bot

from utils import add_flag_to_track
from timezone_utils import format_datetime_for_user
from notifications.utils.link_generators import (
    generate_gpro_link,
    generate_race_analysis_link,
    generate_app_race_analysis_link,
    generate_app_race_summary_link,
)
from notifications.senders.common import (
    DeliveryStatus,
    DeliveryOutcome,
    get_user_info,
    get_text_getter,
    send_notification,
)

logger = logging.getLogger(__name__)


async def send_race_results_notification(
    bot: Bot, user_id: int, race_id: int, race_data: dict, i18n=None
) -> DeliveryOutcome:
    """Send race results notification when next quali opens"""
    user_info = get_user_info(user_id)
    group = user_info["group"]
    gpro_lang = user_info["gpro_lang"]
    ui_lang = user_info["ui_lang"]
    website_mode = user_info["website_mode"]

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")

    # Generate analysis and summary links based on website mode
    if website_mode == "app":
        analysis_link = generate_app_race_analysis_link()
        summary_link = generate_app_race_summary_link(group)
        logger.debug(
            f"User {user_id} using APP mode - Analysis: {analysis_link}, Summary: {summary_link}"
        )
    else:
        # Race Analysis link (same for everyone, just language)
        analysis_link = generate_race_analysis_link(gpro_lang)
        # Race Summary link (group-dependent)
        summary_link = generate_gpro_link(group, gpro_lang, "replay")
        summary_link = summary_link.replace("racescreen.asp", "RaceSummary.asp")
        logger.debug(
            f"User {user_id} using Classic mode - Analysis: {analysis_link}, Summary: {summary_link}"
        )

    get_text = get_text_getter(i18n, ui_lang)

    # Build message based on whether group is set
    if group:
        message = get_text(
            "notif-race-results",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            analysisLink=analysis_link,
            summaryLink=summary_link,
        )
    else:
        message = get_text(
            "notif-race-results-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            analysisLink=analysis_link,
        )

    success = await send_notification(
        bot, user_id, message, "race results notification", race_id
    )
    if success is DeliveryStatus.SENT:
        logger.info(
            f"📊 Sent race results notification to {user_id} for race {race_id}"
        )
    return success

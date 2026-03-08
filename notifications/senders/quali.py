"""Qualifying notification sender (main quali notifications)"""

import logging
from datetime import datetime, UTC

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from gpro_calendar import race_calendar
from utils import add_flag_to_track
from timezone_utils import format_datetime_for_user
from notifications.users import (
    get_user_status,
    mark_user_blocked,
    DEFAULT_USER_LANG,
)
from notifications.utils.link_generators import (
    generate_quali_link,
    generate_app_quali_link,
)
from notifications.utils.snooze_manager import (
    QUALI_NOTIFICATION_TYPES,
    get_snooze_buttons,
)
from notifications.senders.common import get_text_getter

logger = logging.getLogger(__name__)


def is_qualifying_closed(race_id: int, race_data: dict) -> bool:
    """Check if qualifying is currently closed (between deadline and opens_soon)

    Qualifying is closed when:
    - Current time is after the quali_close deadline
    - AND the "opens_soon" notification hasn't been sent yet for this race

    Args:
        race_id: The race ID to check
        race_data: The race data dict

    Returns:
        bool: True if qualifying is closed and waiting for race to be calculated
    """
    from notifications.history import get_notify_history

    notify_history = get_notify_history()
    now = datetime.now(UTC)
    quali_close = race_data.get("quali_close")

    if not quali_close:
        return False

    # Check if qualifying deadline has passed
    if now <= quali_close:
        return False

    # Check if "opens_soon" notification was already sent (meaning quali is open)
    history_key = (race_id, "opens_soon")
    if history_key in notify_history:
        return False

    # Qualifying is closed if deadline passed and opens_soon not sent yet
    return True


async def send_quali_notification(
    bot: Bot,
    user_id: int,
    race_id: int,
    race_data: dict,
    notification_type: str = "deadline",
    i18n=None,
):
    """Send qualifying notification with appropriate formatting and buttons"""
    user_status, _ = get_user_status(user_id)

    # Skip automatic notifications if user marked quali done
    if user_status.get("completed_quali") == race_id and notification_type != "manual":
        return

    track = add_flag_to_track(race_data["track"])
    race_date = race_data["date"]
    quali_close = race_data["quali_close"]
    gpro_lang = user_status.get("gpro_lang", DEFAULT_USER_LANG)
    ui_lang = user_status.get("ui_lang", "gb")
    website_mode = user_status.get("website_mode", "classic")

    # Generate qualifying link based on website mode
    if website_mode == "app":
        quali_link = generate_app_quali_link()
        logger.debug(f"User {user_id} using APP mode - Quali link: {quali_link}")
    else:
        quali_link = generate_quali_link(gpro_lang)
        logger.debug(f"User {user_id} using Classic mode - Quali link: {quali_link}")

    get_text = get_text_getter(i18n, ui_lang)

    # Check if this is a snoozed notification
    is_snoozed = notification_type.startswith("snooze_")
    if is_snoozed:
        original_type = notification_type.replace("snooze_", "")
    else:
        original_type = notification_type

    # Check if qualifying is currently closed (deadline passed)
    now = datetime.now(UTC)
    quali_is_closed = is_qualifying_closed(race_id, race_data) or quali_close < now

    if quali_is_closed and not is_snoozed:
        # Qualifying is closed, waiting for race to be calculated
        emoji = "🔒"
        title = get_text("notif-quali-closed-title")
        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
    elif notification_type == "opens_soon":
        emoji = "🆕"
        title = get_text("notif-quali-opens")
        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
    else:
        if "hours_left" not in race_data:
            hours_left = (quali_close - now).total_seconds() / 3600
        else:
            hours_left = race_data["hours_left"]

        if hours_left >= 24:
            days = int(hours_left / 24)
            remaining_hours = int(hours_left % 24)
            if remaining_hours > 0:
                time_text = get_text(
                    "time-days-hours", days=days, hours=remaining_hours
                )
            else:
                time_text = get_text("time-days", days=days)
            emoji = "🔔"
        elif hours_left >= 2:
            hours = int(hours_left)
            minutes = int((hours_left - hours) * 60)
            if minutes > 0:
                time_text = get_text("time-hours-minutes", hours=hours, minutes=minutes)
            else:
                time_text = get_text("time-hours", hours=hours)
            emoji = "⏰"
        else:
            # For anything under 2 hours, just show minutes
            minutes = int(hours_left * 60)
            time_text = get_text("time-minutes", minutes=minutes)
            if hours_left >= 0.333:
                emoji = "⚠️"
            else:
                emoji = "🚨"

        deadline = format_datetime_for_user(quali_close, user_id, "%d.%m %H:%M")
        race_time = format_datetime_for_user(race_date, user_id, "%d.%m %H:%M")
        title = get_text("notif-quali-closes", time=time_text)

    # Add 🔁 prefix for snoozed notifications
    if is_snoozed:
        title = f"🔁 {title}"

    # Check if user already marked this race done
    is_marked_done = user_status.get("completed_quali") == race_id

    # Check if weather data is available
    has_weather = race_id in race_calendar and "weather" in race_calendar[race_id]

    # Build keyboard and message based on state
    keyboard_buttons = []

    if quali_is_closed:
        # Only show weather button if available (no "Done" button when closed)
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )
        message = get_text(
            "notif-quali-closed-message",
            emoji=emoji,
            title=title,
            raceId=race_id,
            track=track,
            qualiDeadline=deadline,
            raceTime=race_time,
        )
    elif is_marked_done:
        keyboard_buttons = [
            [
                InlineKeyboardButton(
                    text=get_text("button-reenable-race", raceId=race_id),
                    callback_data=f"reset_{race_id}",
                )
            ]
        ]
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )
        message = get_text(
            "notif-quali-message-disabled",
            emoji=emoji,
            title=title,
            raceId=race_id,
            track=track,
            qualiDeadline=deadline,
            raceTime=race_time,
            qualiLink=quali_link,
        )
    else:
        keyboard_buttons = [
            [
                InlineKeyboardButton(
                    text=get_text("button-quali-done"), callback_data=f"done_{race_id}"
                )
            ]
        ]
        if has_weather:
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=get_text("button-weather"),
                        callback_data=f"weather_{race_id}",
                    )
                ]
            )

        # Add snooze buttons for qualifying deadline notifications
        if (
            original_type in QUALI_NOTIFICATION_TYPES
            and original_type != "manual"
            and not quali_is_closed
        ):
            snooze_buttons = get_snooze_buttons(
                user_id, race_id, original_type, get_text
            )
            if snooze_buttons:
                keyboard_buttons.extend(snooze_buttons)

        # Use snooze-specific message template if snoozed
        if is_snoozed:
            message = get_text(
                "notif-snooze-message",
                emoji=emoji,
                title=title,
                raceId=race_id,
                track=track,
                qualiDeadline=deadline,
                raceTime=race_time,
                qualiLink=quali_link,
            )
        else:
            message = get_text(
                "notif-quali-message",
                emoji=emoji,
                title=title,
                raceId=race_id,
                track=track,
                qualiDeadline=deadline,
                raceTime=race_time,
                qualiLink=quali_link,
            )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    try:
        await bot.send_message(
            user_id, message, reply_markup=keyboard, parse_mode="HTML"
        )
        logger.info(f"✅ Sent {notification_type} to {user_id} for race {race_id}")
    except Exception as e:
        from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

        if isinstance(e, TelegramForbiddenError):
            mark_user_blocked(user_id)
            logger.warning(f"🚫 User {user_id} blocked the bot (quali notification)")
        elif isinstance(e, TelegramBadRequest) and "chat not found" in str(e.message).lower():
            logger.warning(f"📍 Chat not found for user {user_id} (quali notification)")
            mark_user_blocked(user_id)
        else:
            logger.error(f"Notify {user_id} failed: {e}")

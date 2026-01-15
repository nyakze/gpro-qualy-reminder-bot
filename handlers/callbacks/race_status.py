"""Race status callback handlers"""

import logging
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext

from gpro_calendar import race_calendar
from notifications import (
    get_user_status,
    mark_quali_done,
    reset_user_status,
    format_weather_data,
)
from utils import add_flag_to_track
from . import router

logger = logging.getLogger(__name__)


def strip_existing_feedback(message_text: str, i18n: I18nContext) -> str:
    """Remove existing feedback messages from notification text"""
    feedback_messages = [
        i18n.get("feedback-race-marked-done"),
        i18n.get("feedback-notifications-reenabled"),
        i18n.get("feedback-notifications-reset"),
    ]

    parts = message_text.split("\n\n")

    cleaned_parts = [
        part
        for part in parts
        if part.strip() not in [msg.strip() for msg in feedback_messages]
    ]

    return "\n\n".join(cleaned_parts)


def build_race_notification_keyboard(
    user_id: int, race_id: int, i18n: I18nContext
) -> InlineKeyboardMarkup:
    """Build keyboard for race notification with toggled done/reset button and weather"""
    user_status = get_user_status(user_id)
    is_marked_done = user_status.get("completed_quali") == race_id

    has_weather = race_id in race_calendar and "weather" in race_calendar[race_id]

    keyboard_buttons = []

    if is_marked_done:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-reenable-race", raceId=race_id),
                    callback_data=f"reset_{race_id}",
                )
            ]
        )
    else:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-quali-done"),
                    callback_data=f"done_{race_id}",
                )
            ]
        )

    if has_weather:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-weather"),
                    callback_data=f"weather_{race_id}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


@router.callback_query(F.data.startswith("done_"))
async def handle_quali_done(callback: CallbackQuery, i18n: I18nContext):
    try:
        race_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
        return

    user_id = callback.from_user.id
    mark_quali_done(user_id, race_id)

    new_keyboard = build_race_notification_keyboard(user_id, race_id, i18n)

    clean_message = strip_existing_feedback(callback.message.html_text, i18n)
    updated_message = clean_message + "\n\n" + i18n.get("feedback-race-marked-done")
    await callback.message.edit_text(
        updated_message, reply_markup=new_keyboard, parse_mode="HTML"
    )

    await callback.answer(i18n.get("feedback-quali-done"))


@router.callback_query(F.data.startswith("reset_"))
async def handle_reset(callback: CallbackQuery, i18n: I18nContext):
    user_id = callback.from_user.id

    if callback.data == "reset_all":
        reset_user_status(user_id)
        await callback.answer(i18n.get("feedback-reset"))
    else:
        try:
            race_id = int(callback.data.split("_")[1])
        except (ValueError, IndexError):
            await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
            return

        reset_user_status(user_id)

        new_keyboard = build_race_notification_keyboard(user_id, race_id, i18n)

        clean_message = strip_existing_feedback(callback.message.html_text, i18n)
        updated_message = (
            clean_message + "\n\n" + i18n.get("feedback-notifications-reenabled")
        )
        await callback.message.edit_text(
            updated_message, reply_markup=new_keyboard, parse_mode="HTML"
        )

        await callback.answer(i18n.get("feedback-reenabled"))


@router.callback_query(F.data.startswith("weather_"))
async def handle_weather(callback: CallbackQuery, i18n: I18nContext):
    """Display weather forecast for a race"""
    try:
        race_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
        return

    if race_id not in race_calendar:
        await callback.answer(i18n.get("error-race-not-found"), show_alert=True)
        return

    race_data = race_calendar[race_id]
    weather_data = race_data.get("weather")

    if not weather_data:
        await callback.answer(i18n.get("error-weather-not-available"), show_alert=True)
        return

    weather_message = format_weather_data(weather_data, i18n)
    track = add_flag_to_track(race_data.get("track", f"Race {race_id}"))

    race_header = i18n.get("weather-race-header", raceId=race_id, track=track)
    full_message = f"<b>{race_header}</b>\n\n{weather_message}"

    try:
        await callback.message.answer(full_message, parse_mode="HTML")
        await callback.answer(i18n.get("feedback-weather-sent"))
    except Exception as e:
        logger.error(f"Failed to send weather for race {race_id}: {e}")
        await callback.answer(i18n.get("error-weather-send-failed"), show_alert=True)

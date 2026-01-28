"""Main menu callback handlers"""

import logging
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_i18n import I18nContext

from gpro_calendar import race_calendar
from notifications import send_quali_notification, get_user_status
from notifications.user_data import set_user_website_mode
from . import router

logger = logging.getLogger(__name__)


@router.callback_query(F.data == "main_menu_status")
async def handle_main_menu_status(callback: CallbackQuery, i18n: I18nContext):
    """Handle Status button from main menu"""
    from datetime import datetime, UTC

    await callback.answer()

    if not race_calendar:
        await callback.message.answer(i18n.get("no-races-scheduled"))
        return

    now = datetime.now(UTC)
    future_races = []

    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close", now)
                race_date = race_data.get("date", now)
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    future_races.append((race_id, race_data))
    else:
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close", now)
                race_date = race_data.get("date", now)
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    race_id = race_data.get("race_id", i + 1)
                    future_races.append((race_id, race_data))

    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        next_race_id, next_race_data = future_races[0]
        await send_quali_notification(
            callback.bot,
            callback.from_user.id,
            next_race_id,
            next_race_data,
            "manual",
            i18n,
        )
        logger.info(
            f"Main menu status sent for race {next_race_id} to {callback.from_user.id}"
        )
    else:
        await callback.message.answer(i18n.get("no-upcoming-qualifications"))


@router.callback_query(F.data == "main_menu_calendar")
async def handle_main_menu_calendar(callback: CallbackQuery, i18n: I18nContext):
    """Handle Calendar button from main menu"""
    from utils import format_full_calendar

    user_id = callback.from_user.id
    await callback.answer()
    calendar_text = format_full_calendar(
        race_calendar, "Full Season", is_current_season=True, user_id=user_id, i18n=i18n
    )
    title = i18n.get("calendar-title-full")
    text = f"{title}\n\n{calendar_text}"
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "main_menu_next")
async def handle_main_menu_next(callback: CallbackQuery, i18n: I18nContext):
    """Handle Next Season button from main menu"""
    from gpro_calendar import next_season_calendar, load_next_season_silent
    from utils import format_full_calendar

    user_id = callback.from_user.id
    await callback.answer()
    await load_next_season_silent()

    if not next_season_calendar:
        await callback.message.answer(i18n.get("next-season-not-published"))
        return

    calendar_text = format_full_calendar(
        next_season_calendar,
        "Next Season",
        is_current_season=False,
        user_id=user_id,
        i18n=i18n,
    )
    title = i18n.get("calendar-title-next", count=len(next_season_calendar))
    text = f"{title}\n\n{calendar_text}"
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "main_menu_settings")
async def handle_main_menu_settings(callback: CallbackQuery, i18n: I18nContext):
    """Handle Settings button from main menu"""
    from .settings import build_settings_keyboard

    await callback.answer()

    user_id = callback.from_user.id
    keyboard = build_settings_keyboard(user_id, i18n)

    await callback.message.answer(
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="HTML"
    )


@router.callback_query(F.data == "toggle_website_mode")
async def handle_toggle_website_mode(callback: CallbackQuery, i18n: I18nContext):
    """Toggle between Classic and APP website modes"""
    from .settings import handle_settings_main

    user_id = callback.from_user.id
    user_status = get_user_status(user_id)[0]
    current_mode = user_status.get("website_mode", "classic")

    new_mode = "app" if current_mode == "classic" else "classic"

    logger.info(f"User {user_id} toggling website mode: {current_mode} → {new_mode}")

    if set_user_website_mode(user_id, new_mode):
        if new_mode == "app":
            message = i18n.get("feedback-switched-to-app")
        else:
            message = i18n.get("feedback-switched-to-classic")

        logger.info(f"User {user_id} successfully switched to {new_mode} mode")
        await callback.answer(message)

        await handle_settings_main(callback, i18n)
    else:
        logger.error(f"User {user_id} failed to switch to {new_mode} mode")
        await callback.answer(i18n.get("error-mode-switch-failed"))

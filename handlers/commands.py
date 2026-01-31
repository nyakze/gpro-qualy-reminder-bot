"""Command handlers for /start, /status, /calendar, etc."""

import logging
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from datetime import datetime, UTC

from gpro_calendar import (
    race_calendar,
    next_season_calendar,
    load_next_season_silent,
)
from notifications import (
    get_user_status,
    send_quali_notification,
    users_data,
    unblock_user,
)
from utils import format_full_calendar
from handlers.admin_commands import format_user_link
from . import router

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, bot, state: FSMContext, i18n: I18nContext):
    user_id = message.from_user.id

    await state.clear()

    # Unblock user if they were previously blocked (user unblocked the bot)
    unblock_user(user_id)

    _, was_new = get_user_status(user_id)

    if was_new:
        logger.info(f"🆕 NEW user {user_id} registered via /start")
        from notifications import update_user_profile

        update_user_profile(
            user_id,
            tg_language_code=message.from_user.language_code,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )

        from config import ADMIN_USER_IDS

        user_link = format_user_link(
            user_id, message.from_user.username, message.from_user.first_name
        )

        timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

        for admin_id in ADMIN_USER_IDS:
            if users_data.get(admin_id, {}).get("notify_new_users", False):
                try:
                    await bot.send_message(
                        admin_id,
                        f"🆕 New user: <code>{user_id}</code> ({user_link}) at {timestamp}",
                        parse_mode="HTML",
                    )
                    logger.info(f"New user notification sent to admin {admin_id}")
                except Exception as e:
                    logger.error(
                        f"Failed to send new user notification to admin {admin_id}: {e}"
                    )
        from .callbacks.settings import build_ui_language_keyboard

        keyboard = build_ui_language_keyboard(
            page=1, current_ui_lang="gb", i18n=None, onboarding=True
        )

        await message.answer(
            "👋 <b>Welcome to GPRO Bot!</b>\n\n" "Choose your preferred bot language:",
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    else:
        logger.debug(f"👤 Existing user {user_id} used /start")
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-main-menu-status"),
                        callback_data="main_menu_status",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-main-menu-calendar"),
                        callback_data="main_menu_calendar",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-main-menu-next"),
                        callback_data="main_menu_next",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-main-menu-settings"),
                        callback_data="main_menu_settings",
                    )
                ],
            ]
        )
        await message.answer(
            i18n.get("start-welcome-existing-buttons"),
            reply_markup=keyboard,
            parse_mode="HTML",
        )


@router.message(Command("settings"))
async def cmd_settings(message: Message, state: FSMContext, i18n: I18nContext):
    """Show main settings menu"""
    await state.clear()

    user_id = message.from_user.id

    from .callbacks import build_settings_keyboard

    keyboard = build_settings_keyboard(user_id, i18n)

    await message.answer(
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="HTML"
    )


@router.message(Command("status"))
async def cmd_status(message: Message, bot, state: FSMContext, i18n: I18nContext):
    """Show next race status with full details including weather"""
    await state.clear()

    if not race_calendar:
        await message.answer(i18n.get("no-races-scheduled"))
        return

    now = datetime.now(UTC)
    future_races = []

    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close")
                race_date = race_data.get("date")
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    future_races.append((race_id, race_data))
    else:
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close")
                race_date = race_data.get("date")
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    race_id = race_data.get("race_id", i + 1)
                    future_races.append((race_id, race_data))

    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        next_race_id, next_race_data = future_races[0]
        await send_quali_notification(
            bot, message.from_user.id, next_race_id, next_race_data, "manual", i18n
        )
        logger.info(
            f"📊 /status sent for race {next_race_id} ({next_race_data.get('track', 'Unknown')}) to {message.from_user.id}"
        )
    else:
        await message.answer(i18n.get("no-upcoming-qualifications"))


@router.message(Command("calendar"))
async def cmd_calendar(message: Message, state: FSMContext, i18n: I18nContext):
    """Show full race calendar"""
    await state.clear()
    user_id = message.from_user.id
    calendar_text = format_full_calendar(
        race_calendar, "Full Season", is_current_season=True, user_id=user_id, i18n=i18n
    )
    title = i18n.get("calendar-title-full")
    text = f"{title}\n\n{calendar_text}"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("next"))
async def cmd_next(message: Message, i18n: I18nContext):
    await load_next_season_silent()

    if not next_season_calendar:
        await message.answer(
            i18n.get("next-season-not-published"),
            parse_mode="HTML"
        )
        return

    user_id = message.from_user.id
    calendar_text = format_full_calendar(
        next_season_calendar,
        "Next Season",
        is_current_season=False,
        user_id=user_id,
        i18n=i18n,
    )
    title = i18n.get("calendar-title-next", count=len(next_season_calendar))
    text = f"{title}\n\n{calendar_text}"
    await message.answer(text, parse_mode="HTML")


@router.message(Command("schedule"))
async def cmd_schedule(message: Message, i18n: I18nContext):
    await cmd_calendar(message, i18n)


@router.message(Command("notify"))
async def cmd_notify(message: Message, bot, state: FSMContext, i18n: I18nContext):
    """Send a test notification for the next race (hidden command for testing)"""
    await state.clear()

    if not race_calendar:
        await message.answer(i18n.get("no-races-scheduled"))
        return

    now = datetime.now(UTC)
    future_races = []

    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close")
                race_date = race_data.get("date")
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    future_races.append((race_id, race_data))
    else:
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict):
                quali_close = race_data.get("quali_close")
                race_date = race_data.get("date")
                # Include race if quali hasn't closed yet, OR if quali is closed but race hasn't happened
                if quali_close > now or (quali_close <= now < race_date):
                    race_id = race_data.get("race_id", i + 1)
                    future_races.append((race_id, race_data))

    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        next_race_id, next_race_data = future_races[0]
        await send_quali_notification(
            bot, message.from_user.id, next_race_id, next_race_data, "deadline", i18n
        )
        logger.info(
            f"🔔 /notify sent test notification for race {next_race_id} ({next_race_data.get('track', 'Unknown')}) to {message.from_user.id}"
        )
    else:
        await message.answer(i18n.get("no-upcoming-qualifications"))

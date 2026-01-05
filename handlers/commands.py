"""Command handlers for /start, /status, /calendar, etc."""

import logging
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from datetime import datetime

from gpro_calendar import (
    race_calendar,
    next_season_calendar,
    update_calendar,
    load_next_season_silent,
)
from notifications import (
    get_user_status,
    reset_user_status,
    send_quali_notification,
    save_users_data,
    users_data,
)
from utils import format_full_calendar
from config import ADMIN_USER_IDS
from . import router

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, i18n: I18nContext):
    user_id = message.from_user.id

    # Clear any active state when command is issued
    await state.clear()

    # Check BEFORE adding
    was_new = user_id not in users_data
    get_user_status(user_id)

    if was_new:
        logger.info(f"🆕 NEW user {user_id} registered via /start")
        # Show bot UI language selection with 2-column layout
        from .callbacks import build_ui_language_keyboard

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
        # Show main menu with buttons for existing users
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
    # Clear any active state when command is issued
    await state.clear()

    # Import here to avoid circular import
    from .callbacks import build_settings_keyboard

    user_id = message.from_user.id
    keyboard = build_settings_keyboard(user_id, i18n)

    await message.answer(
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="HTML"
    )


@router.message(Command("status"))
async def cmd_status(message: Message, bot, state: FSMContext, i18n: I18nContext):
    """Show next race status with full details including weather"""
    # Clear any active state when command is issued
    await state.clear()

    if not race_calendar:
        await message.answer(i18n.get("no-races-scheduled"))
        return

    # Find next upcoming race
    now = datetime.utcnow()
    future_races = []

    # Handle dict or list
    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                future_races.append((race_id, race_data))
    else:
        # List format fallback
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                race_id = race_data.get("race_id", i + 1)
                future_races.append((race_id, race_data))

    # Sort by quali_close (earliest first)
    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        next_race_id, next_race_data = future_races[0]  # First = soonest
        # Send full notification with weather button and all details
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
    # Clear any active state when command is issued
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
        await message.answer(i18n.get("next-season-not-published"))
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


@router.message(Command("update"))
async def cmd_update(message: Message, i18n: I18nContext):
    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    await update_calendar()

    reset_count = 0
    for user_id in list(users_data.keys()):
        reset_user_status(user_id)
        reset_count += 1

    # Current season status
    await message.answer(
        i18n.get(
            "admin-calendar-updated", count=len(race_calendar), userCount=reset_count
        ),
        parse_mode="HTML",
    )

    # Next season status
    if next_season_calendar:
        await message.answer(
            i18n.get("admin-next-season-ready", count=len(next_season_calendar)),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            i18n.get("admin-next-season-not-published"),
            parse_mode="HTML",
        )


@router.message(Command("users"))
async def cmd_users(message: Message, i18n: I18nContext):
    logger.debug(
        f"USERS - User: {message.from_user.id} ({type(message.from_user.id)}), Admins: {ADMIN_USER_IDS}"
    )

    if message.from_user.id not in ADMIN_USER_IDS:
        logger.warning(f"USERS: Access denied for user {message.from_user.id}")
        await message.answer(i18n.get("admin-only"))
        return

    logger.debug("USERS: Admin access granted")

    try:
        logger.debug(f"USERS: Loaded {len(users_data)} users from notifications")

        if not users_data:
            await message.answer(i18n.get("admin-users-none"), parse_mode="HTML")
            return

        header = i18n.get("admin-users-count", count=len(users_data))
        text = f"{header}\n\n"
        for uid, status in users_data.items():
            quali = status.get("completed_quali", "None")
            text += f"• <code>{uid}</code>: Race {quali}\n"

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"USERS ERROR: {e}")
        await message.answer(i18n.get("error-invalid-data"), parse_mode="HTML")


@router.message(Command("deleteuser", "deluser"))
async def cmd_deleteuser(message: Message, i18n: I18nContext):
    """Admin command to delete a user from the database (for testing onboarding)

    Usage:
        /deleteuser USER_ID - Delete specified user
        /deleteuser - Delete yourself
        /deluser - Alias for /deleteuser
    """
    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    # Parse user ID from command
    if message.text and len(message.text.split()) > 1:
        try:
            target_user_id = int(message.text.split()[1])
        except ValueError:
            await message.answer(
                "❌ Invalid user ID. Usage: `/deleteuser USER_ID`",
                parse_mode="HTML",
            )
            return
    else:
        target_user_id = message.from_user.id

    # Delete user
    if target_user_id in users_data:
        del users_data[target_user_id]
        save_users_data()
        await message.answer(
            f"✅ Deleted user `{target_user_id}` from database.\n\n"
            f"They will see onboarding on next /start",
            parse_mode="HTML",
        )
        logger.info(f"Admin {message.from_user.id} deleted user {target_user_id}")
    else:
        await message.answer(
            f"❌ User `{target_user_id}` not found in database", parse_mode="HTML"
        )


@router.message(Command("weather"))
async def cmd_weather(message: Message, i18n: I18nContext):
    """Admin command to manually fetch weather data for next race

    Usage:
        /weather - Fetch weather if not cached
        /weather force - Force fetch even if cached
    """
    from gpro_calendar import fetch_weather_from_api
    from utils import add_flag_to_track

    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    if not race_calendar:
        await message.answer(i18n.get("admin-no-races"), parse_mode="HTML")
        return

    # Check for "force" argument
    force_update = False
    if message.text and len(message.text.split()) > 1:
        args = message.text.split()[1:]
        if "force" in args:
            force_update = True

    # Find next upcoming race
    now = datetime.utcnow()
    next_race_id = None
    next_race_data = None

    for race_id, race_data in sorted(race_calendar.items()):
        if race_data.get("quali_close", now) > now:
            next_race_id = race_id
            next_race_data = race_data
            break

    if not next_race_id:
        await message.answer(i18n.get("admin-no-upcoming-races"), parse_mode="HTML")
        return

    track = add_flag_to_track(next_race_data.get("track", f"Race {next_race_id}"))

    # Check if weather already cached (skip if force update)
    if "weather" in next_race_data and not force_update:
        await message.answer(
            i18n.get("weather-cached", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )
        return

    # Fetch weather
    if force_update and "weather" in next_race_data:
        await message.answer(
            i18n.get("weather-force-updating", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )
        # Clear cached weather to force fresh fetch
        del race_calendar[next_race_id]["weather"]
    else:
        await message.answer(
            i18n.get("weather-fetching", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )

    weather_data = await fetch_weather_from_api(next_race_id)

    if weather_data:
        await message.answer(
            i18n.get("weather-success", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )
    else:
        await message.answer(i18n.get("weather-failed"), parse_mode="HTML")


@router.message(Command("notify"))
async def cmd_notify(message: Message, bot, state: FSMContext, i18n: I18nContext):
    """Send a test notification for the next race (same format as automatic notifications)

    This is a hidden command for testing notification formatting and delivery.
    It sends the exact same notification that users would receive automatically.
    """
    # Clear any active state when command is issued
    await state.clear()

    if not race_calendar:
        await message.answer(i18n.get("no-races-scheduled"))
        return

    # Find next upcoming race
    now = datetime.utcnow()
    future_races = []

    # Handle dict or list
    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                future_races.append((race_id, race_data))
    else:
        # List format fallback
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                race_id = race_data.get("race_id", i + 1)
                future_races.append((race_id, race_data))

    # Sort by quali_close (earliest first)
    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        next_race_id, next_race_data = future_races[0]  # First = soonest
        # Send full notification with weather button and all details
        # Use "deadline" type (not "manual") to show the full notification format
        await send_quali_notification(
            bot, message.from_user.id, next_race_id, next_race_data, "deadline", i18n
        )
        logger.info(
            f"🔔 /notify sent test notification for race {next_race_id} ({next_race_data.get('track', 'Unknown')}) to {message.from_user.id}"
        )
    else:
        await message.answer(i18n.get("no-upcoming-qualifications"))


@router.message(Command("updatetz"))
async def cmd_updatetz(message: Message, i18n: I18nContext):
    """Admin command to download and index timezone metadata from Geoapify

    Usage:
        /updatetz - Download timezone data and rebuild search index
    """
    from timezone_utils import (
        download_timezone_data,
        load_timezone_search_index,
        TIMEZONE_DATA_FILE,
    )
    import os

    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    await message.answer(
        "⏳ Downloading timezone data from Geoapify...", parse_mode="HTML"
    )

    # Download timezone data
    success = await download_timezone_data()

    if not success:
        await message.answer(
            "❌ **Failed to download timezone data**\n\n"
            "Please check logs for details.",
            parse_mode="HTML",
        )
        return

    # Check file size
    file_size = os.path.getsize(TIMEZONE_DATA_FILE) / 1024  # KB

    await message.answer(
        f"✅ **Downloaded timezone data**\n"
        f"File size: {file_size:.1f} KB\n\n"
        f"Building search index...",
        parse_mode="HTML",
    )

    # Build and load search index
    if load_timezone_search_index():
        await message.answer(
            "✅ **Timezone search index ready**\n\n"
            "Users can now search for timezones in multiple languages!",
            parse_mode="HTML",
        )
        logger.info(
            f"Admin {message.from_user.id} updated timezone data and search index"
        )
    else:
        await message.answer(
            "❌ **Failed to build search index**\n\n" "Please check logs for details.",
            parse_mode="HTML",
        )

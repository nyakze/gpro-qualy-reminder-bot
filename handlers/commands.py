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
    update_user_profile,
)
from utils import format_full_calendar
from config import ADMIN_USER_IDS
from . import router

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, i18n: I18nContext):
    user_id = message.from_user.id

    await state.clear()

    was_new = user_id not in users_data
    get_user_status(user_id)

    if was_new:
        logger.info(f"🆕 NEW user {user_id} registered via /start")
        update_user_profile(
            user_id,
            tg_language_code=message.from_user.language_code,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )
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

    # Check for "soft" argument
    soft_update = False
    if message.text and len(message.text.split()) > 1:
        args = message.text.split()[1:]
        if "soft" in args:
            soft_update = True

    await update_calendar()

    # Reset user data unless soft update
    reset_count = 0
    if not soft_update:
        for user_id in list(users_data.keys()):
            reset_user_status(user_id)
            reset_count += 1

    # Current season status
    if soft_update:
        await message.answer(
            f"✅ <b>Calendar updated</b> (soft mode)\n\n"
            f"📅 Current season: {len(race_calendar)} races\n"
            f"👥 User data: <i>preserved</i>",
            parse_mode="HTML",
        )
    else:
        await message.answer(
            i18n.get(
                "admin-calendar-updated",
                count=len(race_calendar),
                userCount=reset_count,
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
    """List all users in compact format"""
    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    try:
        if not users_data:
            await message.answer(i18n.get("admin-users-none"), parse_mode="HTML")
            return

        total_users = len(users_data)
        users_with_group = sum(1 for u in users_data.values() if u.get("group"))

        header = i18n.get("admin-users-count", count=total_users)
        text = f"{header}\n\n"
        text += f"📊 {users_with_group} in groups, {total_users - users_with_group} without\n\n"

        for uid, status in users_data.items():
            quali = status.get("completed_quali", "None")
            group = status.get("group", "—")
            username = status.get("username")
            first_name = status.get("first_name")

            if username:
                display_name = f"@{username}"
                link = f'<a href="tg://user?id={uid}">{display_name}</a>'
            elif first_name:
                display_name = first_name
                link = f'<a href="tg://user?id={uid}">{display_name}</a>'
            else:
                link = "—"

            text += f"• <code>{uid}</code> ({link}): Race {quali} | Group {group}\n"

        text += "\n💡 Use /user USER_ID for details or /userstats for statistics"
        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"USERS ERROR: {e}")
        await message.answer(i18n.get("error-invalid-data"), parse_mode="HTML")


@router.message(Command("user"))
async def cmd_user(message: Message, i18n: I18nContext):
    """Show detailed information about a specific user

    Usage:
        /user USER_ID - Show details for specified user
        /user - Show details for yourself
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
                "❌ Invalid user ID. Usage: <code>/user USER_ID</code>",
                parse_mode="HTML",
            )
            return
    else:
        target_user_id = message.from_user.id

    # Get user data
    if target_user_id not in users_data:
        await message.answer(
            f"❌ User <code>{target_user_id}</code> not found in database",
            parse_mode="HTML",
        )
        return

    status = users_data[target_user_id]

    first_name = status.get("first_name")
    username = status.get("username")
    tg_language_code = status.get("tg_language_code")

    text = f"👤 <b>User Details: <code>{target_user_id}</code></b>\n\n"

    if first_name or username or tg_language_code:
        text += "<b>📱 Telegram Profile:</b>\n"
        if first_name:
            text += f"• Name: {first_name}\n"
        if username:
            text += f"• Username: @{username}\n"
        if tg_language_code:
            text += f"• Language: {tg_language_code}\n"
        text += "\n"

    text += "<b>📋 Basic Info:</b>\n"
    text += f"• Completed Quali: {status.get('completed_quali', 'None')}\n"
    text += f"• Group: {status.get('group', '—')}\n"
    text += f"• Website Mode: {status.get('website_mode', 'classic')}\n\n"

    text += "<b>🌍 Localization:</b>\n"
    text += f"• UI Language: {status.get('ui_lang', 'gb')}\n"
    text += f"• GPRO Language: {status.get('gpro_lang', 'gb')}\n"
    text += f"• Timezone: {status.get('timezone', 'UTC')}\n\n"

    # Notifications
    text += "<b>🔔 Notifications:</b>\n"
    notif = status.get("notifications", {})
    if notif:
        enabled = [k for k, v in notif.items() if v]
        disabled = [k for k, v in notif.items() if not v]
        text += (
            f"• Enabled ({len(enabled)}): {', '.join(enabled) if enabled else '—'}\n"
        )
        text += f"• Disabled ({len(disabled)}): {', '.join(disabled) if disabled else '—'}\n"
    else:
        text += "• No notification settings\n"

    # Custom notifications
    custom = status.get("custom_notifications", [])
    custom_enabled = [c for c in custom if c.get("enabled")]
    if custom_enabled:
        text += "\n<b>⏰ Custom Notifications:</b>\n"
        for i, c in enumerate(custom_enabled, 1):
            hours = c.get("hours_before", "?")
            text += f"• Custom {i}: {hours}h before\n"

    await message.answer(text, parse_mode="HTML")
    logger.info(
        f"Admin {message.from_user.id} viewed user details for {target_user_id}"
    )


@router.message(Command("userstats"))
async def cmd_userstats(message: Message, i18n: I18nContext):
    """Show aggregated statistics about all users"""
    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer(i18n.get("admin-only"))
        return

    try:
        if not users_data:
            await message.answer(i18n.get("admin-users-none"), parse_mode="HTML")
            return

        total_users = len(users_data)

        text = "📊 <b>User Statistics</b>\n\n"
        text += f"👥 Total users: {total_users}\n\n"

        # Group distribution
        text += "<b>🏁 Groups:</b>\n"
        groups = {}
        for status in users_data.values():
            group = status.get("group") or "No group"
            groups[group] = groups.get(group, 0) + 1
        for group, count in sorted(
            groups.items(), key=lambda x: (x[0] == "No group", x[0])
        ):
            percentage = (count / total_users) * 100
            text += f"• {group}: {count} ({percentage:.1f}%)\n"

        # Timezone distribution (top 5)
        text += "\n<b>🌍 Timezones (Top 5):</b>\n"
        tz_counts = {}
        for status in users_data.values():
            tz = status.get("timezone", "UTC")
            tz_counts[tz] = tz_counts.get(tz, 0) + 1
        for tz, count in sorted(tz_counts.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]:
            percentage = (count / total_users) * 100
            text += f"• {tz}: {count} ({percentage:.1f}%)\n"
        if len(tz_counts) > 5:
            text += f"• ...and {len(tz_counts) - 5} more\n"

        # Language distribution
        text += "\n<b>🗣 UI Languages:</b>\n"
        lang_counts = {}
        for status in users_data.values():
            lang = status.get("ui_lang", "gb")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        for lang, count in sorted(
            lang_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {lang}: {count} ({percentage:.1f}%)\n"

        # GPRO language distribution
        text += "\n<b>🏎 GPRO Languages:</b>\n"
        gpro_lang_counts = {}
        for status in users_data.values():
            lang = status.get("gpro_lang", "gb")
            gpro_lang_counts[lang] = gpro_lang_counts.get(lang, 0) + 1
        for lang, count in sorted(
            gpro_lang_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {lang}: {count} ({percentage:.1f}%)\n"

        # Website mode distribution
        text += "\n<b>💻 Website Mode:</b>\n"
        mode_counts = {}
        for status in users_data.values():
            mode = status.get("website_mode", "classic")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        for mode, count in sorted(
            mode_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {mode}: {count} ({percentage:.1f}%)\n"

        # Notification stats
        text += "\n<b>🔔 Notifications:</b>\n"
        all_enabled = sum(
            1 for s in users_data.values() if all(s.get("notifications", {}).values())
        )
        all_disabled = sum(
            1
            for s in users_data.values()
            if not any(s.get("notifications", {}).values())
        )
        partial = total_users - all_enabled - all_disabled
        text += f"• All enabled: {all_enabled} ({(all_enabled/total_users)*100:.1f}%)\n"
        text += (
            f"• All disabled: {all_disabled} ({(all_disabled/total_users)*100:.1f}%)\n"
        )
        text += f"• Partial: {partial} ({(partial/total_users)*100:.1f}%)\n"

        # Custom notifications
        custom_users = sum(
            1
            for s in users_data.values()
            if any(c.get("enabled") for c in s.get("custom_notifications", []))
        )
        if custom_users > 0:
            text += f"• Custom notifications: {custom_users} ({(custom_users/total_users)*100:.1f}%)\n"

        await message.answer(text, parse_mode="HTML")
        logger.info(f"Admin {message.from_user.id} viewed user statistics")

    except Exception as e:
        logger.error(f"USERSTATS ERROR: {e}")
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

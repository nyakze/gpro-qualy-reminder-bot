"""Admin command handlers"""

import logging
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_i18n import I18nContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, UTC

from gpro_calendar import (
    race_calendar,
    next_season_calendar,
    update_calendar,
    fetch_weather_from_api,
)
from notifications import (
    reset_user_status,
    save_users_data,
    users_data,
)
from utils import add_flag_to_track
from config import ADMIN_USER_IDS
from middleware.rate_limit import (
    get_rate_limit_stats,
    get_user_rate_limit_info,
    get_rate_limited_users,
)
from . import router

logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_USER_IDS


def format_user_link(user_id: int, username: str | None, first_name: str | None) -> str:
    """Format user as clickable Telegram link"""
    if username:
        return f'<a href="tg://user?id={user_id}">@{username}</a>'
    elif first_name:
        return f'<a href="tg://user?id={user_id}">{first_name}</a>'
    return "—"


def format_relative_time(iso_timestamp: str | None) -> str:
    """Format ISO timestamp as relative time (e.g., '2 hours ago')"""
    if not iso_timestamp:
        return "—"

    try:
        from datetime import datetime, UTC
        from datetime import timedelta

        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        now = datetime.now(UTC)
        delta = now - dt

        if delta < timedelta(seconds=60):
            return "just now"
        elif delta < timedelta(hours=1):
            minutes = int(delta.total_seconds() / 60)
            return f"{minutes} min ago"
        elif delta < timedelta(days=1):
            hours = int(delta.total_seconds() / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif delta < timedelta(days=30):
            days = delta.days
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif delta < timedelta(days=365):
            months = delta.days // 30
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = delta.days // 365
            return f"{years} year{'s' if years != 1 else ''} ago"
    except Exception:
        return "—"


@router.message(Command("update"))
async def cmd_update(message: Message, i18n: I18nContext):
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

    soft_update = False
    if message.text and len(message.text.split()) > 1:
        args = message.text.split()[1:]
        if "soft" in args:
            soft_update = True

    await update_calendar()

    reset_count = 0
    if not soft_update:
        for user_id in list(users_data.keys()):
            reset_user_status(user_id)
            reset_count += 1

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
    if not is_admin(message.from_user.id):
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
            last_interaction = format_relative_time(status.get("last_interaction"))

            link = format_user_link(uid, username, first_name)

            rl_info = get_user_rate_limit_info(uid)
            if rl_info and rl_info["violation_count"] > 0:
                if rl_info["is_blocked"]:
                    icon = "⛔"
                elif rl_info["warned"]:
                    icon = "⚠️"
                else:
                    icon = ""
            else:
                icon = ""

            text += f"• {icon} <code>{uid}</code> ({link}): Race {quali} | Group {group} | {last_interaction}\n"

        text += "\n💡 Use /user USER_ID for details or /userstats for statistics"
        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        logger.error(f"USERS ERROR: {e}")
        await message.answer(i18n.get("error-invalid-data"), parse_mode="HTML")


@router.message(Command("user"))
async def cmd_user(message: Message, i18n: I18nContext):
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

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
    text += f"• Website Mode: {status.get('website_mode', 'classic')}\n"
    last_interaction = format_relative_time(status.get("last_interaction"))
    text += f"• Last Active: {last_interaction}\n\n"

    text += "<b>🌍 Localization:</b>\n"
    text += f"• UI Language: {status.get('ui_lang', 'gb')}\n"
    text += f"• GPRO Language: {status.get('gpro_lang', 'gb')}\n"
    text += f"• Timezone: {status.get('timezone', 'UTC')}\n\n"

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

    custom = status.get("custom_notifications", [])
    custom_enabled = [c for c in custom if c.get("enabled")]
    if custom_enabled:
        text += "\n<b>⏰ Custom Notifications:</b>\n"
        for i, c in enumerate(custom_enabled, 1):
            hours = c.get("hours_before", "?")
            text += f"• Custom {i}: {hours}h before\n"

    # Rate limiting info
    rl_info = get_user_rate_limit_info(target_user_id)
    if rl_info and rl_info["violation_count"] > 0:
        text += "\n<b>🛡️ Rate Limit Status:</b>\n"
        text += f"• Violations: {rl_info['violation_count']}\n"
        if rl_info["is_blocked"]:
            remaining = rl_info["blocked_remaining_seconds"]
            if remaining < 60:
                time_str = f"{remaining}s"
            else:
                time_str = f"{remaining // 60}m {remaining % 60}s"
            text += f"• Currently blocked: {time_str} remaining\n"
        if rl_info["warned"]:
            text += "• Warned this session: Yes\n"

    await message.answer(text, parse_mode="HTML")
    logger.info(
        f"Admin {message.from_user.id} viewed user details for {target_user_id}"
    )


@router.message(Command("userstats"))
async def cmd_userstats(message: Message, i18n: I18nContext):
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

    try:
        if not users_data:
            await message.answer(i18n.get("admin-users-none"), parse_mode="HTML")
            return

        total_users = len(users_data)

        text = "📊 <b>User Statistics</b>\n\n"
        text += f"👥 Total users: {total_users}\n\n"

        text += "<b>🏁 Groups:</b>\n"
        groups: dict = {}
        for status in users_data.values():
            group = status.get("group") or "No group"
            groups[group] = groups.get(group, 0) + 1
        for group, count in sorted(
            groups.items(), key=lambda x: (x[0] == "No group", x[0])
        ):
            percentage = (count / total_users) * 100
            text += f"• {group}: {count} ({percentage:.1f}%)\n"

        text += "\n<b>🌍 Timezones (Top 5):</b>\n"
        tz_counts: dict = {}
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

        text += "\n<b>🗣 UI Languages:</b>\n"
        lang_counts: dict = {}
        for status in users_data.values():
            lang = status.get("ui_lang", "gb")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        for lang, count in sorted(
            lang_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {lang}: {count} ({percentage:.1f}%)\n"

        text += "\n<b>🏎 GPRO Languages:</b>\n"
        gpro_lang_counts: dict = {}
        for status in users_data.values():
            lang = status.get("gpro_lang", "gb")
            gpro_lang_counts[lang] = gpro_lang_counts.get(lang, 0) + 1
        for lang, count in sorted(
            gpro_lang_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {lang}: {count} ({percentage:.1f}%)\n"

        text += "\n<b>💻 Website Mode:</b>\n"
        mode_counts: dict = {}
        for status in users_data.values():
            mode = status.get("website_mode", "classic")
            mode_counts[mode] = mode_counts.get(mode, 0) + 1
        for mode, count in sorted(
            mode_counts.items(), key=lambda x: x[1], reverse=True
        ):
            percentage = (count / total_users) * 100
            text += f"• {mode}: {count} ({percentage:.1f}%)\n"

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

        custom_users = sum(
            1
            for s in users_data.values()
            if any(c.get("enabled") for c in s.get("custom_notifications", []))
        )
        if custom_users > 0:
            text += f"• Custom notifications: {custom_users} ({(custom_users/total_users)*100:.1f}%)\n"

        # Rate limiting stats
        rl_stats = get_rate_limit_stats()
        if rl_stats["users_with_violations"] > 0:
            text += "\n<b>🛡️ Rate Limiting:</b>\n"
            text += f"• Users with violations: {rl_stats['users_with_violations']}\n"
            if rl_stats["users_warned"] > 0:
                text += f"• Users warned: {rl_stats['users_warned']}\n"
            if rl_stats["users_currently_blocked"] > 0:
                text += f"• Currently blocked: {rl_stats['users_currently_blocked']}\n"

            # Show specific users who are blocked or warned
            rl_users = get_rate_limited_users()
            if rl_users:
                text += "\n<b>⚠️ Flagged Users:</b>\n"
                for uid, info in sorted(rl_users.items()):
                    # Get username from users_data if available
                    user_status = users_data.get(uid, {})
                    username = user_status.get("username")
                    first_name = user_status.get("first_name")
                    link = format_user_link(uid, username, first_name)

                    status = "🚫 BLOCKED"
                    if not info["is_blocked"]:
                        status = "⚠️ warned"
                    details = f"({info['violation_count']} violations)"
                    if info["is_blocked"]:
                        remaining = info["blocked_remaining_seconds"]
                        if remaining < 60:
                            time_str = f"{remaining}s"
                        else:
                            time_str = f"{remaining // 60}m {remaining % 60}s"
                        details += f" - {time_str} left"
                    text += f"• {link} {status} {details}\n"

        await message.answer(text, parse_mode="HTML")
        logger.info(f"Admin {message.from_user.id} viewed user statistics")

    except Exception as e:
        logger.error(f"USERSTATS ERROR: {e}")
        await message.answer(i18n.get("error-invalid-data"), parse_mode="HTML")


@router.message(Command("deleteuser", "deluser"))
async def cmd_deleteuser(message: Message, i18n: I18nContext):
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

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
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

    if not race_calendar:
        await message.answer(i18n.get("admin-no-races"), parse_mode="HTML")
        return

    force_update = False
    if message.text and len(message.text.split()) > 1:
        args = message.text.split()[1:]
        if "force" in args:
            force_update = True

    now = datetime.now(UTC)
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

    if "weather" in next_race_data and not force_update:
        await message.answer(
            i18n.get("weather-cached", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )
        return

    if force_update and "weather" in next_race_data:
        await message.answer(
            i18n.get("weather-force-updating", raceId=next_race_id, track=track),
            parse_mode="HTML",
        )
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


@router.message(Command("welcomealert"))
async def cmd_welcomealert(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Admin only command")
        return

    admin_id = message.from_user.id
    current_setting = users_data.get(admin_id, {}).get("notify_new_users", False)

    if admin_id not in users_data:
        users_data[admin_id] = {}
    users_data[admin_id]["notify_new_users"] = not current_setting
    save_users_data()

    if not current_setting:
        await message.answer(
            "✅ <b>New user notifications enabled</b>\n\n"
            "You will receive notifications when new users register via /start",
            parse_mode="HTML",
        )
        logger.info(f"Admin {admin_id} enabled new user notifications")
    else:
        await message.answer(
            "❌ <b>New user notifications disabled</b>\n\n"
            "You will no longer receive notifications for new users",
            parse_mode="HTML",
        )
        logger.info(f"Admin {admin_id} disabled new user notifications")


@router.message(Command("updatetz"))
async def cmd_updatetz(message: Message, i18n: I18nContext):
    from timezone_utils import (
        download_timezone_data,
        load_timezone_search_index,
        TIMEZONE_DATA_FILE,
    )
    import os

    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

    await message.answer(
        "⏳ Downloading timezone data from Geoapify...", parse_mode="HTML"
    )

    success = await download_timezone_data()

    if not success:
        await message.answer(
            "❌ **Failed to download timezone data**\n\n"
            "Please check logs for details.",
            parse_mode="HTML",
        )
        return

    file_size = os.path.getsize(TIMEZONE_DATA_FILE) / 1024  # KB

    await message.answer(
        f"✅ **Downloaded timezone data**\n"
        f"File size: {file_size:.1f} KB\n\n"
        f"Building search index...",
        parse_mode="HTML",
    )

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


def _get_backup_menu_markup(tg_enabled: bool):
    """Build backup menu keyboard"""
    builder = InlineKeyboardBuilder()

    tg_toggle = (
        "🔴 Disable Telegram Backup" if tg_enabled else "🟢 Enable Telegram Backup"
    )
    tg_data = "backup:tg_disable" if tg_enabled else "backup:tg_enable"

    builder.button(text=tg_toggle, callback_data=tg_data)
    builder.button(text="📤 Send Backup Now", callback_data="backup:send")

    builder.adjust(1)
    return builder.as_markup()


@router.message(Command("backup"))
async def cmd_backup(message: Message, i18n: I18nContext):
    if not is_admin(message.from_user.id):
        await message.answer(i18n.get("admin-only"))
        return

    from infra.backup import (
        is_telegram_backup_enabled,
        get_classic_backup_info,
        is_classic_backup_enabled,
    )

    admin_id = message.from_user.id
    tg_enabled = is_telegram_backup_enabled(admin_id)
    classic_enabled = is_classic_backup_enabled()
    backups = get_classic_backup_info()

    text = "📦 <b>Backup Management</b>\n\n"

    # Classic backup status
    if classic_enabled:
        text += "<b>Classic Backups:</b> ON ✅\n"
        text += f"• Stored: {len(backups)} backup(s)\n"
        if backups:
            latest = backups[0]
            text += f"• Latest: {latest['filename']}\n"
            text += f"  Size: {latest['size_bytes'] / 1024:.1f} KB\n"
        text += "• Schedule: Thursday 2:00 AM UTC\n\n"
    else:
        text += "<b>Classic Backups:</b> OFF ⚪️\n"
        text += "• Disabled in config.py\n\n"

    # Telegram backup status
    text += "<b>Your Telegram Backup:</b>\n"
    text += f"• Status: {'✅ ON' if tg_enabled else '❌ OFF'}\n"
    text += "• Schedule: Sunday 2:00 AM UTC\n"
    if not tg_enabled:
        text += "• You won't receive automatic Telegram backups\n"

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=_get_backup_menu_markup(tg_enabled),
    )


@router.callback_query(lambda c: c.data.startswith("backup:"))
async def callback_backup_menu(callback: CallbackQuery, i18n: I18nContext):
    if not is_admin(callback.from_user.id):
        await callback.answer(i18n.get("admin-only"), show_alert=True)
        return

    action = callback.data.split(":")[1]
    admin_id = callback.from_user.id

    if action in ("tg_enable", "tg_disable"):
        from infra.backup import (
            set_telegram_backup_enabled,
            get_classic_backup_info,
            is_classic_backup_enabled,
        )

        tg_enabled = action == "tg_enable"
        set_telegram_backup_enabled(admin_id, tg_enabled)

        await callback.answer(
            f"Telegram backup {'enabled' if tg_enabled else 'disabled'}",
            show_alert=True,
        )

        # Update the menu
        classic_enabled = is_classic_backup_enabled()
        backups = get_classic_backup_info()

        text = "📦 <b>Backup Management</b>\n\n"

        # Classic backup status
        if classic_enabled:
            text += "<b>Classic Backups:</b> ON ✅\n"
            text += f"• Stored: {len(backups)} backup(s)\n"
            if backups:
                latest = backups[0]
                text += f"• Latest: {latest['filename']}\n"
                text += f"  Size: {latest['size_bytes'] / 1024:.1f} KB\n"
            text += "• Schedule: Thursday 2:00 AM UTC\n\n"
        else:
            text += "<b>Classic Backups:</b> OFF ⚪️\n"
            text += "• Disabled in config.py\n\n"

        # Telegram backup status
        text += "<b>Your Telegram Backup:</b>\n"
        text += f"• Status: {'✅ ON' if tg_enabled else '❌ OFF'}\n"
        text += "• Schedule: Sunday 2:00 AM UTC\n"
        if not tg_enabled:
            text += "• You won't receive automatic Telegram backups\n"

        await callback.message.edit_text(
            text,
            parse_mode="HTML",
            reply_markup=_get_backup_menu_markup(tg_enabled),
        )

    elif action == "send":
        from infra.backup import run_backup_now

        await callback.answer("Creating backup...", show_alert=False)

        try:
            success, result_message = await run_backup_now(callback.bot, admin_id)

            status_emoji = "✅" if success else "❌"
            await callback.message.answer(
                f"{status_emoji} <b>Backup Results</b>\n\n{result_message}",
                parse_mode="HTML",
            )

            logger.info(f"Admin {admin_id} triggered manual backup")

        except Exception as e:
            logger.error(f"Manual backup error: {e}")
            await callback.message.answer(
                "❌ <b>Backup failed</b>\n\nAn error occurred. Check logs for details.",
                parse_mode="HTML",
            )

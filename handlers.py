import logging
import math
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from datetime import datetime
from gpro_calendar import race_calendar, next_season_calendar, get_races_closing_soon, update_calendar
from notifications import get_user_status, mark_quali_done, reset_user_status

logger = logging.getLogger(__name__)
router = Router()


def format_full_calendar(calendar_data, title="Full Season", is_current_season=True):
    """Generic formatter for current/next season"""
    if not calendar_data:
        return "No races scheduled"

    now = datetime.utcnow()
    race_list = []
    
    # Collect races 1-17 in sequential order
    if isinstance(calendar_data, dict):
        for race_id in range(1, 18):
            if race_id in calendar_data and isinstance(calendar_data[race_id], dict):
                race_data = calendar_data[race_id].copy()
                race_data['race_id'] = race_id
                race_list.append(race_data)
    
    # 🔥 Next race ТОЛЬКО для current season
    next_race_id = None
    if is_current_season:
        for race in race_list:
            if race.get('quali_close', now) > now:
                next_race_id = race['race_id']
                break
    
    text = ""
    for race in race_list:
        track = race.get('track', f'Race {race["race_id"]}')
        race_date = race.get('date', now)
        quali_close = race.get('quali_close', now)
        race_id = race['race_id']
        
        date_str = race_date.strftime("%a %d.%m")
        time_text = format_time_until_quali(quali_close)
        
        time_info = date_str
        if time_text:
            time_info += f" • {time_text}"
        
        # 🔥 ONLY для current season next race
        if next_race_id and race_id == next_race_id:
            text += f"🔥 **#{race_id} {track}** - {time_info}\n"
        else:
            text += f"**#{race_id} {track}** - {time_info}\n"
    
    return text.rstrip()

def format_race_beautiful(race_data):
    if not race_data: return "None"

    track = race_data.get('track', 'Unknown')
    hours_left = race_data.get('hours_left', 0)
    quali_close = race_data.get('quali_close', datetime.utcnow())
    
    hours_display = math.floor(hours_left)
    deadline = quali_close.strftime("%d.%m %H:%M")
    
    return f"Qualification closes in {hours_display}h\n**({deadline})** - {track}"

def format_time_until_quali(quali_close):
    """Time remaining until quali deadline - human friendly"""
    now = datetime.utcnow()
    delta = quali_close - now
    
    total_minutes = delta.total_seconds() / 60
    if total_minutes <= 0:
        return ""
    
    total_hours = total_minutes / 60
    total_days = total_hours / 24
    
    if total_minutes < 100:  # Less than 100 minutes → show minutes or H:M
        hours = math.floor(total_minutes / 60)
        minutes = math.floor(total_minutes % 60)
        if hours > 0:
            return f"{hours}h{minutes}m"  # "2h45m"
        else:
            return f"{minutes}m"         # "45m"
    elif total_days >= 30:   # 30+ days → months + days
        months = math.floor(total_days / 30)
        remaining_days = math.floor(total_days % 30)
        if remaining_days > 0:
            return f"{months}mo {remaining_days}d"  # "1m 5d"
        else:
            return f"{months}mo"                   # "1m"
    elif total_hours >= 120:  # 5+ days → just days
        days = math.floor(total_hours / 24)
        return f"{days}d"
    elif total_hours >= 24:   # 1+ day → "1d 14h"
        days = math.floor(total_hours / 24)
        remaining_hours = math.floor(total_hours % 24)
        if remaining_hours > 0:
            return f"{days}d {remaining_hours}h"  # "1d 14h"
        else:
            return f"{days}d"                   # "1d"
    else:
        hours = math.floor(total_hours)
        return f"{hours}h"  # "23h"

@router.message(Command("start"))
async def cmd_start(message: Message):
    from notifications import get_user_status, users_data
    user_id = message.from_user.id
    
    # Check BEFORE adding
    was_new = user_id not in users_data
    get_user_status(user_id)
    
    if was_new:
        logger.info(f"🆕 NEW user {user_id} registered via /start")
    else:
        logger.debug(f"👤 Existing user {user_id} used /start")
    
    await message.answer("🏁 GPRO Bot LIVE!\n/status - Next race\n/calendar - Full season\n/next - Next season\n/notify - Test alert")

@router.message(Command("status"))
async def cmd_status(message: Message):
    status = get_user_status(message.from_user.id)
    races_soon = get_races_closing_soon()
    
    next_race = "No upcoming races"
    if races_soon:
        if isinstance(races_soon, dict) and races_soon:
            next_race = format_race_beautiful(list(races_soon.values())[0])
        elif isinstance(races_soon, list) and len(races_soon) > 0:
            next_race = format_race_beautiful(races_soon[0])
    
    status_text = ""
    if status.get('completed_quali'):
        race_num = status['completed_quali']
        status_text = f"✅ **Race {race_num} qualification done**\n*Next race notifications active*"
    else:
        status_text = "🔔 **Notifications active**"
    
    text = (
        f"🏁 **GPRO Status**\n\n"
        f"🎯 **Next race:**\n{next_race}\n\n"
        f"{status_text}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Reset notifications", callback_data="reset_all")]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode='Markdown')

@router.message(Command("notify"))
async def cmd_notify(message: Message, bot):
    from notifications import send_quali_notification
    
    if not race_calendar:
        await message.answer("🔔 No races scheduled")
        return
    
    # FIXED: Sort by quali_close time to get TRUE next race
    now = datetime.utcnow()
    future_races = []
    
    # Handle dict or list
    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict) and race_data.get('quali_close', now) > now:
                future_races.append((race_id, race_data))
    else:
        # List format fallback
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict) and race_data.get('quali_close', now) > now:
                race_id = race_data.get('race_id', i+1)
                future_races.append((race_id, race_data))
    
    # Sort by quali_close (earliest first)
    future_races.sort(key=lambda x: x[1].get('quali_close', now))
    
    if future_races:
        next_race_id, next_race_data = future_races[0]  # First = soonest
        await send_quali_notification(bot, message.from_user.id, next_race_id, next_race_data, "manual")
        logger.info(f"🔔 /notify sent for race {next_race_id} ({next_race_data.get('track', 'Unknown')}) to {message.from_user.id}")
    else:
        await message.answer("🔔 No upcoming qualifications")

@router.message(Command("calendar"))
async def cmd_calendar(message: Message):
    calendar_text = format_full_calendar(race_calendar, "Full Season", is_current_season=True)
    text = f"🏁 **Full Season**\n\n{calendar_text}"
    await message.answer(text, parse_mode='Markdown')

@router.message(Command("next"))
async def cmd_next(message: Message):
    from gpro_calendar import load_next_season_silent
    
    await load_next_season_silent()
    
    if not next_season_calendar:
        await message.answer("🌟 **Next season not published yet**")
        return
    
    calendar_text = format_full_calendar(next_season_calendar, "Next Season", is_current_season=False)
    text = f"🌟 **NEXT SEASON** ({len(next_season_calendar)} races)\n\n{calendar_text}"
    await message.answer(text, parse_mode='Markdown')

@router.message(Command("schedule"))
async def cmd_schedule(message: Message):
    await cmd_calendar(message)

@router.message(Command("update"))
async def cmd_update(message: Message):
    from config import ADMIN_USER_IDS
    from notifications import users_data, reset_user_status

    if message.from_user.id not in ADMIN_USER_IDS:
        await message.answer("❌ Admin only")
        return

    await update_calendar()

    reset_count = 0
    for user_id in list(users_data.keys()):
        reset_user_status(user_id)
        reset_count += 1

    # Current season status
    await message.answer(
        f"✅ **Calendar**: {len(race_calendar)} races\n"
        f"🔄 **{reset_count} users** reset",
        parse_mode="Markdown",
    )

    # Next season status (no file-removed text)
    if next_season_calendar:
        await message.answer(
            f"🌟 **Next season ready!** {len(next_season_calendar)} races\nUse /next to view",
            parse_mode="Markdown",
        )
    else:
        await message.answer(
            "ℹ️ **Next season not published**",
            parse_mode="Markdown",
        )

@router.message(Command("users"))
async def cmd_users(message: Message):
    from config import ADMIN_USER_IDS
    logger.debug(f"USERS - User: {message.from_user.id} ({type(message.from_user.id)}), Admins: {ADMIN_USER_IDS}")

    if message.from_user.id not in ADMIN_USER_IDS:
        logger.warning(f"USERS: Access denied for user {message.from_user.id}")
        await message.answer("❌ Admin only")
        return

    logger.info("USERS: Admin access granted")

    try:
        from notifications import users_data
        logger.info(f"USERS: Loaded {len(users_data)} users from notifications")

        if not users_data:
            await message.answer("📊 **0 users** in database", parse_mode='Markdown')
            return

        text = f"📊 **{len(users_data)} users**:\n\n"
        for uid, status in users_data.items():
            quali = status.get("completed_quali", "None")
            text += f"• `{uid}`: Race {quali}\n"

        await message.answer(text, parse_mode='Markdown')

    except Exception as e:
        logger.error(f"USERS ERROR: {e}")
        await message.answer("❌ Error loading user data", parse_mode='Markdown')

@router.callback_query(F.data.startswith("done_"))
async def handle_quali_done(callback: CallbackQuery):
    race_id = int(callback.data.split("_")[1])
    mark_quali_done(callback.from_user.id, race_id)
    await callback.message.edit_text(callback.message.text + "\n\n✅ *Race marked done!*")
    await callback.answer("✅ Done!")

@router.callback_query(F.data.startswith("reset_"))
async def handle_reset(callback: CallbackQuery):
    if callback.data == "reset_all":
        reset_user_status(callback.from_user.id)
        await callback.message.edit_text(callback.message.text + "\n\n🔄 *Notifications reset!*")
        await callback.answer("🔄 Reset!")
    else:
        # reset_{race_id} format
        race_id = int(callback.data.split("_")[1])
        reset_user_status(callback.from_user.id)
        await callback.message.edit_text(callback.message.text + "\n\n🔄 *Notifications re-enabled!*")
        await callback.answer("🔄 Re-enabled!")

logger.info("✅ handlers.py loaded - Aiogram 3.x Router ready (/next added)")

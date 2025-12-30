import asyncio
import logging
import json
import os
from typing import Dict
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from gpro_calendar import get_races_closing_soon, race_calendar
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

users_data: Dict[int, Dict] = {}
USERS_FILE = 'users_data.json'

def load_users_data():
    global users_data
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                raw_data = json.load(f)
                # TYPE FIX: Convert string keys → int keys
                clean_data = {int(k_str): status for k_str, status in raw_data.items()}
                users_data.update(clean_data)
                logger.info(f"✅ Loaded {len(users_data)} users (int keys)")
        except Exception as e:
            logger.error(f"Load failed: {e}")

def save_users_data():
    try:
        with open(USERS_FILE, 'w') as f:
            # TYPE FIX: Convert int keys → string for JSON
            save_data = {str(k): v for k, v in users_data.items()}
            json.dump(save_data, f, indent=2)
        logger.debug(f"Saved {len(users_data)} users")
    except Exception as e:
        logger.error(f"Save failed: {e}")

def get_user_status(user_id: int) -> Dict:
    global users_data
    logger.info(f"🔍 DEBUG get_user_status({user_id}): users_data.keys() = {list(users_data.keys())} (len={len(users_data)})")
    
    if not users_data:
        load_users_data()
        logger.info(f"🔍 AFTER load_users_data(): users_data.keys() = {list(users_data.keys())}")
    
    if user_id not in users_data:
        logger.warning(f"🚨 ADDING NEW user {user_id} - NOT FOUND in {list(users_data.keys())}")
        users_data[user_id] = {'completed_quali': None}
        save_users_data()
        logger.info(f"🆕 TRULY NEW user {user_id} added")
    else:
        logger.info(f"✅ User {user_id} EXISTS - no add")
    
    return users_data[user_id]

async def send_quali_notification(bot: Bot, user_id: int, race_id: int, race_data: Dict, notification_type: str = "deadline"):
    user_status = get_user_status(user_id)

    # Skip automatic notifications if user marked quali done
    if user_status.get('completed_quali') == race_id and notification_type != "manual":
        return

    track = race_data['track']
    race_date = race_data['date']
    quali_close = race_data['quali_close']

    if notification_type == "opens_soon":
        emoji = "🆕"
        title = "**Quali is open (or is opening soon)**"
        deadline = quali_close.strftime("%d.%m %H:%M UTC")
        race_time = race_date.strftime('%d.%m %H:%M UTC')
    else:
        now = datetime.utcnow()
        if 'hours_left' not in race_data:
            hours_left = (quali_close - now).total_seconds() / 3600
        else:
            hours_left = race_data['hours_left']
        
        if hours_left >= 24:
            time_text = f"{int(hours_left)}h"; emoji = "🔔"
        elif hours_left >= 2:
            time_text = f"{int(hours_left)}h"; emoji = "⏰"
        elif hours_left >= 0.333:
            time_text = "10min"; emoji = "⚠️"
        else:
            time_text = f"{int(hours_left*60)}min"; emoji = "🚨"

        deadline = quali_close.strftime("%d.%m %H:%M UTC")
        race_time = race_date.strftime('%d.%m %H:%M UTC')
        title = f"**Quali closes in {time_text}!**"

    # Check if user already marked this race done
    is_marked_done = user_status.get('completed_quali') == race_id

    if is_marked_done:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Reset Status", callback_data=f"reset_{race_id}")]
        ])
        message = (
            f"{emoji} {title}\n\n"
            f"🏁 **Race #{race_id}**\n"
            f"📍 **{track}**\n"
            f"📅 **Quali: {deadline} | Race: {race_time}**\n\n"
            f"ℹ️ **Automatic notifications disabled** for this race\n"
            f"Click button to re-enable notifications"
        )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Quali Done", callback_data=f"done_{race_id}")]
        ])
        message = (
            f"{emoji} {title}\n\n"
            f"🏁 **Race #{race_id}**\n"
            f"📍 **{track}**\n"
            f"📅 **Quali: {deadline} | Race: {race_time}**\n\n"
            f"Click button to disable notifications for this race"
        )

    try:
        await bot.send_message(user_id, message, reply_markup=keyboard, parse_mode='Markdown')
        logger.info(f"✅ Sent {notification_type} to {user_id} for race {race_id}")
    except Exception as e:
        logger.error(f"Notify {user_id} failed: {e}")

notification_lock = asyncio.Lock()
notify_history = {}  # {(race_id, window): sent_timestamp}

async def check_notifications(bot: Bot):
    """Continuous notification loop - checks every 5 minutes"""
    global notify_history
    logger.info("🔔 Starting notification checker (5min interval)")
    load_users_data()

    while True:
        try:
            async with notification_lock:
                now = datetime.utcnow()

                # 1. Check races closing within 48 hours
                races_closing = get_races_closing_soon(48)

                for race_id, race_data in races_closing.items():
                    quali_close = race_data['quali_close']

                    # Check each notification window
                    windows = [
                        (48, 6, "48h"),   # 48h ±6min
                        (24, 6, "24h"),   # 24h ±6min
                        (2, 5, "2h"),     # 2h ±5min
                        (10/60, 2, "10min")  # 10min ±2min
                    ]

                    for hours_before, tolerance_min, label in windows:
                        time_until = (quali_close - now).total_seconds() / 3600
                        target_hours = hours_before
                        tolerance_hours = tolerance_min / 60

                        # Check if we're in the notification window
                        if abs(time_until - target_hours) <= tolerance_hours:
                            history_key = (race_id, label)

                            # Only send if not sent before
                            if history_key not in notify_history:
                                logger.info(f"🔔 Sending {label} notification for race {race_id}")
                                for user_id in list(users_data.keys()):
                                    await send_quali_notification(bot, user_id, race_id, race_data, label)

                                notify_history[history_key] = now
                                logger.info(f"✅ Sent {label} for race {race_id} to {len(users_data)} users")

                # 2. Check "quali is open" notifications (2.5h after race time)
                for race_id, race_data in race_calendar.items():
                    race_time = race_data['date']
                    opens_time = race_time + timedelta(hours=2.5)
                    time_since_opens = (now - opens_time).total_seconds() / 60

                    # Send if we're 2.4-2.6h after race (±6min window)
                    if 0 <= time_since_opens <= 12:
                        history_key = (race_id, "opens_soon")

                        if history_key not in notify_history:
                            logger.info(f"🆕 Sending 'quali open' notification for race {race_id}")
                            for user_id in list(users_data.keys()):
                                await send_quali_notification(bot, user_id, race_id, race_data, "opens_soon")

                            notify_history[history_key] = now
                            logger.info(f"✅ Sent 'opens_soon' for race {race_id}")

                # Clean old history entries (keep last 30 days)
                cutoff = now - timedelta(days=30)
                notify_history = {k: v for k, v in notify_history.items() if v > cutoff}

        except Exception as e:
            logger.error(f"❌ Notification check error: {e}")

        # Wait 5 minutes before next check
        await asyncio.sleep(300)

def mark_quali_done(user_id: int, race_id: int):
    get_user_status(user_id)
    users_data[user_id]['completed_quali'] = race_id
    save_users_data()
    logger.info(f"User {user_id} marked race {race_id} done")

def reset_user_status(user_id: int):
    if user_id in users_data:
        users_data[user_id]['completed_quali'] = None
        save_users_data()
        logger.info(f"User {user_id} reset")

load_users_data()

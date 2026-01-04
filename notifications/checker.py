"""Main notification checking loop and helper functions"""

import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot

from gpro_calendar import (
    get_races_closing_soon,
    race_calendar,
    check_quali_status_from_api,
    fetch_weather_from_api,
)
from .user_data import users_data, is_notification_enabled, load_users_data
from .sender import (
    send_quali_notification,
    send_race_live_notification,
    send_race_replay_notification,
    send_race_results_notification,
)

logger = logging.getLogger(__name__)

# Notification windows: (hours_before, tolerance_minutes, label)
NOTIFICATION_WINDOWS = [
    (48, 15, "48h"),  # 48h ±15min (wider tolerance for >36h notifications)
    (24, 10, "24h"),  # 24h ±10min (optimized tolerance)
    (2, 5, "2h"),  # 2h ±5min
    (10 / 60, 2, "10min"),  # 10min ±2min
]

# Additional notification for Tuesday races (more time between races)
TUESDAY_NOTIFICATION = (
    72,
    15,
    "72h",
)  # 72h ±15min (wider tolerance for far-advance notifications)

# Timing constants
CHECK_INTERVAL_NORMAL_SECONDS = 300  # 5 minutes between checks (normal)
CHECK_INTERVAL_FAST_SECONDS = 60  # 1 minute between checks (when race approaching)
RACE_PROXIMITY_THRESHOLD_MINUTES = 10  # Switch to fast checks when race is within 10min
RACE_LIVE_NOTIFICATION_BEFORE_MINUTES = (
    1  # Send race live notification up to 1min before race
)
RACE_LIVE_NOTIFICATION_AFTER_MINUTES = (
    5  # Allow up to 5min after race start (just in case)
)
NOTIFICATION_HISTORY_RETENTION_DAYS = 30  # Keep notification history for 30 days

# API polling configuration for quali opening detection
API_CHECK_START_HOURS = 2  # Start checking API 2 hours after race
API_CHECK_END_HOURS = 3.5  # Stop checking and send fallback at 3.5 hours
API_CHECK_INTERVAL_MINUTES = 10  # Check API every 10 minutes
FALLBACK_TOLERANCE_MINUTES = 15  # Send fallback within 15min of reaching 3.5h

# Custom notification tolerance
CUSTOM_NOTIF_TOLERANCE_MIN = 5  # ±5 minutes tolerance for custom notifications

notification_lock = asyncio.Lock()
notify_history = {}  # {(race_id, window): sent_timestamp}
last_api_check_time = None  # Track last API check to limit calls


def _is_tuesday_race(race_data: dict) -> bool:
    """Check if a race is on Tuesday (weekday 1)

    Args:
        race_data: Race data dict with 'date' field

    Returns:
        bool: True if race is on Tuesday
    """
    race_date = race_data["date"]
    return race_date.weekday() == 1  # 0=Monday, 1=Tuesday, etc.


def _check_quali_closing_notifications(now: datetime) -> list:
    """Check for races with qualifying closing soon

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []
    races_closing = get_races_closing_soon(72)  # Extended to 72h for Tuesday races

    for race_id, race_data in races_closing.items():
        quali_close = race_data["quali_close"]

        # Check each preset notification window
        for hours_before, tolerance_min, label in NOTIFICATION_WINDOWS:
            time_until = (quali_close - now).total_seconds() / 3600
            target_hours = hours_before
            tolerance_hours = tolerance_min / 60

            # Check if we're in the notification window
            if abs(time_until - target_hours) <= tolerance_hours:
                history_key = (race_id, label)

                # Only send if not sent before
                if history_key not in notify_history:
                    notifications.append(
                        ("quali", race_id, race_data, label, history_key)
                    )

        # Check 72h notification for Tuesday races only
        if _is_tuesday_race(race_data):
            hours_before, tolerance_min, label = TUESDAY_NOTIFICATION
            time_until = (quali_close - now).total_seconds() / 3600
            target_hours = hours_before
            tolerance_hours = tolerance_min / 60

            if abs(time_until - target_hours) <= tolerance_hours:
                history_key = (race_id, label)

                if history_key not in notify_history:
                    notifications.append(
                        ("quali", race_id, race_data, label, history_key)
                    )

    return notifications


def _check_custom_notifications(now: datetime) -> list:
    """Check for custom notification times

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key, user_id), ...]
    """
    notifications = []
    races_closing = get_races_closing_soon(
        72
    )  # Check up to 72 hours (max custom time + buffer)

    # Check each user's custom notifications
    for user_id, user_data in users_data.items():
        custom_notifs = user_data.get("custom_notifications", [])

        for slot_idx, custom_notif in enumerate(custom_notifs):
            if not custom_notif.get("enabled", False):
                continue

            hours_before = custom_notif.get("hours_before")
            if hours_before is None:
                continue

            # Check each race
            for race_id, race_data in races_closing.items():
                quali_close = race_data["quali_close"]
                time_until = (quali_close - now).total_seconds() / 3600

                # Check if we're within the custom notification window
                tolerance_hours = CUSTOM_NOTIF_TOLERANCE_MIN / 60
                if abs(time_until - hours_before) <= tolerance_hours:
                    # Create unique history key for this user+race+custom slot
                    label = f"custom_{slot_idx+1}"
                    history_key = (user_id, race_id, label)

                    # Only send if not sent before
                    if history_key not in notify_history:
                        notifications.append(
                            ("custom", race_id, race_data, label, history_key, user_id)
                        )

    return notifications


async def _check_quali_open_notifications(now: datetime) -> list:
    """Check for qualifications that just opened using API when appropriate

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    global last_api_check_time
    notifications = []

    # Determine if we should check the API
    should_check_api = False
    races_in_polling_window = []
    races_for_fallback = []

    for race_id, race_data in race_calendar.items():
        # Skip race 1 (no previous race)
        if race_id == 1:
            continue

        # Check if already notified
        history_key = (race_id, "opens_soon")
        if history_key in notify_history:
            continue

        # Find previous race
        prev_race_id = race_id - 1
        if prev_race_id not in race_calendar:
            continue

        prev_race_time = race_calendar[prev_race_id]["date"]
        hours_since_race = (now - prev_race_time).total_seconds() / 3600

        # Check if we're in the API polling window (2-3.5 hours after race)
        if API_CHECK_START_HOURS <= hours_since_race <= API_CHECK_END_HOURS:
            races_in_polling_window.append(
                (race_id, race_data, prev_race_id, hours_since_race)
            )
            should_check_api = True
        # Check if we've reached fallback time (3.5 hours, within tolerance)
        elif hours_since_race > API_CHECK_END_HOURS:
            minutes_since_fallback = (hours_since_race - API_CHECK_END_HOURS) * 60
            if minutes_since_fallback <= FALLBACK_TOLERANCE_MINUTES:
                races_for_fallback.append(
                    (race_id, race_data, prev_race_id, hours_since_race)
                )

    # Check API if needed (rate limited to every 10 minutes)
    api_result = {}
    if should_check_api:
        # Only call API every 10 minutes
        if (
            last_api_check_time is None
            or (now - last_api_check_time).total_seconds()
            >= API_CHECK_INTERVAL_MINUTES * 60
        ):
            logger.info(
                f"🔍 Checking API for quali open status ({len(races_in_polling_window)} races in window)"
            )
            api_result = await check_quali_status_from_api()
            last_api_check_time = now
        else:
            time_until_next = (
                API_CHECK_INTERVAL_MINUTES * 60
                - (now - last_api_check_time).total_seconds()
            )
            logger.debug(f"API check skipped (next in {int(time_until_next)}s)")

    # Process results from API
    for race_id, race_data, prev_race_id, hours_since in races_in_polling_window:
        if race_id in api_result:
            # API confirmed quali is open!
            logger.info(f"🆕 API confirmed: Race {race_id} quali opened!")

            # Fetch weather data with retry (if not already fetched)
            if "weather" not in race_calendar[race_id]:
                weather_data = await fetch_weather_from_api(race_id)

                # Retry once if failed
                if not weather_data:
                    logger.warning(
                        f"Weather fetch failed for race {race_id}, retrying in 5s..."
                    )
                    await asyncio.sleep(5)
                    weather_data = await fetch_weather_from_api(race_id)

                    if not weather_data:
                        logger.error(
                            f"Weather fetch failed after retry for race {race_id}"
                        )
                    else:
                        logger.info(
                            f"Weather fetch succeeded on retry for race {race_id}"
                        )
            else:
                logger.debug(f"Weather data already cached for race {race_id}")

            history_key = (race_id, "opens_soon")
            notifications.append(
                ("opens", race_id, race_data, "opens_soon", history_key)
            )

            # Also send race replay notification for the previous race
            replay_history_key = (prev_race_id, "race_replay")
            if replay_history_key not in notify_history:
                prev_race_data = race_calendar[prev_race_id]
                notifications.append(
                    (
                        "replay",
                        prev_race_id,
                        prev_race_data,
                        "race_replay",
                        replay_history_key,
                    )
                )

            # Also send race results notification for the previous race
            results_history_key = (prev_race_id, "race_results")
            if results_history_key not in notify_history:
                prev_race_data = race_calendar[prev_race_id]
                notifications.append(
                    (
                        "results",
                        prev_race_id,
                        prev_race_data,
                        "race_results",
                        results_history_key,
                    )
                )

    # Fallback: Send notification if we've reached 3.5h without API detection
    for race_id, race_data, prev_race_id, hours_since in races_for_fallback:
        logger.info(
            f"⏰ Fallback: Sending quali open for race {race_id} at {hours_since:.1f}h (API didn't detect)"
        )

        # Fetch weather data with retry (if not already fetched)
        if "weather" not in race_calendar[race_id]:
            weather_data = await fetch_weather_from_api(race_id)

            # Retry once if failed
            if not weather_data:
                logger.warning(
                    f"Weather fetch failed for race {race_id}, retrying in 5s..."
                )
                await asyncio.sleep(5)
                weather_data = await fetch_weather_from_api(race_id)

                if not weather_data:
                    logger.error(f"Weather fetch failed after retry for race {race_id}")
                else:
                    logger.info(f"Weather fetch succeeded on retry for race {race_id}")
        else:
            logger.debug(f"Weather data already cached for race {race_id}")

        history_key = (race_id, "opens_soon")
        notifications.append(("opens", race_id, race_data, "opens_soon", history_key))

        # Also send race replay notification for the previous race
        replay_history_key = (prev_race_id, "race_replay")
        if replay_history_key not in notify_history:
            prev_race_data = race_calendar[prev_race_id]
            notifications.append(
                (
                    "replay",
                    prev_race_id,
                    prev_race_data,
                    "race_replay",
                    replay_history_key,
                )
            )

        # Also send race results notification for the previous race
        results_history_key = (prev_race_id, "race_results")
        if results_history_key not in notify_history:
            prev_race_data = race_calendar[prev_race_id]
            notifications.append(
                (
                    "results",
                    prev_race_id,
                    prev_race_data,
                    "race_results",
                    results_history_key,
                )
            )

    return notifications


def _check_race_live_notifications(now: datetime) -> list:
    """Check for races that are about to start or just started

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for race_id, race_data in race_calendar.items():
        race_time = race_data["date"]
        time_since_race = (now - race_time).total_seconds() / 60

        # Send if we're within window: 5min before to 2min after race starts
        # This ensures notification is sent early (at 18:55 check for 19:00 race)
        if (
            -RACE_LIVE_NOTIFICATION_BEFORE_MINUTES
            <= time_since_race
            <= RACE_LIVE_NOTIFICATION_AFTER_MINUTES
        ):
            history_key = (race_id, "race_live")
            if history_key not in notify_history:
                notifications.append(
                    ("live", race_id, race_data, "race_live", history_key)
                )

    return notifications


async def _send_notifications_to_users(bot: Bot, notifications_to_send: list):
    """Send notifications to all eligible users

    Args:
        bot: Telegram bot instance
        notifications_to_send: List of notifications [(type, race_id, race_data, label, history_key, [user_id]), ...]
    """
    for notification_data in notifications_to_send:
        # Handle both formats: regular (5 items) and custom (6 items with user_id)
        if len(notification_data) == 6:
            notif_type, race_id, race_data, label, history_key, target_user_id = (
                notification_data
            )
            is_custom = True
        else:
            notif_type, race_id, race_data, label, history_key = notification_data
            target_user_id = None
            is_custom = False

        logger.info(f"🔔 Sending {label} notification for race {race_id}")
        sent_count = 0
        total_users = len(users_data)

        # For custom notifications, send to specific user only
        if is_custom:
            try:
                # Custom notifications are always quali-type
                await send_quali_notification(
                    bot, target_user_id, race_id, race_data, label
                )
                sent_count = 1
                logger.info(
                    f"✅ Sent custom notification ({label}) for race {race_id} to user {target_user_id}"
                )
            except Exception as e:
                logger.error(
                    f"Failed to send custom {label} to user {target_user_id}: {e}"
                )
        else:
            # Regular notifications - send to all users with that notification enabled
            for user_id in users_data:
                if is_notification_enabled(user_id, label):
                    try:
                        if notif_type == "quali" or notif_type == "opens":
                            await send_quali_notification(
                                bot, user_id, race_id, race_data, label
                            )
                        elif notif_type == "replay":
                            await send_race_replay_notification(
                                bot, user_id, race_id, race_data
                            )
                        elif notif_type == "live":
                            await send_race_live_notification(
                                bot, user_id, race_id, race_data
                            )
                        elif notif_type == "results":
                            await send_race_results_notification(
                                bot, user_id, race_id, race_data
                            )
                        sent_count += 1
                    except Exception as e:
                        logger.error(f"Failed to send {label} to user {user_id}: {e}")

            logger.info(
                f"✅ Sent {label} for race {race_id} to {sent_count}/{total_users} users"
            )

        # Update history after sending (re-acquire lock briefly)
        async with notification_lock:
            notify_history[history_key] = datetime.utcnow()


def _get_next_check_interval(now: datetime) -> int:
    """Determine next check interval based on proximity to upcoming races

    Returns faster checks when race is approaching for better timing precision.

    Returns:
        int: Seconds until next check
    """
    # Check if any race is approaching
    for race_id, race_data in race_calendar.items():
        race_time = race_data["date"]
        minutes_until_race = (race_time - now).total_seconds() / 60

        # If race is within threshold, use fast checking
        if (
            -RACE_LIVE_NOTIFICATION_AFTER_MINUTES
            <= minutes_until_race
            <= RACE_PROXIMITY_THRESHOLD_MINUTES
        ):
            return CHECK_INTERVAL_FAST_SECONDS

    # Default to normal interval
    return CHECK_INTERVAL_NORMAL_SECONDS


async def check_notifications(bot: Bot):
    """Continuous notification loop - adaptive check interval based on race proximity"""
    global notify_history
    logger.info(
        f"🔔 Starting notification checker (adaptive: {CHECK_INTERVAL_NORMAL_SECONDS//60}min normal, {CHECK_INTERVAL_FAST_SECONDS}s when race approaching)"
    )
    load_users_data()

    while True:
        try:
            # Determine what notifications to send (quick check under lock)
            async with notification_lock:
                now = datetime.utcnow()

                # Check all notification types
                notifications_to_send = []
                notifications_to_send.extend(_check_quali_closing_notifications(now))
                notifications_to_send.extend(await _check_quali_open_notifications(now))
                notifications_to_send.extend(_check_race_live_notifications(now))
                notifications_to_send.extend(_check_custom_notifications(now))

                # Clean old history entries
                cutoff = now - timedelta(days=NOTIFICATION_HISTORY_RETENTION_DAYS)
                notify_history = {k: v for k, v in notify_history.items() if v > cutoff}

                # Determine next check interval based on race proximity
                next_interval = _get_next_check_interval(now)

            # Send notifications outside the lock (slow operation)
            await _send_notifications_to_users(bot, notifications_to_send)

        except Exception as e:
            logger.error(f"❌ Notification check error: {e}")
            next_interval = CHECK_INTERVAL_NORMAL_SECONDS  # Fallback on error

        # Wait before next check (adaptive interval)
        await asyncio.sleep(next_interval)

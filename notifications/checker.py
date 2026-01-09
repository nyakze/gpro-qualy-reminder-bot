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
    should_trigger_season_transition,
    should_prefetch_next_season,
    transition_to_next_season,
    update_calendar,
)
from .user_data import users_data, is_notification_enabled, load_users_data, save_users_data
from .sender import (
    send_quali_notification,
    send_race_live_notification,
    send_race_replay_notification,
    send_race_results_notification,
    send_quali_results_notification,
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
QUALI_RESULTS_NOTIFICATION_AFTER_MINUTES = (
    10  # Send quali results notification up to 10min after quali closes
)
NOTIFICATION_HISTORY_RETENTION_DAYS = 30  # Keep notification history for 30 days

# API polling configuration for quali opening detection
API_CHECK_START_HOURS = 1.68  # Start checking API 1h41m (101 minutes) after race
API_CHECK_END_HOURS = 3.5  # Stop checking and send fallback at 3.5 hours
API_CHECK_INTERVAL_MINUTES = 10  # Check API every 10 minutes
FALLBACK_TOLERANCE_MINUTES = 15  # Send fallback within 15min of reaching 3.5h

# Custom notification tolerance
CUSTOM_NOTIF_TOLERANCE_MIN = 5  # ±5 minutes tolerance for custom notifications

# Season transition tracking
last_season_transition_check = None
last_prefetch_check = None
SEASON_CHECK_INTERVAL_HOURS = 1  # Check season transition conditions every hour

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


def _check_quali_closing_notifications(now: datetime, races_closing: dict) -> list:
    """Check for races with qualifying closing soon

    Args:
        now: Current datetime
        races_closing: Pre-fetched dict of upcoming races

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

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


def _check_custom_notifications(now: datetime, races_closing: dict) -> list:
    """Check for custom notification times

    Args:
        now: Current datetime
        races_closing: Pre-fetched dict of upcoming races

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key, user_id), ...]
    """
    notifications = []

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


async def _fetch_weather_with_retry(race_id: int) -> None:
    """Fetch weather data for a race with retry logic

    Args:
        race_id: The race ID to fetch weather for
    """
    if "weather" in race_calendar[race_id]:
        logger.debug(f"Weather data already cached for race {race_id}")
        return

    weather_data = await fetch_weather_from_api(race_id)

    # Retry once if failed
    if not weather_data:
        logger.warning(f"Weather fetch failed for race {race_id}, retrying in 5s...")
        await asyncio.sleep(5)
        weather_data = await fetch_weather_from_api(race_id)

        if not weather_data:
            logger.error(f"Weather fetch failed after retry for race {race_id}")
        else:
            logger.info(f"Weather fetch succeeded on retry for race {race_id}")


def _add_replay_and_results_notifications(
    notifications: list, prev_race_id: int
) -> None:
    """Add replay and results notifications for a previous race

    Args:
        notifications: List to append notifications to
        prev_race_id: ID of the previous race
    """
    # Add race replay notification
    replay_history_key = (prev_race_id, "race_replay")
    if replay_history_key not in notify_history:
        prev_race_data = race_calendar[prev_race_id]
        notifications.append(
            ("replay", prev_race_id, prev_race_data, "race_replay", replay_history_key)
        )

    # Add race results notification
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


def _get_races_for_polling(now: datetime) -> list:
    """Get races that are in the API polling window (2-3.5 hours after previous race)

    Args:
        now: Current datetime

    Returns:
        list: Races to check via API [(race_id, race_data, prev_race_id, hours_since), ...]
    """
    races = []

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

        # Check if we're in the API polling window
        if API_CHECK_START_HOURS <= hours_since_race <= API_CHECK_END_HOURS:
            races.append((race_id, race_data, prev_race_id, hours_since_race))

    return races


def _get_races_for_fallback(now: datetime) -> list:
    """Get races that have reached fallback time (3.5 hours after previous race)

    Args:
        now: Current datetime

    Returns:
        list: Races for fallback notification [(race_id, race_data, prev_race_id, hours_since), ...]
    """
    races = []

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

        # Check if we've reached fallback time (within tolerance)
        if hours_since_race > API_CHECK_END_HOURS:
            minutes_since_fallback = (hours_since_race - API_CHECK_END_HOURS) * 60
            if minutes_since_fallback <= FALLBACK_TOLERANCE_MINUTES:
                races.append((race_id, race_data, prev_race_id, hours_since_race))

    return races


async def _check_quali_open_notifications(now: datetime) -> list:
    """Check for qualifications that just opened using API when appropriate

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    global last_api_check_time
    notifications = []

    # Get races to check via API and races for fallback
    races_in_polling_window = _get_races_for_polling(now)
    races_for_fallback = _get_races_for_fallback(now)

    # Check API if we have races in polling window (rate limited to every 10 minutes)
    api_result = {}
    if races_in_polling_window:
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

    # Process API-confirmed races
    for race_id, race_data, prev_race_id, hours_since in races_in_polling_window:
        if race_id in api_result:
            logger.info(f"🆕 API confirmed: Race {race_id} quali opened!")

            # Fetch weather data with retry
            await _fetch_weather_with_retry(race_id)

            # Add replay and results notifications for previous race FIRST
            _add_replay_and_results_notifications(notifications, prev_race_id)

            # Add quali open notification AFTER replay and results
            history_key = (race_id, "opens_soon")
            notifications.append(
                ("opens", race_id, race_data, "opens_soon", history_key)
            )

    # Process fallback races (3.5h without API detection)
    for race_id, race_data, prev_race_id, hours_since in races_for_fallback:
        logger.info(
            f"⏰ Fallback: Sending quali open for race {race_id} at {hours_since:.1f}h (API didn't detect)"
        )

        # Fetch weather data with retry
        await _fetch_weather_with_retry(race_id)

        # Add replay and results notifications for previous race FIRST
        _add_replay_and_results_notifications(notifications, prev_race_id)

        # Add quali open notification AFTER replay and results
        history_key = (race_id, "opens_soon")
        notifications.append(("opens", race_id, race_data, "opens_soon", history_key))

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


def _check_quali_results_notifications(now: datetime) -> list:
    """Check for qualifying results that should be sent after quali deadline

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    notifications = []

    for race_id, race_data in race_calendar.items():
        quali_close = race_data["quali_close"]
        time_since_quali_close = (now - quali_close).total_seconds() / 60

        # Send if qualifying has closed (within 10min window after closing)
        # This ensures we send after deadline has passed but not too late
        if 0 <= time_since_quali_close <= QUALI_RESULTS_NOTIFICATION_AFTER_MINUTES:
            history_key = (race_id, "quali_results")
            if history_key not in notify_history:
                notifications.append(
                    ("quali_results", race_id, race_data, "quali_results", history_key)
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
            # Use list() to avoid "dictionary changed size during iteration" error
            for user_id in list(users_data):
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
                        elif notif_type == "quali_results":
                            await send_quali_results_notification(
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


def _cleanup_completed_quali_for_all_users() -> None:
    """Reset completed_quali to empty array for all users
    
    This is called during season transition to clean up old quali data.
    """
    logger.info("🧹 Cleaning up completed_quali for all users...")
    
    for user_id in users_data:
        users_data[user_id]["completed_quali"] = []
    
    save_users_data()
    logger.info(f"✅ Cleaned completed_quali for {len(users_data)} users")


async def _check_season_transition(now: datetime) -> None:
    """Check and handle season transition conditions
    
    Args:
        now: Current datetime
    """
    global last_season_transition_check, last_prefetch_check
    
    # Season transition check (after last race concludes)
    if should_trigger_season_transition(now):
        logger.info("🔄 Season transition triggered!")
        
        # Perform transition
        success = await transition_to_next_season()
        
        if success:
            # Clean up user data
            _cleanup_completed_quali_for_all_users()
            
            # Mark as checked to avoid repeated transitions
            last_season_transition_check = now
            logger.info("🎉 Season transition completed successfully!")
        else:
            logger.error("❌ Season transition failed")
    
    # Prefetch check (4 days before first race)
    # Only check every hour to avoid excessive checks
    if (
        last_prefetch_check is None
        or (now - last_prefetch_check).total_seconds() >= SEASON_CHECK_INTERVAL_HOURS * 3600
    ):
        if should_prefetch_next_season(now):
            logger.info("📅 Pre-fetching next season calendar...")
            
            # Fetch calendar from API
            success = await update_calendar()
            
            if success:
                logger.info("✅ Next season calendar pre-fetched successfully!")
            else:
                logger.error("❌ Failed to pre-fetch next season calendar")
        
        last_prefetch_check = now


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

                # Check season transition conditions
                await _check_season_transition(now)

                # Fetch upcoming races once for efficiency (used by multiple checks)
                races_closing = get_races_closing_soon(
                    72
                )  # Extended to 72h for Tuesday races

                # Check all notification types
                notifications_to_send = []
                notifications_to_send.extend(
                    _check_quali_closing_notifications(now, races_closing)
                )
                notifications_to_send.extend(await _check_quali_open_notifications(now))
                notifications_to_send.extend(_check_quali_results_notifications(now))
                notifications_to_send.extend(_check_race_live_notifications(now))
                notifications_to_send.extend(
                    _check_custom_notifications(now, races_closing)
                )

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

"""Season-related notification checks and utilities"""

import logging
from datetime import datetime
from typing import List, Tuple

from gpro_calendar import (
    should_trigger_season_transition,
    should_prefetch_next_season,
    transition_to_next_season,
    update_calendar,
    fetch_weather_from_api,
    race_calendar,
)
from notifications.history import is_already_notified

logger = logging.getLogger(__name__)

# Track last check times
last_season_transition_check = None
last_prefetch_check = None
SEASON_CHECK_INTERVAL_HOURS = 1  # Check season transition conditions every hour


def _cleanup_completed_quali_for_all_users() -> None:
    """Clean up completed quali data for all users after season transition.

    This is called during season transition to clean up old quali data.
    """
    from notifications.users import users_data, save_users_data

    cleaned_count = 0
    for user_id, user_data in users_data.items():
        if "completed_quali" in user_data:
            del user_data["completed_quali"]
            cleaned_count += 1

    if cleaned_count > 0:
        save_users_data()
        logger.info(f"Cleaned up completed_quali data for {cleaned_count} users")


async def check_season_transition(now: datetime) -> None:
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
        or (now - last_prefetch_check).total_seconds()
        >= SEASON_CHECK_INTERVAL_HOURS * 3600
    ):
        if should_prefetch_next_season(now):
            logger.info("📅 Pre-fetching next season calendar...")

            # Fetch calendar from API
            success = await update_calendar()

            if success:
                logger.info("✅ Next season calendar pre-fetched successfully!")

                # Also fetch weather for Race 1 (it won't be auto-fetched later)
                if 1 in race_calendar:
                    logger.info("🌤️ Fetching weather for Race 1...")
                    weather_data = await fetch_weather_from_api(1)
                    if weather_data:
                        logger.info("✅ Race 1 weather fetched successfully")
                    else:
                        logger.warning(
                            "⚠️ Race 1 weather not available yet (may need retry later)"
                        )
            else:
                logger.error("❌ Failed to pre-fetch next season calendar")

        last_prefetch_check = now


def check_new_season_reminder(now: datetime) -> List[Tuple]:
    """Check for new season reminder notifications (1-2 days before first race)

    Returns:
        list: Notifications to send [(type, race_id, race_data, label, history_key), ...]
    """
    from gpro_calendar import get_first_race_date, next_season_calendar

    notifications = []

    # Check if we have a next season calendar (meaning new season is coming)
    if not next_season_calendar:
        return notifications

    first_race_date = get_first_race_date()
    if not first_race_date:
        return notifications

    days_until = (first_race_date - now).total_seconds() / (24 * 3600)

    # Send single reminder at 30 hours before (1.25 days)
    # Window: 28.8-30 hours before (1.20-1.25 days with tolerance)
    reminder_label = "new_season_reminder"
    target_days = 1.25  # 30 hours
    min_days = 1.20  # 28.8 hours (30 min tolerance)

    history_key = (0, reminder_label)  # race_id=0 for season-level reminders

    # Skip if already notified
    if not is_already_notified(0, reminder_label):
        # Check if we're within the notification window
        if min_days <= days_until <= target_days:
            # Use race_id=1 data for track name, but label indicates season reminder
            if 1 in next_season_calendar:
                race_data = next_season_calendar[1].copy()
                race_data["days_until"] = days_until
                notifications.append(
                    ("new_season", 1, race_data, reminder_label, history_key)
                )

    return notifications

"""Main notification checking loop and helper functions - COMPATIBILITY SHIM

This module now re-exports from the modular structure for backwards compatibility.
New code should import from:
- notifications.history for history management
- notifications.timing for timing utilities
- notifications.checks for individual check functions

This file maintains the main check_notifications() entry point.
"""

import asyncio
import logging
from datetime import datetime, UTC

from aiogram import Bot

from gpro_calendar import (
    get_races_closing_soon,
    race_calendar,
)
from notifications.users import (
    users_data,
    load_users_data,
    is_user_blocked,
    is_notification_enabled,
    remove_active_snooze,
)
from notifications.senders import send_notification_to_user
from notifications.history import (
    load_notify_history,
    save_notify_history,
    mark_notified,
    cleanup_old_entries,
)
from notifications.timing import (
    get_next_check_interval,
    CHECK_INTERVAL_NORMAL_SECONDS,
)
from notifications.checks import (
    check_quali_closing,
    check_quali_open,
    check_quali_results,
    check_race_live_notifications,
    check_last_race_results,
    check_custom_notifications,
    check_snooze_reminders,
    check_season_transition,
    check_new_season_reminder,
    reset_snooze_counts_for_past_deadlines,
)
from infra.logging import log_structured

logger = logging.getLogger(__name__)

# Module-level in-memory caches (lazy loaded)
notification_lock = asyncio.Lock()


def _is_already_notified(race_id: int, label: str) -> bool:
    """Backwards compatibility wrapper"""
    from notifications.history import is_already_notified as _is_notified

    return _is_notified(race_id, label)


def _mark_notified(race_id: int, label: str) -> None:
    """Backwards compatibility wrapper"""
    from notifications.history import mark_notified as _mark

    _mark(race_id, label)


async def check_notifications(bot: Bot):
    """Continuous notification loop - adaptive check interval based on race proximity"""
    logger.info(
        "🔔 Starting notification checker (adaptive: 5min normal, 60s when race approaching)"
    )
    load_users_data()
    load_notify_history()  # Loads into notify_history from history.py

    while True:
        try:
            # Determine what notifications to send (quick check under lock)
            async with notification_lock:
                now = datetime.now(UTC)

                # Check season transition conditions
                await check_season_transition(now)

                # Fetch upcoming races once for efficiency (used by multiple checks)
                races_closing = get_races_closing_soon(
                    72
                )  # Extended to 72h for Tuesday races

                # Check all notification types
                notifications_to_send = []
                notifications_to_send.extend(check_quali_closing(now, races_closing))
                notifications_to_send.extend(await check_quali_open(now))
                notifications_to_send.extend(check_quali_results(now))
                notifications_to_send.extend(check_race_live_notifications(now))
                notifications_to_send.extend(await check_last_race_results(now))
                notifications_to_send.extend(
                    check_custom_notifications(now, races_closing)
                )
                notifications_to_send.extend(check_new_season_reminder(now))
                notifications_to_send.extend(check_snooze_reminders(now, races_closing))

                # Reset snooze counts for past deadlines
                reset_snooze_counts_for_past_deadlines(now)

                # Clean old history entries
                cleanup_old_entries()

                # Determine next check interval based on race proximity
                next_interval = get_next_check_interval(now, race_calendar)

            # Send notifications outside the lock (slow operation)
            await _send_notifications_to_users(bot, notifications_to_send)

        except Exception as e:
            logger.error(f"❌ Notification check error: {e}")
            next_interval = CHECK_INTERVAL_NORMAL_SECONDS  # Fallback on error

        # Wait before next check (adaptive interval)
        await asyncio.sleep(next_interval)


async def _send_notifications_to_users(bot: Bot, notifications: list) -> None:
    """Send notifications to all eligible users

    Args:
        bot: Bot instance
        notifications: List of (type, race_id, race_data, label, history_key, [user_id]) tuples.
                      For snooze notifications, user_id is included as the 6th element for targeted delivery.
    """
    for notification in notifications:
        try:
            # Handle both formats: regular (5 items) and snooze (6 items with user_id)
            if len(notification) == 6:
                ntype, race_id, race_data, label, history_key, target_user_id = (
                    notification
                )
                is_targeted = True
            else:
                ntype, race_id, race_data, label, history_key = notification
                target_user_id = None
                is_targeted = False

            race_name = race_data.get("track", f"Race {race_id}")

            # Log notification type
            if ntype == "closing":
                log_structured(
                    logging.INFO,
                    f"🔔 Quali {label} notification: Race {race_id} - {race_name}",
                    race_id=race_id,
                    race_name=race_name,
                    hours_remaining=(
                        race_data["quali_close"] - datetime.now(UTC)
                    ).total_seconds()
                    / 3600,
                )
            elif ntype == "opens":
                logger.info(f"🆕 Quali opened: Race {race_id} - {race_name}")
            elif ntype == "replay":
                logger.info(f"📺 Race replay available: Race {race_id} - {race_name}")
            elif ntype == "results":
                logger.info(f"📊 Race results available: Race {race_id} - {race_name}")
            elif ntype == "live":
                logger.info(f"🏁 Race is LIVE: Race {race_id} - {race_name}")
            elif ntype == "custom":
                logger.info(
                    f"🔔 Custom notification {label}: Race {race_id} - {race_name}"
                )
            elif ntype == "snooze":
                logger.info(
                    f"⏰ Snooze reminder: user {target_user_id}, race {race_id} - {race_name}"
                )
            elif ntype == "new_season":
                logger.info(f"🎉 New season reminder: {label}")

            # For targeted notifications (snoozes), only send to the specific user
            if is_targeted and target_user_id is not None:
                try:
                    user_id_int = int(target_user_id)

                    # Skip blocked users
                    if is_user_blocked(user_id_int):
                        continue

                    await send_notification_to_user(
                        bot, user_id_int, ntype, race_id, race_data, label
                    )
                except Exception as e:
                    logger.error(
                        f"Error sending targeted {ntype} to user {target_user_id}: {e}"
                    )
                    # Skip to next notification (don't mark notified if error)
                    continue

            # Send to all users (for non-targeted notifications)
            for user_id, user_data in list(users_data.items()):
                try:
                    user_id_int = int(user_id)

                    # Skip blocked users
                    if is_user_blocked(user_id_int):
                        continue

                    # Check notification type and settings
                    should_send = False

                    if ntype == "new_season":
                        # New season reminder uses new_season_reminder setting
                        should_send = is_notification_enabled(
                            user_id_int, "new_season_reminder"
                        )
                    elif ntype == "closing":
                        # Map labels to settings
                        label_map = {
                            "72h": "72h",
                            "48h": "48h",
                            "24h": "24h",
                            "2h": "2h",
                            "10min": "10min",
                            "custom_1": "custom_1",
                            "custom_2": "custom_2",
                        }
                        setting = label_map.get(label, label)
                        should_send = is_notification_enabled(user_id_int, setting)
                    elif ntype == "opens":
                        should_send = is_notification_enabled(user_id_int, "opens_soon")
                    elif ntype == "replay":
                        should_send = is_notification_enabled(
                            user_id_int, "race_replay"
                        )
                    elif ntype == "live":
                        should_send = is_notification_enabled(user_id_int, "race_live")
                    elif ntype == "results":
                        # Check label to determine which setting to use
                        if label == "quali_results":
                            should_send = is_notification_enabled(
                                user_id_int, "quali_results"
                            )
                        else:
                            should_send = is_notification_enabled(
                                user_id_int, "race_results"
                            )

                    if should_send:
                        await send_notification_to_user(
                            bot, user_id_int, ntype, race_id, race_data, label
                        )

                except Exception as e:
                    logger.error(f"Error sending to user {user_id}: {e}")

            # Mark as notified (snoozes are marked in check_snooze_reminders before being added to list)
            if ntype != "snooze":
                # Use history_key[0] for race_id to match the key used in is_already_notified check
                # This ensures new_season reminders (which use race_id=0 in history_key) are properly marked
                mark_notified(history_key[0], label)
            else:
                # For snoozes, remove from active_snoozes after sending (history already marked)
                _, snooze_key = history_key
                if snooze_key.startswith("snooze_"):
                    snooze_id = snooze_key.replace("snooze_", "")
                    from notifications.users import get_all_active_snoozes

                    logger.debug(
                        f"Removing snooze {snooze_id} from active_snoozes after sending"
                    )
                    for snooze in get_all_active_snoozes():
                        if snooze["id"] == snooze_id:
                            if remove_active_snooze(snooze["user_id"], snooze_id):
                                logger.debug(f"Removed active snooze {snooze_id}")
                            else:
                                logger.warning(
                                    f"Failed to remove active snooze {snooze_id}"
                                )
                            break

        except Exception as e:
            logger.error(f"Error processing notification {notification}: {e}")

    # Persist history after processing all notifications
    save_notify_history()

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
from datetime import datetime, timedelta, UTC

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
    get_all_active_snoozes,
)
from notifications.senders import send_notification_to_user
from notifications.history import (
    load_notify_history,
    save_notify_history,
    mark_notified,
    cleanup_old_entries,
    get_notify_history,
    clear_delivery_entries,
)
from notifications.timing import (
    get_next_check_interval,
    CHECK_INTERVAL_NORMAL_SECONDS,
)
from notifications.delivery_queue import (
    RetryState,
    load_delivery_queue,
    save_delivery_queue,
)
from notifications.senders.common import DeliveryStatus, RetryableDelivery
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

logger = logging.getLogger(__name__)

# Module-level in-memory caches (lazy loaded)
notification_lock = asyncio.Lock()
MAX_DELIVERY_ATTEMPTS = 3
DEFAULT_RETRY_DELAY_SECONDS = 60
_pending_notifications: dict[tuple[int, str], tuple] = {}
_delivery_attempts: dict[tuple[int, str, int], RetryState] = {}


def _save_delivery_state() -> None:
    save_delivery_queue(_pending_notifications, _delivery_attempts)


def _load_delivery_state() -> None:
    pending, attempts = load_delivery_queue()
    _pending_notifications.clear()
    _pending_notifications.update(pending)
    _delivery_attempts.clear()
    _delivery_attempts.update(attempts)


def _get_next_retry_delay(now: datetime | None = None) -> float | None:
    """Return seconds until the closest scheduled retry."""
    if not _delivery_attempts:
        return None
    current_time = now or datetime.now(UTC)
    return max(
        1.0,
        min(
            (state.next_attempt_at - current_time).total_seconds()
            for state in _delivery_attempts.values()
        ),
    )


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
    _load_delivery_state()
    next_interval: float = CHECK_INTERVAL_NORMAL_SECONDS

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

                # Keep retryable events after their original trigger window closes.
                for notification in notifications_to_send:
                    history_key = notification[4]
                    _pending_notifications[history_key] = notification
                _save_delivery_state()
                notifications_to_send = list(_pending_notifications.values())

                # Reset snooze counts for past deadlines
                reset_snooze_counts_for_past_deadlines(now)

                # Clean old history entries
                cleanup_old_entries()

                # Determine next check interval based on race proximity
                next_interval = get_next_check_interval(now, race_calendar)

            # Send notifications outside the lock (slow operation)
            await _send_notifications_to_users(bot, notifications_to_send)
            retry_delay = _get_next_retry_delay()
            if retry_delay is not None:
                next_interval = min(next_interval, retry_delay)

        except Exception as e:
            logger.error(f"❌ Notification check error: {e}")
            next_interval = CHECK_INTERVAL_NORMAL_SECONDS  # Fallback on error

        # Wait before next check (adaptive interval)
        await asyncio.sleep(next_interval)


def _should_send_to_user(user_id: int, ntype: str, label: str) -> bool:
    """Return whether the user's settings allow this event."""
    if ntype == "snooze":
        return True
    if ntype == "new_season":
        return is_notification_enabled(user_id, "new_season_reminder")
    if ntype in ("closing", "custom"):
        return is_notification_enabled(user_id, label)
    if ntype == "opens":
        return is_notification_enabled(user_id, "opens_soon")
    if ntype == "replay":
        return is_notification_enabled(user_id, "race_replay")
    if ntype == "live":
        return is_notification_enabled(user_id, "race_live")
    if ntype == "results":
        setting = "quali_results" if label == "quali_results" else "race_results"
        return is_notification_enabled(user_id, setting)
    return False


def _delivery_marker(history_key: tuple[int, str], user_id: int) -> tuple[int, str]:
    """Build a temporary per-user marker for a broadcast event."""
    return history_key[0], f"{history_key[1]}:user:{user_id}"


def _mark_delivery_complete(history_key: tuple[int, str]) -> None:
    """Persist a terminal marker before mutating the retry queue."""
    mark_notified(history_key[0], history_key[1])
    save_notify_history()


def _clear_attempts_for_event(history_key: tuple[int, str]) -> None:
    keys_to_remove = [
        key
        for key in _delivery_attempts
        if key[0] == history_key[0] and key[1] == history_key[1]
    ]
    for key in keys_to_remove:
        del _delivery_attempts[key]


async def _attempt_delivery(
    bot: Bot,
    user_id: int,
    ntype: str,
    race_id: int,
    race_data: dict,
    label: str,
    history_key: tuple[int, str],
) -> bool:
    """Attempt one due delivery and return True when no retries remain."""
    attempt_key = (history_key[0], history_key[1], user_id)
    now = datetime.now(UTC)
    previous_state = _delivery_attempts.get(attempt_key)
    if previous_state and now < previous_state.next_attempt_at:
        return False

    try:
        outcome = await send_notification_to_user(
            bot, user_id, ntype, race_id, race_data, label
        )
    except Exception as error:
        logger.exception("Unexpected delivery error for user %s: %s", user_id, error)
        outcome = RetryableDelivery()

    if isinstance(outcome, RetryableDelivery):
        retry_after = outcome.retry_after
    elif outcome is DeliveryStatus.RETRYABLE_FAILURE:
        # Compatibility for third-party/custom senders returning the old enum.
        retry_after = None
    else:
        _delivery_attempts.pop(attempt_key, None)
        _save_delivery_state()
        return True

    attempts = (previous_state.attempts if previous_state else 0) + 1
    if attempts >= MAX_DELIVERY_ATTEMPTS:
        _delivery_attempts.pop(attempt_key, None)
        _save_delivery_state()
        logger.error(
            "Delivery retries exhausted for user %s, race %s, notification %s",
            user_id,
            race_id,
            history_key[1],
        )
        return True

    delay = max(
        1.0,
        retry_after if retry_after is not None else DEFAULT_RETRY_DELAY_SECONDS,
    )
    next_attempt_at = now + timedelta(seconds=delay)
    _delivery_attempts[attempt_key] = RetryState(attempts, next_attempt_at)
    _save_delivery_state()
    logger.warning(
        "Temporary delivery failure for user %s; attempt %s/%s, retry at %s",
        user_id,
        attempts,
        MAX_DELIVERY_ATTEMPTS,
        next_attempt_at.isoformat(),
    )
    return False


def _remove_delivered_snooze(history_key: tuple[int, str]) -> None:
    """Remove a terminal snooze from user storage."""
    snooze_key = history_key[1]
    if not snooze_key.startswith("snooze_"):
        return

    snooze_id = snooze_key.removeprefix("snooze_")
    for snooze in get_all_active_snoozes():
        if snooze["id"] == snooze_id:
            remove_active_snooze(snooze["user_id"], snooze_id)
            return


async def _send_notifications_to_users(bot: Bot, notifications: list) -> None:
    """Deliver queued events with per-user deduplication and bounded retries."""
    history = get_notify_history()

    for notification in notifications:
        if len(notification) == 6:
            ntype, race_id, race_data, label, history_key, target_user_id = notification
            targeted = True
        else:
            ntype, race_id, race_data, label, history_key = notification
            target_user_id = None
            targeted = False

        if history_key in history:
            _pending_notifications.pop(history_key, None)
            _clear_attempts_for_event(history_key)
            continue

        event_complete = True

        if targeted and target_user_id is not None:
            user_id = int(target_user_id)
            if (
                user_id not in users_data
                or is_user_blocked(user_id)
                or not _should_send_to_user(user_id, ntype, label)
            ):
                _mark_delivery_complete(history_key)
            else:
                terminal = await _attempt_delivery(
                    bot,
                    user_id,
                    ntype,
                    race_id,
                    race_data,
                    label,
                    history_key,
                )
                if terminal:
                    _mark_delivery_complete(history_key)
                else:
                    event_complete = False

            if event_complete and ntype == "snooze":
                _remove_delivered_snooze(history_key)
        else:
            for raw_user_id in list(users_data):
                user_id = int(raw_user_id)
                marker = _delivery_marker(history_key, user_id)
                if marker in history:
                    continue

                if is_user_blocked(user_id) or not _should_send_to_user(
                    user_id, ntype, label
                ):
                    _mark_delivery_complete(marker)
                    continue

                terminal = await _attempt_delivery(
                    bot,
                    user_id,
                    ntype,
                    race_id,
                    race_data,
                    label,
                    history_key,
                )
                if terminal:
                    _mark_delivery_complete(marker)
                else:
                    event_complete = False

            if event_complete:
                _mark_delivery_complete(history_key)
                clear_delivery_entries(history_key[0], history_key[1])

        if event_complete:
            _pending_notifications.pop(history_key, None)
            _clear_attempts_for_event(history_key)

    save_notify_history()
    _save_delivery_state()

"""Tests for per-user delivery outcomes and bounded persistent retries."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from notifications.delivery_queue import RetryState
from notifications.senders.common import DeliveryStatus, RetryableDelivery


@pytest.fixture(autouse=True)
def reset_delivery_state():
    from notifications import checker
    from notifications.history import set_notify_history
    from notifications.users.storage import users_data

    users_data.clear()
    set_notify_history({})
    checker._delivery_attempts.clear()
    checker._pending_notifications.clear()

    yield

    users_data.clear()
    set_notify_history({})
    checker._delivery_attempts.clear()
    checker._pending_notifications.clear()


def _race_data() -> dict:
    now = datetime.now(UTC)
    return {
        "track": "Test GP",
        "quali_close": now + timedelta(hours=24),
        "date": now + timedelta(hours=48),
    }


def _enable_notification(user_id: int, label: str = "48h") -> None:
    from notifications.users import get_user_status

    user_status, _ = get_user_status(user_id)
    if label in ("custom_1", "custom_2"):
        slot_idx = int(label.split("_")[1]) - 1
        user_status["custom_notifications"][slot_idx] = {
            "enabled": True,
            "hours_before": 8.0,
        }
    else:
        user_status["notifications"][label] = True


def _make_retry_due(history_key: tuple[int, str], user_id: int) -> None:
    from notifications import checker

    attempt_key = (history_key[0], history_key[1], user_id)
    state = checker._delivery_attempts[attempt_key]
    checker._delivery_attempts[attempt_key] = RetryState(
        state.attempts, datetime.now(UTC) - timedelta(seconds=1)
    )


@pytest.mark.asyncio
async def test_retryable_failure_stops_after_three_due_attempts():
    from notifications.checker import _attempt_delivery

    sender = AsyncMock(return_value=RetryableDelivery())
    history_key = (1, "48h")

    with patch("notifications.checker.send_notification_to_user", sender):
        first = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )
        _make_retry_due(history_key, 123)
        second = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )
        _make_retry_due(history_key, 123)
        third = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )

    assert (first, second, third) == (False, False, True)
    assert sender.await_count == 3


@pytest.mark.asyncio
async def test_retry_after_schedules_exact_next_attempt():
    from notifications import checker

    sender = AsyncMock(return_value=RetryableDelivery(retry_after=37))
    before = datetime.now(UTC)

    with patch("notifications.checker.send_notification_to_user", sender):
        terminal = await checker._attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", (1, "48h")
        )

    state = checker._delivery_attempts[(1, "48h", 123)]
    assert terminal is False
    assert state.attempts == 1
    assert before + timedelta(seconds=36) <= state.next_attempt_at
    assert state.next_attempt_at <= datetime.now(UTC) + timedelta(seconds=38)
    assert 35 <= checker._get_next_retry_delay() <= 37


@pytest.mark.asyncio
async def test_retry_is_not_attempted_before_due_time():
    from notifications import checker

    checker._delivery_attempts[(1, "48h", 123)] = RetryState(
        1, datetime.now(UTC) + timedelta(minutes=5)
    )
    sender = AsyncMock(return_value=DeliveryStatus.SENT)

    with patch("notifications.checker.send_notification_to_user", sender):
        terminal = await checker._attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", (1, "48h")
        )

    assert terminal is False
    sender.assert_not_awaited()


@pytest.mark.asyncio
async def test_blocked_user_is_terminal_without_send():
    from notifications.checker import _send_notifications_to_users
    from notifications.history import get_notify_history
    from notifications.users import get_user_status

    user_status, _ = get_user_status(123)
    user_status["blocked_at"] = datetime.now(UTC).isoformat()
    history_key = (1, "custom_1:user:123")
    notification = (
        "custom",
        1,
        _race_data(),
        "custom_1",
        history_key,
        123,
    )
    sender = AsyncMock()

    with patch("notifications.checker.send_notification_to_user", sender):
        await _send_notifications_to_users(AsyncMock(), [notification])
        await _send_notifications_to_users(AsyncMock(), [notification])

    sender.assert_not_awaited()
    assert history_key in get_notify_history()


@pytest.mark.asyncio
async def test_permanent_failure_is_not_retried():
    from notifications.checker import _send_notifications_to_users
    from notifications.history import get_notify_history

    _enable_notification(123, "custom_1")
    history_key = (1, "custom_1:user:123")
    notification = (
        "custom",
        1,
        _race_data(),
        "custom_1",
        history_key,
        123,
    )
    sender = AsyncMock(return_value=DeliveryStatus.PERMANENT_FAILURE)

    with patch("notifications.checker.send_notification_to_user", sender):
        await _send_notifications_to_users(AsyncMock(), [notification])
        await _send_notifications_to_users(AsyncMock(), [notification])

    assert sender.await_count == 1
    assert history_key in get_notify_history()


@pytest.mark.asyncio
async def test_broadcast_retries_only_temporarily_failed_user():
    from notifications.checker import _send_notifications_to_users
    from notifications.history import get_notify_history

    _enable_notification(111)
    _enable_notification(222)
    history_key = (1, "48h")
    notification = ("closing", 1, _race_data(), "48h", history_key)
    sender = AsyncMock(
        side_effect=[
            DeliveryStatus.SENT,
            RetryableDelivery(),
            DeliveryStatus.SENT,
        ]
    )

    with patch("notifications.checker.send_notification_to_user", sender):
        await _send_notifications_to_users(AsyncMock(), [notification])
        _make_retry_due(history_key, 222)
        await _send_notifications_to_users(AsyncMock(), [notification])

    assert [call.args[1] for call in sender.await_args_list] == [111, 222, 222]
    history = get_notify_history()
    assert history_key in history
    assert not any(label.startswith("48h:user:") for _, label in history)


def test_delivery_state_survives_memory_reset():
    from notifications import checker

    history_key = (1, "48h")
    notification = ("closing", 1, _race_data(), "48h", history_key)
    retry_at = datetime.now(UTC) + timedelta(seconds=45)
    checker._pending_notifications[history_key] = notification
    checker._delivery_attempts[(1, "48h", 123)] = RetryState(1, retry_at)
    checker._save_delivery_state()

    checker._pending_notifications.clear()
    checker._delivery_attempts.clear()
    checker._load_delivery_state()

    restored = checker._pending_notifications[history_key]
    restored_state = checker._delivery_attempts[(1, "48h", 123)]
    assert restored[:2] == notification[:2]
    assert restored[2]["quali_close"] == notification[2]["quali_close"]
    assert restored_state == RetryState(1, retry_at)

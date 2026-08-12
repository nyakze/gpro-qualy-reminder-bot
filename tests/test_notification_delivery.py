"""Tests for per-user delivery outcomes and bounded retries."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, patch

import pytest

from notifications.senders.common import DeliveryStatus


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


@pytest.mark.asyncio
async def test_retryable_failure_stops_after_three_attempts():
    from notifications.checker import _attempt_delivery

    sender = AsyncMock(return_value=DeliveryStatus.RETRYABLE_FAILURE)
    history_key = (1, "48h")

    with patch("notifications.checker.send_notification_to_user", sender):
        first = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )
        second = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )
        third = await _attempt_delivery(
            AsyncMock(), 123, "closing", 1, _race_data(), "48h", history_key
        )

    assert (first, second, third) == (False, False, True)
    assert sender.await_count == 3


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
    notification = ("closing", 1, _race_data(), "48h", (1, "48h"))
    sender = AsyncMock(
        side_effect=[
            DeliveryStatus.SENT,
            DeliveryStatus.RETRYABLE_FAILURE,
            DeliveryStatus.SENT,
        ]
    )

    with patch("notifications.checker.send_notification_to_user", sender):
        await _send_notifications_to_users(AsyncMock(), [notification])
        await _send_notifications_to_users(AsyncMock(), [notification])

    assert [call.args[1] for call in sender.await_args_list] == [111, 222, 222]
    history = get_notify_history()
    assert (1, "48h") in history
    assert not any(label.startswith("48h:user:") for _, label in history)

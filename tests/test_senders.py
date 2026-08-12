"""Tests for notification senders and dispatcher"""

import pytest
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def reset_user_data():
    """Reset user data before and after each test"""
    from notifications.users.storage import users_data
    from notifications.history import set_notify_history

    users_data.clear()
    set_notify_history({})

    yield

    users_data.clear()
    set_notify_history({})


@pytest.fixture
def mock_bot():
    """Create a mock aiogram Bot"""
    bot = AsyncMock()
    bot.send_message = AsyncMock(return_value=MagicMock())
    return bot


@pytest.fixture
def sample_race_data():
    """Sample race data for testing"""
    now = datetime.now(UTC)
    return {
        "track": "Spa GP (Belgium)",
        "date": now + timedelta(hours=48),
        "quali_close": now + timedelta(hours=24),
        "group": "Pro",
    }


@pytest.fixture
def sample_user():
    """Create a sample user for testing"""
    from notifications.users import get_user_status

    user_id = 12345
    user_status, _ = get_user_status(user_id)
    user_status["group"] = "P15"
    user_status["gpro_lang"] = "gb"
    user_status["ui_lang"] = "gb"
    user_status["website_mode"] = "classic"

    return user_id


class TestSenderCommon:
    """Tests for notifications/senders/common.py"""

    def test_get_user_info(self, sample_user):
        """Test getting user info"""
        from notifications.senders.common import get_user_info

        info = get_user_info(sample_user)

        assert info["group"] == "P15"
        assert info["gpro_lang"] == "gb"
        assert info["ui_lang"] == "gb"
        assert info["website_mode"] == "classic"

    def test_get_text_getter_with_i18n(self):
        """Test text getter with i18n context"""
        from notifications.senders.common import get_text_getter

        mock_i18n = MagicMock()
        mock_i18n.get = MagicMock(return_value="translated text")

        get_text = get_text_getter(mock_i18n, "gb")
        result = get_text("test-key", param="value")

        assert result == "translated text"
        mock_i18n.get.assert_called_once_with("test-key", param="value")

    def test_get_text_getter_without_i18n(self):
        """Test text getter without i18n uses translation function"""
        from notifications.senders.common import get_text_getter

        with patch("i18n_setup.get_translation", return_value="fallback text"):
            get_text = get_text_getter(None, "gb")
            result = get_text("test-key")

            assert result == "fallback text"

    @pytest.mark.asyncio
    async def test_send_notification_success(self, mock_bot):
        """Test successful notification sending"""
        from notifications.senders.common import DeliveryStatus, send_notification

        result = await send_notification(mock_bot, 12345, "Test message", "test", 1)

        assert result is DeliveryStatus.SENT
        mock_bot.send_message.assert_called_once_with(
            12345, "Test message", reply_markup=None, parse_mode="HTML"
        )

    @pytest.mark.asyncio
    async def test_send_notification_blocked(self, mock_bot):
        """Test notification handling when user blocked bot"""
        from aiogram.exceptions import TelegramForbiddenError
        from notifications.senders.common import DeliveryStatus, send_notification

        mock_bot.send_message.side_effect = TelegramForbiddenError(
            method="send_message", message="Forbidden: bot was blocked by the user"
        )

        with patch(
            "notifications.senders.common.mark_user_blocked"
        ) as mock_mark_blocked:
            result = await send_notification(mock_bot, 12345, "Test message", "test", 1)

        assert result is DeliveryStatus.PERMANENT_FAILURE
        mock_mark_blocked.assert_called_once_with(12345)

    @pytest.mark.asyncio
    async def test_send_notification_deleted_chat_is_permanent(self, mock_bot):
        """A deleted/unavailable chat is blocked and never retried."""
        from aiogram.exceptions import TelegramNotFound
        from notifications.senders.common import DeliveryStatus, send_notification

        mock_bot.send_message.side_effect = TelegramNotFound(
            method="send_message", message="Not Found: chat not found"
        )

        with patch(
            "notifications.senders.common.mark_user_blocked"
        ) as mock_mark_blocked:
            result = await send_notification(mock_bot, 12345, "Test message", "test", 1)

        assert result is DeliveryStatus.PERMANENT_FAILURE
        mock_mark_blocked.assert_called_once_with(12345)

    @pytest.mark.asyncio
    async def test_send_notification_error(self, mock_bot):
        """Unexpected delivery errors remain eligible for a bounded retry."""
        from notifications.senders.common import RetryableDelivery, send_notification

        mock_bot.send_message.side_effect = Exception("Network error")

        result = await send_notification(mock_bot, 12345, "Test message", "test", 1)

        assert result == RetryableDelivery()

    @pytest.mark.asyncio
    async def test_send_notification_preserves_retry_after(self, mock_bot):
        from aiogram.exceptions import TelegramRetryAfter
        from notifications.senders.common import RetryableDelivery, send_notification

        mock_bot.send_message.side_effect = TelegramRetryAfter(
            method="send_message",
            message="Too Many Requests",
            retry_after=23,
        )

        result = await send_notification(mock_bot, 12345, "Test message", "test", 1)

        assert result == RetryableDelivery(retry_after=23)


class TestQualiNotificationSender:
    """Tests for notifications/senders/quali.py"""

    def test_is_qualifying_closed_true(self, sample_race_data):
        """Test qualifying closed detection when deadline passed"""
        from notifications.senders.quali import is_qualifying_closed
        from notifications import history

        now = datetime.now(UTC)
        # Quali closed 1 hour ago
        sample_race_data["quali_close"] = now - timedelta(hours=1)

        # Clear the notify_history directly
        history._notify_history.clear()
        result = is_qualifying_closed(1, sample_race_data)
        assert result is True

    def test_is_qualifying_closed_false_before_deadline(self, sample_race_data):
        """Test qualifying not closed before deadline"""
        from notifications.senders.quali import is_qualifying_closed
        from notifications import history

        now = datetime.now(UTC)
        # Quali closes in 1 hour
        sample_race_data["quali_close"] = now + timedelta(hours=1)

        history._notify_history.clear()
        result = is_qualifying_closed(1, sample_race_data)
        assert result is False

    def test_is_qualifying_closed_false_opens_soon_sent(self, sample_race_data):
        """Test qualifying not closed if opens_soon was sent"""
        from notifications.senders.quali import is_qualifying_closed
        from notifications import history

        now = datetime.now(UTC)
        sample_race_data["quali_close"] = now - timedelta(hours=1)

        history._notify_history[(1, "opens_soon")] = now
        result = is_qualifying_closed(1, sample_race_data)
        assert result is False
        # Clean up
        del history._notify_history[(1, "opens_soon")]

    def test_is_qualifying_closed_no_quali_close(self):
        """Test qualifying not closed if no quali_close time"""
        from notifications.senders.quali import is_qualifying_closed

        result = is_qualifying_closed(1, {})
        assert result is False

    @pytest.mark.asyncio
    async def test_send_quali_notification_skips_completed(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test quali notification skipped if user marked done"""
        from notifications.senders.quali import send_quali_notification
        from notifications.users import get_user_status

        # Mark race as done
        user_status, _ = get_user_status(sample_user)
        user_status["completed_quali"] = 1

        await send_quali_notification(mock_bot, sample_user, 1, sample_race_data, "48h")

        # Bot should not be called
        mock_bot.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_send_quali_notification_allows_manual(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test manual quali notification sent even if marked done"""
        from notifications.senders.quali import send_quali_notification
        from notifications.users import get_user_status

        # Mark race as done
        user_status, _ = get_user_status(sample_user)
        user_status["completed_quali"] = 1

        # But manual notification should still be sent
        await send_quali_notification(
            mock_bot, sample_user, 1, sample_race_data, "manual"
        )

        # Bot should be called
        mock_bot.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_quali_notification_opens_soon(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test opens_soon notification"""
        from notifications.senders.quali import send_quali_notification

        await send_quali_notification(
            mock_bot, sample_user, 1, sample_race_data, "opens_soon"
        )

        mock_bot.send_message.assert_called_once()
        # Just verify the notification was sent - the actual template used depends on timing logic


class TestRaceLiveNotificationSender:
    """Tests for notifications/senders/race_live.py"""

    @pytest.mark.asyncio
    async def test_send_race_live_notification_with_group(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test race live notification with group set"""
        from notifications.senders.race_live import send_race_live_notification

        await send_race_live_notification(mock_bot, sample_user, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()
        # Just verify the notification was sent - message content depends on i18n

    @pytest.mark.asyncio
    async def test_send_race_live_notification_no_group(
        self, mock_bot, sample_race_data
    ):
        """Test race live notification without group"""
        from notifications.senders.race_live import send_race_live_notification
        from notifications.users import get_user_status

        user_id = 99999
        get_user_status(user_id)
        # Group is None by default

        await send_race_live_notification(mock_bot, user_id, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_race_live_notification_app_mode(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test race live notification in app mode"""
        from notifications.senders.race_live import send_race_live_notification
        from notifications.users import get_user_status

        user_status, _ = get_user_status(sample_user)
        user_status["website_mode"] = "app"

        await send_race_live_notification(mock_bot, sample_user, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()


class TestQualiResultsNotificationSender:
    """Tests for notifications/senders/quali_results.py"""

    @pytest.mark.asyncio
    async def test_send_quali_results_with_group(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test quali results notification with group"""
        from notifications.senders.quali_results import send_quali_results_notification

        await send_quali_results_notification(
            mock_bot, sample_user, 1, sample_race_data
        )

        mock_bot.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_quali_results_no_group(self, mock_bot, sample_race_data):
        """Test quali results notification without group"""
        from notifications.senders.quali_results import send_quali_results_notification
        from notifications.users import get_user_status

        user_id = 88888
        get_user_status(user_id)

        await send_quali_results_notification(mock_bot, user_id, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()


class TestRaceReplayNotificationSender:
    """Tests for notifications/senders/race_replay.py"""

    @pytest.mark.asyncio
    async def test_send_race_replay_notification(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test race replay notification"""
        from notifications.senders.race_replay import send_race_replay_notification

        await send_race_replay_notification(mock_bot, sample_user, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()


class TestRaceResultsNotificationSender:
    """Tests for notifications/senders/race_results.py"""

    @pytest.mark.asyncio
    async def test_send_race_results_notification(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test race results notification"""
        from notifications.senders.race_results import send_race_results_notification

        await send_race_results_notification(mock_bot, sample_user, 1, sample_race_data)

        mock_bot.send_message.assert_called_once()


class TestNewSeasonNotificationSender:
    """Tests for notifications/senders/new_season.py"""

    @pytest.mark.asyncio
    async def test_send_new_season_reminder(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test new season reminder notification"""
        from notifications.senders.new_season import (
            send_new_season_reminder_notification,
        )

        await send_new_season_reminder_notification(
            mock_bot, sample_user, 1, sample_race_data
        )

        mock_bot.send_message.assert_called_once()


class TestNotificationDispatcher:
    """Tests for notifications/senders/dispatcher.py"""

    @pytest.mark.asyncio
    async def test_dispatcher_closing_48h(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test dispatcher routes closing notification to quali sender"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_quali_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "closing", 1, sample_race_data, "48h"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data, "48h"
            )

    @pytest.mark.asyncio
    async def test_dispatcher_opens(self, mock_bot, sample_user, sample_race_data):
        """Test dispatcher routes opens notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_quali_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "opens", 1, sample_race_data, "opens_soon"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data, "opens_soon"
            )

    @pytest.mark.asyncio
    async def test_dispatcher_live(self, mock_bot, sample_user, sample_race_data):
        """Test dispatcher routes live notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_race_live_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "live", 1, sample_race_data, "race_live"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data
            )

    @pytest.mark.asyncio
    async def test_dispatcher_replay(self, mock_bot, sample_user, sample_race_data):
        """Test dispatcher routes replay notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_race_replay_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "replay", 1, sample_race_data, "race_replay"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data
            )

    @pytest.mark.asyncio
    async def test_dispatcher_quali_results(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test dispatcher routes quali results notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_quali_results_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "results", 1, sample_race_data, "quali_results"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data
            )

    @pytest.mark.asyncio
    async def test_dispatcher_race_results(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test dispatcher routes race results notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_race_results_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "results", 1, sample_race_data, "race_results"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data
            )

    @pytest.mark.asyncio
    async def test_dispatcher_snooze(self, mock_bot, sample_user, sample_race_data):
        """Test dispatcher routes snooze notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_quali_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot, sample_user, "snooze", 1, sample_race_data, "48h"
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data, "snooze_48h"
            )

    @pytest.mark.asyncio
    async def test_dispatcher_new_season(self, mock_bot, sample_user, sample_race_data):
        """Test dispatcher routes new season notification"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch(
            "notifications.senders.dispatcher.send_new_season_reminder_notification"
        ) as mock_sender:
            await send_notification_to_user(
                mock_bot,
                sample_user,
                "new_season",
                1,
                sample_race_data,
                "new_season_reminder",
            )

            mock_sender.assert_called_once_with(
                mock_bot, sample_user, 1, sample_race_data
            )

    @pytest.mark.asyncio
    async def test_dispatcher_unknown_type(
        self, mock_bot, sample_user, sample_race_data
    ):
        """Test dispatcher handles unknown notification type"""
        from notifications.senders.dispatcher import send_notification_to_user

        with patch("notifications.senders.dispatcher.logger") as mock_logger:
            await send_notification_to_user(
                mock_bot, sample_user, "unknown_type", 1, sample_race_data, "label"
            )

            mock_logger.warning.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

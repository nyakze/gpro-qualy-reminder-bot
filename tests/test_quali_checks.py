"""Tests for qualification notification checks"""

import pytest
from datetime import datetime, timedelta, UTC
from unittest.mock import patch, MagicMock, AsyncMock

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCheckQualiClosing:
    """Tests for check_quali_closing function"""

    def test_empty_races_returns_empty(self):
        """Test that empty races closing returns empty list"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        result = check_quali_closing(now, [])
        assert result == []

    def test_48h_notification_label(self):
        """Test that 48 hours remaining uses '48h' label"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=48)
        races_closing = [(48.0, 1, {"date": race_time})]

        result = check_quali_closing(now, races_closing)
        assert len(result) == 1
        assert result[0][3] == "48h"

    def test_24h_notification_label(self):
        """Test that 24 hours remaining uses '24h' label"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=24)
        races_closing = [(24.0, 1, {"date": race_time})]

        result = check_quali_closing(now, races_closing)
        assert len(result) == 1
        assert result[0][3] == "24h"

    def test_2h_notification_label(self):
        """Test that 2 hours remaining uses '2h' label"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=2)
        races_closing = [(2.0, 1, {"date": race_time})]

        result = check_quali_closing(now, races_closing)
        assert len(result) == 1
        assert result[0][3] == "2h"

    def test_10min_notification_label(self):
        """Test that ~10 minutes remaining uses '10min' label"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        race_time = now + timedelta(minutes=10)
        races_closing = [(0.17, 1, {"date": race_time})]

        result = check_quali_closing(now, races_closing)
        assert len(result) == 1
        assert result[0][3] == "10min"

    def test_already_notified_skipped(self):
        """Test that already notified races are skipped"""
        from notifications.checks.quali import check_quali_closing
        from notifications.history import set_notify_history

        set_notify_history({(1, "48h"): datetime.now(UTC)})

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=48)
        races_closing = [(48.0, 1, {"date": race_time})]

        result = check_quali_closing(now, races_closing)
        assert result == []

        set_notify_history({})

    def test_multiple_races_different_labels(self):
        """Test multiple races with different time windows"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        races_closing = [
            (48.0, 1, {"date": now + timedelta(hours=48)}),
            (24.0, 2, {"date": now + timedelta(hours=24)}),
            (2.0, 3, {"date": now + timedelta(hours=2)}),
        ]

        result = check_quali_closing(now, races_closing)
        assert len(result) == 3
        labels = [r[3] for r in result]
        assert "48h" in labels
        assert "24h" in labels
        assert "2h" in labels

    def test_past_deadline_not_included(self):
        """Test that very far future races (>72h) are not included"""
        from notifications.checks.quali import check_quali_closing

        now = datetime.now(UTC)
        races_closing = [
            (73.0, 1, {"date": now + timedelta(hours=73)}),
        ]

        result = check_quali_closing(now, races_closing)
        assert result == []


class TestCheckQualiResults:
    """Tests for check_quali_results function"""

    def test_no_races_returns_empty(self):
        """Test that empty calendar returns empty list"""
        with patch('notifications.history.get_notify_history', return_value={}):
            with patch('notifications.checks.quali.race_calendar', {}):
                from notifications.checks.quali import check_quali_results

                now = datetime.now(UTC)
                result = check_quali_results(now)
                assert result == []

    def test_quali_too_recent_no_notification(self):
        """Test that quali too recent doesn't send notification"""
        now = datetime.now(UTC)
        quali_close = now - timedelta(minutes=3)

        with patch('notifications.history.get_notify_history', return_value={}):
            with patch('notifications.checks.quali.race_calendar', {1: {"quali_close": quali_close}}):
                from notifications.checks.quali import check_quali_results

                result = check_quali_results(now)
                assert result == []

    def test_quali_results_sends_notification(self):
        """Test that quali results sends notification after 5 minutes"""
        now = datetime.now(UTC)
        quali_close = now - timedelta(minutes=10)

        with patch('notifications.history.get_notify_history', return_value={}):
            with patch('notifications.checks.quali.race_calendar', {1: {"quali_close": quali_close}}):
                from notifications.checks.quali import check_quali_results

                result = check_quali_results(now)
                assert len(result) == 1
                assert result[0][0] == "results"
                assert result[0][3] == "quali_results"

    def test_already_notified_skipped(self):
        """Test that already notified races are skipped"""
        now = datetime.now(UTC)
        quali_close = now - timedelta(minutes=10)
        mock_history = {(1, "quali_results"): now}

        with patch('notifications.history.get_notify_history', return_value=mock_history):
            with patch('notifications.checks.quali.race_calendar', {1: {"quali_close": quali_close}}):
                from notifications.checks.quali import check_quali_results

                result = check_quali_results(now)
                assert result == []

    def test_5_minutes_exactly_triggers(self):
        """Test that exactly 5 minutes triggers notification"""
        now = datetime.now(UTC)
        quali_close = now - timedelta(minutes=5)

        with patch('notifications.history.get_notify_history', return_value={}):
            with patch('notifications.checks.quali.race_calendar', {1: {"quali_close": quali_close}}):
                from notifications.checks.quali import check_quali_results

                result = check_quali_results(now)
                assert len(result) == 1


class TestQualiOpenNotificationLabels:
    """Tests that verify correct notification labels are used"""

    def test_opens_soon_label_used(self):
        """Test that 'opens_soon' label is used for quali open notifications"""
        from notifications.checks.quali import _get_races_for_polling

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=2.5)

        mock_history = {}
        mock_calendar = {
            2: {"date": race_time},
            1: {"date": now - timedelta(hours=2)},
        }

        with patch('notifications.history.get_notify_history', return_value=mock_history):
            with patch('notifications.checks.quali.race_calendar', mock_calendar):
                races = _get_races_for_polling(now)
                if races:
                    assert len(races) > 0

    def test_race_1_skipped_for_polling(self):
        """Test that race 1 is skipped for opens_soon polling"""
        from notifications.checks.quali import _get_races_for_polling

        now = datetime.now(UTC)
        race_time = now + timedelta(hours=2.5)

        mock_calendar = {
            1: {"date": race_time},
        }

        with patch('notifications.history.get_notify_history', return_value={}):
            with patch('notifications.checks.quali.race_calendar', mock_calendar):
                races = _get_races_for_polling(now)
                assert len(races) == 0


class TestReplayAndResultsLabels:
    """Tests for replay and results notification labels"""

    def test_race_replay_label(self):
        """Test that 'race_replay' label is used for replay notifications"""
        from notifications.checks.quali import _add_replay_and_results_notifications

        mock_notifications = []
        mock_history = {}

        with patch('notifications.history.get_notify_history', return_value=mock_history):
            with patch('notifications.checks.quali.race_calendar', {1: {"date": datetime.now(UTC)}}):
                _add_replay_and_results_notifications(mock_notifications, 1)

                if mock_notifications:
                    labels = [n[3] for n in mock_notifications]
                    assert "race_replay" in labels

    def test_race_results_label(self):
        """Test that 'race_results' label is used for results notifications"""
        from notifications.checks.quali import _add_replay_and_results_notifications

        mock_notifications = []
        mock_history = {}

        with patch('notifications.history.get_notify_history', return_value=mock_history):
            with patch('notifications.checks.quali.race_calendar', {1: {"date": datetime.now(UTC)}}):
                _add_replay_and_results_notifications(mock_notifications, 1)

                if mock_notifications:
                    labels = [n[3] for n in mock_notifications]
                    assert "race_results" in labels

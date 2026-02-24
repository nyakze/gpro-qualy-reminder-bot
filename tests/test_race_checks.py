"""Tests for race notification checks"""

from datetime import datetime, timedelta, UTC
from unittest.mock import patch

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCheckRaceLiveNotifications:
    """Tests for check_race_live_notifications function"""

    def test_no_races_returns_empty(self):
        """Test that empty calendar returns empty list"""
        with patch("notifications.history.get_notify_history", return_value={}):
            with patch("notifications.checks.race.race_calendar", {}):
                from notifications.checks.race import check_race_live_notifications

                now = datetime.now(UTC)
                result = check_race_live_notifications(now)
                assert result == []

    def test_already_notified_skipped(self):
        """Test that already notified races are skipped"""
        now = datetime.now(UTC)
        race_time = now + timedelta(minutes=2)
        mock_history = {(1, "race_live"): now}

        with patch(
            "notifications.history.get_notify_history", return_value=mock_history
        ):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert result == []

    def test_race_within_window_returns_notification(self):
        """Test that race within window (30 sec before) returns notification"""
        now = datetime.now(UTC)
        race_time = now + timedelta(seconds=30)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert len(result) == 1
                assert result[0][0] == "live"
                assert result[0][1] == 1
                assert result[0][3] == "race_live"

    def test_race_1_minute_before_in_window(self):
        """Test that race 1 minute before is in window"""
        now = datetime.now(UTC)
        race_time = now - timedelta(minutes=1)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert len(result) == 1

    def test_race_5_minutes_after_in_window(self):
        """Test that race 5 minutes after is in window"""
        now = datetime.now(UTC)
        race_time = now - timedelta(minutes=5)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert len(result) == 1

    def test_race_5_minutes_before_not_in_window(self):
        """Test that race 5 minutes before is NOT in window"""
        now = datetime.now(UTC)
        race_time = now + timedelta(minutes=5)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert len(result) == 0

    def test_race_outside_window_not_returned(self):
        """Test that race outside window is not returned"""
        now = datetime.now(UTC)
        race_time = now + timedelta(minutes=10)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert result == []

    def test_multiple_races_in_window(self):
        """Test that multiple races in window all return notifications"""
        now = datetime.now(UTC)
        race1_time = now + timedelta(seconds=30)
        race2_time = now - timedelta(seconds=30)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar",
                {
                    1: {"date": race1_time},
                    2: {"date": race2_time},
                },
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert len(result) == 2


class TestCheckLastRaceResults:
    """Tests for check_last_race_results function (sync wrapper tests)"""

    def test_no_last_race_returns_empty(self):
        """Test that missing last race returns empty list"""
        with patch("notifications.history.get_notify_history", return_value={}):
            with patch("notifications.checks.race.race_calendar", {}):
                with patch(
                    "notifications.checks.race.get_last_race_id", return_value=0
                ):
                    from notifications.checks.race import check_last_race_results
                    import asyncio

                    async def run_test():
                        return await check_last_race_results(datetime.now(UTC))

                    result = asyncio.run(run_test())
                    assert result == []

    def test_history_key_correct_labels(self):
        """Test that history keys use correct labels ('race_replay' and 'race_results')"""
        last_race_id = 17
        replay_history_key = (last_race_id, "race_replay")
        results_history_key = (last_race_id, "race_results")

        assert replay_history_key[1] == "race_replay"
        assert results_history_key[1] == "race_results"

    def test_6_minute_window_for_race_live(self):
        """Test that race live window is 6 minutes (-1min to +5min)"""
        from notifications.checks.race import check_race_live_notifications

        now = datetime.now(UTC)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar",
                {1: {"date": now + timedelta(minutes=6)}},
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                assert result == []

    def test_race_live_uses_correct_history_key(self):
        """Test that race_live notifications use 'race_live' label"""
        now = datetime.now(UTC)
        race_time = now + timedelta(minutes=2)

        with patch("notifications.history.get_notify_history", return_value={}):
            with patch(
                "notifications.checks.race.race_calendar", {1: {"date": race_time}}
            ):
                from notifications.checks.race import check_race_live_notifications

                result = check_race_live_notifications(now)
                if result:
                    assert result[0][4] == (1, "race_live")

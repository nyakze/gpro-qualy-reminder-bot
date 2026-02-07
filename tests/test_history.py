"""Tests for notification history module"""

import os
from datetime import datetime, timedelta, UTC
from unittest.mock import patch

import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestHistorySizeLimit:
    """Tests for _enforce_history_size_limit function"""

    def test_empty_history_unchanged(self):
        """Test that empty history is returned unchanged"""
        from notifications.history import _enforce_history_size_limit

        history = {}
        result = _enforce_history_size_limit(history)
        assert result == {}
        assert result is history

    def test_history_under_limit_unchanged(self):
        """Test that history under limit is returned unchanged"""
        from notifications.history import _enforce_history_size_limit

        now = datetime.now(UTC)
        history = {
            (1, "48h"): now,
            (2, "24h"): now,
        }
        result = _enforce_history_size_limit(history)
        assert len(result) == 2
        assert result is history

    def test_history_over_limit_trims_oldest(self):
        """Test that history over limit removes oldest entries"""
        from notifications.history import _enforce_history_size_limit, MAX_HISTORY_SIZE

        now = datetime.now(UTC)
        old = now - timedelta(hours=1)
        newer = now

        history = {}
        for i in range(MAX_HISTORY_SIZE + 3):
            timestamp = old if i < 3 else newer
            history[(i, "label")] = timestamp

        result = _enforce_history_size_limit(history)
        assert len(result) == MAX_HISTORY_SIZE
        assert (0, "label") not in result
        assert (1, "label") not in result
        assert (2, "label") not in result
        assert (3, "label") in result


class TestIsAlreadyNotified:
    """Tests for is_already_notified function"""

    def setup_method(self):
        """Reset notification history before each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def teardown_method(self):
        """Clean up after each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def test_not_notified_returns_false(self):
        """Test that missing notification returns False"""
        from notifications.history import is_already_notified

        result = is_already_notified(1, "48h")
        assert result is False

    def test_recently_notified_returns_true(self):
        """Test that recent notification returns True"""
        from notifications.history import is_already_notified, mark_notified

        mark_notified(1, "48h")
        result = is_already_notified(1, "48h")
        assert result is True

    def test_old_notification_cleaned_up(self):
        """Test that old notifications are cleaned up and return False"""
        from notifications.history import is_already_notified, set_notify_history

        old_time = datetime.now(UTC) - timedelta(hours=24 * 30 + 1)
        set_notify_history({(1, "48h"): old_time})

        result = is_already_notified(1, "48h")
        assert result is False

    def test_different_label_not_blocked(self):
        """Test that different labels are tracked separately"""
        from notifications.history import is_already_notified, mark_notified

        mark_notified(1, "48h")
        result = is_already_notified(1, "24h")
        assert result is False


class TestMarkNotified:
    """Tests for mark_notified function"""

    def setup_method(self):
        """Reset notification history before each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def teardown_method(self):
        """Clean up after each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def test_mark_notified_adds_entry(self):
        """Test that mark_notified adds an entry"""
        from notifications.history import mark_notified, get_notify_history

        mark_notified(1, "48h")
        history = get_notify_history()
        assert (1, "48h") in history

    def test_mark_notified_sets_current_time(self):
        """Test that mark_notified sets current timestamp"""
        from notifications.history import mark_notified, get_notify_history
        from datetime import datetime, UTC

        before = datetime.now(UTC)
        mark_notified(1, "48h")
        after = datetime.now(UTC)

        history = get_notify_history()
        assert (1, "48h") in history
        entry_time = history[(1, "48h")]
        assert before <= entry_time <= after

    def test_mark_notified_updates_existing(self):
        """Test that mark_notified updates existing entry"""
        from notifications.history import mark_notified, get_notify_history
        from notifications.history import set_notify_history

        set_notify_history({(1, "48h"): datetime.now(UTC)})
        old_time = get_notify_history()[(1, "48h")]

        mark_notified(1, "48h")
        new_time = get_notify_history()[(1, "48h")]

        assert new_time > old_time


class TestCleanupOldEntries:
    """Tests for cleanup_old_entries function"""

    def setup_method(self):
        """Reset notification history before each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def teardown_method(self):
        """Clean up after each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def test_removes_expired_entries(self):
        """Test that cleanup_old_entries removes expired entries"""
        from notifications.history import (
            cleanup_old_entries,
            set_notify_history,
            get_notify_history,
        )

        now = datetime.now(UTC)
        old_time = now - timedelta(hours=24 * 30 + 1)
        recent_time = now

        set_notify_history(
            {
                (1, "48h"): old_time,
                (2, "24h"): recent_time,
            }
        )

        cleanup_old_entries()

        history = get_notify_history()
        assert (1, "48h") not in history
        assert (2, "24h") in history

    def test_preserves_recent_entries(self):
        """Test that cleanup_old_entries preserves recent entries"""
        from notifications.history import (
            cleanup_old_entries,
            set_notify_history,
            get_notify_history,
        )

        now = datetime.now(UTC)
        recent_time = now - timedelta(hours=1)

        set_notify_history(
            {
                (1, "48h"): recent_time,
                (2, "24h"): recent_time,
            }
        )

        cleanup_old_entries()

        history = get_notify_history()
        assert len(history) == 2


class TestNotifyHistoryPersistence:
    """Tests for notification history file persistence"""

    def setup_method(self):
        """Reset notification history before each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def teardown_method(self):
        """Clean up after each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def test_save_and_load_notify_history(self):
        """Test that notification history can be saved and loaded"""
        from notifications.history import save_notify_history, load_notify_history
        from notifications.history import set_notify_history

        now = datetime.now(UTC)
        test_history = {
            (1, "48h"): now,
            (2, "24h"): now - timedelta(hours=12),
        }
        set_notify_history(test_history)

        save_notify_history()
        loaded = load_notify_history()

        assert len(loaded) == 2
        assert (1, "48h") in loaded
        assert (2, "24h") in loaded

    def test_load_nonexistent_file_returns_empty(self):
        """Test that loading nonexistent file returns empty history"""
        from notifications.history import load_notify_history

        with patch(
            "notifications.history._get_history_file_path",
            return_value="/nonexistent/path.json",
        ):
            from notifications.history import set_notify_history

            set_notify_history({})
            loaded = load_notify_history()
            assert loaded == {}


class TestSharedNotifyHistory:
    """Tests for shared notify_history instance"""

    def setup_method(self):
        """Reset notification history before each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def teardown_method(self):
        """Clean up after each test"""
        from notifications.history import set_notify_history

        set_notify_history({})

    def test_set_notify_history_updates_global(self):
        """Test that set_notify_history updates the global instance"""
        from notifications.history import set_notify_history, get_notify_history

        test_data = {(1, "test"): datetime.now(UTC)}
        set_notify_history(test_data)

        result = get_notify_history()
        assert result is test_data

    def test_notify_history_reference_points_to_same_dict(self):
        """Test that notify_history reference updates when _notify_history changes"""
        from notifications.history import (
            set_notify_history,
            get_notify_history,
        )

        test_data = {(1, "test"): datetime.now(UTC)}
        set_notify_history(test_data)

        current = get_notify_history()
        assert current is test_data

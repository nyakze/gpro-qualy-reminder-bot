"""Tests for backup scheduling and persisted admin preferences."""

import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch


def test_same_day_backup_before_target_runs_today():
    from infra import backup

    class ThursdayBeforeRun(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 8, 13, 1, 0, tzinfo=UTC)

    with patch.object(backup, "datetime", ThursdayBeforeRun):
        seconds = backup._seconds_until_next_day(target_day=3, target_hour=2)

    assert seconds == 60 * 60


def test_same_day_backup_after_target_runs_next_week():
    from infra import backup

    class ThursdayAfterRun(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, 8, 13, 3, 0, tzinfo=UTC)

    with patch.object(backup, "datetime", ThursdayAfterRun):
        seconds = backup._seconds_until_next_day(target_day=3, target_hour=2)

    assert seconds == 6 * 24 * 60 * 60 + 23 * 60 * 60


def test_telegram_backup_preference_survives_reload():
    from infra import backup
    from notifications.users import storage

    admin_id = 12345
    storage.users_data.clear()

    backup.set_telegram_backup_enabled(admin_id, True)

    saved = json.loads(Path(storage.USERS_FILE).read_text(encoding="utf-8"))
    assert saved[str(admin_id)]["telegram_backup_enabled"] is True

    storage.users_data.clear()
    storage.load_users_data()

    assert backup.is_telegram_backup_enabled(admin_id) is True

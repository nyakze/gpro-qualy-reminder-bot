"""Tests for user data storage and persistence"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def reset_user_data():
    """Reset user data before and after each test"""
    from notifications.users.storage import users_data

    users_data.clear()
    yield
    users_data.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "language": "gb",
        "timezone": "Europe/London",
        "notifications": {
            "48h": True,
            "24h": True,
            "2h": True,
            "10min": True,
        },
        "group": "P15",
        "gpro_lang": "gb",
        "ui_lang": "gb",
        "website_mode": "classic",
    }


class TestUserStorageLoad:
    """Tests for load_users_data function"""

    def test_load_users_data_success(self, sample_user_data):
        """Test loading user data from valid JSON file"""
        from notifications.users.storage import load_users_data, users_data

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            # Write data with string keys (as stored in file)
            json.dump({"12345": sample_user_data, "67890": sample_user_data}, f)
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                load_users_data()

                assert len(users_data) == 2
                assert 12345 in users_data  # Should be converted to int
                assert 67890 in users_data
                assert users_data[12345]["language"] == "gb"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_users_data_file_not_found(self):
        """Test loading when file doesn't exist"""
        from notifications.users.storage import load_users_data, users_data

        with patch("notifications.users.storage.USERS_FILE", "/nonexistent/path.json"):
            load_users_data()
            assert len(users_data) == 0

    def test_load_users_data_corrupted_json(self):
        """Test loading corrupted JSON file"""
        from notifications.users.storage import load_users_data, users_data

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json {{{")
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                load_users_data()
                assert len(users_data) == 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_users_data_invalid_keys(self):
        """Test loading with invalid/non-integer keys fails gracefully"""
        from notifications.users.storage import load_users_data, users_data

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            # Write data with non-integer keys that can't be converted
            json.dump({"user123": {"language": "gb"}, "456": {"language": "ru"}}, f)
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                load_users_data()
                # Should fail gracefully and load nothing when keys are invalid
                assert len(users_data) == 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_failed_recovery_preserves_loaded_memory(self, tmp_path, monkeypatch):
        """A transient disk failure must not erase the live in-memory cache."""
        from notifications.users import storage

        storage.users_data[999] = {"language": "gb"}
        monkeypatch.setattr(
            storage, "USERS_FILE", str(tmp_path / "missing" / "users_data.json")
        )

        storage.load_users_data()

        assert storage.users_data == {999: {"language": "gb"}}


class TestUserStorageSave:
    """Tests for save_users_data function"""

    def test_save_users_data_success(self, sample_user_data):
        """Test saving user data to JSON file"""
        from notifications.users.storage import save_users_data, users_data

        # Set up in-memory data with int keys
        users_data[12345] = sample_user_data.copy()
        users_data[67890] = sample_user_data.copy()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                save_users_data()

                # Verify file was created and has string keys
                with open(temp_path, "r") as f:
                    saved_data = json.load(f)

                assert "12345" in saved_data
                assert "67890" in saved_data
                assert saved_data["12345"]["language"] == "gb"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_save_users_data_atomic_write(self, sample_user_data):
        """Test atomic write doesn't corrupt file on failure"""
        from notifications.users.storage import save_users_data, users_data

        users_data[12345] = sample_user_data.copy()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            # Write initial valid data
            json.dump({"existing": "data"}, f)
            temp_path = f.name

        try:
            # Make the directory read-only to force failure
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                with patch(
                    "tempfile.mkstemp", side_effect=PermissionError("No permission")
                ):
                    save_users_data()

                    # Original file should still exist and be valid
                    with open(temp_path, "r") as f:
                        data = json.load(f)
                    assert data == {"existing": "data"}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_save_empty_users_data(self):
        """Test saving empty user data"""
        from notifications.users.storage import save_users_data, users_data

        users_data.clear()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                save_users_data()

                with open(temp_path, "r") as f:
                    saved_data = json.load(f)

                assert saved_data == {}
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestUserStorageMigration:
    """Tests for data migration between versions"""

    def test_migration_string_to_int_keys(self):
        """Test migration from string keys to int keys"""
        from notifications.users.storage import load_users_data, users_data

        # Simulate old format with string keys
        old_data = {
            "12345": {
                "language": "gb",
                "group": "P1",
                "custom_notifications": [{"enabled": False}],
            },
            "67890": {
                "language": "ru",
                "group": "M2",
            },
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(old_data, f)
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                load_users_data()

                # Keys should be integers now
                assert all(isinstance(k, int) for k in users_data.keys())
                assert 12345 in users_data
                assert 67890 in users_data
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_migration_adds_missing_fields(self):
        """Test that missing fields get default values on load"""
        from notifications.users.storage import load_users_data, users_data

        # Old data missing some new fields
        old_data = {
            "12345": {
                "language": "gb",
                # Missing ui_lang, website_mode, snooze_tracking
            }
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(old_data, f)
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                load_users_data()

                # Data should load even with missing fields
                assert 12345 in users_data
                assert users_data[12345]["language"] == "gb"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_preserve_existing_data_on_save(self):
        """Test that save preserves all existing user data"""
        from notifications.users.storage import (
            save_users_data,
            load_users_data,
            users_data,
        )

        # Complex user data
        complex_data = {
            12345: {
                "language": "gb",
                "timezone": "Europe/London",
                "notifications": {"48h": True, "24h": False},
                "custom_notifications": [
                    {"enabled": True, "hours_before": 12.0},
                    {"enabled": False, "hours_before": None},
                ],
                "group": "P15",
                "gpro_lang": "gb",
                "ui_lang": "gb",
                "website_mode": "classic",
                "completed_quali": 5,
                "active_snoozes": {
                    "1_48h_20250715120000": {
                        "until": "2025-07-15T12:00:00+00:00",
                        "notification_type": "48h",
                        "race_id": 1,
                    }
                },
            }
        }

        users_data.update(complex_data)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                save_users_data()

                # Clear and reload
                users_data.clear()
                load_users_data()

                # Verify all data preserved
                assert 12345 in users_data
                user = users_data[12345]
                assert user["language"] == "gb"
                assert user["group"] == "P15"
                assert user["completed_quali"] == 5
                assert "active_snoozes" in user
                assert "1_48h_20250715120000" in user["active_snoozes"]
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestUserStorageConcurrency:
    """Tests for storage operation safety"""

    def test_multiple_saves_atomic(self):
        """Test multiple saves don't corrupt data"""
        from notifications.users.storage import save_users_data, users_data
        import threading

        def save_user_data(user_id):
            users_data[user_id] = {"language": "gb", "test_id": user_id}
            save_users_data()

        # Clear any existing data
        users_data.clear()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            with patch("notifications.users.storage.USERS_FILE", temp_path):
                # Simulate concurrent saves
                threads = []
                for i in range(10):
                    t = threading.Thread(target=save_user_data, args=(i,))
                    threads.append(t)
                    t.start()

                for t in threads:
                    t.join()

                # File should contain all users (or be valid at minimum)
                with open(temp_path, "r") as f:
                    final_data = json.load(f)

                # At minimum, file should be valid JSON
                assert isinstance(final_data, dict)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestUserStorageRecovery:
    """Tests for automatic recovery from classic backups."""

    def test_missing_primary_restores_latest_valid_backup(
        self, tmp_path, sample_user_data, monkeypatch
    ):
        from notifications.users import storage

        users_file = tmp_path / "users_data.json"
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        older = backup_dir / "users_data_20260101_020000.json"
        newer_invalid = backup_dir / "users_data_20260108_020000.json"
        older.write_text(json.dumps({"12345": sample_user_data}), encoding="utf-8")
        newer_invalid.write_text("broken", encoding="utf-8")
        os.utime(older, (1, 1))
        os.utime(newer_invalid, (2, 2))
        monkeypatch.setattr(storage, "USERS_FILE", str(users_file))

        storage.load_users_data()

        assert 12345 in storage.users_data
        assert (
            json.loads(users_file.read_text(encoding="utf-8"))["12345"]["group"]
            == "P15"
        )

    def test_corrupt_primary_is_quarantined_before_restore(
        self, tmp_path, sample_user_data, monkeypatch
    ):
        from notifications.users import storage

        users_file = tmp_path / "users_data.json"
        users_file.write_text("corrupt primary", encoding="utf-8")
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        backup = backup_dir / "users_data_20260101_020000.json"
        backup.write_text(json.dumps({"67890": sample_user_data}), encoding="utf-8")
        monkeypatch.setattr(storage, "USERS_FILE", str(users_file))

        storage.load_users_data()

        assert 67890 in storage.users_data
        quarantined = list(tmp_path.glob("users_data.json.corrupt_*"))
        assert len(quarantined) == 1
        assert quarantined[0].read_text(encoding="utf-8") == "corrupt primary"

    def test_empty_backup_is_not_used(self, tmp_path, monkeypatch):
        from notifications.users import storage

        users_file = tmp_path / "users_data.json"
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "users_data_20260101_020000.json").write_text(
            "{}", encoding="utf-8"
        )
        monkeypatch.setattr(storage, "USERS_FILE", str(users_file))

        storage.load_users_data()

        assert storage.users_data == {}
        assert not users_file.exists()

    def test_unrelated_json_is_not_considered_a_backup(
        self, tmp_path, sample_user_data, monkeypatch
    ):
        from notifications.users import storage

        users_file = tmp_path / "users_data.json"
        backup_dir = tmp_path / "backup"
        backup_dir.mkdir()
        (backup_dir / "recovery_test_artifact_users_data_20260101.json").write_text(
            json.dumps({"12345": sample_user_data}), encoding="utf-8"
        )
        monkeypatch.setattr(storage, "USERS_FILE", str(users_file))

        storage.load_users_data()

        assert storage.users_data == {}
        assert not users_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

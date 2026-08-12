"""Tests for user notification interactions - toggles, groups, and settings"""

import pytest

import os
import sys

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


class TestToggleNotification:
    """Tests for individual notification toggle functionality"""

    def test_toggle_notification_enable_to_disable(self):
        """Test toggling notification from enabled to disabled"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 11111
        get_user_status(user_id)

        initial_state = is_notification_enabled(user_id, "48h")
        assert initial_state is True

        new_state = toggle_notification(user_id, "48h")
        assert new_state is False

        result = is_notification_enabled(user_id, "48h")
        assert result is False

    def test_toggle_notification_disable_to_enable(self):
        """Test toggling notification from disabled to enabled"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 22222
        get_user_status(user_id)

        toggle_notification(user_id, "48h")
        new_state = toggle_notification(user_id, "48h")

        assert new_state is True
        result = is_notification_enabled(user_id, "48h")
        assert result is True

    def test_toggle_all_notification_types(self):
        """Test toggling all notification types"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 33333
        get_user_status(user_id)

        notification_types = [
            "72h",
            "48h",
            "24h",
            "2h",
            "10min",
            "opens_soon",
            "quali_results",
            "race_live",
            "race_replay",
            "race_results",
            "new_season_reminder",
        ]

        for notif_type in notification_types:
            toggle_notification(user_id, notif_type)
            assert is_notification_enabled(user_id, notif_type) is False

    def test_default_all_notifications_enabled(self):
        """Test that all notifications are enabled by default for new user"""
        from notifications import get_user_status, is_notification_enabled

        user_id = 44444
        get_user_status(user_id)

        all_enabled = is_notification_enabled(user_id, "48h")
        assert all_enabled is True


class TestMassEnableDisable:
    """Tests for mass enabling/disabling notifications"""

    def test_disable_all_notifications(self):
        """Test disabling all notifications at once"""
        from notifications import (
            get_user_status,
            is_notification_enabled,
            set_user_group,
        )

        user_id = 11111
        get_user_status(user_id)
        set_user_group(user_id, "Pro")

        user_status = get_user_status(user_id)[0]
        notif_types = list(user_status["notifications"].keys())

        for notif_type in notif_types:
            user_status["notifications"][notif_type] = False

        from notifications.users.storage import save_users_data

        save_users_data()

        for notif_type in notif_types:
            assert is_notification_enabled(user_id, notif_type) is False

    def test_enable_all_notifications(self):
        """Test enabling all notifications at once"""
        from notifications import (
            get_user_status,
            is_notification_enabled,
            set_user_group,
        )

        user_id = 22222
        get_user_status(user_id)
        set_user_group(user_id, "Pro")

        user_status = get_user_status(user_id)[0]
        notif_types = list(user_status["notifications"].keys())

        for notif_type in notif_types:
            user_status["notifications"][notif_type] = False

        for notif_type in notif_types:
            user_status["notifications"][notif_type] = True

        from notifications.users.storage import save_users_data

        save_users_data()

        for notif_type in notif_types:
            assert is_notification_enabled(user_id, notif_type) is True

    def test_partial_disable_then_enable_all(self):
        """Test enabling all after partial disable"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 33333
        get_user_status(user_id)

        toggle_notification(user_id, "48h")
        toggle_notification(user_id, "24h")

        user_status = get_user_status(user_id)[0]
        notif_types = list(user_status["notifications"].keys())

        for notif_type in notif_types:
            user_status["notifications"][notif_type] = True

        from notifications.users.storage import save_users_data

        save_users_data()

        for notif_type in notif_types:
            assert is_notification_enabled(user_id, notif_type) is True


class TestNotificationCategories:
    """Tests for notification category operations"""

    def test_category_before_qualifying_types(self):
        """Test that before_qualifying category has correct types"""
        from handlers.callbacks.notifications import NOTIFICATION_CATEGORIES

        category = NOTIFICATION_CATEGORIES["before_qualifying"]
        assert "72h" in category["types"]
        assert "48h" in category["types"]
        assert "24h" in category["types"]
        assert "2h" in category["types"]
        assert "10min" in category["types"]

    def test_category_qualifying_events_types(self):
        """Test that qualifying_events category has correct types"""
        from handlers.callbacks.notifications import NOTIFICATION_CATEGORIES

        category = NOTIFICATION_CATEGORIES["qualifying_events"]
        assert "opens_soon" in category["types"]
        assert "quali_results" in category["types"]

    def test_category_race_events_types(self):
        """Test that race_events category has correct types"""
        from handlers.callbacks.notifications import NOTIFICATION_CATEGORIES

        category = NOTIFICATION_CATEGORIES["race_events"]
        assert "race_live" in category["types"]
        assert "race_replay" in category["types"]
        assert "race_results" in category["types"]

    def test_disable_category(self):
        """Test disabling all notifications in a category"""
        from notifications import get_user_status, is_notification_enabled

        user_id = 99901
        from notifications import get_user_status as load_user

        load_user(user_id)

        user_status = get_user_status(user_id)[0]

        category_types = ["72h", "48h", "24h", "2h", "10min"]
        for notif_type in category_types:
            user_status["notifications"][notif_type] = False

        from notifications.users.storage import save_users_data

        save_users_data()

        for notif_type in category_types:
            assert is_notification_enabled(user_id, notif_type) is False

        assert is_notification_enabled(user_id, "opens_soon") is True
        assert is_notification_enabled(user_id, "race_live") is True


class TestUserGroupSetting:
    """Tests for user group setting functionality"""

    def test_set_user_group_pro(self):
        """Test setting user group to Pro"""
        from notifications import get_user_status, set_user_group

        user_id = 11111
        get_user_status(user_id)

        result = set_user_group(user_id, "Pro")
        assert result is None

        user_status = get_user_status(user_id)[0]
        assert user_status["group"] == "Pro"

    def test_set_user_group_amateur(self):
        """Test setting user group to Amateur"""
        from notifications import get_user_status, set_user_group

        user_id = 22222
        get_user_status(user_id)

        set_user_group(user_id, "Amateur")

        user_status = get_user_status(user_id)[0]
        assert user_status["group"] == "Amateur"

    def test_set_user_group_rookie(self):
        """Test setting user group to Rookie"""
        from notifications import get_user_status, set_user_group

        user_id = 33333
        get_user_status(user_id)

        set_user_group(user_id, "Rookie")

        user_status = get_user_status(user_id)[0]
        assert user_status["group"] == "Rookie"

    def test_set_user_group_master(self):
        """Test setting user group to Master"""
        from notifications import get_user_status, set_user_group

        user_id = 44444
        get_user_status(user_id)

        set_user_group(user_id, "Master")

        user_status = get_user_status(user_id)[0]
        assert user_status["group"] == "Master"

    def test_default_group_is_none(self):
        """Test that new user has no group set by default"""
        from notifications import get_user_status

        user_id = 55555
        get_user_status(user_id)

        user_status = get_user_status(user_id)[0]
        assert user_status["group"] is None


class TestNotificationSendingConditions:
    """Tests for notification sending based on user settings"""

    def test_notification_sent_when_enabled(self):
        """Test that notification is sent when user has it enabled"""
        from notifications import get_user_status, is_notification_enabled

        user_id = 99902
        get_user_status(user_id)

        assert is_notification_enabled(user_id, "48h") is True

    def test_notification_blocked_when_disabled(self):
        """Test that notification is blocked when user has it disabled"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 22222
        get_user_status(user_id)

        toggle_notification(user_id, "48h")

        assert is_notification_enabled(user_id, "48h") is False

    def test_race_live_requires_enabled_setting(self):
        """Test race_live notification check"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 33333
        get_user_status(user_id)

        assert is_notification_enabled(user_id, "race_live") is True

        toggle_notification(user_id, "race_live")
        assert is_notification_enabled(user_id, "race_live") is False

    def test_quali_results_requires_enabled_setting(self):
        """Test quali_results notification check"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 44444
        get_user_status(user_id)

        assert is_notification_enabled(user_id, "quali_results") is True

        toggle_notification(user_id, "quali_results")
        assert is_notification_enabled(user_id, "quali_results") is False

    def test_opens_soon_requires_enabled_setting(self):
        """Test opens_soon notification check"""
        from notifications import (
            get_user_status,
            toggle_notification,
            is_notification_enabled,
        )

        user_id = 55555
        get_user_status(user_id)

        assert is_notification_enabled(user_id, "opens_soon") is True

        toggle_notification(user_id, "opens_soon")
        assert is_notification_enabled(user_id, "opens_soon") is False

    def test_custom_notifications_require_enabled_setting(self):
        """Test custom notification check via is_notification_enabled"""
        from notifications import (
            get_user_status,
            is_notification_enabled,
            set_custom_notification,
        )

        user_id = 66666
        get_user_status(user_id)

        # Custom notifications default to disabled (False)
        assert is_notification_enabled(user_id, "custom_1") is False
        assert is_notification_enabled(user_id, "custom_2") is False

        # Enable custom_1 with 8 hours before
        set_custom_notification(user_id, 0, 8)
        assert is_notification_enabled(user_id, "custom_1") is True
        assert is_notification_enabled(user_id, "custom_2") is False

        # Enable custom_2 with 12 hours before
        set_custom_notification(user_id, 1, 12)
        assert is_notification_enabled(user_id, "custom_1") is True
        assert is_notification_enabled(user_id, "custom_2") is True

        # Disable custom_1
        set_custom_notification(user_id, 0, None)
        assert is_notification_enabled(user_id, "custom_1") is False
        assert is_notification_enabled(user_id, "custom_2") is True

    def test_label_to_setting_mapping(self):
        """Test that notification labels map to correct settings"""
        from notifications import get_user_status, is_notification_enabled

        user_id = 77777
        get_user_status(user_id)

        label_map = {
            "72h": "72h",
            "48h": "48h",
            "24h": "24h",
            "2h": "2h",
            "10min": "10min",
        }

        for label, setting in label_map.items():
            result = is_notification_enabled(user_id, setting)
            assert result is True

    def test_blocked_user_receives_no_notifications(self):
        """Test that blocked users are filtered out"""
        from notifications import get_user_status
        from notifications.users.blocked import mark_user_blocked, is_user_blocked

        user_id = 88888
        get_user_status(user_id)

        mark_user_blocked(user_id)
        assert is_user_blocked(user_id) is True


class TestUserRegistration:
    """Tests for user registration via /start"""

    def test_new_user_gets_default_preferences(self):
        """Test that new user gets all default notification preferences"""
        from notifications import get_user_status

        user_id = 111111
        user_status, was_new = get_user_status(user_id)

        assert was_new is True
        assert user_status["notifications"]["48h"] is True
        assert user_status["notifications"]["24h"] is True
        assert user_status["notifications"]["2h"] is True
        assert user_status["notifications"]["10min"] is True
        assert user_status["notifications"]["opens_soon"] is True

    def test_existing_user_not_marked_new(self):
        """Test that existing user is not marked as new"""
        from notifications import get_user_status

        user_id = 222222
        get_user_status(user_id)

        user_status, was_new = get_user_status(user_id)
        assert was_new is False

    def test_new_user_initialized_with_defaults(self):
        """Test that new user is initialized with all default fields"""
        from notifications import get_user_status

        user_id = 333333
        user_status, was_new = get_user_status(user_id)

        assert was_new is True
        assert user_status["group"] is None
        assert user_status["gpro_lang"] == "gb"
        assert user_status["ui_lang"] == "gb"
        assert user_status["timezone"] == "UTC"
        assert user_status["website_mode"] == "classic"


class TestLanguageSettings:
    """Tests for user language settings"""

    def test_set_user_language(self):
        """Test setting user GPRO language"""
        from notifications import get_user_status, set_user_language, get_user_language

        user_id = 11111
        get_user_status(user_id)

        result = set_user_language(user_id, "ru")
        assert result is True

        lang = get_user_language(user_id)
        assert lang == "ru"

    def test_set_invalid_language(self):
        """Test setting invalid language returns False"""
        from notifications import get_user_status, set_user_language

        user_id = 22222
        get_user_status(user_id)

        result = set_user_language(user_id, "invalid")
        assert result is False

    def test_set_ui_language(self):
        """Test setting user UI language"""
        from notifications import (
            get_user_status,
            set_user_ui_language,
            get_user_ui_language,
        )

        user_id = 33333
        get_user_status(user_id)

        result = set_user_ui_language(user_id, "ru")
        assert result is True

        lang = get_user_ui_language(user_id)
        assert lang == "ru"

    def test_set_invalid_ui_language(self):
        """Test setting invalid UI language returns False"""
        from notifications import get_user_status, set_user_ui_language

        user_id = 44444
        get_user_status(user_id)

        result = set_user_ui_language(user_id, "xx")
        assert result is False


class TestTimezoneSetting:
    """Tests for user timezone setting"""

    def test_set_user_timezone(self):
        """Test setting user timezone"""
        from notifications import get_user_status, set_user_timezone, get_user_timezone

        user_id = 11111
        get_user_status(user_id)

        result = set_user_timezone(user_id, "Europe/Moscow")
        assert result is True

        tz = get_user_timezone(user_id)
        assert tz == "Europe/Moscow"

    def test_set_invalid_timezone(self):
        """Test setting invalid timezone returns False"""
        from notifications import get_user_status, set_user_timezone

        user_id = 22222
        get_user_status(user_id)

        result = set_user_timezone(user_id, "Invalid/Timezone")
        assert result is False


class TestWebsiteMode:
    """Tests for user website mode setting"""

    def test_set_website_mode_classic(self):
        """Test setting website mode to classic"""
        from notifications import (
            get_user_status,
            set_user_website_mode,
            get_user_website_mode,
        )

        user_id = 11111
        get_user_status(user_id)

        result = set_user_website_mode(user_id, "classic")
        assert result is True

        mode = get_user_website_mode(user_id)
        assert mode == "classic"

    def test_set_website_mode_app(self):
        """Test setting website mode to app"""
        from notifications import (
            get_user_status,
            set_user_website_mode,
            get_user_website_mode,
        )

        user_id = 22222
        get_user_status(user_id)

        set_user_website_mode(user_id, "app")
        mode = get_user_website_mode(user_id)
        assert mode == "app"

    def test_set_invalid_website_mode(self):
        """Test setting invalid website mode returns False"""
        from notifications import get_user_status, set_user_website_mode

        user_id = 33333
        get_user_status(user_id)

        result = set_user_website_mode(user_id, "mobile")
        assert result is False


class TestUserProfile:
    """Tests for user profile updates"""

    def test_update_username(self):
        """Test updating user username"""
        from notifications import get_user_status, update_user_profile

        user_id = 11111
        get_user_status(user_id)

        result = update_user_profile(user_id, username="testuser")
        assert result is True

        profile = get_user_status(user_id)[0]
        assert profile["username"] == "testuser"

    def test_update_first_name(self):
        """Test updating user first name"""
        from notifications import get_user_status, update_user_profile

        user_id = 22222
        get_user_status(user_id)

        result = update_user_profile(user_id, first_name="Test")
        assert result is True

        profile = get_user_status(user_id)[0]
        assert profile["first_name"] == "Test"

    def test_update_language_code(self):
        """Test updating Telegram language code"""
        from notifications import get_user_status, update_user_profile

        user_id = 33333
        get_user_status(user_id)

        result = update_user_profile(user_id, tg_language_code="ru")
        assert result is True

        profile = get_user_status(user_id)[0]
        assert profile["tg_language_code"] == "ru"

    def test_get_user_profile(self):
        """Test getting user profile"""
        from notifications import get_user_status, update_user_profile, get_user_profile

        user_id = 44444
        get_user_status(user_id)
        update_user_profile(
            user_id, username="testuser", first_name="Test", tg_language_code="en"
        )

        profile = get_user_profile(user_id)
        assert profile["username"] == "testuser"
        assert profile["first_name"] == "Test"
        assert profile["tg_language_code"] == "en"

    def test_new_user_has_last_interaction(self):
        """Test that new user is created with last_interaction timestamp (registration is an interaction)"""
        from notifications import get_user_status

        user_id = 55555
        user_status, was_new = get_user_status(user_id)

        assert was_new is True
        assert "last_interaction" in user_status
        assert user_status["last_interaction"] is not None

    def test_update_user_profile_updates_last_interaction(self):
        """Test that update_user_profile updates last_interaction"""
        from notifications import get_user_status, update_user_profile
        import time

        user_id = 66666
        get_user_status(user_id)
        initial_time = get_user_status(user_id)[0]["last_interaction"]

        time.sleep(0.1)
        update_user_profile(user_id, username="testuser")

        updated_time = get_user_status(user_id)[0]["last_interaction"]
        assert updated_time != initial_time

    def test_unchanged_profile_does_not_write_activity_immediately(self):
        """Repeated interactions inside the debounce window avoid a full JSON write."""
        from unittest.mock import patch

        from notifications import get_user_status
        from notifications.users import core

        user_id = 77777
        get_user_status(user_id)

        with patch.object(core, "save_users_data") as save_users_data:
            changed = core.update_user_profile(user_id)

        assert changed is False
        save_users_data.assert_not_called()


class TestFormatRelativeTime:
    """Tests for format_relative_time helper function"""

    def test_just_now(self):
        """Test 'just now' for very recent timestamps"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC

        now = datetime.now(UTC).isoformat()
        assert format_relative_time(now) == "just now"

    def test_minutes_ago(self):
        """Test minutes ago"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(minutes=5)).isoformat()
        assert format_relative_time(past) == "5 min ago"

    def test_single_minute_ago(self):
        """Test singular minute"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(minutes=1)).isoformat()
        assert format_relative_time(past) == "1 min ago"

    def test_hours_ago(self):
        """Test hours ago"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(hours=3)).isoformat()
        assert format_relative_time(past) == "3 hours ago"

    def test_single_hour_ago(self):
        """Test singular hour"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
        assert format_relative_time(past) == "1 hour ago"

    def test_days_ago(self):
        """Test days ago"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(days=10)).isoformat()
        assert format_relative_time(past) == "10 days ago"

    def test_single_day_ago(self):
        """Test singular day"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
        assert format_relative_time(past) == "1 day ago"

    def test_months_ago(self):
        """Test months ago"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(days=60)).isoformat()
        assert format_relative_time(past) == "2 months ago"

    def test_years_ago(self):
        """Test years ago"""
        from handlers.admin_commands import format_relative_time
        from datetime import datetime, UTC, timedelta

        past = (datetime.now(UTC) - timedelta(days=400)).isoformat()
        assert format_relative_time(past) == "1 year ago"

    def test_none_timestamp(self):
        """Test None timestamp returns dash"""
        from handlers.admin_commands import format_relative_time

        assert format_relative_time(None) == "—"

    def test_invalid_timestamp(self):
        """Test invalid timestamp returns dash"""
        from handlers.admin_commands import format_relative_time

        assert format_relative_time("invalid-date") == "—"

    def test_empty_string_timestamp(self):
        """Test empty string timestamp returns dash"""
        from handlers.admin_commands import format_relative_time

        assert format_relative_time("") == "—"


class TestQualiDone:
    """Tests for marking qualification as done"""

    def test_mark_quali_done(self):
        """Test marking quali as done for a race"""
        from notifications import get_user_status, mark_quali_done

        user_id = 11111
        get_user_status(user_id)

        mark_quali_done(user_id, 1)

        user_status = get_user_status(user_id)[0]
        assert user_status["completed_quali"] == 1

    def test_reset_user_status(self):
        """Test resetting user status"""
        from notifications import get_user_status, mark_quali_done, reset_user_status

        user_id = 22222
        get_user_status(user_id)
        mark_quali_done(user_id, 1)

        reset_user_status(user_id)

        user_status = get_user_status(user_id)[0]
        assert user_status["completed_quali"] is None

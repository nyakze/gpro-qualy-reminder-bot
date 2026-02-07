"""Tests for validation functions (group, time input, custom notifications)"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGroupValidation:
    """Test GPRO group input validation"""

    def test_valid_elite_group(self):
        """Test Elite group validation"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("E")
        assert is_valid is True
        assert normalized == "E"
        assert error == ""

    def test_valid_elite_group_lowercase(self):
        """Test Elite group validation (lowercase accepted)"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("e")
        assert is_valid is True
        assert normalized == "E"

    def test_valid_master_group(self):
        """Test Master group validation with numbers"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("M3")
        assert is_valid is True
        assert normalized == "M3"

    def test_valid_pro_group(self):
        """Test Pro group validation"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("P15")
        assert is_valid is True
        assert normalized == "P15"

    def test_valid_amateur_group(self):
        """Test Amateur group validation"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("A42")
        assert is_valid is True
        assert normalized == "A42"

    def test_valid_rookie_group(self):
        """Test Rookie group validation"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("R99")
        assert is_valid is True
        assert normalized == "R99"

    def test_invalid_elite_with_number(self):
        """Test Elite group cannot have numbers"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("E5")
        assert is_valid is False
        assert normalized is None
        assert error != ""

    def test_invalid_format(self):
        """Test invalid group format is rejected"""
        from notifications.validation import validate_group_input

        invalid_formats = [
            "5",  # No letter
            "MP",  # Two letters
            "M",  # Master without number
            "1M",  # Number first
            "E5",  # Elite with number (explicitly rejected)
        ]

        for group in invalid_formats:
            is_valid, normalized, error = validate_group_input(group)
            assert is_valid is False, f"Expected {group} to be invalid"

    def test_master_range_boundaries(self):
        """Test Master group number boundaries (1-5)"""
        from notifications.validation import validate_group_input

        valid_master = ["M1", "M2", "M3", "M4", "M5"]
        for group in valid_master:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is True, f"Expected {group} to be valid"

        invalid_master = ["M0", "M6"]
        for group in invalid_master:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is False, f"Expected {group} to be invalid"

    def test_pro_range_boundaries(self):
        """Test Pro group number boundaries (1-25)"""
        from notifications.validation import validate_group_input

        valid_pro = ["P1", "P12", "P25"]
        for group in valid_pro:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is True, f"Expected {group} to be valid"

        invalid_pro = ["P0", "P26"]
        for group in invalid_pro:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is False, f"Expected {group} to be invalid"

    def test_amateur_range_boundaries(self):
        """Test Amateur group number boundaries (1-80)"""
        from notifications.validation import validate_group_input

        valid_amateur = ["A1", "A40", "A80"]
        for group in valid_amateur:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is True, f"Expected {group} to be valid"

        invalid_amateur = ["A0", "A81"]
        for group in invalid_amateur:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is False, f"Expected {group} to be invalid"

    def test_rookie_range_boundaries(self):
        """Test Rookie group number boundaries (1-150)"""
        from notifications.validation import validate_group_input

        valid_rookie = ["R1", "R75", "R150"]
        for group in valid_rookie:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is True, f"Expected {group} to be valid"

        invalid_rookie = ["R0", "R151"]
        for group in invalid_rookie:
            is_valid, _, _ = validate_group_input(group)
            assert is_valid is False, f"Expected {group} to be invalid"

    def test_leading_zeros_stripped(self):
        """Test that group validation handles input correctly"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("P7")
        assert is_valid is True
        assert normalized == "P7"

    def test_empty_input(self):
        """Test empty input is rejected"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("")
        assert is_valid is False
        assert normalized is None

    def test_whitespace_handling(self):
        """Test whitespace is stripped"""
        from notifications.validation import validate_group_input

        is_valid, normalized, error = validate_group_input("  M3  ")
        assert is_valid is True
        assert normalized == "M3"


class TestTimeInputParsing:
    """Test time input parsing for custom notifications"""

    def test_parse_hours_only(self):
        """Test parsing hours only format"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("12h")
        assert error == ""
        assert hours == 12.0

        hours, error = parse_time_input("24 hours")
        assert error == ""
        assert hours == 24.0

    def test_parse_minutes_only(self):
        """Test parsing minutes only format"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("30m")
        assert error == ""
        assert hours == 0.5

        hours, error = parse_time_input("45 minutes")
        assert error == ""
        assert hours == 0.75

    def test_parse_days_only(self):
        """Test parsing days only format"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("2d")
        assert error == ""
        assert hours == 48.0

        hours, error = parse_time_input("3 days")
        assert error == ""
        assert hours == 72.0

    def test_parse_hours_minutes(self):
        """Test parsing combined hours and minutes"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("2h 30m")
        assert error == ""
        assert hours == 2.5

        hours, error = parse_time_input("1h30m")
        assert error == ""
        assert hours == 1.5

    def test_parse_days_hours_minutes(self):
        """Test parsing days, hours, and minutes"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("1d 12h 30m")
        assert error == ""
        assert hours == 36.5

        hours, error = parse_time_input("2d12h30m")
        assert error == ""
        assert hours == 60.5

    def test_parse_russian_format(self):
        """Test parsing Russian language formats"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("2ч 30м")
        assert error == ""
        assert hours == 2.5

        hours, error = parse_time_input("1д")
        assert error == ""
        assert hours == 24.0

    def test_parse_portuguese_format(self):
        """Test parsing Portuguese language formats"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("2h 30min")
        assert error == ""
        assert hours == 2.5

        hours, error = parse_time_input("1 dia")
        assert error == ""
        assert hours == 24.0

    def test_parse_spanish_format(self):
        """Test parsing Spanish language formats"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("2h 45m")
        assert error == ""
        assert hours == 2.75

        hours, error = parse_time_input("3 días")
        assert error == ""
        assert hours == 72.0

    def test_parse_invalid_format(self):
        """Test invalid format returns error"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("invalid")
        assert hours is None
        assert error != ""

        hours, error = parse_time_input("abc123")
        assert hours is None
        assert error != ""

    def test_parse_empty_string(self):
        """Test empty string returns error"""
        from notifications.validation import parse_time_input

        hours, error = parse_time_input("")
        assert hours is None
        assert error != ""


class TestCustomNotificationValidation:
    """Test custom notification hour validation"""

    def test_valid_custom_notification_hours(self):
        """Test valid custom notification hours"""
        from notifications.validation import validate_custom_notification_hours

        valid_hours = [1.0, 24.0, 48.0, 70.0, 0.5, 69.99]

        for hours in valid_hours:
            is_valid, error = validate_custom_notification_hours(hours)
            assert is_valid is True, f"Expected {hours} to be valid"

    def test_minimum_hours(self):
        """Test minimum hours (20 minutes = 0.333... hours)"""
        from notifications.validation import validate_custom_notification_hours
        from notifications.validation import CUSTOM_NOTIF_MIN_HOURS

        is_valid, error = validate_custom_notification_hours(CUSTOM_NOTIF_MIN_HOURS)
        assert is_valid is True

        is_valid, error = validate_custom_notification_hours(CUSTOM_NOTIF_MIN_HOURS - 0.01)
        assert is_valid is False

    def test_maximum_hours(self):
        """Test maximum hours (70 hours)"""
        from notifications.validation import validate_custom_notification_hours
        from notifications.validation import CUSTOM_NOTIF_MAX_HOURS

        is_valid, error = validate_custom_notification_hours(CUSTOM_NOTIF_MAX_HOURS)
        assert is_valid is True

        is_valid, error = validate_custom_notification_hours(CUSTOM_NOTIF_MAX_HOURS + 0.01)
        assert is_valid is False

    def test_none_hours(self):
        """Test None hours returns invalid"""
        from notifications.validation import validate_custom_notification_hours

        is_valid, error = validate_custom_notification_hours(0.0)
        assert is_valid is False


class TestFormatCustomNotificationTime:
    """Test formatting custom notification time"""

    def test_format_hours_only(self):
        """Test formatting hours only"""
        from notifications.validation import format_custom_notification_time

        result = format_custom_notification_time(12.0)
        assert "12" in result
        assert "h" in result.lower() or "hour" in result.lower()

    def test_format_minutes_only(self):
        """Test formatting minutes only"""
        from notifications.validation import format_custom_notification_time

        result = format_custom_notification_time(0.5)  # 30 minutes
        assert result == "30m"

    def test_format_hours_and_minutes(self):
        """Test formatting hours and minutes"""
        from notifications.validation import format_custom_notification_time

        result = format_custom_notification_time(2.5)  # 2 hours 30 minutes
        assert result == "2h 30m"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

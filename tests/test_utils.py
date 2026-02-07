"""Tests for utility functions and user data serialization"""

import pytest
import json
from datetime import datetime, UTC
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCountryCodeToFlag:
    """Test country code to flag emoji conversion"""

    def test_valid_country_codes(self):
        """Test conversion of valid country codes"""
        from utils import country_code_to_flag

        test_cases = [
            ("US", "🇺🇸"),
            ("GB", "🇬🇧"),
            ("FR", "🇫🇷"),
            ("DE", "🇩🇪"),
            ("JP", "🇯🇵"),
            ("BR", "🇧🇷"),
            ("RU", "🇷🇺"),
            ("AU", "🇦🇺"),
        ]

        for code, expected_flag in test_cases:
            result = country_code_to_flag(code)
            assert (
                result == expected_flag
            ), f"Expected {code} -> {expected_flag}, got {result}"

    def test_lowercase_country_codes(self):
        """Test conversion handles lowercase"""
        from utils import country_code_to_flag

        result = country_code_to_flag("us")
        assert result == "🇺🇸"

    def test_invalid_country_codes(self):
        """Test invalid country codes return empty string"""
        from utils import country_code_to_flag

        invalid_codes = ["", "XXX", "ABCDE", "USXX"]

        for code in invalid_codes:
            result = country_code_to_flag(code)
            assert result == "", f"Expected empty string for {code}"

    def test_two_digit_country_codes(self):
        """Test two digit country codes return flag"""
        from utils import country_code_to_flag

        result = country_code_to_flag("12")
        assert len(result) > 0


class TestCountryNameToISO:
    """Test country name to ISO code conversion"""

    def test_valid_country_names(self):
        """Test conversion of valid country names"""
        from utils import get_country_iso_code

        test_cases = [
            ("United States", "US"),
            ("United Kingdom", "GB"),
            ("France", "FR"),
            ("Germany", "DE"),
            ("Japan", "JP"),
            ("Brazil", "BR"),
            ("Russia", "RU"),
            ("Australia", "AU"),
        ]

        for name, expected_code in test_cases:
            result = get_country_iso_code(name)
            assert (
                result == expected_code
            ), f"Expected {name} -> {expected_code}, got {result}"

    def test_manual_mappings(self):
        """Test manual country name mappings"""
        from utils import get_country_iso_code

        result = get_country_iso_code("Turkey")
        assert result == "TR"

    def test_invalid_country_names(self):
        """Test invalid country names return empty string"""
        from utils import get_country_iso_code

        result = get_country_iso_code("Invalid Country Name")
        assert result == ""

    def test_empty_input(self):
        """Test empty input returns empty string"""
        from utils import get_country_iso_code

        assert get_country_iso_code("") == ""


class TestTrackFlagFormatting:
    """Test track name flag formatting"""

    def test_add_flag_to_track(self):
        """Test adding flag to track name"""
        from utils import add_flag_to_track

        test_cases = [
            ("Yas Marina GP (United Arab Emirates)", "Yas Marina GP 🇦🇪"),
            ("Silverstone GP (United Kingdom)", "Silverstone GP 🇬🇧"),
            ("Monaco GP (Monaco)", "Monaco GP 🇲🇨"),
        ]

        for input_track, expected in test_cases:
            result = add_flag_to_track(input_track)
            assert result == expected

    def test_track_without_country(self):
        """Test track without country name is unchanged"""
        from utils import add_flag_to_track

        result = add_flag_to_track("Unknown Track")
        assert result == "Unknown Track"

    def test_empty_track(self):
        """Test empty track returns empty"""
        from utils import add_flag_to_track

        assert add_flag_to_track("") == ""


class TestGroupDisplayFormatting:
    """Test group display name formatting"""

    def test_format_elite(self):
        """Test Elite group formatting"""
        from utils import format_group_display

        result = format_group_display("E")
        assert result == "Elite"

    def test_format_master(self):
        """Test Master group formatting"""
        from utils import format_group_display

        assert format_group_display("M3") == "Master - 3"
        assert format_group_display("M1") == "Master - 1"

    def test_format_pro(self):
        """Test Pro group formatting"""
        from utils import format_group_display

        assert format_group_display("P15") == "Pro - 15"
        assert format_group_display("P1") == "Pro - 1"

    def test_format_amateur(self):
        """Test Amateur group formatting"""
        from utils import format_group_display

        assert format_group_display("A42") == "Amateur - 42"
        assert format_group_display("A1") == "Amateur - 1"

    def test_format_rookie(self):
        """Test Rookie group formatting"""
        from utils import format_group_display

        assert format_group_display("R99") == "Rookie - 99"
        assert format_group_display("R1") == "Rookie - 1"

    def test_format_invalid(self):
        """Test invalid group returns uppercase"""
        from utils import format_group_display

        result = format_group_display("Invalid")
        assert "INVALID" in result

    def test_format_lowercase(self):
        """Test lowercase is converted"""
        from utils import format_group_display

        result = format_group_display("p15")
        assert result == "Pro - 15"


class TestLanguageMapping:
    """Test Telegram language code mapping"""

    def test_telegram_to_ui_language_mapping(self):
        """Test mapping Telegram codes to UI codes"""
        from utils import map_telegram_language

        test_cases = [
            ("en", "gb"),
            ("ru", "ru"),
            ("pt-br", "br"),
            ("pt", "pt"),
            ("uk", "ua"),
            ("cs", "cz"),
            ("hi", "in"),
        ]

        for telegram_code, expected_ui in test_cases:
            result = map_telegram_language(telegram_code)
            assert (
                result == expected_ui
            ), f"Expected {telegram_code} -> {expected_ui}, got {result}"

    def test_unknown_language(self):
        """Test unknown language falls back to English"""
        from utils import map_telegram_language

        result = map_telegram_language("unknown")
        assert result == "gb"

    def test_none_language(self):
        """Test None language falls back to English"""
        from utils import map_telegram_language

        result = map_telegram_language(None)
        assert result == "gb"

    def test_regional_variant_handling(self):
        """Test regional variants are handled"""
        from utils import map_telegram_language

        result = map_telegram_language("pt-BR")
        assert result == "br"


class TestUIDisplayNames:
    """Test UI language display names"""

    def test_all_supported_languages(self):
        """Test all supported languages have display names"""
        from utils import UI_LANGUAGE_DISPLAY

        expected_languages = [
            "gb",
            "ru",
            "br",
            "it",
            "es",
            "fr",
            "nl",
            "bg",
            "cz",
            "in",
            "ua",
            "pt",
        ]

        for lang in expected_languages:
            assert lang in UI_LANGUAGE_DISPLAY
            assert len(UI_LANGUAGE_DISPLAY[lang]) > 0

    def test_get_ui_language_display(self):
        """Test getting UI language display name"""
        from utils import get_ui_language_display

        result = get_ui_language_display("gb")
        assert "🇬🇧" in result or "English" in result

    def test_unknown_language_defaults(self):
        """Test unknown language defaults to English"""
        from utils import get_ui_language_display

        result = get_ui_language_display("xx")
        assert "🇬🇧" in result or "English" in result


class TestUserDataSerialization:
    """Test user data JSON serialization"""

    def test_user_data_structure(self):
        """Test user data structure is valid"""
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            test_data = {
                "12345": {
                    "language": "gb",
                    "timezone": "UTC",
                    "notifications": {
                        "48h": True,
                        "24h": True,
                        "2h": True,
                        "10min": True,
                    },
                    "custom_notifications": [
                        {"enabled": False, "hours_before": None},
                        {"enabled": False, "hours_before": None},
                    ],
                    "group": "P15",
                }
            }

            with open(temp_path, "w") as f:
                json.dump(test_data, f)

            with open(temp_path, "r") as f:
                loaded = json.load(f)

            assert loaded is not None
            assert "12345" in loaded
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_atomic_write_pattern(self):
        """Test atomic write pattern works correctly"""
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            test_data = {
                "user1": {
                    "language": "gb",
                    "timezone": "UTC",
                    "notifications": {},
                    "custom_notifications": [],
                    "group": "E",
                }
            }

            with open(temp_path, "w") as f:
                json.dump(test_data, f, indent=2)

            with open(temp_path, "r") as f:
                loaded = json.load(f)

            assert loaded["user1"]["language"] == "gb"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestDateTimeFormatting:
    """Test datetime formatting functions"""

    def test_format_race_beautiful(self):
        """Test beautiful race formatting"""
        from utils import format_race_beautiful

        race_data = {
            "track": "Test GP (Country)",
            "hours_left": 24.5,
            "quali_close": datetime(2025, 7, 15, 18, 0, tzinfo=UTC),
        }

        result = format_race_beautiful(race_data)
        assert "24" in result
        assert "Test GP" in result

    def test_format_race_beautiful_empty(self):
        """Test beautiful race formatting with empty data"""
        from utils import format_race_beautiful

        result = format_race_beautiful({})
        assert result == "None"

    def test_format_race_beautiful_none(self):
        """Test beautiful race formatting with None"""
        from utils import format_race_beautiful

        result = format_race_beautiful({})
        assert result == "None"

    def test_localized_weekday(self):
        """Test localized weekday"""
        from utils import get_localized_weekday

        now = datetime.now(UTC)
        result = get_localized_weekday(now)
        assert len(result) <= 3  # Short abbreviation

    def test_localized_weekday_with_i18n(self):
        """Test localized weekday with i18n context"""
        from utils import get_localized_weekday

        now = datetime.now(UTC)

        class MockI18n:
            def get(self, key):
                return key

        result = get_localized_weekday(now, i18n=MockI18n())
        assert result is not None


class TestFullCalendarFormatting:
    """Test full calendar formatting"""

    def test_format_full_calendar_empty(self):
        """Test formatting empty calendar"""
        from utils import format_full_calendar

        result = format_full_calendar({})
        assert result == "No races scheduled"

    def test_format_full_calendar_with_races(self):
        """Test formatting calendar with races"""
        from utils import format_full_calendar
        from datetime import timedelta

        calendar_data = {
            1: {
                "track": "Test Track (Test Country)",
                "quali_close": datetime.now(UTC) + timedelta(days=7),
                "date": datetime.now(UTC) + timedelta(days=7),
                "group": "Pro",
            }
        }

        result = format_full_calendar(calendar_data)
        assert "Test Track" in result

    def test_format_full_calendar_with_user_timezone(self):
        """Test formatting calendar with user timezone"""
        from utils import format_full_calendar
        from datetime import timedelta

        calendar_data = {
            1: {
                "track": "Test Track (Test Country)",
                "quali_close": datetime.now(UTC) + timedelta(days=7),
                "date": datetime.now(UTC) + timedelta(days=7),
                "group": "Pro",
            }
        }

        result = format_full_calendar(calendar_data, user_id=12345)
        assert "Test Track" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

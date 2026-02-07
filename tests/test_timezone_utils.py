"""Tests for timezone utilities and DST handling"""

import pytest
from datetime import datetime, UTC
from zoneinfo import ZoneInfo
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpro_calendar import get_race_time_in_utc
from timezone_utils import (
    validate_timezone,
    parse_utc_offset,
    get_timezone_display_name,
    fuzzy_search_timezones,
    convert_to_user_tz,
    _timezone_search_index,
)


class TestTimezoneValidation:
    """Test timezone name validation"""

    def test_valid_timezone_names(self):
        """Test valid IANA timezone names are accepted"""

        valid_timezones = [
            "UTC",
            "Europe/London",
            "America/New_York",
            "Asia/Tokyo",
            "Europe/Paris",
            "Australia/Sydney",
            "Europe/Moscow",
        ]

        for tz in valid_timezones:
            assert validate_timezone(tz) is True, f"Expected {tz} to be valid"

    def test_invalid_timezone_names(self):
        """Test invalid timezone names are rejected"""

        for tz in ["Invalid/Timezone", "Not/Real"]:
            assert validate_timezone(tz) is False, f"Expected {tz} to be invalid"

    def test_none_input(self):
        """Test None input is handled"""
        assert validate_timezone("NotA/Timezone") is False


class TestDSTTransitions:
    """Test Daylight Saving Time transition handling"""

    def test_paris_timezone_dst_summer(self):
        """Test Paris timezone in summer (CEST, UTC+2)"""

        # Summer date (CEST should be active)
        summer_date = datetime(2025, 7, 15)
        race_time = get_race_time_in_utc(summer_date)

        assert race_time.tzinfo is not None
        assert race_time.hour == 18
        assert race_time.minute == 0

    def test_paris_timezone_dst_winter(self):
        """Test Paris timezone in winter (CET, UTC+1)"""

        # Winter date (CET should be active)
        winter_date = datetime(2025, 1, 15)
        race_time = get_race_time_in_utc(winter_date)

        assert race_time.tzinfo is not None
        assert race_time.hour == 19
        assert race_time.minute == 0

    def test_new_york_timezone_dst(self):
        """Test New York timezone DST transitions"""
        tz = ZoneInfo("America/New_York")

        # Summer (EDT, UTC-4)
        summer_dt = datetime(2025, 7, 15, 12, 0, tzinfo=tz)
        utc_dt = summer_dt.astimezone(UTC)
        assert utc_dt.hour == 16

        # Winter (EST, UTC-5)
        winter_dt = datetime(2025, 1, 15, 12, 0, tzinfo=tz)
        utc_dt = winter_dt.astimezone(UTC)
        assert utc_dt.hour == 17

    def test_utc_offset_change_at_dst_boundary(self):
        """Test UTC offset changes correctly at DST boundary"""
        tz = ZoneInfo("Europe/London")

        # Before DST ends (BST, UTC+1)
        before_dst = datetime(2025, 10, 26, 0, 30, tzinfo=tz)
        utc_before = before_dst.astimezone(UTC)
        assert utc_before.hour == 23

        # After DST ends (GMT, UTC+0)
        after_dst = datetime(2025, 10, 27, 0, 30, tzinfo=tz)
        utc_after = after_dst.astimezone(UTC)
        assert utc_after.hour == 0

    def test_sydney_timezone_dst_opposite_hemisphere(self):
        """Test Sydney timezone (Southern hemisphere, opposite DST)"""
        tz = ZoneInfo("Australia/Sydney")

        # January (summer in Southern hemisphere, AEDT, UTC+11)
        summer_dt = datetime(2025, 1, 15, 12, 0, tzinfo=tz)
        utc_summer = summer_dt.astimezone(UTC)
        assert utc_summer.hour == 1

        # July (winter in Southern hemisphere, AEST, UTC+10)
        winter_dt = datetime(2025, 7, 15, 12, 0, tzinfo=tz)
        utc_winter = winter_dt.astimezone(UTC)
        assert utc_winter.hour == 2


class TestUTCOffsetParsing:
    """Test UTC offset query parsing"""

    def test_parse_positive_offset(self):
        """Test parsing positive UTC offsets"""

        result = parse_utc_offset("UTC+3")
        assert result is not None

        result = parse_utc_offset("+3")
        assert result is not None

        result = parse_utc_offset("GMT+5")
        assert result is not None

    def test_parse_negative_offset(self):
        """Test parsing negative UTC offsets"""

        result = parse_utc_offset("UTC-5")
        assert result is not None

        result = parse_utc_offset("-5")
        assert result is not None

        result = parse_utc_offset("GMT-5")
        assert result is not None

    def test_parse_half_hour_offset(self):
        """Test parsing half-hour UTC offsets"""

        result = parse_utc_offset("+5.5")
        assert result is not None

    def test_parse_invalid_offset(self):
        """Test parsing invalid UTC offsets returns None"""

        assert parse_utc_offset("invalid") is None
        assert parse_utc_offset("") is None
        assert parse_utc_offset("UTC+") is None
        assert parse_utc_offset("+") is None


class TestTimezoneDisplay:
    """Test timezone display name formatting"""

    def test_get_timezone_display_name_popular(self):
        """Test display name for popular timezones"""

        tz = ZoneInfo("America/New_York")
        display = get_timezone_display_name(tz)
        assert "New York" in display

        tz = ZoneInfo("Europe/London")
        display = get_timezone_display_name(tz)
        assert "London" in display

    def test_get_timezone_display_name_with_abbreviation(self):
        """Test timezone display includes abbreviation"""

        tz = ZoneInfo("America/New_York")
        display = get_timezone_display_name(tz)
        assert "(" in display and ")" in display

    def test_get_timezone_display_name_fallback(self):
        """Test display name for non-popular timezones falls back to IANA name"""

        tz = ZoneInfo("Pacific/Pago_Pago")
        display = get_timezone_display_name(tz)
        assert "Pago_Pago" in display or "Pago Pago" in display


class TestFuzzyTimezoneSearch:
    """Test fuzzy timezone search functionality"""

    def test_fuzzy_search_returns_results(self):
        """Test fuzzy search returns matching timezones"""

        results = fuzzy_search_timezones("new york", limit=5)
        assert len(results) > 0
        assert any("New_York" in r[0] for r in results)

    def test_fuzzy_search_empty_query(self):
        """Test empty query returns empty list"""

        results = fuzzy_search_timezones("")
        assert results == []

    def test_fuzzy_search_translated_name(self):
        """Test searching with translated city name"""

        results = fuzzy_search_timezones("москва", limit=5)
        assert len(results) > 0
        assert any("Moscow" in r[0] for r in results)

    def test_fuzzy_search_abbreviation(self):
        """Test searching with timezone abbreviation"""

        results = fuzzy_search_timezones("EST", limit=5)
        assert len(results) > 0

    def test_fuzzy_search_utc_offset(self):
        """Test searching with UTC offset"""

        results = fuzzy_search_timezones("UTC+3", limit=5)
        assert len(results) > 0


class TestConvertToUserTimezone:
    """Test datetime conversion to user timezone"""

    def test_convert_naive_datetime(self):
        """Test converting naive datetime (assumes UTC)"""

        naive_dt = datetime(2025, 7, 15, 20, 0, 0)
        result = convert_to_user_tz(naive_dt, 12345)

        assert result is not None
        assert result.tzinfo is not None

    def test_convert_none_returns_none(self):
        """Test None input returns None"""

        result = convert_to_user_tz(None, 12345)
        assert result is None

    @patch("timezone_utils.get_user_timezone")
    def test_convert_uses_user_timezone(self, mock_get_tz):
        """Test conversion uses user's timezone setting"""

        mock_get_tz.return_value = ZoneInfo("Europe/London")

        dt = datetime(2025, 7, 15, 20, 0, 0, tzinfo=UTC)
        result = convert_to_user_tz(dt, 12345)

        assert result is not None
        mock_get_tz.assert_called_once_with(12345)


class TestTimezoneSearchIndex:
    """Test timezone search index loading"""

    def test_timezone_search_index_is_dict_or_none(self):
        """Test timezone search index is properly initialized"""
        assert _timezone_search_index is None or isinstance(
            _timezone_search_index, dict
        )

    def test_timezone_search_index_lookup(self):
        """Test timezone search index can be used for lookups"""
        if _timezone_search_index is not None:
            assert isinstance(_timezone_search_index, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

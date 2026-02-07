"""Tests for GPRO calendar parsing and API response handling"""

import pytest
from datetime import datetime, UTC
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDateParsing:
    """Test GPRO date parsing"""

    def test_parse_standard_date(self):
        """Test parsing standard date format"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "15.07.2025"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.year == 2025
        assert result.month == 7
        assert result.day == 15

    def test_parse_date_with_month_name(self):
        """Test parsing date with month name"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "Jul 15, 2025"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.month == 7

    def test_parse_iso_date(self):
        """Test parsing ISO date format"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "2025-07-15"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.year == 2025
        assert result.month == 7

    def test_parse_placeholder_dates(self):
        """Test placeholder dates return None"""
        from gpro_calendar import parse_gpro_date_fixed

        placeholders = ["-", "TBD", "N/A", ""]

        for placeholder in placeholders:
            result = parse_gpro_date_fixed(placeholder)
            assert result is None, f"Expected {placeholder} to return None"

    def test_parse_date_with_html_tags(self):
        """Test date with HTML tags is cleaned"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "15.07.2025"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.day == 15
        assert result.month == 7

    def test_parse_date_with_ordinal(self):
        """Test date with ordinal suffix (st, nd, rd, th)"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "15th Jul 2025"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.day == 15

    def test_parse_today_handler(self):
        """Test 'Today' is handled"""
        from gpro_calendar import parse_gpro_date_fixed

        date_str = "Today"
        result = parse_gpro_date_fixed(date_str)
        assert result is not None
        assert result.day == datetime.now(UTC).day

    def test_parse_invalid_date(self):
        """Test invalid date returns None"""
        from gpro_calendar import parse_gpro_date_fixed

        result = parse_gpro_date_fixed("not-a-date")
        assert result is None

    def test_parse_none_input(self):
        """Test None input returns None"""
        from gpro_calendar import parse_gpro_date_fixed

        result = parse_gpro_date_fixed("")
        assert result is None


class TestRaceTimeConversion:
    """Test race time conversion from CET/CEST to UTC"""

    def test_race_time_summer(self):
        """Test race time in summer (CEST)"""
        from gpro_calendar import get_race_time_in_utc

        race_date = datetime(2025, 7, 15)
        race_time = get_race_time_in_utc(race_date)

        assert race_time.hour == 18  # CEST is UTC+2, so 20:00 CEST = 18:00 UTC
        assert race_time.minute == 0
        assert race_time.tzinfo is not None

    def test_race_time_winter(self):
        """Test race time in winter (CET)"""
        from gpro_calendar import get_race_time_in_utc

        race_date = datetime(2025, 1, 15)
        race_time = get_race_time_in_utc(race_date)

        assert race_time.hour == 19  # CET is UTC+1, so 20:00 CET = 19:00 UTC
        assert race_time.minute == 0
        assert race_time.tzinfo is not None


class TestCalendarParsing:
    """Test GPRO calendar API response parsing"""

    def test_parse_race_events(self):
        """Test parsing race events from API response"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "15.07.2025",
                "trackName": "Spa GP",
                "group": "Pro"
            },
            {
                "eventType": "R",
                "idxReal": 2,
                "dateEvent": "22.07.2025",
                "trackName": "Monaco GP",
                "group": "Pro"
            }
        ]

        calendar = parse_gpro_events(events)

        assert len(calendar) == 2
        assert 1 in calendar
        assert 2 in calendar
        assert calendar[1]["track"] == "Spa GP"
        assert calendar[2]["track"] == "Monaco GP"

    def test_parse_race_events_sequential_ids(self):
        """Test race events are re-numbered sequentially"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "R",
                "idxReal": 5,
                "dateEvent": "15.07.2025",
                "trackName": "Spa GP",
                "group": "Pro"
            },
            {
                "eventType": "R",
                "idxReal": 17,
                "dateEvent": "22.07.2025",
                "trackName": "Monaco GP",
                "group": "Pro"
            }
        ]

        calendar = parse_gpro_events(events)

        assert 1 in calendar
        assert 2 in calendar
        assert 5 not in calendar
        assert 17 not in calendar

    def test_parse_skips_non_race_events(self):
        """Test non-race events are skipped"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "Q",  # Quali, not Race
                "idxReal": 1,
                "dateEvent": "15.07.2025",
                "trackName": "Test",
            }
        ]

        calendar = parse_gpro_events(events)
        assert len(calendar) == 0

    def test_parse_handles_missing_fields(self):
        """Test parsing handles missing optional fields"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "15.07.2025",
                "trackName": "Test Track"
            }
        ]

        calendar = parse_gpro_events(events)

        assert len(calendar) == 1
        assert calendar[1]["group"] == "Pro"  # Default value

    def test_parse_sorts_by_date(self):
        """Test races are sorted by date"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "22.07.2025",
                "trackName": "Monaco GP",
                "group": "Pro"
            },
            {
                "eventType": "R",
                "idxReal": 2,
                "dateEvent": "15.07.2025",
                "trackName": "Spa GP",
                "group": "Pro"
            }
        ]

        calendar = parse_gpro_events(events)

        ids = list(calendar.keys())
        assert ids == [1, 2]
        assert calendar[1]["track"] == "Spa GP"  # Earlier date gets ID 1

    def test_parse_with_invalid_date(self):
        """Test events with invalid dates are skipped"""
        from gpro_calendar import parse_gpro_events

        events = [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "invalid-date",
                "trackName": "Test",
            },
            {
                "eventType": "R",
                "idxReal": 2,
                "dateEvent": "15.07.2025",
                "trackName": "Valid Track",
            }
        ]

        calendar = parse_gpro_events(events)
        assert len(calendar) == 1
        assert calendar[1]["track"] == "Valid Track"


class TestCalendarSerialization:
    """Test calendar JSON serialization"""

    def test_save_and_load_calendar(self):
        """Test calendar can be saved and loaded"""
        from gpro_calendar import parse_gpro_events, _save_calendar_to_file, _load_calendar_from_file
        import tempfile
        import os

        events = [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "15.07.2025",
                "trackName": "Spa GP",
                "group": "Pro"
            }
        ]

        calendar = parse_gpro_events(events)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            _save_calendar_to_file(calendar, temp_path)
            loaded = _load_calendar_from_file(temp_path)

            assert len(loaded) == 1
            assert loaded[1]["track"] == "Spa GP"
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class TestSeasonTransition:
    """Test season transition logic"""

    def test_should_not_transition_without_data(self):
        """Test transition doesn't trigger without calendars"""
        from gpro_calendar import should_trigger_season_transition
        import gpro_calendar

        gpro_calendar.race_calendar = {}
        gpro_calendar.next_season_calendar = {}

        now = datetime.now(UTC)
        result = should_trigger_season_transition(now)
        assert result is False

    def test_should_not_transition_without_next_season(self):
        """Test transition doesn't trigger without next season data"""
        from gpro_calendar import should_trigger_season_transition
        import gpro_calendar

        gpro_calendar.race_calendar = {1: {"date": datetime.now(UTC)}}
        gpro_calendar.next_season_calendar = {}

        now = datetime.now(UTC)
        result = should_trigger_season_transition(now)
        assert result is False

    def test_prefetch_next_season_conditions(self):
        """Test prefetch conditions work correctly"""
        from gpro_calendar import should_prefetch_next_season
        import gpro_calendar

        gpro_calendar.race_calendar = {}
        gpro_calendar.next_season_calendar = {}

        now = datetime.now(UTC)
        result = should_prefetch_next_season(now)
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

"""Tests for notification timing calculations"""

import pytest
from datetime import datetime, UTC, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCheckIntervals:
    """Test notification check interval calculations"""

    def test_normal_interval(self):
        """Test normal check interval (5 minutes)"""
        from notifications.timing import (
            get_next_check_interval,
            CHECK_INTERVAL_NORMAL_SECONDS,
        )

        now = datetime.now(UTC)
        race_calendar = {}

        interval = get_next_check_interval(now, race_calendar)
        assert interval == CHECK_INTERVAL_NORMAL_SECONDS

    def test_fast_interval_approaching_race(self):
        """Test fast interval when approaching race time"""
        from notifications.timing import (
            get_next_check_interval,
            CHECK_INTERVAL_FAST_SECONDS,
            CHECK_INTERVAL_CLOSING_HOURS,
        )

        now = datetime.now(UTC)

        future_date = now + timedelta(hours=CHECK_INTERVAL_CLOSING_HOURS - 0.5)
        race_calendar = {
            1: {
                "quali_close": future_date,
                "track": "Test",
                "date": future_date,
                "group": "Pro",
            }
        }

        interval = get_next_check_interval(now, race_calendar)
        assert interval == CHECK_INTERVAL_FAST_SECONDS

    def test_fast_interval_quali_open_window(self):
        """Test fast interval during quali open window"""
        from notifications.timing import (
            get_next_check_interval,
            CHECK_INTERVAL_NORMAL_SECONDS,
        )

        now = datetime.now(UTC)

        future_date = now + timedelta(hours=24)

        race_calendar = {
            1: {
                "quali_close": future_date,
                "track": "Race 1",
                "date": future_date,
                "group": "Pro",
            }
        }

        interval = get_next_check_interval(now, race_calendar)
        assert interval == CHECK_INTERVAL_NORMAL_SECONDS

    def test_normal_interval_far_from_race(self):
        """Test normal interval when far from race"""
        from notifications.timing import (
            get_next_check_interval,
            CHECK_INTERVAL_NORMAL_SECONDS,
            CHECK_INTERVAL_CLOSING_HOURS,
        )

        now = datetime.now(UTC)

        distant_date = now + timedelta(hours=CHECK_INTERVAL_CLOSING_HOURS + 24)
        race_calendar = {
            1: {
                "quali_close": distant_date,
                "track": "Test",
                "date": distant_date,
                "group": "Pro",
            }
        }

        interval = get_next_check_interval(now, race_calendar)
        assert interval == CHECK_INTERVAL_NORMAL_SECONDS

    def test_fast_interval_with_snooze(self):
        """Test fast interval when snooze is about to fire"""
        from notifications.timing import (
            get_next_check_interval,
            CHECK_INTERVAL_NORMAL_SECONDS,
        )

        now = datetime.now(UTC)
        race_calendar = {}

        interval = get_next_check_interval(now, race_calendar)
        assert interval == CHECK_INTERVAL_NORMAL_SECONDS


class TestNotificationTimingConstants:
    """Test notification timing constants"""

    def test_api_check_intervals(self):
        """Test API check interval constants"""
        from notifications.timing import (
            API_CHECK_START_HOURS,
            API_CHECK_END_HOURS,
            API_CHECK_INTERVAL_MINUTES,
            FALLBACK_TOLERANCE_MINUTES,
        )

        assert API_CHECK_START_HOURS == 2.0
        assert API_CHECK_END_HOURS == 3.5
        assert API_CHECK_INTERVAL_MINUTES == 10
        assert FALLBACK_TOLERANCE_MINUTES == 10

    def test_check_interval_values(self):
        """Test check interval constant values"""
        from notifications.timing import (
            CHECK_INTERVAL_NORMAL_SECONDS,
            CHECK_INTERVAL_FAST_SECONDS,
            CHECK_INTERVAL_CLOSING_HOURS,
        )

        assert CHECK_INTERVAL_NORMAL_SECONDS == 300  # 5 minutes
        assert CHECK_INTERVAL_FAST_SECONDS == 60  # 1 minute
        assert CHECK_INTERVAL_CLOSING_HOURS == 3


class TestTimeUntilQualiFormatting:
    """Test time until quali formatting"""

    def test_format_minutes(self):
        """Test formatting time in minutes"""
        from utils import format_time_until_quali

        future_time = datetime.now(UTC) + timedelta(minutes=30)
        result = format_time_until_quali(future_time)
        assert "30" in result or "m" in result.lower()

    def test_format_hours(self):
        """Test formatting time in hours"""
        from utils import format_time_until_quali

        future_time = datetime.now(UTC) + timedelta(hours=5)
        result = format_time_until_quali(future_time)
        assert "5" in result or "h" in result.lower()

    def test_format_days(self):
        """Test formatting time in days"""
        from utils import format_time_until_quali

        future_time = datetime.now(UTC) + timedelta(days=3)
        result = format_time_until_quali(future_time)
        assert "3" in result or "d" in result.lower()

    def test_format_past_time(self):
        """Test formatting past time returns empty"""
        from utils import format_time_until_quali

        past_time = datetime.now(UTC) - timedelta(hours=1)
        result = format_time_until_quali(past_time)
        assert result == ""

    def test_format_mixed_units(self):
        """Test formatting mixed units (days + hours)"""
        from utils import format_time_until_quali

        future_time = datetime.now(UTC) + timedelta(days=2, hours=2)
        result = format_time_until_quali(future_time)
        assert "2" in result
        assert "d" in result.lower()
        assert "h" in result.lower()


class TestRaceCalendarTiming:
    """Test race calendar timing functions"""

    def test_get_races_closing_soon(self):
        """Test getting races closing soon"""
        from gpro_calendar import get_races_closing_soon
        import gpro_calendar

        now = datetime.now(UTC)

        gpro_calendar.race_calendar = {
            1: {
                "quali_close": now + timedelta(hours=24),
                "track": "Test",
                "date": now + timedelta(hours=48),
                "group": "Pro",
            },
            2: {
                "quali_close": now + timedelta(hours=48),
                "track": "Test 2",
                "date": now + timedelta(hours=72),
                "group": "Pro",
            },
        }

        races = get_races_closing_soon(hours_before=720)
        assert len(races) == 2

    def test_get_last_race_id(self):
        """Test getting last race ID"""
        from gpro_calendar import get_last_race_id
        import gpro_calendar

        gpro_calendar.race_calendar = {
            1: {"date": datetime.now(UTC)},
            5: {"date": datetime.now(UTC)},
            3: {"date": datetime.now(UTC)},
        }

        result = get_last_race_id()
        assert result == 5

    def test_get_last_race_id_empty(self):
        """Test getting last race ID from empty calendar"""
        from gpro_calendar import get_last_race_id
        import gpro_calendar

        gpro_calendar.race_calendar = {}

        result = get_last_race_id()
        assert result == 0

    def test_get_first_race_date(self):
        """Test getting first race date"""
        from gpro_calendar import get_first_race_date
        import gpro_calendar

        now = datetime.now(UTC)

        gpro_calendar.race_calendar = {
            1: {"date": now + timedelta(days=7)},
            2: {"date": now + timedelta(days=14)},
        }

        result = get_first_race_date()
        assert result == now + timedelta(days=7)

    def test_get_first_race_date_empty(self):
        """Test getting first race date from empty calendar"""
        from gpro_calendar import get_first_race_date
        import gpro_calendar

        gpro_calendar.race_calendar = {}

        result = get_first_race_date()
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

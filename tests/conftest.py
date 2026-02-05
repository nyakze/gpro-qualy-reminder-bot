"""Pytest configuration and fixtures for GPRO bot tests"""

import pytest
import sys
import os
from datetime import datetime, UTC, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_race_calendar():
    """Sample race calendar for testing"""
    now = datetime.now(UTC)

    return {
        1: {
            "quali_close": now + timedelta(hours=24),
            "track": "Spa GP (Belgium)",
            "date": now + timedelta(hours=48),
            "group": "Pro",
            "weather": {"temp": 20, "condition": "sunny"}
        },
        2: {
            "quali_close": now + timedelta(hours=168),
            "track": "Monaco GP (Monaco)",
            "date": now + timedelta(hours=192),
            "group": "Pro"
        }
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "12345": {
            "language": "gb",
            "timezone": "Europe/London",
            "notifications": {
                "48h": True,
                "24h": True,
                "2h": True,
                "10min": True,
                "opens_soon": True,
                "race_live": True,
                "race_replay": True,
                "race_results": True,
                "custom_1": False,
                "custom_2": False
            },
            "custom_notifications": [
                {"enabled": False, "hours_before": None},
                {"enabled": False, "hours_before": None}
            ],
            "group": "P15",
            "snoozes": []
        },
        "67890": {
            "language": "ru",
            "timezone": "Europe/Moscow",
            "notifications": {
                "48h": False,
                "24h": True,
                "2h": True,
                "10min": True,
                "opens_soon": False,
                "race_live": True,
                "race_replay": True,
                "race_results": True,
                "custom_1": True,
                "custom_2": False
            },
            "custom_notifications": [
                {"enabled": True, "hours_before": 12.0},
                {"enabled": False, "hours_before": None}
            ],
            "group": "M3",
            "snoozes": []
        }
    }


@pytest.fixture
def mock_api_response_races():
    """Mock API response containing race events"""
    return {
        "events": [
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
        ],
        "nextSeasonPublished": True,
        "nextSeasonEvents": [
            {
                "eventType": "R",
                "idxReal": 1,
                "dateEvent": "01.01.2026",
                "trackName": "New Season GP",
                "group": "Pro"
            }
        ]
    }


@pytest.fixture
def summer_datetime():
    """Sample datetime in summer (DST active in Northern hemisphere)"""
    return datetime(2025, 7, 15, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def winter_datetime():
    """Sample datetime in winter (DST inactive in Northern hemisphere)"""
    return datetime(2025, 1, 15, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def mock_timezone_search_index():
    """Mock timezone search index"""
    return {
        "search_corpus": ["America/New_York", "New York", "US Eastern", "EST", "EDT"],
        "tz_name_map": {
            "America/New_York": "America/New_York",
            "New York": "America/New_York",
            "US Eastern": "America/New_York",
            "EST": "America/New_York",
            "EDT": "America/New_York"
        },
        "timezone_info": {
            "America/New_York": {
                "tzIdentifier": "America/New_York",
                "abbreviationStandard": "EST",
                "abbreviationDst": "EDT",
                "utcOffsetStandard": "-05:00",
                "type": "canonical"
            }
        }
    }


@pytest.fixture
def mock_i18n():
    """Mock i18n context"""
    class MockI18n:
        def get(self, key, **kwargs):
            return key

    return MockI18n()


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

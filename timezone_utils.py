"""
Timezone conversion and management utilities for GPRO bot.

This module provides timezone conversion functions, fuzzy timezone search,
and display formatting with automatic DST handling using Python's zoneinfo.
"""

import logging
import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, available_timezones
from typing import Optional

from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)

# Default timezone for users who haven't set a preference
DEFAULT_TIMEZONE = 'UTC'

# Curated list of ~100 popular timezones with search aliases
# Format: 'IANA_Zone_Name': ['City Name', 'Abbreviation', 'Alternate Names', ...]
POPULAR_TIMEZONES = {
    # Americas - North America
    'America/New_York': ['New York', 'NYC', 'EST', 'EDT', 'Eastern', 'US Eastern'],
    'America/Chicago': ['Chicago', 'CST', 'CDT', 'Central', 'US Central'],
    'America/Denver': ['Denver', 'MST', 'MDT', 'Mountain', 'US Mountain'],
    'America/Los_Angeles': ['Los Angeles', 'LA', 'PST', 'PDT', 'Pacific', 'US Pacific'],
    'America/Phoenix': ['Phoenix', 'Arizona', 'MST'],
    'America/Anchorage': ['Anchorage', 'Alaska', 'AKST', 'AKDT'],
    'Pacific/Honolulu': ['Honolulu', 'Hawaii', 'HST'],
    'America/Toronto': ['Toronto', 'Canada Eastern'],
    'America/Vancouver': ['Vancouver', 'Canada Pacific'],
    'America/Mexico_City': ['Mexico City', 'Mexico'],
    'America/Monterrey': ['Monterrey'],

    # Americas - South America
    'America/Sao_Paulo': ['São Paulo', 'Sao Paulo', 'Brazil', 'BRT', 'BRST'],
    'America/Buenos_Aires': ['Buenos Aires', 'Argentina', 'ART'],
    'America/Santiago': ['Santiago', 'Chile', 'CLT', 'CLST'],
    'America/Bogota': ['Bogota', 'Bogotá', 'Colombia', 'COT'],
    'America/Lima': ['Lima', 'Peru', 'PET'],
    'America/Caracas': ['Caracas', 'Venezuela', 'VET'],

    # Americas - Central America & Caribbean
    'America/Panama': ['Panama'],
    'America/Costa_Rica': ['Costa Rica', 'San Jose', 'San José'],
    'America/Havana': ['Havana', 'Cuba', 'CST', 'CDT'],
    'America/Jamaica': ['Jamaica', 'Kingston', 'EST'],

    # Europe - Western
    'Europe/London': ['London', 'UK', 'GMT', 'BST', 'Britain', 'England'],
    'Europe/Dublin': ['Dublin', 'Ireland', 'IST'],
    'Europe/Lisbon': ['Lisbon', 'Portugal', 'WET', 'WEST'],
    'Atlantic/Reykjavik': ['Reykjavik', 'Iceland', 'GMT'],

    # Europe - Central
    'Europe/Paris': ['Paris', 'France', 'CET', 'CEST'],
    'Europe/Berlin': ['Berlin', 'Germany', 'CET', 'CEST'],
    'Europe/Amsterdam': ['Amsterdam', 'Netherlands', 'CET', 'CEST'],
    'Europe/Brussels': ['Brussels', 'Belgium', 'CET', 'CEST'],
    'Europe/Madrid': ['Madrid', 'Spain', 'CET', 'CEST'],
    'Europe/Rome': ['Rome', 'Italy', 'CET', 'CEST'],
    'Europe/Vienna': ['Vienna', 'Austria', 'CET', 'CEST'],
    'Europe/Zurich': ['Zurich', 'Zürich', 'Switzerland', 'CET', 'CEST'],
    'Europe/Prague': ['Prague', 'Czech', 'CET', 'CEST'],
    'Europe/Warsaw': ['Warsaw', 'Poland', 'CET', 'CEST'],
    'Europe/Budapest': ['Budapest', 'Hungary', 'CET', 'CEST'],
    'Europe/Stockholm': ['Stockholm', 'Sweden', 'CET', 'CEST'],
    'Europe/Oslo': ['Oslo', 'Norway', 'CET', 'CEST'],
    'Europe/Copenhagen': ['Copenhagen', 'Denmark', 'CET', 'CEST'],

    # Europe - Eastern
    'Europe/Helsinki': ['Helsinki', 'Finland', 'EET', 'EEST'],
    'Europe/Athens': ['Athens', 'Greece', 'EET', 'EEST'],
    'Europe/Bucharest': ['Bucharest', 'Romania', 'EET', 'EEST'],
    'Europe/Sofia': ['Sofia', 'Bulgaria', 'EET', 'EEST'],
    'Europe/Istanbul': ['Istanbul', 'Turkey', 'TRT'],
    'Europe/Kiev': ['Kiev', 'Kyiv', 'Ukraine', 'EET', 'EEST'],
    'Europe/Moscow': ['Moscow', 'Russia', 'MSK'],
    'Europe/Minsk': ['Minsk', 'Belarus', 'MSK'],
    'Europe/Kaliningrad': ['Kaliningrad', 'Russia Kaliningrad'],
    'Europe/Samara': ['Samara', 'Russia Samara'],
    'Europe/Volgograd': ['Volgograd', 'Russia Volgograd'],

    # Asia - Middle East
    'Asia/Dubai': ['Dubai', 'UAE', 'GST'],
    'Asia/Riyadh': ['Riyadh', 'Saudi Arabia', 'AST'],
    'Asia/Jerusalem': ['Jerusalem', 'Israel', 'IST', 'IDT'],
    'Asia/Beirut': ['Beirut', 'Lebanon', 'EET', 'EEST'],
    'Asia/Tehran': ['Tehran', 'Iran', 'IRST', 'IRDT'],

    # Asia - South Asia
    'Asia/Kolkata': ['Kolkata', 'Calcutta', 'India', 'IST', 'Mumbai', 'Delhi', 'Bangalore'],
    'Asia/Karachi': ['Karachi', 'Pakistan', 'PKT'],
    'Asia/Dhaka': ['Dhaka', 'Bangladesh', 'BST'],
    'Asia/Kathmandu': ['Kathmandu', 'Nepal', 'NPT'],
    'Asia/Colombo': ['Colombo', 'Sri Lanka', 'IST'],

    # Asia - Southeast Asia
    'Asia/Bangkok': ['Bangkok', 'Thailand', 'ICT'],
    'Asia/Singapore': ['Singapore', 'SGT'],
    'Asia/Kuala_Lumpur': ['Kuala Lumpur', 'Malaysia', 'MYT'],
    'Asia/Jakarta': ['Jakarta', 'Indonesia', 'WIB'],
    'Asia/Manila': ['Manila', 'Philippines', 'PHT'],
    'Asia/Ho_Chi_Minh': ['Ho Chi Minh', 'Saigon', 'Vietnam', 'ICT'],

    # Asia - East Asia
    'Asia/Hong_Kong': ['Hong Kong', 'HKT'],
    'Asia/Shanghai': ['Shanghai', 'China', 'CST', 'Beijing'],
    'Asia/Taipei': ['Taipei', 'Taiwan', 'CST'],
    'Asia/Tokyo': ['Tokyo', 'Japan', 'JST'],
    'Asia/Seoul': ['Seoul', 'South Korea', 'KST'],
    'Asia/Pyongyang': ['Pyongyang', 'North Korea', 'KST'],

    # Asia - Central Asia
    'Asia/Almaty': ['Almaty', 'Kazakhstan', 'ALMT'],
    'Asia/Tashkent': ['Tashkent', 'Uzbekistan', 'UZT'],
    'Asia/Yekaterinburg': ['Yekaterinburg', 'Russia Yekaterinburg', 'YEKT'],
    'Asia/Novosibirsk': ['Novosibirsk', 'Russia Novosibirsk', 'NOVT'],
    'Asia/Krasnoyarsk': ['Krasnoyarsk', 'Russia Krasnoyarsk', 'KRAT'],
    'Asia/Irkutsk': ['Irkutsk', 'Russia Irkutsk', 'IRKT'],
    'Asia/Yakutsk': ['Yakutsk', 'Russia Yakutsk', 'YAKT'],
    'Asia/Vladivostok': ['Vladivostok', 'Russia Vladivostok', 'VLAT'],

    # Pacific - Oceania
    'Pacific/Auckland': ['Auckland', 'New Zealand', 'NZST', 'NZDT'],
    'Pacific/Fiji': ['Fiji', 'Suva', 'FJT'],
    'Pacific/Guam': ['Guam', 'ChST'],
    'Pacific/Port_Moresby': ['Port Moresby', 'Papua New Guinea', 'PGT'],

    # Australia
    'Australia/Sydney': ['Sydney', 'Australia', 'AEST', 'AEDT'],
    'Australia/Melbourne': ['Melbourne', 'AEST', 'AEDT'],
    'Australia/Brisbane': ['Brisbane', 'AEST'],
    'Australia/Perth': ['Perth', 'AWST'],
    'Australia/Adelaide': ['Adelaide', 'ACST', 'ACDT'],
    'Australia/Darwin': ['Darwin', 'ACST'],

    # Africa
    'Africa/Cairo': ['Cairo', 'Egypt', 'EET', 'EEST'],
    'Africa/Johannesburg': ['Johannesburg', 'South Africa', 'SAST'],
    'Africa/Lagos': ['Lagos', 'Nigeria', 'WAT'],
    'Africa/Nairobi': ['Nairobi', 'Kenya', 'EAT'],
    'Africa/Casablanca': ['Casablanca', 'Morocco', 'WET', 'WEST'],
    'Africa/Algiers': ['Algiers', 'Algeria', 'CET'],
    'Africa/Tunis': ['Tunis', 'Tunisia', 'CET'],

    # Atlantic
    'Atlantic/Azores': ['Azores', 'AZOT', 'AZOST'],
    'Atlantic/Cape_Verde': ['Cape Verde', 'CVT'],

    # UTC
    'UTC': ['UTC', 'GMT', 'Universal'],
    'Etc/GMT': ['GMT', 'UTC', 'Universal'],
}


def get_user_timezone(user_id: int) -> ZoneInfo:
    """
    Get user's timezone as ZoneInfo object.

    Args:
        user_id: Telegram user ID

    Returns:
        ZoneInfo object for user's timezone (defaults to UTC)
    """
    from notifications import get_user_timezone as get_tz_string

    try:
        tz_string = get_tz_string(user_id)
        return ZoneInfo(tz_string)
    except Exception as e:
        logger.warning(f"Failed to get timezone for user {user_id}: {e}, falling back to UTC")
        return ZoneInfo('UTC')


def convert_to_user_tz(dt: Optional[datetime], user_id: int) -> Optional[datetime]:
    """
    Convert UTC datetime to user's timezone.

    Args:
        dt: UTC datetime (naive or aware)
        user_id: Telegram user ID

    Returns:
        Datetime converted to user's timezone, or None if dt is None
    """
    if dt is None:
        return None

    try:
        # Make sure datetime is aware (has timezone info)
        if dt.tzinfo is None:
            # Assume naive datetimes are UTC
            dt = dt.replace(tzinfo=timezone.utc)

        # Get user's timezone
        user_tz = get_user_timezone(user_id)

        # Convert to user timezone
        return dt.astimezone(user_tz)
    except Exception as e:
        logger.error(f"Failed to convert datetime to user timezone: {e}")
        return dt


def format_datetime_for_user(
    dt: datetime,
    user_id: int,
    format_str: str = "%d.%m %H:%M"
) -> str:
    """
    Convert UTC datetime to user's timezone and format with timezone abbreviation.

    Args:
        dt: UTC datetime
        user_id: Telegram user ID
        format_str: strftime format string (default: "%d.%m %H:%M")

    Returns:
        Formatted string like "15.01 19:00 EST" or "15.01 19:00 UTC"
    """
    try:
        # Convert to user timezone
        local_dt = convert_to_user_tz(dt, user_id)
        if local_dt is None:
            return "N/A"

        # Format the datetime
        formatted = local_dt.strftime(format_str)

        # Get timezone abbreviation
        tz_abbr = local_dt.tzname()

        # Return with timezone abbreviation
        return f"{formatted} {tz_abbr}"
    except Exception as e:
        logger.error(f"Failed to format datetime for user {user_id}: {e}")
        # Fallback to UTC
        if dt:
            return f"{dt.strftime(format_str)} UTC"
        return "N/A"


def get_timezone_display_name(tz: ZoneInfo, dt: Optional[datetime] = None) -> str:
    """
    Get human-readable timezone display name with abbreviation.

    Args:
        tz: ZoneInfo object
        dt: Optional datetime to get DST-aware abbreviation (default: now)

    Returns:
        Display name like "New York (EST)" or "UTC+3"
    """
    try:
        # Use provided datetime or current time
        if dt is None:
            dt = datetime.now(timezone.utc)

        # Make datetime aware if needed
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        # Convert to target timezone
        local_dt = dt.astimezone(tz)

        # Get timezone abbreviation
        tz_abbr = local_dt.tzname()

        # Get timezone string (e.g., "America/New_York")
        tz_str = str(tz)

        # Try to find city name in POPULAR_TIMEZONES
        for tz_name, aliases in POPULAR_TIMEZONES.items():
            if tz_name == tz_str and aliases:
                # Use first alias (usually the city name)
                city_name = aliases[0]
                return f"{city_name} ({tz_abbr})"

        # Fallback: extract city name from IANA zone
        if '/' in tz_str:
            city = tz_str.split('/')[-1].replace('_', ' ')
            return f"{city} ({tz_abbr})"

        # Fallback: just show abbreviation
        return tz_abbr
    except Exception as e:
        logger.error(f"Failed to get timezone display name: {e}")
        return str(tz)


def parse_utc_offset(query: str) -> Optional[str]:
    """
    Parse UTC offset queries like "UTC+3", "GMT-5" and find matching IANA timezone.

    Args:
        query: Query string like "UTC+3", "GMT-5", "UTC+5.5"

    Returns:
        IANA timezone name or None if not found
    """
    # Match patterns: UTC+3, GMT-5, UTC+5.5, etc.
    pattern = r'^(?:UTC|GMT)\s*([+-]?\d+(?:\.\d+)?)\s*$'
    match = re.match(pattern, query.upper().strip())

    if not match:
        return None

    try:
        offset_str = match.group(1)
        offset_hours = float(offset_str)

        # Common UTC offset mappings to representative timezones
        offset_map = {
            -12: 'Etc/GMT+12',
            -11: 'Pacific/Pago_Pago',
            -10: 'Pacific/Honolulu',
            -9: 'America/Anchorage',
            -8: 'America/Los_Angeles',
            -7: 'America/Denver',
            -6: 'America/Chicago',
            -5: 'America/New_York',
            -4: 'America/Caracas',
            -3: 'America/Sao_Paulo',
            -2: 'Atlantic/South_Georgia',
            -1: 'Atlantic/Azores',
            0: 'UTC',
            1: 'Europe/London',  # Will show GMT or BST depending on season
            2: 'Europe/Paris',
            3: 'Europe/Istanbul',
            4: 'Asia/Dubai',
            5: 'Asia/Karachi',
            5.5: 'Asia/Kolkata',
            6: 'Asia/Dhaka',
            7: 'Asia/Bangkok',
            8: 'Asia/Shanghai',
            9: 'Asia/Tokyo',
            9.5: 'Australia/Adelaide',
            10: 'Australia/Sydney',
            11: 'Pacific/Guadalcanal',
            12: 'Pacific/Auckland',
            13: 'Pacific/Tongatapu',
            14: 'Pacific/Kiritimati',
        }

        return offset_map.get(offset_hours)
    except Exception as e:
        logger.warning(f"Failed to parse UTC offset '{query}': {e}")
        return None


def fuzzy_search_timezones(query: str, limit: int = 5) -> list[tuple[str, float]]:
    """
    Fuzzy search timezones by city name, abbreviation, or UTC offset.

    Args:
        query: Search query (e.g., "new york", "pst", "utc+3")
        limit: Maximum number of results to return (default: 5)

    Returns:
        List of tuples: [(tz_name, confidence_score), ...]
        Sorted by confidence score (highest first)
    """
    query = query.strip()

    if not query:
        return []

    # Special case: UTC offset parsing
    utc_offset_tz = parse_utc_offset(query)
    if utc_offset_tz:
        return [(utc_offset_tz, 100.0)]

    # Build search corpus from POPULAR_TIMEZONES
    search_corpus = []
    tz_name_map = {}  # Maps search string → IANA timezone name

    for tz_name, aliases in POPULAR_TIMEZONES.items():
        # Add timezone name itself
        search_corpus.append(tz_name)
        tz_name_map[tz_name] = tz_name

        # Add all aliases
        for alias in aliases:
            search_corpus.append(alias)
            tz_name_map[alias] = tz_name

    # Perform fuzzy search using rapidfuzz
    results = process.extract(
        query,
        search_corpus,
        scorer=fuzz.WRatio,  # Weighted ratio - good for partial matches
        limit=limit * 3  # Get more results initially to filter duplicates
    )

    # Deduplicate by timezone name (keep highest score for each timezone)
    seen_timezones = {}
    for match_text, score, _ in results:
        tz_name = tz_name_map.get(match_text)
        if tz_name and tz_name not in seen_timezones:
            seen_timezones[tz_name] = score

    # Sort by score and limit results
    final_results = sorted(
        seen_timezones.items(),
        key=lambda x: x[1],
        reverse=True
    )[:limit]

    return final_results


def validate_timezone(tz_name: str) -> bool:
    """
    Validate if a timezone name is valid.

    Args:
        tz_name: IANA timezone name (e.g., "America/New_York")

    Returns:
        True if valid, False otherwise
    """
    try:
        ZoneInfo(tz_name)
        return True
    except Exception:
        return False

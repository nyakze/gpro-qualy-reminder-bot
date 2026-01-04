"""
Timezone conversion and management utilities for GPRO bot.

This module provides timezone conversion functions, fuzzy timezone search,
and display formatting with automatic DST handling using Python's zoneinfo.
"""

import logging
import re
import json
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from typing import Optional

from rapidfuzz import fuzz, process

logger = logging.getLogger(__name__)

# Path to timezone metadata file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TIMEZONE_DATA_FILE = os.path.join(SCRIPT_DIR, "timezone-info.json")

# Global timezone search index (loaded from file)
_timezone_search_index = None

# Default timezone for users who haven't set a preference
DEFAULT_TIMEZONE = "UTC"


async def download_timezone_data() -> bool:
    """
    Download timezone metadata from Geoapify and save to timezone-info.json.

    Returns:
        True if successful, False otherwise
    """
    import aiohttp

    url = "https://www.geoapify.com/data-share/timezones/timezone-info.json"

    try:
        logger.info(f"Downloading timezone data from {url}...")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    logger.error(
                        f"Failed to download timezone data: HTTP {response.status}"
                    )
                    return False

                data = await response.json()

                # Save to file
                with open(TIMEZONE_DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                logger.info(f"✅ Downloaded timezone data: {len(data)} timezones")
                return True

    except Exception as e:
        logger.error(f"Failed to download timezone data: {e}")
        return False


def build_timezone_search_index() -> dict:
    """
    Build search index from timezone-info.json.

    The index structure:
    {
        'search_corpus': ['entry1', 'entry2', ...],  # All searchable strings
        'tz_name_map': {'entry1': 'IANA/Timezone', ...},  # Maps search strings to IANA names
        'timezone_info': {'IANA/Timezone': {...}, ...}  # Full timezone metadata
    }

    Returns:
        Search index dict, or empty dict if file doesn't exist
    """
    if not os.path.exists(TIMEZONE_DATA_FILE):
        logger.warning(f"Timezone data file not found: {TIMEZONE_DATA_FILE}")
        return {}

    try:
        with open(TIMEZONE_DATA_FILE, "r", encoding="utf-8") as f:
            timezone_data = json.load(f)

        logger.info(
            f"Loaded timezone data: type={type(timezone_data).__name__}, "
            f"length={len(timezone_data) if isinstance(timezone_data, (list, dict)) else 'N/A'}"
        )

        # Log sample of first entry to understand structure
        if isinstance(timezone_data, list) and len(timezone_data) > 0:
            logger.debug(f"Sample entry: {list(timezone_data[0].keys())[:10]}")
        elif isinstance(timezone_data, dict):
            logger.debug(f"Data is dict with keys: {list(timezone_data.keys())[:10]}")

        search_corpus = []
        tz_name_map = {}
        timezone_info = {}

        # Sort entries: canonical timezones first, then aliases
        # This ensures canonical timezones get priority in the mapping
        sorted_entries = sorted(
            timezone_data, key=lambda e: (e.get("type") != "canonical", e.get("tzIdentifier", ""))
        )

        for entry in sorted_entries:
            # Geoapify format uses 'tzIdentifier' instead of 'timezone'
            tz_name = entry.get("tzIdentifier")
            if not tz_name:
                continue

            # Store full metadata
            timezone_info[tz_name] = entry

            # Add timezone name itself (always unique)
            search_corpus.append(tz_name)
            tz_name_map[tz_name] = tz_name

            # Extract region and city from timezone identifier
            region = None
            city = None
            if "/" in tz_name:
                parts = tz_name.split("/")
                region = parts[0] if len(parts) > 0 else None
                city = parts[-1].replace("_", " ")

                # Add city name (only if not already mapped - first one wins, and we sorted canonical first)
                search_corpus.append(city)
                if city not in tz_name_map:
                    tz_name_map[city] = tz_name

                # Add region + city (always unique since we include tz_name)
                region_city = f"{region} {city}"
                search_corpus.append(region_city)
                tz_name_map[region_city] = tz_name

            # Add abbreviations - only if not already mapped (canonical processed first)
            abbr_standard = entry.get("abbreviationStandard")
            if abbr_standard:
                search_corpus.append(abbr_standard)
                if abbr_standard not in tz_name_map:
                    tz_name_map[abbr_standard] = tz_name

                # Add city+abbreviation for better matching (always unique if city exists)
                if city:
                    city_abbr = f"{city} {abbr_standard}"
                    search_corpus.append(city_abbr)
                    tz_name_map[city_abbr] = tz_name

            abbr_dst = entry.get("abbreviationDst")
            if abbr_dst and abbr_dst != abbr_standard:
                search_corpus.append(abbr_dst)
                if abbr_dst not in tz_name_map:
                    tz_name_map[abbr_dst] = tz_name

                # Add city+abbreviation for DST too
                if city:
                    city_abbr_dst = f"{city} {abbr_dst}"
                    search_corpus.append(city_abbr_dst)
                    tz_name_map[city_abbr_dst] = tz_name

            # Add abbreviations (if we had them, but Geoapify doesn't provide them)
            # We could compute current abbreviation, but it changes with DST

        logger.info(
            f"✅ Built search index: {len(timezone_info)} timezones, {len(search_corpus)} search terms"
        )

        return {
            "search_corpus": search_corpus,
            "tz_name_map": tz_name_map,
            "timezone_info": timezone_info,
        }

    except Exception as e:
        logger.error(f"Failed to build timezone search index: {e}")
        return {}


def load_timezone_search_index() -> bool:
    """
    Load timezone search index from file into global _timezone_search_index.

    Returns:
        True if loaded successfully, False otherwise
    """
    global _timezone_search_index

    index = build_timezone_search_index()
    if not index:
        logger.warning(
            "Failed to load timezone search index, falling back to POPULAR_TIMEZONES"
        )
        return False

    _timezone_search_index = index
    return True


# Curated list of ~100 popular timezones with search aliases (DEPRECATED - kept for fallback)
# Format: 'IANA_Zone_Name': ['City Name', 'Abbreviation', 'Alternate Names', ...]
POPULAR_TIMEZONES = {
    # Americas - North America
    "America/New_York": ["New York", "NYC", "EST", "EDT", "Eastern", "US Eastern"],
    "America/Chicago": ["Chicago", "CST", "CDT", "Central", "US Central"],
    "America/Denver": ["Denver", "MST", "MDT", "Mountain", "US Mountain"],
    "America/Los_Angeles": ["Los Angeles", "LA", "PST", "PDT", "Pacific", "US Pacific"],
    "America/Phoenix": ["Phoenix", "Arizona", "MST"],
    "America/Anchorage": ["Anchorage", "Alaska", "AKST", "AKDT"],
    "Pacific/Honolulu": ["Honolulu", "Hawaii", "HST"],
    "America/Toronto": ["Toronto", "Canada Eastern"],
    "America/Vancouver": ["Vancouver", "Canada Pacific"],
    "America/Mexico_City": ["Mexico City", "Mexico"],
    "America/Monterrey": ["Monterrey"],
    # Americas - South America
    "America/Sao_Paulo": ["São Paulo", "Sao Paulo", "Brazil", "BRT", "BRST"],
    "America/Buenos_Aires": ["Buenos Aires", "Argentina", "ART"],
    "America/Santiago": ["Santiago", "Chile", "CLT", "CLST"],
    "America/Bogota": ["Bogota", "Bogotá", "Colombia", "COT"],
    "America/Lima": ["Lima", "Peru", "PET"],
    "America/Caracas": ["Caracas", "Venezuela", "VET"],
    # Americas - Central America & Caribbean
    "America/Panama": ["Panama"],
    "America/Costa_Rica": ["Costa Rica", "San Jose", "San José"],
    "America/Havana": ["Havana", "Cuba", "CST", "CDT"],
    "America/Jamaica": ["Jamaica", "Kingston", "EST"],
    # Europe - Western
    "Europe/London": ["London", "UK", "GMT", "BST", "Britain", "England"],
    "Europe/Dublin": ["Dublin", "Ireland", "IST"],
    "Europe/Lisbon": ["Lisbon", "Portugal", "WET", "WEST"],
    "Atlantic/Reykjavik": ["Reykjavik", "Iceland", "GMT"],
    # Europe - Central
    "Europe/Paris": ["Paris", "France", "CET", "CEST"],
    "Europe/Berlin": ["Berlin", "Germany", "CET", "CEST"],
    "Europe/Amsterdam": ["Amsterdam", "Netherlands", "CET", "CEST"],
    "Europe/Brussels": ["Brussels", "Belgium", "CET", "CEST"],
    "Europe/Madrid": ["Madrid", "Spain", "CET", "CEST"],
    "Europe/Rome": ["Rome", "Italy", "CET", "CEST"],
    "Europe/Vienna": ["Vienna", "Austria", "CET", "CEST"],
    "Europe/Zurich": ["Zurich", "Zürich", "Switzerland", "CET", "CEST"],
    "Europe/Prague": ["Prague", "Czech", "CET", "CEST"],
    "Europe/Warsaw": ["Warsaw", "Poland", "CET", "CEST"],
    "Europe/Budapest": ["Budapest", "Hungary", "CET", "CEST"],
    "Europe/Stockholm": ["Stockholm", "Sweden", "CET", "CEST"],
    "Europe/Oslo": ["Oslo", "Norway", "CET", "CEST"],
    "Europe/Copenhagen": ["Copenhagen", "Denmark", "CET", "CEST"],
    # Europe - Eastern
    "Europe/Helsinki": ["Helsinki", "Finland", "EET", "EEST"],
    "Europe/Athens": ["Athens", "Greece", "EET", "EEST"],
    "Europe/Bucharest": ["Bucharest", "Romania", "EET", "EEST"],
    "Europe/Sofia": ["Sofia", "Bulgaria", "EET", "EEST"],
    "Europe/Istanbul": ["Istanbul", "Turkey", "TRT"],
    "Europe/Kiev": ["Kiev", "Kyiv", "Ukraine", "EET", "EEST"],
    "Europe/Moscow": ["Moscow", "Russia", "MSK"],
    "Europe/Minsk": ["Minsk", "Belarus", "MSK"],
    "Europe/Kaliningrad": ["Kaliningrad", "Russia Kaliningrad"],
    "Europe/Samara": ["Samara", "Russia Samara"],
    "Europe/Volgograd": ["Volgograd", "Russia Volgograd"],
    # Asia - Middle East
    "Asia/Dubai": ["Dubai", "UAE", "GST"],
    "Asia/Riyadh": ["Riyadh", "Saudi Arabia", "AST"],
    "Asia/Jerusalem": ["Jerusalem", "Israel", "IST", "IDT"],
    "Asia/Beirut": ["Beirut", "Lebanon", "EET", "EEST"],
    "Asia/Tehran": ["Tehran", "Iran", "IRST", "IRDT"],
    # Asia - South Asia
    "Asia/Kolkata": [
        "Kolkata",
        "Calcutta",
        "India",
        "IST",
        "Mumbai",
        "Delhi",
        "Bangalore",
    ],
    "Asia/Karachi": ["Karachi", "Pakistan", "PKT"],
    "Asia/Dhaka": ["Dhaka", "Bangladesh", "BST"],
    "Asia/Kathmandu": ["Kathmandu", "Nepal", "NPT"],
    "Asia/Colombo": ["Colombo", "Sri Lanka", "IST"],
    # Asia - Southeast Asia
    "Asia/Bangkok": ["Bangkok", "Thailand", "ICT"],
    "Asia/Singapore": ["Singapore", "SGT"],
    "Asia/Kuala_Lumpur": ["Kuala Lumpur", "Malaysia", "MYT"],
    "Asia/Jakarta": ["Jakarta", "Indonesia", "WIB"],
    "Asia/Manila": ["Manila", "Philippines", "PHT"],
    "Asia/Ho_Chi_Minh": ["Ho Chi Minh", "Saigon", "Vietnam", "ICT"],
    # Asia - East Asia
    "Asia/Hong_Kong": ["Hong Kong", "HKT"],
    "Asia/Shanghai": ["Shanghai", "China", "CST", "Beijing"],
    "Asia/Taipei": ["Taipei", "Taiwan", "CST"],
    "Asia/Tokyo": ["Tokyo", "Japan", "JST"],
    "Asia/Seoul": ["Seoul", "South Korea", "KST"],
    "Asia/Pyongyang": ["Pyongyang", "North Korea", "KST"],
    # Asia - Central Asia
    "Asia/Almaty": ["Almaty", "Kazakhstan", "ALMT"],
    "Asia/Tashkent": ["Tashkent", "Uzbekistan", "UZT"],
    "Asia/Yekaterinburg": ["Yekaterinburg", "Russia Yekaterinburg", "YEKT"],
    "Asia/Novosibirsk": ["Novosibirsk", "Russia Novosibirsk", "NOVT"],
    "Asia/Krasnoyarsk": ["Krasnoyarsk", "Russia Krasnoyarsk", "KRAT"],
    "Asia/Irkutsk": ["Irkutsk", "Russia Irkutsk", "IRKT"],
    "Asia/Yakutsk": ["Yakutsk", "Russia Yakutsk", "YAKT"],
    "Asia/Vladivostok": ["Vladivostok", "Russia Vladivostok", "VLAT"],
    # Pacific - Oceania
    "Pacific/Auckland": ["Auckland", "New Zealand", "NZST", "NZDT"],
    "Pacific/Fiji": ["Fiji", "Suva", "FJT"],
    "Pacific/Guam": ["Guam", "ChST"],
    "Pacific/Port_Moresby": ["Port Moresby", "Papua New Guinea", "PGT"],
    # Australia
    "Australia/Sydney": ["Sydney", "Australia", "AEST", "AEDT"],
    "Australia/Melbourne": ["Melbourne", "AEST", "AEDT"],
    "Australia/Brisbane": ["Brisbane", "AEST"],
    "Australia/Perth": ["Perth", "AWST"],
    "Australia/Adelaide": ["Adelaide", "ACST", "ACDT"],
    "Australia/Darwin": ["Darwin", "ACST"],
    # Africa
    "Africa/Cairo": ["Cairo", "Egypt", "EET", "EEST"],
    "Africa/Johannesburg": ["Johannesburg", "South Africa", "SAST"],
    "Africa/Lagos": ["Lagos", "Nigeria", "WAT"],
    "Africa/Nairobi": ["Nairobi", "Kenya", "EAT"],
    "Africa/Casablanca": ["Casablanca", "Morocco", "WET", "WEST"],
    "Africa/Algiers": ["Algiers", "Algeria", "CET"],
    "Africa/Tunis": ["Tunis", "Tunisia", "CET"],
    # Atlantic
    "Atlantic/Azores": ["Azores", "AZOT", "AZOST"],
    "Atlantic/Cape_Verde": ["Cape Verde", "CVT"],
    # UTC
    "UTC": ["UTC", "GMT", "Universal"],
    "Etc/GMT": ["GMT", "UTC", "Universal"],
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
        logger.warning(
            f"Failed to get timezone for user {user_id}: {e}, falling back to UTC"
        )
        return ZoneInfo("UTC")


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
    dt: datetime, user_id: int, format_str: str = "%d.%m %H:%M"
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
        if "/" in tz_str:
            city = tz_str.split("/")[-1].replace("_", " ")
            return f"{city} ({tz_abbr})"

        # Fallback: just show abbreviation
        return tz_abbr
    except Exception as e:
        logger.error(f"Failed to get timezone display name: {e}")
        return str(tz)


def parse_utc_offset(query: str) -> Optional[str]:
    """
    Parse UTC offset queries like "UTC+3", "GMT-5", "+04", "-5" and find matching IANA timezone.

    Args:
        query: Query string like "UTC+3", "GMT-5", "UTC+5.5", "+04", "-5"

    Returns:
        IANA timezone name or None if not found
    """
    # Match patterns: UTC+3, GMT-5, UTC+5.5, +04, -5, etc.
    # More flexible pattern that handles: UTC+3, GMT-5, +04, -5, +0400
    pattern = r"^(?:UTC|GMT)?\s*([+-]?\d+(?:[:.]\d+)?)\s*$"
    match = re.match(pattern, query.upper().strip())

    if not match:
        return None

    try:
        offset_str = match.group(1)

        # Handle different offset formats
        if ":" in offset_str or "." in offset_str:
            # Already in hour.decimal or hour:minute format
            offset_hours = float(offset_str.replace(":", "."))
        elif len(offset_str) >= 3 and offset_str[-2:].isdigit():
            # Format like "+0400" or "-0530" (HHMM format)
            sign = 1 if offset_str[0] != "-" else -1
            offset_str = offset_str.lstrip("+-")
            if len(offset_str) == 4:
                hours = int(offset_str[:2])
                minutes = int(offset_str[2:])
                offset_hours = sign * (hours + minutes / 60.0)
            else:
                offset_hours = float(offset_str)
        else:
            # Simple format like "+4" or "-5"
            offset_hours = float(offset_str)

        # Common UTC offset mappings to representative timezones
        offset_map = {
            -12: "Etc/GMT+12",
            -11: "Pacific/Pago_Pago",
            -10: "Pacific/Honolulu",
            -9: "America/Anchorage",
            -8: "America/Los_Angeles",
            -7: "America/Denver",
            -6: "America/Chicago",
            -5: "America/New_York",
            -4: "America/Caracas",
            -3: "America/Sao_Paulo",
            -2: "Atlantic/South_Georgia",
            -1: "Atlantic/Azores",
            0: "UTC",
            1: "Europe/London",  # Will show GMT or BST depending on season
            2: "Europe/Paris",
            3: "Europe/Istanbul",
            4: "Asia/Dubai",
            5: "Asia/Karachi",
            5.5: "Asia/Kolkata",
            6: "Asia/Dhaka",
            7: "Asia/Bangkok",
            8: "Asia/Shanghai",
            9: "Asia/Tokyo",
            9.5: "Australia/Adelaide",
            10: "Australia/Sydney",
            11: "Pacific/Guadalcanal",
            12: "Pacific/Auckland",
            13: "Pacific/Tongatapu",
            14: "Pacific/Kiritimati",
        }

        return offset_map.get(offset_hours)
    except Exception as e:
        logger.warning(f"Failed to parse UTC offset '{query}': {e}")
        return None


def fuzzy_search_timezones(query: str, limit: int = 5) -> list[tuple[str, float]]:
    """
    Fuzzy search timezones by city name, country, or UTC offset.

    Args:
        query: Search query (e.g., "new york", "moscow", "москва", "utc+3")
        limit: Maximum number of results to return (default: 5)

    Returns:
        List of tuples: [(tz_name, confidence_score), ...]
        Sorted by confidence score (highest first)
    """
    query = query.strip()

    if not query:
        return []

    # Note: We used to have UTC offset parsing here that returned a single hardcoded timezone
    # Now we let fuzzy search find ALL timezones matching the offset abbreviation (e.g., all +04 zones)
    # The abbreviations are already in the search corpus from Geoapify data

    # Try to use new search index if available
    if _timezone_search_index:
        search_corpus = _timezone_search_index["search_corpus"]
        tz_name_map = _timezone_search_index["tz_name_map"]
        logger.debug(
            f"Using timezone search index: {len(search_corpus)} search terms, {len(tz_name_map)} mappings"
        )
    else:
        # Fallback to POPULAR_TIMEZONES
        logger.debug("Using POPULAR_TIMEZONES fallback for timezone search")
        search_corpus = []
        tz_name_map = {}

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
        limit=limit * 3,  # Get more results initially to filter duplicates
    )

    logger.debug(f"Fuzzy search for '{query}': found {len(results)} raw matches")

    # Deduplicate by timezone name (keep highest score for each timezone)
    seen_timezones = {}
    for match_text, score, _ in results:
        tz_name = tz_name_map.get(match_text)
        if tz_name and tz_name not in seen_timezones:
            seen_timezones[tz_name] = score
        elif not tz_name:
            logger.warning(
                f"Match '{match_text}' not found in tz_name_map (score: {score})"
            )

    logger.debug(
        f"After deduplication: {len(seen_timezones)} unique timezones for query '{query}'"
    )

    # Sort by score and limit results
    final_results = sorted(seen_timezones.items(), key=lambda x: x[1], reverse=True)[
        :limit
    ]

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

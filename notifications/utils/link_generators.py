"""Link generation utilities for GPRO website and APP URLs"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# GPRO URL endpoints
GPRO_LIVE_ENDPOINT = "racescreenlive.asp"
GPRO_REPLAY_ENDPOINT = "racescreen.asp"

# Group name mapping
GROUP_NAMES = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}


def _validate_language(gpro_lang: str) -> str:
    """Validate and return language code, fallback to 'gb' if invalid"""
    from notifications.users import is_valid_language

    if not is_valid_language(gpro_lang):
        logger.warning(f"Invalid language code '{gpro_lang}', falling back to 'gb'")
        return "gb"
    return gpro_lang


def _parse_group(group: str) -> tuple[Optional[str], Optional[str]]:
    """Parse group string into letter and number

    Returns:
        Tuple of (letter, number) or (None, None) if invalid
    """
    if not group:
        return None, None

    group = group.strip().upper()

    if group == "E":
        return "E", None

    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        return None, None

    return match.groups()


def generate_gpro_link(
    group: str, gpro_lang: str = "gb", link_type: str = "live"
) -> str:
    """Generate GPRO race link based on group format and type

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')
        link_type: 'live' for live race, 'replay' for replay

    Examples: E → Elite, M3 → Master - 3, A42 → Amateur - 42, R11 → Rookie - 11
    """
    gpro_lang = _validate_language(gpro_lang)
    endpoint = GPRO_LIVE_ENDPOINT if link_type == "live" else GPRO_REPLAY_ENDPOINT
    base_url = f"https://gpro.net/{gpro_lang}/{endpoint}?Group="

    letter, number = _parse_group(group)

    if letter is None:
        return base_url

    if letter == "E":
        return f"{base_url}Elite"

    group_name = GROUP_NAMES[letter]
    encoded = f"{group_name}%20-%20{number}"
    return f"{base_url}{encoded}"


def generate_race_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate race live link - wrapper for backwards compatibility"""
    return generate_gpro_link(group, gpro_lang, "live")


def generate_replay_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate race replay link - wrapper for backwards compatibility"""
    return generate_gpro_link(group, gpro_lang, "replay")


def generate_starting_grid_link(group: str, gpro_lang: str = "gb") -> str:
    """Generate Starting Grid link with user's group

    Args:
        group: User's GPRO group (E, M3, R11, etc.)
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Starting Grid page
    """
    gpro_lang = _validate_language(gpro_lang)
    base_url = f"https://gpro.net/{gpro_lang}/StartingGrid.asp?Group="

    letter, number = _parse_group(group)

    if letter is None:
        return base_url

    if letter == "E":
        return f"{base_url}Elite"

    group_name = GROUP_NAMES[letter]
    encoded = f"{group_name}%20-%20{number}"
    return f"{base_url}{encoded}"


def generate_quali_link(gpro_lang: str = "gb") -> str:
    """Generate Qualifying page link

    Args:
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Qualifying page
    """
    gpro_lang = _validate_language(gpro_lang)
    return f"https://gpro.net/{gpro_lang}/Qualify.asp"


def generate_race_analysis_link(gpro_lang: str = "gb") -> str:
    """Generate Race Analysis page link

    Args:
        gpro_lang: GPRO language code for URL (e.g., 'gb', 'de', 'fr')

    Returns:
        str: URL to Race Analysis page
    """
    gpro_lang = _validate_language(gpro_lang)
    return f"https://gpro.net/{gpro_lang}/RaceAnalysis.asp"


# ==========================================
# APP Website URL Generators
# ==========================================


def format_group_for_app_url(group: str) -> str:
    """Convert group code to APP URL format

    Examples:
        E → Elite
        M3 → Master%20-%203
        R11 → Rookie%20-%2011

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL-encoded group string for APP URLs
    """
    letter, number = _parse_group(group)

    if letter is None:
        return ""

    if letter == "E":
        return "Elite"

    group_name = GROUP_NAMES[letter]
    return f"{group_name}%20-%20{number}"


def generate_app_quali_link() -> str:
    """Generate APP qualifying page link (office page)

    Returns:
        str: URL to APP office page (no language or group support)
    """
    return "https://app.gpro.net/office"


def generate_app_starting_grid_link(group: str = None) -> str:
    """Generate APP starting grid link

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL to APP starting grid page
    """
    base_url = "https://app.gpro.net/qstandings/startgrid"

    if not group:
        return base_url

    formatted_group = format_group_for_app_url(group)
    if formatted_group:
        return f"{base_url}/{formatted_group}"
    return base_url


def generate_app_race_live_link() -> str:
    """Generate APP race live link

    Returns:
        str: URL to APP race live page (no group or language support)
    """
    return "https://app.gpro.net/liverace"


def generate_app_race_replay_link() -> str:
    """Generate APP race replay link

    Returns:
        str: URL to APP race replay page (no group or language support)
    """
    return "https://app.gpro.net/pastrace/racereplay"


def generate_app_race_analysis_link() -> str:
    """Generate APP race analysis link

    Returns:
        str: URL to APP race analysis page (no group or language support)
    """
    return "https://app.gpro.net/pastrace/analysis"


def generate_app_race_summary_link(group: str = None) -> str:
    """Generate APP race summary link

    Args:
        group: User's GPRO group (E, M3, R11, etc.)

    Returns:
        str: URL to APP race summary page
    """
    base_url = "https://app.gpro.net/pastrace/summary"

    if not group:
        return base_url

    formatted_group = format_group_for_app_url(group)
    if formatted_group:
        return f"{base_url}/{formatted_group}"
    return base_url

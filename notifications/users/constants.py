"""User data constants and defaults"""

import logging

logger = logging.getLogger(__name__)

# Snooze configuration constants
SNOOZE_TOLERANCE_SECONDS = 120  # Snoozes fire up to 2 minutes late
SNOOZE_MAX_COUNTS = {
    "72h": 3,
    "48h": 3,
    "24h": 3,
    "2h": 3,
    "10min": 3,
    "opens_soon": 3,
    "deadline": 3,
}

# Import UI language list for validation
try:
    from utils import UI_LANGUAGE_DISPLAY
except ImportError:
    # Fallback if import fails (shouldn't happen in normal operation)
    UI_LANGUAGE_DISPLAY = {
        "gb": "English",
        "ru": "Русский",
        "br": "Português",
        "it": "Italiano",
        "es": "Español",
        "fr": "Français",
        "nl": "Nederlands",
        "bg": "Български",
        "cz": "Čeština",
        "in": "हिन्दी",
        "ua": "Українська",
        "pt": "Português",
    }

# Language options for URL generation (user-facing)
LANGUAGE_OPTIONS = {
    "gb": "🇬🇧 English",
    "de": "🇩🇪 Deutsch",
    "es": "🇪🇸 Español",
    "ro": "🇷🇴 Română",
    "it": "🇮🇹 Italiano",
    "fr": "🇫🇷 Français",
    "pl": "🇵🇱 Polski",
    "bg": "🇧🇬 Български",
    "mk": "🇲🇰 Македонски",
    "nl": "🇳🇱 Nederlands",
    "fi": "🇫🇮 Suomi",
    "hu": "🇭🇺 Magyar",
    "tr": "🇹🇷 Türkçe",
    "gr": "🇬🇷 Ελληνικά",
    "dk": "🇩🇰 Dansk",
    "pt": "🇵🇹 Português",
    "ru": "🇷🇺 Русский",
    "rs": "🇷🇸 Српски",
    "se": "🇸🇪 Svenska",
    "lt": "🇱🇹 Lietuvių",
    "ee": "🇪🇪 Eesti",
    "al": "🇦🇱 Shqip",
    "hr": "🇭🇷 Hrvatski",
    "cn": "🇨🇳 中文",
    "my": "🇲🇾 Bahasa Melayu",
    "in": "🇮🇳 हिन्दी",
    "pi": "🏴‍☠️ Pirate",
    "be": "🇧🇪 Vlaams",
    "br": "🇧🇷 Português (BR)",
    "cz": "🇨🇿 Čeština",
    "sk": "🇸🇰 Slovenčina",
}

DEFAULT_USER_LANG = "gb"


def get_default_notification_preferences():
    """Default notification settings - all enabled by default"""
    return {
        "72h": True,
        "48h": True,
        "24h": True,
        "2h": True,
        "10min": True,
        "opens_soon": True,
        "quali_results": True,
        "race_replay": True,
        "race_live": True,
        "race_results": True,
        "new_season_reminder": True,
    }


def get_default_custom_notifications():
    """Default custom notification settings - empty slots"""
    return [
        {"enabled": False, "hours_before": None},
        {"enabled": False, "hours_before": None},
    ]


def get_default_snooze_tracking():
    """Default snooze tracking - 0 snoozes per notification type"""
    return {
        "72h": 0,
        "48h": 0,
        "24h": 0,
        "2h": 0,
        "10min": 0,
    }

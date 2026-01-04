import os
from dotenv import load_dotenv

load_dotenv()

# Validate required tokens
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in .env file")

GPRO_API_TOKEN = os.getenv("GPRO_API_TOKEN")
if not GPRO_API_TOKEN:
    raise ValueError("GPRO_API_TOKEN not set in .env file")

# Validate ADMIN_USER_ID (supports comma-separated values)
admin_id_str = os.getenv("ADMIN_USER_ID")
if not admin_id_str:
    raise ValueError("ADMIN_USER_ID not set in .env file")

try:
    # Parse comma-separated IDs
    admin_ids = [int(uid.strip()) for uid in admin_id_str.split(",")]
    if not admin_ids:
        raise ValueError("ADMIN_USER_ID cannot be empty")
    ADMIN_USER_IDS = set(admin_ids)  # Use set for O(1) membership checks
except ValueError as e:
    if "invalid literal for int()" in str(e):
        raise ValueError(
            f"ADMIN_USER_ID must contain valid integers, got: {admin_id_str}"
        )
    raise

# Use absolute paths based on script location for robustness
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NEXT_SEASON_FILE = os.path.join(_SCRIPT_DIR, "next_season_calendar.json")
CALENDAR_FILE = os.path.join(_SCRIPT_DIR, "gpro_calendar.json")
GPRO_API_LANG = "gb"

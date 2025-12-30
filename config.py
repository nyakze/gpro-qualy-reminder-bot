import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GPRO_API_TOKEN = os.getenv('GPRO_API_TOKEN')

# Validate ADMIN_USER_ID (supports comma-separated values)
admin_id_str = os.getenv('ADMIN_USER_ID')
if not admin_id_str:
    raise ValueError("ADMIN_USER_ID not set in .env file")

try:
    # Parse comma-separated IDs
    admin_ids = [int(uid.strip()) for uid in admin_id_str.split(',')]
    if not admin_ids:
        raise ValueError("ADMIN_USER_ID cannot be empty")
    ADMIN_USER_IDS = set(admin_ids)  # Use set for O(1) membership checks
except ValueError as e:
    if "invalid literal for int()" in str(e):
        raise ValueError(f"ADMIN_USER_ID must contain valid integers, got: {admin_id_str}")
    raise

NEXT_SEASON_FILE = 'next_season_calendar.json'
CALENDAR_FILE = 'gpro_calendar.json'
GPRO_LANG = 'gb'

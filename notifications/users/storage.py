"""User data storage and persistence"""

import json
import logging
import os
import tempfile
from typing import Dict

logger = logging.getLogger(__name__)

# Use absolute path based on script location for robustness
# This file is at notifications/users/storage.py, so we need to go up 2 levels
_SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
USERS_FILE = os.path.join(_SCRIPT_DIR, "users_data.json")

# In-memory cache
users_data: Dict[int, Dict] = {}


def load_users_data():
    """Load user data from JSON file into memory"""
    global users_data
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                raw_data = json.load(f)
                # TYPE FIX: Convert string keys → int keys
                clean_data = {int(k_str): status for k_str, status in raw_data.items()}
                users_data.update(clean_data)
                logger.debug(f"✅ Loaded {len(users_data)} users (int keys)")
        except Exception as e:
            logger.error(f"Load failed: {e}")


def save_users_data():
    """Save user data with atomic write to prevent corruption"""
    temp_file = None
    try:
        # Use unique temp file to avoid race conditions
        fd, temp_file = tempfile.mkstemp(dir=os.path.dirname(USERS_FILE), suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                save_data = {str(k): v for k, v in users_data.items()}
                json.dump(save_data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_file, USERS_FILE)
            logger.debug(f"Saved {len(users_data)} users")
        except Exception:
            # Close the fd if it wasn't closed by os.fdopen
            try:
                os.close(fd)
            except (OSError, ValueError):
                pass
            raise
    except Exception as e:
        logger.error(f"Save failed: {e}")
    finally:
        # Clean up temp file if it still exists
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

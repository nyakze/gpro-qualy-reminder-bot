"""User data storage, persistence, and backup recovery."""

import json
import logging
import os
import re
import tempfile
from datetime import UTC, datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

_SCRIPT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
USERS_FILE = os.path.join(_SCRIPT_DIR, "users_data.json")
_BACKUP_FILENAME_RE = re.compile(r"^users_data_\d{8}_\d{6}\.json$")

users_data: Dict[int, Dict] = {}


def _get_backup_dir() -> str:
    """Return the backup directory beside the configured users file."""
    return os.path.join(os.path.dirname(USERS_FILE), "backup")


def _validate_users_payload(
    raw_data: Any, *, require_nonempty: bool = False
) -> dict[int, dict]:
    """Validate and normalize JSON user data."""
    if not isinstance(raw_data, dict):
        raise ValueError("users data must be a JSON object")
    if require_nonempty and not raw_data:
        raise ValueError("backup contains no users")

    clean_data: dict[int, dict] = {}
    for raw_user_id, status in raw_data.items():
        user_id = int(raw_user_id)
        if not isinstance(status, dict):
            raise ValueError(f"profile for user {user_id} must be an object")
        clean_data[user_id] = status
    return clean_data


def _read_users_file(path: str, *, require_nonempty: bool = False) -> dict[int, dict]:
    with open(path, encoding="utf-8") as users_file:
        raw_data = json.load(users_file)
    return _validate_users_payload(raw_data, require_nonempty=require_nonempty)


def _write_users_payload(path: str, payload: dict[int, dict]) -> None:
    """Atomically write normalized user data."""
    temp_file: str | None = None
    try:
        fd, temp_file = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as users_file:
            save_data = {str(user_id): status for user_id, status in payload.items()}
            json.dump(save_data, users_file, indent=2)
            users_file.flush()
            os.fsync(users_file.fileno())
        os.replace(temp_file, path)
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass


def _find_latest_valid_backup() -> tuple[str, dict[int, dict]] | None:
    """Return the newest valid classic backup."""
    backup_dir = _get_backup_dir()
    try:
        filenames = [
            filename
            for filename in os.listdir(backup_dir)
            if _BACKUP_FILENAME_RE.fullmatch(filename)
        ]
    except OSError:
        return None

    candidates: list[tuple[float, str]] = []
    for filename in filenames:
        path = os.path.join(backup_dir, filename)
        try:
            candidates.append((os.path.getmtime(path), path))
        except OSError:
            continue

    for _, path in sorted(candidates, reverse=True):
        try:
            return path, _read_users_file(path, require_nonempty=True)
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
            logger.warning(
                "Skipping invalid users backup %s: %s",
                os.path.basename(path),
                error,
            )
    return None


def _restore_users_from_backup(reason: str) -> dict[int, dict] | None:
    """Restore the newest valid backup after missing/corrupt primary data."""
    backup = _find_latest_valid_backup()
    if backup is None:
        logger.error("Users data unavailable (%s); no valid backup found", reason)
        return None

    backup_path, restored_data = backup
    quarantined_path: str | None = None
    if os.path.exists(USERS_FILE):
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S_%f")
        quarantined_path = f"{USERS_FILE}.corrupt_{timestamp}"
        try:
            os.replace(USERS_FILE, quarantined_path)
        except OSError as error:
            logger.error("Failed to quarantine invalid users file: %s", error)
            return None

    try:
        _write_users_payload(USERS_FILE, restored_data)
    except OSError as error:
        logger.error("Failed to restore users data from backup: %s", error)
        return None

    logger.warning(
        "Restored %s users from backup %s after %s%s",
        len(restored_data),
        os.path.basename(backup_path),
        reason,
        (
            f"; invalid file saved as {os.path.basename(quarantined_path)}"
            if quarantined_path
            else ""
        ),
    )
    return restored_data


def load_users_data() -> None:
    """Load users, automatically recovering missing or invalid primary data."""
    clean_data: dict[int, dict] | None
    try:
        clean_data = _read_users_file(USERS_FILE)
    except FileNotFoundError:
        clean_data = _restore_users_from_backup("primary file is missing")
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        logger.error("Users data load failed: %s", error)
        clean_data = _restore_users_from_backup("primary file is invalid")

    if clean_data is None:
        return

    users_data.clear()
    users_data.update(clean_data)
    logger.debug("Loaded %s users (int keys)", len(users_data))


def save_users_data() -> None:
    """Save user data with an atomic write."""
    try:
        _write_users_payload(USERS_FILE, users_data)
        logger.debug("Saved %s users", len(users_data))
    except OSError as error:
        logger.error("Save failed: %s", error)

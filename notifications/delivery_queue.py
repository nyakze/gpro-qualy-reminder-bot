"""Persistent storage for pending notification deliveries."""

from __future__ import annotations

import json
import logging
import os
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

logger = logging.getLogger(__name__)

QUEUE_VERSION = 1


@dataclass(frozen=True)
class RetryState:
    """Persisted retry metadata for one event/user pair."""

    attempts: int
    next_attempt_at: datetime


def _get_delivery_queue_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "notification_delivery_queue.json",
    )


def _encode_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return {"__datetime__": value.isoformat()}
    if isinstance(value, dict):
        return {str(key): _encode_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode_value(item) for item in value]
    return value


def _decode_value(value: Any) -> Any:
    if isinstance(value, dict):
        if set(value) == {"__datetime__"}:
            parsed = datetime.fromisoformat(value["__datetime__"])
            return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
        return {key: _decode_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_decode_value(item) for item in value]
    return value


def _serialize_notification(notification: tuple) -> dict[str, Any]:
    ntype, race_id, race_data, label, history_key, *target = notification
    data = {
        "type": ntype,
        "race_id": race_id,
        "race_data": _encode_value(race_data),
        "label": label,
        "history_key": [history_key[0], history_key[1]],
    }
    if target:
        data["target_user_id"] = target[0]
    return data


def _deserialize_notification(data: dict[str, Any]) -> tuple:
    history_key_data = data["history_key"]
    history_key = (int(history_key_data[0]), str(history_key_data[1]))
    notification: tuple[Any, ...]
    notification = (
        str(data["type"]),
        int(data["race_id"]),
        _decode_value(data["race_data"]),
        str(data["label"]),
        history_key,
    )
    if "target_user_id" in data:
        notification += (int(data["target_user_id"]),)
    return notification


def load_delivery_queue() -> (
    tuple[dict[tuple[int, str], tuple], dict[tuple[int, str, int], RetryState]]
):
    """Load pending events and retry metadata, skipping malformed entries."""
    path = _get_delivery_queue_path()
    if not os.path.exists(path):
        return {}, {}

    try:
        with open(path, encoding="utf-8") as queue_file:
            payload = json.load(queue_file)
        if not isinstance(payload, dict):
            raise ValueError("delivery queue root must be an object")
        if payload.get("version") != QUEUE_VERSION:
            raise ValueError("unsupported delivery queue version")

        pending: dict[tuple[int, str], tuple] = {}
        for raw_notification in payload.get("pending", []):
            try:
                notification = _deserialize_notification(raw_notification)
                pending[notification[4]] = notification
            except (KeyError, TypeError, ValueError, IndexError) as error:
                logger.warning("Skipping malformed pending delivery: %s", error)

        attempts: dict[tuple[int, str, int], RetryState] = {}
        for raw_attempt in payload.get("attempts", []):
            try:
                key = (
                    int(raw_attempt["race_id"]),
                    str(raw_attempt["label"]),
                    int(raw_attempt["user_id"]),
                )
                if (key[0], key[1]) not in pending:
                    continue
                next_attempt_at = datetime.fromisoformat(raw_attempt["next_attempt_at"])
                if next_attempt_at.tzinfo is None:
                    next_attempt_at = next_attempt_at.replace(tzinfo=UTC)
                attempts[key] = RetryState(
                    attempts=max(0, int(raw_attempt["attempts"])),
                    next_attempt_at=next_attempt_at,
                )
            except (KeyError, TypeError, ValueError) as error:
                logger.warning("Skipping malformed delivery retry: %s", error)

        logger.info(
            "Loaded persistent delivery queue: %s events, %s retries",
            len(pending),
            len(attempts),
        )
        return pending, attempts
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        logger.error("Failed to load delivery queue: %s", error)
        return {}, {}


def save_delivery_queue(
    pending: dict[tuple[int, str], tuple],
    attempts: dict[tuple[int, str, int], RetryState],
) -> None:
    """Atomically persist pending events and their retry schedule."""
    path = _get_delivery_queue_path()
    payload = {
        "version": QUEUE_VERSION,
        "pending": [
            _serialize_notification(notification) for notification in pending.values()
        ],
        "attempts": [
            {
                "race_id": race_id,
                "label": label,
                "user_id": user_id,
                "attempts": state.attempts,
                "next_attempt_at": state.next_attempt_at.isoformat(),
            }
            for (race_id, label, user_id), state in attempts.items()
        ],
    }

    temp_path: str | None = None
    try:
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(path), suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as queue_file:
            json.dump(payload, queue_file, indent=2)
            queue_file.flush()
            os.fsync(queue_file.fileno())
        os.replace(temp_path, path)
    except OSError as error:
        logger.error("Failed to save delivery queue: %s", error)
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

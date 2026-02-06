"""Rate limiting middleware - progressive penalties for repeat offenders"""

import json
import logging
import os
import tempfile
import time
from typing import Callable, Awaitable, Dict, Any, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, field
from aiogram import BaseMiddleware
from aiogram.types import Update

logger = logging.getLogger(__name__)

# Use absolute path based on script location
_SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RL_FILE = os.path.join(_SCRIPT_DIR, "rate_limit_data.json")

# Very loose limits - only catch blatant abuse
# Normal users clicking through menus won't hit these
RATE_LIMITS = {
    # Commands: max 10 per 30 seconds (very generous)
    "command": {"max": 10, "window": 30},
    # Callbacks: max 20 per 15 seconds (clicking through menus is fine)
    "callback": {"max": 20, "window": 15},
    # Messages (text): max 15 per 20 seconds
    "message": {"max": 15, "window": 20},
}

# Progressive block durations (seconds)
BLOCK_DURATIONS = [30, 120, 300]  # First: 30s, Second: 2min, Third+: 5min

# Reset violation count after this many seconds of good behavior
VIOLATION_RESET_AFTER = 604800  # 7 days

# Track if data has been loaded
_rl_data_loaded = False


@dataclass
class UserRateLimitState:
    """Track rate limit state for a user"""

    request_history: Dict[str, deque] = field(
        default_factory=lambda: defaultdict(lambda: deque(maxlen=100))
    )
    violation_count: int = 0
    blocked_until: float = 0
    last_warning: float = 0
    warned_this_session: bool = False
    last_violation_time: float = 0


# Track rate limit state per user
_user_states: Dict[int, UserRateLimitState] = defaultdict(UserRateLimitState)


def _load_rate_limit_data():
    """Load rate limit state from JSON file"""
    global _rl_data_loaded
    if _rl_data_loaded:
        return

    if os.path.exists(RL_FILE):
        try:
            with open(RL_FILE, "r") as f:
                raw_data = json.load(f)
                loaded_count = 0
                now = time.time()
                for uid_str, state_data in raw_data.items():
                    uid = int(uid_str)
                    state = _user_states[uid]
                    state.violation_count = state_data.get("violation_count", 0)
                    state.blocked_until = state_data.get("blocked_until", 0)
                    state.last_warning = state_data.get("last_warning", 0)
                    state.warned_this_session = state_data.get(
                        "warned_this_session", False
                    )
                    state.last_violation_time = state_data.get("last_violation_time", 0)
                    loaded_count += 1
                logger.info(f"Loaded rate limit data for {loaded_count} users")
        except Exception as e:
            logger.error(f"Failed to load rate limit data: {e}")

    _rl_data_loaded = True


def _save_rate_limit_data():
    """Save rate limit state with atomic write"""
    temp_file = None
    try:
        fd, temp_file = tempfile.mkstemp(dir=os.path.dirname(RL_FILE), suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                save_data = {}
                for uid, state in _user_states.items():
                    # Only save users with violations or blocks
                    if (
                        state.violation_count > 0
                        or state.blocked_until > 0
                        or state.warned_this_session
                    ):
                        save_data[str(uid)] = {
                            "violation_count": state.violation_count,
                            "blocked_until": state.blocked_until,
                            "last_warning": state.last_warning,
                            "warned_this_session": state.warned_this_session,
                            "last_violation_time": state.last_violation_time,
                        }
                json.dump(save_data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_file, RL_FILE)
            logger.debug(f"Saved rate limit data for {len(save_data)} users")
        except Exception:
            try:
                os.close(fd)
            except (OSError, ValueError):
                pass
            raise
    except Exception as e:
        logger.error(f"Failed to save rate limit data: {e}")
    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass


class RateLimitMiddleware(BaseMiddleware):
    """Middleware for progressive rate limiting with escalating penalties.

    Behavior:
    - First violation: Warn only (message shown to user)
    - Second violation: Block for 30 seconds
    - Third violation: Block for 2 minutes
    - Fourth+ violation: Block for 5 minutes

    - Admins are exempt from all rate limiting
    - Normal menu interactions won't trigger these limits
    - State is persisted to rate_limit_data.json
    """

    def __init__(self, admin_ids: Optional[set] = None):
        super().__init__()
        self.admin_ids = admin_ids or set()
        _load_rate_limit_data()

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user_id = self._get_user_id(event)
        if not user_id:
            return await handler(event, data)

        # Admins are exempt
        if user_id in self.admin_ids:
            return await handler(event, data)

        request_type = self._get_request_type(event)
        if not request_type:
            return await handler(event, data)

        state = _user_states[user_id]
        now = time.time()

        # Check if user is currently blocked
        if now < state.blocked_until:
            remaining = int(state.blocked_until - now)
            logger.debug(f"Rate limit block for user {user_id}: {remaining}s remaining")
            # Silently drop the request
            return None

        # Reset violations if enough time has passed since last violation
        self._maybe_reset_violations(state, now)

        # Check rate limit
        is_violation, reason = self._check_rate_limit(state, request_type, now)

        if is_violation:
            return await self._handle_violation(
                user_id, state, reason, event, handler, data
            )

        return await handler(event, data)

    def _maybe_reset_violations(self, state: UserRateLimitState, now: float):
        """Reset violation count after period of good behavior"""
        if (
            state.violation_count > 0
            and state.last_violation_time > 0
            and now - state.last_violation_time > VIOLATION_RESET_AFTER
        ):
            logger.debug(
                f"Resetting violation count after {VIOLATION_RESET_AFTER}s of good behavior"
            )
            state.violation_count = 0
            state.warned_this_session = False
            _save_rate_limit_data()

    def _get_user_id(self, event: Update) -> Optional[int]:
        """Extract user ID from update"""
        if event.message and event.message.from_user:
            return event.message.from_user.id
        elif event.callback_query and event.callback_query.from_user:
            return event.callback_query.from_user.id
        elif event.inline_query and event.inline_query.from_user:
            return event.inline_query.from_user.id
        elif event.chosen_inline_result and event.chosen_inline_result.from_user:
            return event.chosen_inline_result.from_user.id
        return None

    def _get_request_type(self, event: Update) -> Optional[str]:
        """Classify the request type for rate limiting"""
        if event.message:
            if event.message.text and event.message.text.startswith("/"):
                return "command"
            return "message"
        elif event.callback_query:
            return "callback"
        return None

    def _check_rate_limit(
        self, state: UserRateLimitState, request_type: str, now: float
    ) -> tuple[bool, str]:
        """Check if user has exceeded rate limit"""
        if request_type not in RATE_LIMITS:
            return False, ""

        limits = RATE_LIMITS[request_type]
        max_requests = limits["max"]
        window = limits["window"]

        history = state.request_history[request_type]

        # Add current request
        history.append(now)

        # Count requests in window
        cutoff = now - window
        recent_count = sum(1 for t in history if t > cutoff)

        if recent_count > max_requests:
            return True, f"{recent_count} requests in {window}s (limit: {max_requests})"

        return False, ""

    async def _handle_violation(
        self,
        user_id: int,
        state: UserRateLimitState,
        reason: str,
        event: Update,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        data: Dict[str, Any],
    ) -> Any:
        """Handle rate limit violation with progressive penalties"""
        now = time.time()
        state.violation_count += 1
        state.last_violation_time = now

        if state.violation_count == 1:
            # First violation: Warn only
            if not state.warned_this_session:
                await self._send_warning(event)
                state.warned_this_session = True
                state.last_warning = now
                logger.info(f"Rate limit warning for user {user_id}: {reason}")
            _save_rate_limit_data()
            return await handler(event, data)

        # Subsequent violations: Block with progressive duration
        block_duration = BLOCK_DURATIONS[
            min(state.violation_count - 2, len(BLOCK_DURATIONS) - 1)
        ]
        state.blocked_until = now + block_duration

        logger.warning(
            f"Rate limit block for user {user_id}: {reason}. "
            f"Violation #{state.violation_count}, blocked for {block_duration}s"
        )

        await self._send_block_message(event, block_duration)
        _save_rate_limit_data()
        return None

    async def _send_warning(self, event: Update):
        """Send warning message to user"""
        warning_text = (
            "⚠️ <b>Slow down!</b>\n\n"
            "You're sending requests too quickly. "
            "Please take a moment. Next time you'll be temporarily blocked."
        )
        try:
            if event.message:
                await event.message.answer(warning_text, parse_mode="HTML")
            elif event.callback_query:
                await event.callback_query.answer(
                    "⚠️ Slow down! Next time you'll be blocked briefly.", show_alert=True
                )
        except Exception as e:
            logger.debug(f"Failed to send rate limit warning: {e}")

    async def _send_block_message(self, event: Update, duration: int):
        """Send block notification to user"""
        if duration < 60:
            time_str = f"{duration} seconds"
        else:
            time_str = f"{duration // 60} minute{'s' if duration >= 120 else ''}"

        block_text = (
            f"⏸️ <b>Rate limit exceeded</b>\n\n"
            f"Please wait {time_str} before sending more requests."
        )
        try:
            if event.message:
                await event.message.answer(block_text, parse_mode="HTML")
            elif event.callback_query:
                await event.callback_query.answer(
                    f"⏸️ Rate limited. Wait {time_str}.", show_alert=True
                )
        except Exception as e:
            logger.debug(f"Failed to send block message: {e}")

    def _get_event_context(self, event: Update) -> str:
        """Get context for logging"""
        if event.message and event.message.text:
            text = event.message.text[:50]
            return f"message='{text}'"
        elif event.callback_query and event.callback_query.data:
            return f"callback='{event.callback_query.data}'"
        return "unknown"


def get_rate_limit_stats() -> Dict[str, Any]:
    """Get current rate limiting statistics"""
    _load_rate_limit_data()
    users_with_violations = sum(
        1 for s in _user_states.values() if s.violation_count > 0
    )

    total_requests = sum(
        sum(len(q) for q in state.request_history.values())
        for state in _user_states.values()
    )
    warned_users = sum(1 for s in _user_states.values() if s.warned_this_session)
    blocked_users = sum(
        1 for s in _user_states.values() if s.blocked_until > time.time()
    )

    return {
        "users_with_violations": users_with_violations,
        "total_requests_tracked": total_requests,
        "users_warned": warned_users,
        "users_currently_blocked": blocked_users,
        "limits": RATE_LIMITS,
        "block_durations": BLOCK_DURATIONS,
        "violation_reset_after": VIOLATION_RESET_AFTER,
    }


def get_user_rate_limit_info(user_id: int) -> Optional[Dict[str, Any]]:
    """Get rate limit information for a specific user"""
    _load_rate_limit_data()
    if user_id not in _user_states:
        return None

    state = _user_states[user_id]
    now = time.time()

    # Calculate total requests across all types
    total_requests = sum(len(q) for q in state.request_history.values())

    # Check if currently blocked
    is_blocked = now < state.blocked_until
    blocked_remaining = max(0, int(state.blocked_until - now)) if is_blocked else 0

    return {
        "violation_count": state.violation_count,
        "warned": state.warned_this_session,
        "is_blocked": is_blocked,
        "blocked_remaining_seconds": blocked_remaining,
        "total_requests_tracked": total_requests,
        "last_warning": state.last_warning,
    }


def get_rate_limited_users() -> Dict[int, Dict[str, Any]]:
    """Get all users who have triggered rate limiting with their current status.

    Returns a dict mapping user_id to their rate limit info for users who have
    violations or are currently blocked/warned.
    """
    _load_rate_limit_data()
    result = {}
    now = time.time()

    for user_id, state in _user_states.items():
        # Only include users who have been warned or blocked (violations > 0)
        if state.violation_count > 0 or state.warned_this_session:
            is_blocked = now < state.blocked_until
            blocked_remaining = (
                max(0, int(state.blocked_until - now)) if is_blocked else 0
            )

            result[user_id] = {
                "violation_count": state.violation_count,
                "warned": state.warned_this_session,
                "is_blocked": is_blocked,
                "blocked_remaining_seconds": blocked_remaining,
                "total_requests_tracked": sum(
                    len(q) for q in state.request_history.values()
                ),
            }

    return result


def reset_rate_limit_stats():
    """Reset all rate limiting statistics (for testing)"""
    _user_states.clear()
    if os.path.exists(RL_FILE):
        try:
            os.remove(RL_FILE)
        except Exception:
            pass


def set_admin_ids(admin_ids: set):
    """Update admin IDs for the middleware (called after initialization)"""
    global _admin_ids
    _admin_ids = admin_ids


def save_rate_limit_data():
    """Manually trigger save (for periodic backup)"""
    _save_rate_limit_data()

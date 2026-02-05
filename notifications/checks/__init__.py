"""Notification checks package

This package contains individual notification check modules,
organized by check type for better maintainability.
"""

from notifications.checks.quali import (
    check_quali_closing,
    check_quali_open,
    check_quali_results,
)
from notifications.checks.race import (
    check_race_live_notifications,
    check_last_race_results,
)
from notifications.checks.snooze import (
    check_snooze_reminders,
    check_custom_notifications,
    reset_snooze_counts_for_past_deadlines,
)
from notifications.checks.season import (
    check_season_transition,
    check_new_season_reminder,
)

__all__ = [
    # Quali checks
    "check_quali_closing",
    "check_quali_open",
    "check_quali_results",
    # Race checks
    "check_race_live_notifications",
    "check_last_race_results",
    # Snooze & custom checks
    "check_snooze_reminders",
    "check_custom_notifications",
    "reset_snooze_counts_for_past_deadlines",
    # Season checks
    "check_season_transition",
    "check_new_season_reminder",
]

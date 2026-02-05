"""Notification senders package

This package contains individual notification sender modules,
organized by notification type for better maintainability.
"""

from notifications.senders.dispatcher import send_notification_to_user
from notifications.senders.quali import send_quali_notification
from notifications.senders.race_live import send_race_live_notification
from notifications.senders.race_replay import send_race_replay_notification
from notifications.senders.race_results import send_race_results_notification
from notifications.senders.quali_results import send_quali_results_notification
from notifications.senders.new_season import send_new_season_reminder_notification

__all__ = [
    "send_notification_to_user",
    "send_quali_notification",
    "send_race_live_notification",
    "send_race_replay_notification",
    "send_race_results_notification",
    "send_quali_results_notification",
    "send_new_season_reminder_notification",
]

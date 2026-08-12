"""Tests for admin command helpers."""

from handlers.admin_commands import _last_interaction_sort_key


def test_users_sort_by_last_interaction_newest_first():
    users = {
        1: {"last_interaction": "2026-08-10T12:00:00+00:00"},
        2: {"last_interaction": None},
        3: {"last_interaction": "2026-08-12T12:00:00Z"},
        4: {"last_interaction": "invalid"},
        5: {"last_interaction": "2026-08-11T10:00:00-04:00"},
    }

    sorted_users = sorted(
        users.items(), key=_last_interaction_sort_key, reverse=True
    )

    assert [user_id for user_id, _ in sorted_users] == [3, 5, 1, 2, 4]

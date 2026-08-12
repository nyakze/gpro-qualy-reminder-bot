"""Tests for admin command helpers."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from handlers.admin_commands import _last_interaction_sort_key, format_user_link


def test_users_sort_by_last_interaction_newest_first():
    users = {
        1: {"last_interaction": "2026-08-10T12:00:00+00:00"},
        2: {"last_interaction": None},
        3: {"last_interaction": "2026-08-12T12:00:00Z"},
        4: {"last_interaction": "invalid"},
        5: {"last_interaction": "2026-08-11T10:00:00-04:00"},
    }

    sorted_users = sorted(users.items(), key=_last_interaction_sort_key, reverse=True)

    assert [user_id for user_id, _ in sorted_users] == [3, 5, 1, 2, 4]


def test_format_user_link_escapes_telegram_name():
    link = format_user_link(123, None, "<b>Alice & Bob</b>")

    assert link == (
        '<a href="tg://user?id=123">' "&lt;b&gt;Alice &amp; Bob&lt;/b&gt;</a>"
    )


@pytest.mark.asyncio
async def test_failed_calendar_update_does_not_reset_users():
    from handlers.admin_commands import cmd_update

    message = MagicMock()
    message.from_user.id = 123
    message.text = "/update"
    message.answer = AsyncMock()

    i18n = MagicMock()
    i18n.get.side_effect = lambda key, *args, **kwargs: key

    with (
        patch("handlers.admin_commands.is_admin", return_value=True),
        patch(
            "handlers.admin_commands.update_calendar",
            new=AsyncMock(return_value=False),
        ),
        patch("handlers.admin_commands.reset_user_status") as reset_user_status,
    ):
        await cmd_update(message, i18n)

    reset_user_status.assert_not_called()
    message.answer.assert_awaited_once_with(
        "admin-calendar-update-failed", parse_mode="HTML"
    )

"""FSM state handlers and state group definitions"""

import logging
import re
from aiogram import F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext

from notifications import set_user_group, parse_time_input, set_custom_notification
from utils import format_group_display
from . import router

logger = logging.getLogger(__name__)


class SetGroupStates(StatesGroup):
    waiting_for_group = State()


class CustomNotificationStates(StatesGroup):
    waiting_for_time = State()
    slot_index = State()


class OnboardingStates(StatesGroup):
    waiting_for_group = State()


class TimezoneStates(StatesGroup):
    waiting_for_timezone_input = State()


@router.message(SetGroupStates.waiting_for_group, F.text & ~F.text.startswith("/"))
async def process_group_input(message: Message, state: FSMContext, i18n: I18nContext):
    """Process user's group input from settings"""
    group_input = message.text.strip().upper()

    # Validate format: E or M/P/A/R followed by 1-3 digits
    if group_input == "E":
        pass
    elif re.match(r"^[MPAR]\d{1,3}$", group_input):
        pass
    else:
        await message.answer(i18n.get("error-invalid-format"), parse_mode="HTML")
        return

    # Save the group
    set_user_group(message.from_user.id, group_input)
    group_display = format_group_display(group_input)
    await state.clear()

    # Show success with back to settings button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("button-back-to-settings"),
                    callback_data="settings_main",
                )
            ]
        ]
    )

    await message.answer(
        i18n.get("settings-group-set", group=group_display),
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.message(
    CustomNotificationStates.waiting_for_time, F.text & ~F.text.startswith("/")
)
async def process_custom_notification_time_input(
    message: Message, state: FSMContext, i18n: I18nContext
):
    """Process user's custom time input"""
    user_id = message.from_user.id
    time_input = message.text.strip()

    # Get slot index from state
    state_data = await state.get_data()
    slot_idx = state_data.get("slot_index", 0)

    # Parse time input
    hours, error_msg = parse_time_input(time_input, i18n)

    if error_msg:
        await message.answer(
            i18n.get("custom-notif-error-parsing", error=error_msg),
            parse_mode="HTML",
        )
        return

    # Set custom notification
    success, result_msg = set_custom_notification(user_id, slot_idx, hours, i18n)

    # Clear state
    await state.clear()

    if success:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-back-custom-notif"),
                        callback_data="custom_notif_menu",
                    )
                ]
            ]
        )

        await message.answer(
            i18n.get("custom-notif-success", message=result_msg),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-try-again"),
                        callback_data=f"custom_notif_input_{slot_idx}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text=i18n.get("button-back"), callback_data="custom_notif_menu"
                    )
                ],
            ]
        )

        await message.answer(
            i18n.get("custom-notif-error-setting", error=result_msg),
            reply_markup=keyboard,
            parse_mode="HTML",
        )


@router.message(OnboardingStates.waiting_for_group, F.text & ~F.text.startswith("/"))
async def process_onboarding_group_input(
    message: Message, state: FSMContext, i18n: I18nContext
):
    """Process custom group input during onboarding"""
    user_id = message.from_user.id
    group_input = message.text.strip().upper()

    # Validate format
    if group_input == "E":
        pass
    elif re.match(r"^[MPAR]\d{1,3}$", group_input):
        pass
    else:
        await message.answer(
            i18n.get("error-invalid-format-onboarding"), parse_mode="HTML"
        )
        return

    # Save the group
    set_user_group(user_id, group_input)
    group_display = format_group_display(group_input)
    await state.clear()

    # Show welcome complete message with main menu buttons
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("button-main-menu-status"),
                    callback_data="main_menu_status",
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("button-main-menu-calendar"),
                    callback_data="main_menu_calendar",
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("button-main-menu-next"),
                    callback_data="main_menu_next",
                )
            ],
            [
                InlineKeyboardButton(
                    text=i18n.get("button-main-menu-settings"),
                    callback_data="main_menu_settings",
                )
            ],
        ]
    )

    await message.answer(
        i18n.get("onboard-complete-with-group", group=group_display),
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.message(
    TimezoneStates.waiting_for_timezone_input, F.text & ~F.text.startswith("/")
)
async def process_timezone_input(
    message: Message, state: FSMContext, i18n: I18nContext
):
    """Process user's timezone search input and show fuzzy-matched options"""
    from timezone_utils import fuzzy_search_timezones

    query = message.text.strip()

    # Fuzzy search timezones (increased limit to 30)
    matches = fuzzy_search_timezones(query, limit=30)

    if not matches:
        # No matches found
        await message.answer(
            i18n.get("error-timezone-not-found", query=query), parse_mode="HTML"
        )
        return

    # Store matches in state for pagination
    await state.update_data(tz_matches=matches, tz_query=query)

    # Show first page
    await show_timezone_page(message, state, i18n, page=0)


async def build_timezone_page_keyboard(
    matches: list, query: str, page: int, i18n: I18nContext
) -> tuple[InlineKeyboardMarkup, str]:
    """Build keyboard and message text for a timezone search results page"""
    from timezone_utils import get_timezone_display_name
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone as tz

    RESULTS_PER_PAGE = 10
    total_pages = (len(matches) + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    page = max(0, min(page, total_pages - 1))  # Clamp page number

    start_idx = page * RESULTS_PER_PAGE
    end_idx = min(start_idx + RESULTS_PER_PAGE, len(matches))
    page_matches = matches[start_idx:end_idx]

    # Build inline keyboard with matches for this page
    keyboard_buttons = []
    now = datetime.now(tz.utc)

    for tz_name, score in page_matches:
        try:
            timezone_obj = ZoneInfo(tz_name)
            display_name = get_timezone_display_name(timezone_obj, now)
            keyboard_buttons.append(
                [
                    InlineKeyboardButton(
                        text=display_name, callback_data=f"tz_select_{tz_name}"
                    )
                ]
            )
        except Exception as e:
            logger.warning(f"Failed to create button for {tz_name}: {e}")

    # Add pagination buttons if needed
    if total_pages > 1:
        nav_buttons = []
        if page > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    text=i18n.get("button-previous"), callback_data=f"tz_page_{page-1}"
                )
            )
        if page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    text=i18n.get("button-next"), callback_data=f"tz_page_{page+1}"
                )
            )
        if nav_buttons:
            keyboard_buttons.append(nav_buttons)

    # Add cancel button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-cancel"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    # Format message with page indicator if multiple pages
    if total_pages > 1:
        message_text = i18n.get(
            "timezone-select-matches-paginated",
            query=query,
            page=page + 1,
            total=total_pages,
        )
    else:
        message_text = i18n.get("timezone-select-matches", query=query)

    return keyboard, message_text


async def show_timezone_page(
    message: Message, state: FSMContext, i18n: I18nContext, page: int = 0
):
    """Display a page of timezone search results with pagination (send new message)"""
    data = await state.get_data()
    matches = data.get("tz_matches", [])
    query = data.get("tz_query", "")

    keyboard, message_text = await build_timezone_page_keyboard(
        matches, query, page, i18n
    )

    await message.answer(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def show_timezone_page_edit(
    message: Message, state: FSMContext, i18n: I18nContext, page: int = 0
):
    """Display a page of timezone search results with pagination (edit existing message)"""
    data = await state.get_data()
    matches = data.get("tz_matches", [])
    query = data.get("tz_query", "")

    keyboard, message_text = await build_timezone_page_keyboard(
        matches, query, page, i18n
    )

    await message.edit_text(
        message_text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )

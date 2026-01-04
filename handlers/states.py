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


@router.message(SetGroupStates.waiting_for_group, F.text & ~F.text.startswith('/'))
async def process_group_input(message: Message, state: FSMContext, i18n: I18nContext):
    """Process user's group input from settings"""
    group_input = message.text.strip().upper()

    # Validate format: E or M/P/A/R followed by 1-3 digits
    if group_input == 'E':
        valid = True
    elif re.match(r'^[MPAR]\d{1,3}$', group_input):
        valid = True
    else:
        await message.answer(
            i18n.get("error-invalid-format"),
            parse_mode='Markdown'
        )
        return

    # Save the group
    set_user_group(message.from_user.id, group_input)
    group_display = format_group_display(group_input)
    await state.clear()

    # Show success with back to settings button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i18n.get("button-back-to-settings"), callback_data="settings_main")]
    ])

    await message.answer(
        i18n.get("settings-group-set", group=group_display),
        reply_markup=keyboard,
        parse_mode='Markdown'
    )


@router.message(CustomNotificationStates.waiting_for_time, F.text & ~F.text.startswith('/'))
async def process_custom_notification_time_input(message: Message, state: FSMContext, i18n: I18nContext):
    """Process user's custom time input"""
    user_id = message.from_user.id
    time_input = message.text.strip()

    # Get slot index from state
    state_data = await state.get_data()
    slot_idx = state_data.get('slot_index', 0)

    # Parse time input
    hours, error_msg = parse_time_input(time_input, i18n)

    if error_msg:
        await message.answer(
            i18n.get("custom-notif-error-parsing", error=error_msg),
            parse_mode='Markdown'
        )
        return

    # Set custom notification
    success, result_msg = set_custom_notification(user_id, slot_idx, hours, i18n)

    # Clear state
    await state.clear()

    if success:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=i18n.get("button-back-custom-notif"), callback_data="custom_notif_menu")]
        ])

        await message.answer(
            i18n.get("custom-notif-success", message=result_msg),
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=i18n.get("button-try-again"), callback_data=f"custom_notif_input_{slot_idx}")],
            [InlineKeyboardButton(text=i18n.get("button-back"), callback_data="custom_notif_menu")]
        ])

        await message.answer(
            i18n.get("custom-notif-error-setting", error=result_msg),
            reply_markup=keyboard,
            parse_mode='Markdown'
        )


@router.message(OnboardingStates.waiting_for_group, F.text & ~F.text.startswith('/'))
async def process_onboarding_group_input(message: Message, state: FSMContext, i18n: I18nContext):
    """Process custom group input during onboarding"""
    user_id = message.from_user.id
    group_input = message.text.strip().upper()

    # Validate format
    if group_input == 'E':
        valid = True
    elif re.match(r'^[MPAR]\d{1,3}$', group_input):
        valid = True
    else:
        await message.answer(
            i18n.get("error-invalid-format-onboarding"),
            parse_mode='Markdown'
        )
        return

    # Save the group
    set_user_group(user_id, group_input)
    group_display = format_group_display(group_input)
    await state.clear()

    # Show welcome complete message with main menu buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=i18n.get("button-main-menu-status"), callback_data="main_menu_status")],
        [InlineKeyboardButton(text=i18n.get("button-main-menu-calendar"), callback_data="main_menu_calendar")],
        [InlineKeyboardButton(text=i18n.get("button-main-menu-next"), callback_data="main_menu_next")],
        [InlineKeyboardButton(text=i18n.get("button-main-menu-settings"), callback_data="main_menu_settings")]
    ])

    await message.answer(
        i18n.get("onboard-complete-with-group", group=group_display),
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

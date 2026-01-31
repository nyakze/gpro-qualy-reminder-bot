"""Onboarding flow for new users"""

import logging
from aiogram import F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from notifications import (
    set_user_language,
    set_user_ui_language,
    get_user_status,
    get_user_ui_language,
)
from .states import OnboardingStates
from . import router

logger = logging.getLogger(__name__)


@router.callback_query(F.data.startswith("onboard_ui_lang_page_"))
async def handle_onboarding_ui_language_page(
    callback: CallbackQuery, i18n: I18nContext
):
    """Handle UI language pagination during onboarding"""
    user_id = callback.from_user.id

    try:
        page = int(callback.data.split("_")[4])
    except (ValueError, IndexError):
        await callback.answer("Invalid page", show_alert=True)
        return

    from .callbacks import build_ui_language_keyboard

    # Get current UI language or default to 'gb'
    current_ui_lang = get_user_ui_language(user_id) or "gb"
    keyboard = build_ui_language_keyboard(
        page=page, current_ui_lang=current_ui_lang, i18n=i18n, onboarding=True
    )

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "onboard_skip_ui_lang")
async def handle_onboarding_skip_ui_lang(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Skip UI language selection during onboarding"""
    user_id = callback.from_user.id

    # Set default UI language to English (gb)
    set_user_ui_language(user_id, "gb")
    set_user_language(user_id, "gb")
    logger.debug(f"User {user_id} skipped UI language selection, defaults set to 'gb'")

    # Show group selection menu
    await show_onboarding_group_menu(callback.message, user_id, i18n, state)
    await callback.answer()


@router.callback_query(
    F.data.startswith("onboard_ui_lang_") & ~F.data.startswith("onboard_ui_lang_page_")
)
async def handle_onboarding_ui_language_select(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle bot UI language selection at start of onboarding"""
    user_id = callback.from_user.id

    # Extract language code (gb, ru, br, it, es, fr, etc.)
    ui_lang = callback.data.replace("onboard_ui_lang_", "")

    # Set UI language
    if set_user_ui_language(user_id, ui_lang):
        logger.debug(f"User {user_id} selected UI language: {ui_lang}")

        # Map UI language to GPRO language
        # ua -> gb (Ukrainian not in GPRO), all others use same code
        if ui_lang == "ua":
            # Ukrainian not available in GPRO, use English (gb)
            gpro_lang = "gb"
        else:
            # All other UI languages match their GPRO language code
            gpro_lang = ui_lang

        set_user_language(user_id, gpro_lang)
        logger.debug(f"User {user_id} GPRO language auto-set to: {gpro_lang}")

        # Show group selection menu in the newly selected language
        with i18n.use_locale(ui_lang):
            await show_onboarding_group_menu(callback.message, user_id, i18n, state)
        await callback.answer()
    else:
        await callback.answer("Error setting language", show_alert=True)


async def show_onboarding_group_menu(
    message: Message, user_id: int, i18n: I18nContext, state: FSMContext = None
):
    """Show group selection menu during onboarding - text input only"""
    # Set state to wait for group input
    if state:
        await state.set_state(OnboardingStates.waiting_for_group)

    # Only show skip button
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("button-skip"), callback_data="onboard_skip_group"
                )
            ]
        ]
    )

    await message.edit_text(
        i18n.get("onboard-group-custom"), reply_markup=keyboard, parse_mode="HTML"
    )


@router.callback_query(F.data == "onboard_skip_group")
async def handle_onboarding_skip_group(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Skip group selection during onboarding"""
    user_id = callback.from_user.id
    await state.clear()

    # Get user's selected language and show completion message in that language
    user_status = get_user_status(user_id)[0]
    ui_lang = user_status.get("ui_lang", "gb")

    with i18n.use_locale(ui_lang):
        await callback.answer(i18n.get("feedback-skip-group"))
        # Show welcome complete message
        await show_onboarding_complete(callback.message, i18n)


async def show_onboarding_complete(message: Message, i18n: I18nContext):
    """Show onboarding complete message with main menu buttons"""
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

    await message.edit_text(
        i18n.get("onboard-complete"), reply_markup=keyboard, parse_mode="HTML"
    )


@router.callback_query(F.data == "onboard_complete")
async def handle_onboarding_complete(callback: CallbackQuery, i18n: I18nContext):
    """Acknowledge onboarding complete"""
    await callback.answer(i18n.get("feedback-welcome"))

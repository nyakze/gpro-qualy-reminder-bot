"""Settings callback handlers"""

import logging
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from notifications import (
    get_user_status,
    get_user_language,
    set_user_language,
    LANGUAGE_OPTIONS,
    get_user_ui_language,
    set_user_ui_language,
)
from utils import (
    format_group_display,
    get_ui_language_display,
    UI_LANGUAGE_DISPLAY,
)
from . import router

logger = logging.getLogger(__name__)


def build_settings_keyboard(user_id: int, i18n: I18nContext) -> InlineKeyboardMarkup:
    """Build settings menu keyboard with all options"""
    from notifications import get_user_timezone
    from timezone_utils import get_timezone_display_name
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone

    user_status = get_user_status(user_id)
    current_ui_lang = user_status.get("ui_lang", "gb")
    current_lang = user_status.get("gpro_lang", "gb")
    current_group = user_status.get("group")
    website_mode = user_status.get("website_mode", "classic")

    keyboard_buttons = []

    ui_lang_display = get_ui_language_display(current_ui_lang)
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-ui-language", language=ui_lang_display),
                callback_data="ui_lang_menu",
            )
        ]
    )

    mode_display = "APP" if website_mode == "app" else i18n.get("website-mode-classic")
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-website-mode", mode=mode_display),
                callback_data="toggle_website_mode",
            )
        ]
    )

    if website_mode == "classic":
        lang_display = LANGUAGE_OPTIONS.get(current_lang, current_lang)
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-gpro-language", language=lang_display),
                    callback_data="lang_menu",
                )
            ]
        )

    group_display = format_group_display(current_group)
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-group", group=group_display),
                callback_data="group_menu",
            )
        ]
    )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-notifications"), callback_data="notif_menu"
            )
        ]
    )

    current_tz = get_user_timezone(user_id)
    tz = ZoneInfo(current_tz)
    tz_display = get_timezone_display_name(tz, datetime.now(timezone.utc))
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-timezone", timezone=tz_display),
                callback_data="timezone_menu",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def build_language_keyboard(
    page: int = 1, current_lang: str = "gb", onboarding: bool = False, i18n=None
) -> InlineKeyboardMarkup:
    """Build paginated GPRO language selection keyboard with 2-column layout"""
    all_gpro_langs = [
        "gb",
        "ru",
        "br",
        "it",
        "es",
        "fr",
        "de",
        "pt",
        "ro",
        "pl",
        "bg",
        "mk",
        "nl",
        "fi",
        "hu",
        "tr",
        "gr",
        "dk",
        "rs",
        "se",
        "lt",
        "ee",
        "al",
        "hr",
        "cn",
        "my",
        "in",
        "pi",
        "be",
        "cz",
        "sk",
    ]

    items_per_page = 12
    pages = [
        all_gpro_langs[i : i + items_per_page]
        for i in range(0, len(all_gpro_langs), items_per_page)
    ]

    if page < 1 or page > len(pages):
        page = 1

    buttons = []
    callback_prefix = "onboard_lang_" if onboarding else "lang_"

    current_page_langs = pages[page - 1]
    for i in range(0, len(current_page_langs), 2):
        row = []
        lang_code_left = current_page_langs[i]
        is_current_left = lang_code_left == current_lang
        prefix_left = "✅ " if is_current_left else ""
        button_text_left = f"{prefix_left}{LANGUAGE_OPTIONS[lang_code_left]}"
        row.append(
            InlineKeyboardButton(
                text=button_text_left,
                callback_data=f"{callback_prefix}{lang_code_left}",
            )
        )

        if i + 1 < len(current_page_langs):
            lang_code_right = current_page_langs[i + 1]
            is_current_right = lang_code_right == current_lang
            prefix_right = "✅ " if is_current_right else ""
            button_text_right = f"{prefix_right}{LANGUAGE_OPTIONS[lang_code_right]}"
            row.append(
                InlineKeyboardButton(
                    text=button_text_right,
                    callback_data=f"{callback_prefix}{lang_code_right}",
                )
            )

        buttons.append(row)

    if page == len(pages) and not onboarding:
        reset_text = (
            i18n.get("button-reset-language")
            if i18n
            else "🔄 Reset to Default (English)"
        )
        buttons.append(
            [InlineKeyboardButton(text=reset_text, callback_data="lang_reset_default")]
        )

    footer = []
    if page > 1:
        prev_text = i18n.get("button-previous") if i18n else "◀ Previous"
        callback_data = (
            f"onboard_lang_page_{page-1}" if onboarding else f"lang_page_{page-1}"
        )
        footer.append(InlineKeyboardButton(text=prev_text, callback_data=callback_data))

    if onboarding:
        skip_text = i18n.get("button-skip") if i18n else "⏭️ Skip"
        footer.append(
            InlineKeyboardButton(text=skip_text, callback_data="onboard_skip_lang")
        )
    else:
        menu_text = i18n.get("button-main-menu") if i18n else "🏠 Main Menu"
        footer.append(
            InlineKeyboardButton(text=menu_text, callback_data="lang_back_main")
        )

    if page < len(pages):
        next_text = i18n.get("button-next") if i18n else "Next ▶"
        callback_data = (
            f"onboard_lang_page_{page+1}" if onboarding else f"lang_page_{page+1}"
        )
        footer.append(InlineKeyboardButton(text=next_text, callback_data=callback_data))

    buttons.append(footer)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_ui_language_keyboard(
    page: int = 1, current_ui_lang: str = "gb", i18n=None, onboarding: bool = False
) -> InlineKeyboardMarkup:
    """Build paginated UI language selection keyboard with 2-column layout"""
    all_ui_langs = [
        "gb",
        "ru",
        "br",
        "it",
        "es",
        "fr",
        "nl",
        "bg",
        "cz",
        "in",
        "ua",
        "pt",
    ]

    items_per_page = 12
    ui_lang_pages = [
        all_ui_langs[i : i + items_per_page]
        for i in range(0, len(all_ui_langs), items_per_page)
    ]

    if page < 1 or page > len(ui_lang_pages):
        page = 1

    keyboard_buttons = []
    callback_prefix = "onboard_ui_lang_" if onboarding else "set_ui_lang_"

    current_page_langs = ui_lang_pages[page - 1]
    for i in range(0, len(current_page_langs), 2):
        row = []
        lang_code_left = current_page_langs[i]
        lang_display_left = UI_LANGUAGE_DISPLAY.get(lang_code_left, lang_code_left)
        prefix_left = "✅ " if current_ui_lang == lang_code_left else ""
        row.append(
            InlineKeyboardButton(
                text=f"{prefix_left}{lang_display_left}",
                callback_data=f"{callback_prefix}{lang_code_left}",
            )
        )

        if i + 1 < len(current_page_langs):
            lang_code_right = current_page_langs[i + 1]
            lang_display_right = UI_LANGUAGE_DISPLAY.get(
                lang_code_right, lang_code_right
            )
            prefix_right = "✅ " if current_ui_lang == lang_code_right else ""
            row.append(
                InlineKeyboardButton(
                    text=f"{prefix_right}{lang_display_right}",
                    callback_data=f"{callback_prefix}{lang_code_right}",
                )
            )

        keyboard_buttons.append(row)

    footer = []
    if page > 1:
        prev_text = i18n.get("button-previous") if i18n else "◀ Previous"
        callback_data = (
            f"onboard_ui_lang_page_{page-1}" if onboarding else f"ui_lang_page_{page-1}"
        )
        footer.append(InlineKeyboardButton(text=prev_text, callback_data=callback_data))

    if page < len(ui_lang_pages):
        next_text = i18n.get("button-next") if i18n else "Next ▶"
        callback_data = (
            f"onboard_ui_lang_page_{page+1}" if onboarding else f"ui_lang_page_{page+1}"
        )
        footer.append(InlineKeyboardButton(text=next_text, callback_data=callback_data))

    if footer:
        keyboard_buttons.append(footer)

    if onboarding:
        skip_text = i18n.get("button-skip") if i18n else "⏭️ Skip"
        keyboard_buttons.append(
            [InlineKeyboardButton(text=skip_text, callback_data="onboard_skip_ui_lang")]
        )
    else:
        back_text = i18n.get("button-back") if i18n else "◀ Back"
        keyboard_buttons.append(
            [InlineKeyboardButton(text=back_text, callback_data="settings_main")]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


@router.callback_query(F.data == "lang_menu")
async def handle_language_menu(callback: CallbackQuery, i18n: I18nContext):
    """Open language selection menu (page 1)"""
    user_id = callback.from_user.id
    current_lang = get_user_language(user_id)

    keyboard = build_language_keyboard(page=1, current_lang=current_lang, i18n=i18n)

    await callback.message.edit_text(
        i18n.get(
            "lang-menu-title",
            currentLang=LANGUAGE_OPTIONS.get(current_lang, current_lang),
        ),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang_page_"))
async def handle_language_page(callback: CallbackQuery, i18n: I18nContext):
    """Handle language pagination"""
    user_id = callback.from_user.id
    current_lang = get_user_language(user_id)

    try:
        page = int(callback.data.split("_")[2])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-page"), show_alert=True)
        return

    keyboard = build_language_keyboard(page=page, current_lang=current_lang, i18n=i18n)

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(
    F.data.startswith("lang_")
    & ~F.data.in_(["lang_menu", "lang_back_main", "lang_reset_default"])
)
async def handle_language_select(callback: CallbackQuery, i18n: I18nContext):
    """Handle language selection"""
    user_id = callback.from_user.id

    lang_code = callback.data.replace("lang_", "")

    if lang_code.startswith("page_"):
        return

    if set_user_language(user_id, lang_code):
        lang_display = LANGUAGE_OPTIONS.get(lang_code, lang_code)
        await callback.answer(i18n.get("feedback-language-set", language=lang_display))

        await handle_settings_main(callback, i18n)
    else:
        await callback.answer(i18n.get("error-invalid-language"), show_alert=True)


@router.callback_query(F.data == "lang_reset_default")
async def handle_language_reset(callback: CallbackQuery, i18n: I18nContext):
    """Reset language to default (English GB)"""
    user_id = callback.from_user.id

    if set_user_language(user_id, "gb"):
        keyboard = build_language_keyboard(page=1, current_lang="gb", i18n=i18n)

        await callback.message.edit_text(
            i18n.get("lang-menu-title", currentLang=LANGUAGE_OPTIONS["gb"]),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        await callback.answer(i18n.get("feedback-language-reset"))
    else:
        await callback.answer(i18n.get("error-reset-failed"), show_alert=True)


@router.callback_query(F.data == "ui_lang_menu")
async def handle_ui_language_menu(callback: CallbackQuery, i18n: I18nContext):
    """Show bot UI language selection menu (paginated)"""
    user_id = callback.from_user.id
    current_ui_lang = get_user_ui_language(user_id)

    keyboard = build_ui_language_keyboard(
        page=1, current_ui_lang=current_ui_lang, i18n=i18n
    )

    await callback.message.edit_text(
        i18n.get("ui-lang-menu-title"), reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ui_lang_page_"))
async def handle_ui_language_page(callback: CallbackQuery, i18n: I18nContext):
    """Handle UI language pagination"""
    user_id = callback.from_user.id
    current_ui_lang = get_user_ui_language(user_id)

    try:
        page = int(callback.data.split("_")[3])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-page"), show_alert=True)
        return

    keyboard = build_ui_language_keyboard(
        page=page, current_ui_lang=current_ui_lang, i18n=i18n
    )

    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("set_ui_lang_"))
async def handle_set_ui_language(callback: CallbackQuery, i18n: I18nContext):
    """Handle bot UI language selection in settings"""
    user_id = callback.from_user.id

    ui_lang = callback.data.replace("set_ui_lang_", "")

    if set_user_ui_language(user_id, ui_lang):
        lang_display = get_ui_language_display(ui_lang)
        await callback.answer(f"✅ {lang_display}")

        with i18n.use_locale(ui_lang):
            await handle_settings_main(callback, i18n)
    else:
        await callback.answer(i18n.get("error-invalid-language"), show_alert=True)


@router.callback_query(F.data == "settings_main")
async def handle_settings_main(callback: CallbackQuery, i18n: I18nContext):
    """Return to main settings menu"""
    user_id = callback.from_user.id
    keyboard = build_settings_keyboard(user_id, i18n)

    await callback.message.edit_text(
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data == "lang_back_main")
async def handle_language_back(callback: CallbackQuery, i18n: I18nContext):
    """Alias for returning to main settings"""
    await handle_settings_main(callback, i18n)


@router.callback_query(F.data == "group_menu")
async def handle_group_menu(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Show group settings menu"""
    from notifications import get_user_status

    user_id = callback.from_user.id
    user_status = get_user_status(user_id)
    current_group = user_status.get("group")
    group_display = format_group_display(current_group)

    from handlers.states import SetGroupStates

    keyboard_buttons = []

    if current_group:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-reset-group"), callback_data="group_reset"
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-settings"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await state.set_state(SetGroupStates.waiting_for_group)
    await callback.message.edit_text(
        i18n.get("group-menu-title", groupDisplay=group_display),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "group_reset")
async def handle_group_reset(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Reset group to default (remove data)"""
    from notifications import set_user_group

    user_id = callback.from_user.id
    set_user_group(user_id, None)
    await state.clear()
    await callback.answer(i18n.get("group-reset-success"), show_alert=True)
    await handle_settings_main(callback, i18n)


@router.callback_query(F.data == "timezone_menu")
async def handle_timezone_menu(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Show timezone settings menu"""
    from notifications import get_user_timezone
    from timezone_utils import get_timezone_display_name
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone
    from handlers.states import TimezoneStates

    user_id = callback.from_user.id
    current_tz = get_user_timezone(user_id)
    tz = ZoneInfo(current_tz)
    tz_display = get_timezone_display_name(tz, datetime.now(timezone.utc))

    keyboard_buttons = []

    if current_tz != "UTC":
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-reset-timezone"), callback_data="tz_reset_utc"
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-settings"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await state.set_state(TimezoneStates.waiting_for_timezone_input)

    await callback.message.edit_text(
        i18n.get("timezone-menu-title", timezone=tz_display),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tz_page_"))
async def handle_timezone_page(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle timezone search results pagination"""
    from handlers.states import show_timezone_page_edit

    page = int(callback.data.replace("tz_page_", ""))

    await show_timezone_page_edit(callback.message, state, i18n, page)
    await callback.answer()


@router.callback_query(F.data.startswith("tz_select_"))
async def handle_timezone_select(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle timezone selection from fuzzy search results"""
    from notifications import set_user_timezone
    from timezone_utils import get_timezone_display_name
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone

    user_id = callback.from_user.id

    tz_name = callback.data.replace("tz_select_", "")

    if set_user_timezone(user_id, tz_name):
        await state.clear()

        tz = ZoneInfo(tz_name)
        tz_display = get_timezone_display_name(tz, datetime.now(timezone.utc))

        utc_now = datetime.now(timezone.utc)
        local_now = utc_now.astimezone(tz)
        local_time_str = local_now.strftime("%H:%M")

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

        await callback.message.edit_text(
            i18n.get(
                "timezone-set-success", timezone=tz_display, localTime=local_time_str
            ),
            reply_markup=keyboard,
            parse_mode="HTML",
        )
        await callback.answer(i18n.get("feedback-timezone-set"))
    else:
        await callback.answer(i18n.get("error-invalid-timezone"), show_alert=True)


@router.callback_query(F.data == "tz_reset_utc")
async def handle_timezone_reset(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Reset timezone to UTC"""
    from notifications import set_user_timezone

    user_id = callback.from_user.id

    if set_user_timezone(user_id, "UTC"):
        await state.clear()
        await callback.answer(i18n.get("feedback-timezone-reset"))
        await handle_settings_main(callback, i18n)
    else:
        await callback.answer(i18n.get("error-reset-failed"), show_alert=True)

"""Callback handlers for button interactions"""

import logging
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from gpro_calendar import race_calendar
from notifications import (
    get_user_status,
    toggle_notification,
    mark_quali_done,
    reset_user_status,
    save_users_data,
    get_user_language,
    set_user_language,
    LANGUAGE_OPTIONS,
    get_custom_notifications,
    set_custom_notification,
    format_custom_notification_time,
    CUSTOM_NOTIF_MIN_HOURS,
    CUSTOM_NOTIF_MAX_HOURS,
    format_weather_data,
    set_user_ui_language,
    get_user_ui_language,
)
from utils import (
    add_flag_to_track,
    format_group_display,
    get_ui_language_display,
    UI_LANGUAGE_DISPLAY,
)
from .states import CustomNotificationStates, SetGroupStates
from . import router

logger = logging.getLogger(__name__)


def build_settings_keyboard(user_id: int, i18n: I18nContext) -> InlineKeyboardMarkup:
    """Build settings menu keyboard with all options

    Args:
        user_id: Telegram user ID
        i18n: I18n context for translations

    Returns:
        InlineKeyboardMarkup with all settings buttons
    """
    from notifications import get_user_timezone
    from timezone_utils import get_timezone_display_name
    from zoneinfo import ZoneInfo
    from datetime import datetime, timezone

    user_status = get_user_status(user_id)
    current_ui_lang = user_status.get("ui_lang", "en")
    current_lang = user_status.get("gpro_lang", "gb")
    current_group = user_status.get("group")

    keyboard_buttons = []

    # Bot UI Language button
    ui_lang_display = get_ui_language_display(current_ui_lang)
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-ui-language", language=ui_lang_display),
                callback_data="ui_lang_menu",
            )
        ]
    )

    # GPRO Website Language button
    lang_display = LANGUAGE_OPTIONS.get(current_lang, current_lang)
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-gpro-language", language=lang_display),
                callback_data="lang_menu",
            )
        ]
    )

    # Group button
    group_display = format_group_display(current_group)
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-group", group=group_display),
                callback_data="group_menu",
            )
        ]
    )

    # Notifications button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-notifications"), callback_data="notif_menu"
            )
        ]
    )

    # Timezone button
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


# Notification types - labels are fetched from i18n
NOTIFICATION_TYPES = (
    "72h",
    "48h",
    "24h",
    "2h",
    "10min",
    "opens_soon",
    "race_replay",
    "race_live",
    "race_results",
)


def build_language_keyboard(
    page: int = 1, current_lang: str = "gb", onboarding: bool = False, i18n=None
) -> InlineKeyboardMarkup:
    """Build paginated language selection keyboard

    Args:
        page: Page number (1-4)
        current_lang: User's current language code
        onboarding: If True, use onboarding callbacks and add Skip button
        i18n: I18n context for translations (optional)

    Returns:
        InlineKeyboardMarkup with language options and navigation
    """
    # Language codes distributed across 4 pages (31 total)
    # All bot UI languages (gb, ru, br, it, es, fr) appear first on page 1
    pages = [
        ["gb", "ru", "br", "it", "es", "fr", "de", "pt"],
        ["ro", "pl", "bg", "mk", "nl", "fi", "hu", "tr"],
        ["gr", "dk", "rs", "se", "lt", "ee", "al", "hr"],
        ["ch", "my", "in", "pi", "be", "cz", "sk"],
    ]

    buttons = []
    callback_prefix = "onboard_lang_" if onboarding else "lang_"

    # Language selection buttons
    for lang_code in pages[page - 1]:
        is_current = lang_code == current_lang
        prefix = "✅ " if is_current else ""
        button_text = f"{prefix}{LANGUAGE_OPTIONS[lang_code]}"
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"{callback_prefix}{lang_code}"
                )
            ]
        )

    # Add reset button on last page (only in settings, not onboarding)
    if page == len(pages) and not onboarding:
        reset_text = (
            i18n.get("button-reset-language")
            if i18n
            else "🔄 Reset to Default (English)"
        )
        buttons.append(
            [InlineKeyboardButton(text=reset_text, callback_data="lang_reset_default")]
        )

    # Navigation footer
    footer = []
    if page > 1:
        prev_text = i18n.get("button-previous") if i18n else "◀ Previous"
        if onboarding:
            footer.append(
                InlineKeyboardButton(
                    text=prev_text, callback_data=f"onboard_lang_page_{page-1}"
                )
            )
        else:
            footer.append(
                InlineKeyboardButton(
                    text=prev_text, callback_data=f"lang_page_{page-1}"
                )
            )

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
        if onboarding:
            footer.append(
                InlineKeyboardButton(
                    text=next_text, callback_data=f"onboard_lang_page_{page+1}"
                )
            )
        else:
            footer.append(
                InlineKeyboardButton(
                    text=next_text, callback_data=f"lang_page_{page+1}"
                )
            )

    buttons.append(footer)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ====================
# Main Menu Handlers
# ====================


@router.callback_query(F.data == "main_menu_status")
async def handle_main_menu_status(callback: CallbackQuery, i18n: I18nContext):
    """Handle Status button from main menu"""
    from datetime import datetime

    await callback.answer()

    if not race_calendar:
        await callback.message.answer(i18n.get("no-races-scheduled"))
        return

    # Find next upcoming race
    now = datetime.utcnow()
    future_races = []

    if isinstance(race_calendar, dict):
        for race_id, race_data in race_calendar.items():
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                future_races.append((race_id, race_data))
    else:
        for i, race_data in enumerate(race_calendar):
            if isinstance(race_data, dict) and race_data.get("quali_close", now) > now:
                race_id = race_data.get("race_id", i + 1)
                future_races.append((race_id, race_data))

    future_races.sort(key=lambda x: x[1].get("quali_close", now))

    if future_races:
        from notifications import send_quali_notification

        next_race_id, next_race_data = future_races[0]
        await send_quali_notification(
            callback.bot,
            callback.from_user.id,
            next_race_id,
            next_race_data,
            "manual",
            i18n,
        )
        logger.info(
            f"📊 Main menu status sent for race {next_race_id} to {callback.from_user.id}"
        )
    else:
        await callback.message.answer(i18n.get("no-upcoming-qualifications"))


@router.callback_query(F.data == "main_menu_calendar")
async def handle_main_menu_calendar(callback: CallbackQuery, i18n: I18nContext):
    """Handle Calendar button from main menu"""
    from utils import format_full_calendar

    user_id = callback.from_user.id
    await callback.answer()
    calendar_text = format_full_calendar(
        race_calendar, "Full Season", is_current_season=True, user_id=user_id, i18n=i18n
    )
    title = i18n.get("calendar-title-full")
    text = f"{title}\n\n{calendar_text}"
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "main_menu_next")
async def handle_main_menu_next(callback: CallbackQuery, i18n: I18nContext):
    """Handle Next Season button from main menu"""
    from gpro_calendar import next_season_calendar, load_next_season_silent
    from utils import format_full_calendar

    user_id = callback.from_user.id
    await callback.answer()
    await load_next_season_silent()

    if not next_season_calendar:
        await callback.message.answer(i18n.get("next-season-not-published"))
        return

    calendar_text = format_full_calendar(
        next_season_calendar,
        "Next Season",
        is_current_season=False,
        user_id=user_id,
        i18n=i18n,
    )
    title = i18n.get("calendar-title-next", count=len(next_season_calendar))
    text = f"{title}\n\n{calendar_text}"
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "main_menu_settings")
async def handle_main_menu_settings(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle Settings button from main menu"""
    await callback.answer()

    user_id = callback.from_user.id
    keyboard = build_settings_keyboard(user_id, i18n)

    await callback.message.answer(
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith("toggle_"))
async def handle_toggle_notification(callback: CallbackQuery, i18n: I18nContext):
    """Handle notification toggle button clicks"""
    user_id = callback.from_user.id

    # Handle "Enable All" / "Disable All"
    if callback.data == "toggle_all_on":
        user_status = get_user_status(user_id)
        for notif_type in user_status["notifications"].keys():
            user_status["notifications"][notif_type] = True
        save_users_data()
        feedback_text = i18n.get("feedback-all-enabled")
    elif callback.data == "toggle_all_off":
        user_status = get_user_status(user_id)
        for notif_type in user_status["notifications"].keys():
            user_status["notifications"][notif_type] = False
        save_users_data()
        feedback_text = i18n.get("feedback-all-disabled")
    else:
        # Toggle individual notification
        notification_type = callback.data.replace("toggle_", "")
        new_state = toggle_notification(user_id, notification_type)

        # Get translated label for feedback
        label_key = f"notif-label-{notification_type.replace('_', '-')}"
        label_text = i18n.get(label_key)

        if new_state:
            feedback_text = i18n.get("feedback-notif-enabled", label=label_text)
        else:
            feedback_text = i18n.get("feedback-notif-disabled", label=label_text)

        # Get updated status after toggle
        user_status = get_user_status(user_id)

    # Rebuild the notification sub-menu with updated states (user_status already fetched above)
    notifications = user_status.get("notifications", {})

    keyboard_buttons = []
    for notif_type in NOTIFICATION_TYPES:
        enabled = notifications.get(notif_type, True)
        icon = "✅" if enabled else "❌"
        # Get translated label
        label_key = f"notif-label-{notif_type.replace('_', '-')}"
        label_text = i18n.get(label_key)
        button_text = f"{icon} {label_text}"
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"toggle_{notif_type}"
                )
            ]
        )

    # Custom notifications button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-custom-notifications"),
                callback_data="custom_notif_menu",
            )
        ]
    )

    # Add "Enable All" / "Disable All" button
    all_enabled = all(notifications.get(t, True) for t in NOTIFICATION_TYPES)
    if all_enabled:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-disable-all"), callback_data="toggle_all_off"
                )
            ]
        )
    else:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-enable-all"), callback_data="toggle_all_on"
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    # Update the message
    await callback.message.edit_reply_markup(reply_markup=keyboard)

    # Show feedback
    await callback.answer(feedback_text)


@router.callback_query(F.data.startswith("done_"))
async def handle_quali_done(callback: CallbackQuery, i18n: I18nContext):
    try:
        race_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
        return

    mark_quali_done(callback.from_user.id, race_id)
    await callback.message.edit_text(
        callback.message.text + "\n\n" + i18n.get("feedback-race-marked-done")
    )
    await callback.answer(i18n.get("feedback-quali-done"))


@router.callback_query(F.data.startswith("reset_"))
async def handle_reset(callback: CallbackQuery, i18n: I18nContext):
    if callback.data == "reset_all":
        reset_user_status(callback.from_user.id)
        await callback.message.edit_text(
            callback.message.text + "\n\n" + i18n.get("feedback-notifications-reset")
        )
        await callback.answer(i18n.get("feedback-reset"))
    else:
        # reset_{race_id} format
        try:
            race_id = int(callback.data.split("_")[1])
        except (ValueError, IndexError):
            await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
            return

        reset_user_status(callback.from_user.id)
        await callback.message.edit_text(
            callback.message.text
            + "\n\n"
            + i18n.get("feedback-notifications-reenabled")
        )
        await callback.answer(i18n.get("feedback-reenabled"))


@router.callback_query(F.data.startswith("weather_"))
async def handle_weather(callback: CallbackQuery, i18n: I18nContext):
    """Display weather forecast for a race"""
    try:
        race_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-race"), show_alert=True)
        return

    # Get weather data from race_calendar
    if race_id not in race_calendar:
        await callback.answer(i18n.get("error-race-not-found"), show_alert=True)
        return

    race_data = race_calendar[race_id]
    weather_data = race_data.get("weather")

    if not weather_data:
        await callback.answer(i18n.get("error-weather-not-available"), show_alert=True)
        return

    # Format and send weather message
    weather_message = format_weather_data(weather_data, i18n)
    track = add_flag_to_track(race_data.get("track", f"Race {race_id}"))

    full_message = f"**Race #{race_id}: {track}**\n\n{weather_message}"

    try:
        await callback.message.answer(full_message, parse_mode="Markdown")
        await callback.answer(i18n.get("feedback-weather-sent"))
    except Exception as e:
        logger.error(f"Failed to send weather for race {race_id}: {e}")
        await callback.answer(i18n.get("error-weather-send-failed"), show_alert=True)


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
        parse_mode="Markdown",
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

    # Extract language code from callback data (e.g., "lang_de" -> "de")
    lang_code = callback.data.replace("lang_", "")

    # Handle pagination separately (already handled by handle_language_page)
    if lang_code.startswith("page_"):
        return

    # Set user language
    if set_user_language(user_id, lang_code):
        lang_display = LANGUAGE_OPTIONS.get(lang_code, lang_code)

        # Get current page to rebuild keyboard with updated selection
        current_lang = get_user_language(user_id)
        # Determine which page this language is on (all bot UI languages on page 1)
        pages = [
            ["gb", "ru", "br", "it", "es", "fr", "de", "pt"],
            ["ro", "pl", "bg", "mk", "nl", "fi", "hu", "tr"],
            ["gr", "dk", "rs", "se", "lt", "ee", "al", "hr"],
            ["ch", "my", "in", "pi", "be", "cz", "sk"],
        ]
        current_page = 1
        for i, page_langs in enumerate(pages, 1):
            if lang_code in page_langs:
                current_page = i
                break

        keyboard = build_language_keyboard(
            page=current_page, current_lang=current_lang, i18n=i18n
        )

        await callback.message.edit_text(
            i18n.get("lang-menu-title", currentLang=lang_display),
            reply_markup=keyboard,
            parse_mode="Markdown",
        )
        await callback.answer(i18n.get("feedback-language-set", language=lang_display))
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
            parse_mode="Markdown",
        )
        await callback.answer(i18n.get("feedback-language-reset"))
    else:
        await callback.answer(i18n.get("error-reset-failed"), show_alert=True)


@router.callback_query(F.data == "ui_lang_menu")
async def handle_ui_language_menu(callback: CallbackQuery, i18n: I18nContext):
    """Show bot UI language selection menu"""
    user_id = callback.from_user.id
    current_ui_lang = get_user_ui_language(user_id)

    # Build UI language selection keyboard
    keyboard_buttons = []

    # Build language buttons dynamically from UI_LANGUAGE_DISPLAY
    for lang_code, lang_display in UI_LANGUAGE_DISPLAY.items():
        prefix = "✅ " if current_ui_lang == lang_code else ""
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{prefix}{lang_display}",
                    callback_data=f"set_ui_lang_{lang_code}",
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(
        i18n.get("ui-lang-menu-title"), reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_ui_lang_"))
async def handle_set_ui_language(callback: CallbackQuery, i18n: I18nContext):
    """Handle bot UI language selection in settings"""
    user_id = callback.from_user.id

    # Extract language code
    ui_lang = callback.data.replace("set_ui_lang_", "")

    # Set UI language
    if set_user_ui_language(user_id, ui_lang):
        lang_display = get_ui_language_display(ui_lang)
        await callback.answer(f"✅ {lang_display}")

        # Return to main settings menu using the new language context
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
        i18n.get("settings-title"), reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()


# Alias for backwards compatibility
@router.callback_query(F.data == "lang_back_main")
async def handle_language_back(callback: CallbackQuery, i18n: I18nContext):
    """Alias for returning to main settings"""
    await handle_settings_main(callback, i18n)


@router.callback_query(F.data == "notif_menu")
async def handle_notifications_menu(callback: CallbackQuery, i18n: I18nContext):
    """Show notifications sub-menu"""
    user_id = callback.from_user.id
    user_status = get_user_status(user_id)
    notifications = user_status.get("notifications", {})

    # Build notification toggles keyboard
    keyboard_buttons = []

    for notif_type in NOTIFICATION_TYPES:
        enabled = notifications.get(notif_type, True)
        icon = "✅" if enabled else "❌"
        # Get translated label
        label_key = f"notif-label-{notif_type.replace('_', '-')}"
        label_text = i18n.get(label_key)
        button_text = f"{icon} {label_text}"
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"toggle_{notif_type}"
                )
            ]
        )

    # Custom notifications button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-custom-notifications"),
                callback_data="custom_notif_menu",
            )
        ]
    )

    # Enable/Disable All button
    all_enabled = all(notifications.get(t, True) for t in NOTIFICATION_TYPES)
    if all_enabled:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-disable-all"), callback_data="toggle_all_off"
                )
            ]
        )
    else:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-enable-all"), callback_data="toggle_all_on"
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(
        i18n.get("notif-menu-title"), reply_markup=keyboard, parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data == "custom_notif_menu")
async def handle_custom_notifications_menu(callback: CallbackQuery, i18n: I18nContext):
    """Show custom notifications menu"""
    user_id = callback.from_user.id
    custom_notifs = get_custom_notifications(user_id)

    # Build keyboard with custom notification slots
    keyboard_buttons = []

    for slot_idx, custom_notif in enumerate(custom_notifs):
        enabled = custom_notif.get("enabled", False)
        hours_before = custom_notif.get("hours_before")

        if enabled and hours_before is not None:
            time_str = format_custom_notification_time(hours_before, i18n)
            button_text = i18n.get(
                "button-custom-slot-set", slot=slot_idx + 1, time=time_str
            )
        else:
            button_text = i18n.get("button-custom-slot-empty", slot=slot_idx + 1)

        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"custom_notif_edit_{slot_idx}"
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-notifications"),
                callback_data="notif_menu",
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    min_time = int(CUSTOM_NOTIF_MIN_HOURS * 60)  # Convert to minutes
    max_time = int(CUSTOM_NOTIF_MAX_HOURS)  # Already in hours

    await callback.message.edit_text(
        i18n.get("custom-notif-menu-title", minTime=min_time, maxTime=max_time),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("custom_notif_edit_"))
async def handle_custom_notification_edit(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle editing a custom notification slot"""
    user_id = callback.from_user.id

    try:
        slot_idx = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-slot"), show_alert=True)
        return

    custom_notifs = get_custom_notifications(user_id)
    custom_notif = custom_notifs[slot_idx]

    # Build preset buttons
    preset_times = [
        ("20m", 20 / 60),
        ("30m", 30 / 60),
        ("1h", 1),
        ("3h", 3),
        ("6h", 6),
        ("12h", 12),
        ("24h", 24),
        ("48h", 48),
        ("70h", 70),
    ]

    keyboard_buttons = []

    # Add preset buttons in rows of 3
    for i in range(0, len(preset_times), 3):
        row = []
        for label, hours in preset_times[i : i + 3]:
            row.append(
                InlineKeyboardButton(
                    text=label, callback_data=f"custom_notif_set_{slot_idx}_{hours}"
                )
            )
        keyboard_buttons.append(row)

    # Add "Custom time" button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-enter-custom-time"),
                callback_data=f"custom_notif_input_{slot_idx}",
            )
        ]
    )

    # Add "Disable" button if currently enabled
    if custom_notif.get("enabled", False):
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-disable-notification"),
                    callback_data=f"custom_notif_disable_{slot_idx}",
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back"), callback_data="custom_notif_menu"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    current_status = ""
    if custom_notif.get("enabled", False):
        time_str = format_custom_notification_time(
            custom_notif.get("hours_before"), i18n
        )
        current_status = f"\n\n**Current:** {time_str}"

    await callback.message.edit_text(
        i18n.get(
            "settings-custom-notif-edit", slot=slot_idx + 1, current=current_status
        ),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("custom_notif_set_"))
async def handle_custom_notification_set(callback: CallbackQuery, i18n: I18nContext):
    """Handle setting a custom notification with a preset value"""
    user_id = callback.from_user.id

    try:
        parts = callback.data.split("_")
        slot_idx = int(parts[3])
        hours_before = float(parts[4])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-data"), show_alert=True)
        return

    success, message = set_custom_notification(user_id, slot_idx, hours_before)

    if success:
        await callback.answer(i18n.get("feedback-custom-notif-set", message=message))
        # Return to custom notifications menu
        await handle_custom_notifications_menu(callback, i18n)
    else:
        await callback.answer(f"❌ {message}", show_alert=True)


@router.callback_query(F.data.startswith("custom_notif_disable_"))
async def handle_custom_notification_disable(
    callback: CallbackQuery, i18n: I18nContext
):
    """Handle disabling a custom notification"""
    user_id = callback.from_user.id

    try:
        slot_idx = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-slot"), show_alert=True)
        return

    success, message = set_custom_notification(user_id, slot_idx, None)

    if success:
        await callback.answer(
            i18n.get("feedback-custom-notif-disabled", slot=slot_idx + 1)
        )
        # Return to custom notifications menu
        await handle_custom_notifications_menu(callback, i18n)
    else:
        await callback.answer(f"❌ {message}", show_alert=True)


@router.callback_query(F.data.startswith("custom_notif_input_"))
async def handle_custom_notification_input_prompt(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Prompt user to enter custom time"""
    try:
        slot_idx = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-slot"), show_alert=True)
        return

    # Store slot index in state
    await state.update_data(slot_index=slot_idx)
    await state.set_state(CustomNotificationStates.waiting_for_time)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=i18n.get("button-cancel"), callback_data="custom_notif_menu"
                )
            ]
        ]
    )

    await callback.message.edit_text(
        i18n.get("settings-custom-notif-input", slot=slot_idx + 1),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data == "group_menu")
async def handle_group_menu(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Show group settings menu"""
    user_id = callback.from_user.id
    user_status = get_user_status(user_id)
    current_group = user_status.get("group")
    group_display = format_group_display(current_group)

    # Build keyboard with back and reset buttons
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

    # Prompt for group input
    await state.set_state(SetGroupStates.waiting_for_group)
    await callback.message.edit_text(
        i18n.get("group-menu-title", groupDisplay=group_display),
        reply_markup=keyboard,
        parse_mode="Markdown",
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
    from .states import TimezoneStates

    user_id = callback.from_user.id
    current_tz = get_user_timezone(user_id)
    tz = ZoneInfo(current_tz)
    tz_display = get_timezone_display_name(tz, datetime.now(timezone.utc))

    # Build keyboard with reset and back buttons
    keyboard_buttons = []

    # Reset to UTC button (only if not already UTC)
    if current_tz != "UTC":
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-reset-timezone"), callback_data="tz_reset_utc"
                )
            ]
        )

    # Back button
    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-settings"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    # Set state to wait for timezone input
    await state.set_state(TimezoneStates.waiting_for_timezone_input)

    await callback.message.edit_text(
        i18n.get("timezone-menu-title", timezone=tz_display),
        reply_markup=keyboard,
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("tz_page_"))
async def handle_timezone_page(
    callback: CallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Handle timezone search results pagination"""
    from handlers.states import show_timezone_page_edit

    # Extract page number from callback data
    page = int(callback.data.replace("tz_page_", ""))

    # Show the requested page (edit existing message)
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

    # Extract timezone name from callback data
    tz_name = callback.data.replace("tz_select_", "")

    # Set timezone
    if set_user_timezone(user_id, tz_name):
        await state.clear()

        # Get display name and example time
        tz = ZoneInfo(tz_name)
        tz_display = get_timezone_display_name(tz, datetime.now(timezone.utc))

        # Show example time conversion
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
            parse_mode="Markdown",
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

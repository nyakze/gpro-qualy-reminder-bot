"""Notification settings callback handlers"""

import logging
from aiogram import F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from notifications import (
    get_user_status,
    toggle_notification,
    save_users_data,
    get_custom_notifications,
    set_custom_notification,
    format_custom_notification_time,
    CUSTOM_NOTIF_MIN_HOURS,
    CUSTOM_NOTIF_MAX_HOURS,
)
from . import router

from handlers.event_types import AccessibleCallbackQuery

logger = logging.getLogger(__name__)

NOTIFICATION_TYPES = (
    "72h",
    "48h",
    "24h",
    "2h",
    "10min",
    "opens_soon",
    "quali_results",
    "race_replay",
    "race_live",
    "race_results",
    "new_season_reminder",
)

NOTIFICATION_CATEGORIES = {
    "before_qualifying": {
        "types": ["72h", "48h", "24h", "2h", "10min"],
        "icon": "⏰",
    },
    "qualifying_events": {
        "types": ["opens_soon", "quali_results"],
        "icon": "🏁",
    },
    "race_events": {
        "types": ["race_live", "race_replay", "race_results"],
        "icon": "🏎️",
    },
    "season_prep": {
        "types": ["new_season_reminder"],
        "icon": "🌟",
    },
}


@router.callback_query(F.data.startswith("toggle_category_"))
async def handle_toggle_category(callback: AccessibleCallbackQuery, i18n: I18nContext):
    """Enable or disable all notifications in a category"""
    user_id = callback.from_user.id
    user_status, _ = get_user_status(user_id)

    parts = callback.data.split("_")
    action = parts[2]
    category_id = "_".join(parts[3:])

    if category_id not in NOTIFICATION_CATEGORIES:
        await callback.answer(i18n.get("error-invalid-category"), show_alert=True)
        logger.warning(
            f"User {user_id} tried to toggle invalid category: {category_id}"
        )
        return

    category_types = NOTIFICATION_CATEGORIES[category_id]["types"]
    new_state = action == "on"
    state_str = "enabled" if new_state else "disabled"

    for notif_type in category_types:
        user_status["notifications"][notif_type] = new_state

    save_users_data()

    logger.info(
        f"User {user_id} {state_str} category '{category_id}' "
        f"({len(category_types)} notifications: {', '.join(category_types)})"
    )

    category_name = i18n.get(f"notif-category-{category_id.replace('_', '-')}")

    if new_state:
        feedback_text = i18n.get("feedback-category-enabled", category=category_name)
    else:
        feedback_text = i18n.get("feedback-category-disabled", category=category_name)

    await callback.answer(feedback_text)

    await handle_notification_category(callback, i18n, category_id=category_id)


@router.callback_query(F.data.startswith("toggle_"))
async def handle_toggle_notification(
    callback: AccessibleCallbackQuery, i18n: I18nContext
):
    """Handle notification toggle button clicks"""
    user_id = callback.from_user.id

    if callback.data == "toggle_all_on":
        user_status = get_user_status(user_id)[0]
        notif_types = list(user_status["notifications"].keys())
        for notif_type in notif_types:
            user_status["notifications"][notif_type] = True
        save_users_data()
        logger.info(
            f"User {user_id} enabled all notifications "
            f"({len(notif_types)} total: {', '.join(notif_types)})"
        )
        feedback_text = i18n.get("feedback-all-enabled")
        await callback.answer(feedback_text)
        await handle_notifications_menu(callback, i18n)
        return
    elif callback.data == "toggle_all_off":
        user_status = get_user_status(user_id)[0]
        notif_types = list(user_status["notifications"].keys())
        for notif_type in notif_types:
            user_status["notifications"][notif_type] = False
        save_users_data()
        logger.info(
            f"User {user_id} disabled all notifications "
            f"({len(notif_types)} total: {', '.join(notif_types)})"
        )
        feedback_text = i18n.get("feedback-all-disabled")
        await callback.answer(feedback_text)
        await handle_notifications_menu(callback, i18n)
        return
    else:
        callback_parts = callback.data.replace("toggle_", "").split("_cat_")
        notification_type = callback_parts[0]
        category_id = callback_parts[1] if len(callback_parts) > 1 else None

        new_state = toggle_notification(user_id, notification_type)

        label_key = f"notif-label-{notification_type.replace('_', '-')}"
        label_text = i18n.get(label_key)

        if new_state:
            feedback_text = i18n.get("feedback-notif-enabled", label=label_text)
        else:
            feedback_text = i18n.get("feedback-notif-disabled", label=label_text)

        await callback.answer(feedback_text)

        if category_id:
            await handle_notification_category(callback, i18n, category_id=category_id)
        else:
            await handle_notifications_menu(callback, i18n)


@router.callback_query(F.data == "notif_menu")
async def handle_notifications_menu(
    callback: AccessibleCallbackQuery, i18n: I18nContext
):
    """Show notifications menu with categories"""
    user_id = callback.from_user.id
    user_status, _ = get_user_status(user_id)
    notifications = user_status.get("notifications", {})

    keyboard_buttons = []

    for category_id, category_data in NOTIFICATION_CATEGORIES.items():
        category_types = category_data["types"]
        icon = category_data["icon"]

        enabled_count = sum(1 for t in category_types if notifications.get(t, True))
        total_count = len(category_types)

        category_name = i18n.get(f"notif-category-{category_id.replace('_', '-')}")
        button_text = f"{icon} {category_name} ({enabled_count}/{total_count})"

        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text, callback_data=f"notif_category_{category_id}"
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-custom-notifications"),
                callback_data="custom_notif_menu",
            )
        ]
    )

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

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back"), callback_data="settings_main"
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    await callback.message.edit_text(
        i18n.get("notif-menu-title"), reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("notif_category_"))
async def handle_notification_category(
    callback: AccessibleCallbackQuery, i18n: I18nContext, category_id: str | None = None
):
    """Show individual notification toggles for a category"""
    user_id = callback.from_user.id
    user_status, _ = get_user_status(user_id)
    notifications = user_status.get("notifications", {})

    if category_id is None:
        category_id = callback.data.replace("notif_category_", "")

    if category_id not in NOTIFICATION_CATEGORIES:
        await callback.answer(i18n.get("error-invalid-category"), show_alert=True)
        return

    category_data = NOTIFICATION_CATEGORIES[category_id]
    category_types = category_data["types"]
    icon = category_data["icon"]

    keyboard_buttons = []

    for notif_type in category_types:
        enabled = notifications.get(notif_type, True)
        toggle_icon = "✅" if enabled else "❌"
        label_key = f"notif-label-{notif_type.replace('_', '-')}"
        label_text = i18n.get(label_key)
        button_text = f"{toggle_icon} {label_text}"
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"toggle_{notif_type}_cat_{category_id}",
                )
            ]
        )

    category_all_enabled = all(notifications.get(t, True) for t in category_types)
    if category_all_enabled:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-disable-category"),
                    callback_data=f"toggle_category_off_{category_id}",
                )
            ]
        )
    else:
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-enable-category"),
                    callback_data=f"toggle_category_on_{category_id}",
                )
            ]
        )

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-notifications"),
                callback_data="notif_menu",
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    category_name = i18n.get(f"notif-category-{category_id.replace('_', '-')}")
    title = f"{icon} <b>{category_name}</b>"

    await callback.message.edit_text(title, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data == "custom_notif_menu")
async def handle_custom_notifications_menu(
    callback: AccessibleCallbackQuery, i18n: I18nContext
):
    """Show custom notifications menu"""
    user_id = callback.from_user.id
    custom_notifs = get_custom_notifications(user_id)

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

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-back-to-notifications"),
                callback_data="notif_menu",
            )
        ]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    min_time = int(CUSTOM_NOTIF_MIN_HOURS * 60)
    max_time = int(CUSTOM_NOTIF_MAX_HOURS)

    await callback.message.edit_text(
        i18n.get("custom-notif-menu-title", minTime=min_time, maxTime=max_time),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("custom_notif_edit_"))
async def handle_custom_notification_edit(
    callback: AccessibleCallbackQuery, state: FSMContext, i18n: I18nContext
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

    preset_configs = [
        (0.5, "minutes"),
        (1, "hours"),
        (1.5, "combined_hm"),
        (2.5, "combined_hm"),
        (6, "hours"),
        (12, "hours"),
        (18, "hours"),
        (32, "combined_dh"),
        (60, "hours"),
    ]

    preset_times = []
    for hours_val, time_type in preset_configs:
        total_minutes = int(hours_val * 60)
        d = total_minutes // (24 * 60)
        remaining_minutes = total_minutes % (24 * 60)
        h = remaining_minutes // 60
        m = remaining_minutes % 60

        if time_type == "combined_dh" and d > 0:
            label = i18n.get("time-days-hours-short", days=d, hours=h)
        elif time_type == "combined_hm" and m > 0:
            label = i18n.get("time-hours-minutes-short", hours=h, minutes=m)
        elif h > 0 or d > 0:
            label = i18n.get("time-hours-short", hours=int(hours_val))
        else:
            label = i18n.get("time-minutes-short", minutes=m)

        preset_times.append((label, hours_val))

    keyboard_buttons = []

    for i in range(0, len(preset_times), 3):
        row = []
        for label, hours in preset_times[i : i + 3]:
            row.append(
                InlineKeyboardButton(
                    text=label, callback_data=f"custom_notif_set_{slot_idx}_{hours}"
                )
            )
        keyboard_buttons.append(row)

    keyboard_buttons.append(
        [
            InlineKeyboardButton(
                text=i18n.get("button-enter-custom-time"),
                callback_data=f"custom_notif_input_{slot_idx}",
            )
        ]
    )

    if custom_notif.get("enabled", False):
        keyboard_buttons.append(
            [
                InlineKeyboardButton(
                    text=i18n.get("button-disable-notification"),
                    callback_data=f"custom_notif_disable_{slot_idx}",
                )
            ]
        )

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
        current_label = i18n.get("settings-custom-notif-current")
        current_status = f"\n\n<b>{current_label}</b> {time_str}"

    await callback.message.edit_text(
        i18n.get(
            "settings-custom-notif-edit", slot=slot_idx + 1, current=current_status
        ),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("custom_notif_set_"))
async def handle_custom_notification_set(
    callback: AccessibleCallbackQuery, i18n: I18nContext
):
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
        await handle_custom_notifications_menu(callback, i18n)
    else:
        await callback.answer(f"❌ {message}", show_alert=True)


@router.callback_query(F.data.startswith("custom_notif_disable_"))
async def handle_custom_notification_disable(
    callback: AccessibleCallbackQuery, i18n: I18nContext
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
        await handle_custom_notifications_menu(callback, i18n)
    else:
        await callback.answer(f"❌ {message}", show_alert=True)


@router.callback_query(F.data.startswith("custom_notif_input_"))
async def handle_custom_notification_input_prompt(
    callback: AccessibleCallbackQuery, state: FSMContext, i18n: I18nContext
):
    """Prompt user to enter custom time"""
    from handlers.states import CustomNotificationStates

    try:
        slot_idx = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer(i18n.get("error-invalid-slot"), show_alert=True)
        return

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
        parse_mode="HTML",
    )
    await callback.answer()

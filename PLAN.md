# Implementation Plan: Website Mode Toggle (Classic vs APP)

## Overview
Add a toggle in settings to switch between Classic GPRO website and APP website modes. When APP mode is selected, notifications will use app.gpro.net URLs instead of gpro.net URLs, and the GPRO Language setting will be hidden/disabled since APP doesn't support language parameter in most URLs.

## Requirements Summary
1. **Toggle Button**: Add "Link type: Classic / APP" button-toggle on main settings page
2. **Mode Switching Notifications**:
   - APP mode: "Switched to APP mode. GPRO Language setting will not be applied for URLs"
   - Classic mode: "Switched to Classic mode. GPRO Language will be used."
3. **GPRO Language Submenu**: Hide from settings when APP mode is selected
4. **URL Generation**: Generate different URLs based on selected mode
5. **Personalization Messages**: Adjust "add group in settings" messages for APP mode (some APP URLs don't parse group)
6. **Localization**: "APP" stays the same in all languages, "Classic" should be localized

## URL Mappings

### Classic Website (current implementation)
- Quali: `https://gpro.net/{lang}/Qualify.asp`
- Starting Grid: `https://gpro.net/{lang}/StartingGrid.asp?Group={group}`
- Race Live: `https://gpro.net/{lang}/racescreenlive.asp?Group={group}`
- Race Replay: `https://gpro.net/{lang}/racescreen.asp?Group={group}`
- Race Analysis: `https://gpro.net/{lang}/RaceAnalysis.asp`
- Race Summary: `https://gpro.net/{lang}/RaceSummary.asp?Group={group}`

**Note**: Q1/Q2 Standings link removed - users can navigate to it from starting grid on the website interface.

### APP Website (new implementation)
- Quali (office): `https://app.gpro.net/office` (NO group, NO lang)
- Starting Grid: `https://app.gpro.net/qstandings/startgrid/{group}` (group parsed)
- Race Live: **NOT FOUND YET - use classic for now**
- Race Replay: `https://app.gpro.net/pastrace/racereplay` (NO group)
- Race Analysis: `https://app.gpro.net/pastrace/analysis` (NO group)
- Race Summary: `https://app.gpro.net/pastrace/summary/{group}` (group parsed)

**Note**: Q1/Q2 standings links removed - users can navigate to them from starting grid on the website interface.

### Group Format Conversion
For APP URLs that support group, need to convert from `M3`, `R11`, etc. to:
- `M3` → `Master%20-%203` (URL encoded)
- `R11` → `Rookie%20-%2011`
- `E` → `Elite`
- Format: `{GroupName}%20-%20{Number}` or just `Elite`

## Implementation Steps

### 1. Data Structure Changes

**File**: `notifications/user_data.py`

- Add `website_mode` field to default user structure
- Default value: `"classic"`
- Possible values: `"classic"` or `"app"`
- Add migration logic in `get_user_status()` to add field to existing users

**Changes**:
```python
# In get_user_status() - add to new user creation:
"website_mode": "classic",

# Add migration for existing users (after loading):
if "website_mode" not in users_data[user_id]:
    users_data[user_id]["website_mode"] = "classic"
    save_users_data()
```

### 2. URL Generation Updates

**File**: `notifications/sender.py`

**New Functions**:
- `generate_app_quali_link()` → returns `https://app.gpro.net/office`
- `generate_app_starting_grid_link(group)` → returns `https://app.gpro.net/qstandings/startgrid/{formatted_group}`
- `generate_app_race_live_link(group, gpro_lang)` → returns classic link (fallback until APP link found)
- `generate_app_race_replay_link()` → returns `https://app.gpro.net/pastrace/racereplay` (no group)
- `generate_app_race_analysis_link()` → returns `https://app.gpro.net/pastrace/analysis` (no group)
- `generate_app_race_summary_link(group)` → returns `https://app.gpro.net/pastrace/summary/{formatted_group}`

**Helper Function**:
```python
def format_group_for_app_url(group: str) -> str:
    """Convert group code to APP URL format

    Examples:
        E → Elite
        M3 → Master%20-%203
        R11 → Rookie%20-%2011
    """
    if not group:
        return ""

    group = group.strip().upper()

    if group == "E":
        return "Elite"

    match = re.match(r"^([MPAR])(\d{1,3})$", group)
    if not match:
        return ""

    letter, number = match.groups()
    group_names = {"M": "Master", "P": "Pro", "A": "Amateur", "R": "Rookie"}
    group_name = group_names[letter]

    return f"{group_name}%20-%20{number}"
```

**Update Existing Functions**:
Modify all notification sending functions to check `website_mode` and call appropriate URL generator:

- `send_quali_notification()` - check mode, use `generate_app_quali_link()` if APP
- `send_quali_results_notification()` - check mode, use APP starting grid link only (no Q1/Q2 in both modes)
- `send_race_live_notification()` - check mode (use classic fallback for APP)
- `send_race_replay_notification()` - check mode, use `generate_app_race_replay_link()` if APP
- `send_race_results_notification()` - check mode, use APP analysis/summary links if APP

**Example Update Pattern**:
```python
# In send_quali_notification()
user_status = get_user_status(user_id)
website_mode = user_status.get("website_mode", "classic")

if website_mode == "app":
    quali_link = generate_app_quali_link()
else:
    quali_link = generate_quali_link(gpro_lang)
```

### 3. Settings UI Changes

**File**: `handlers/callbacks.py`

**Update `build_settings_keyboard()` function**:
- Add "Website Mode" button before or after UI Language button
- Show current mode (Classic or APP)
- **Conditionally hide GPRO Language button** when APP mode is selected

**Changes**:
```python
def build_settings_keyboard(user_id: int, i18n: I18nContext) -> InlineKeyboardMarkup:
    user_status = get_user_status(user_id)
    current_ui_lang = user_status.get("ui_lang", "gb")
    current_lang = user_status.get("gpro_lang", "gb")
    current_group = user_status.get("group")
    website_mode = user_status.get("website_mode", "classic")  # NEW

    keyboard_buttons = []

    # Bot UI Language button
    # ... existing code ...

    # Website Mode button (NEW)
    mode_display = "APP" if website_mode == "app" else i18n.get("website-mode-classic")
    keyboard_buttons.append([
        InlineKeyboardButton(
            text=i18n.get("button-website-mode", mode=mode_display),
            callback_data="toggle_website_mode"
        )
    ])

    # GPRO Website Language button - ONLY show if Classic mode
    if website_mode == "classic":
        lang_display = LANGUAGE_OPTIONS.get(current_lang, current_lang)
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=i18n.get("button-gpro-language", language=lang_display),
                callback_data="lang_menu"
            )
        ])

    # Group button
    # ... rest of existing code ...
```

### 4. Callback Handler for Toggle

**File**: `handlers/callbacks.py`

**New Handler**:
```python
@router.callback_query(F.data == "toggle_website_mode")
async def handle_toggle_website_mode(callback: CallbackQuery, i18n: I18nContext):
    """Toggle between Classic and APP website modes"""
    from notifications import set_user_website_mode

    user_id = callback.from_user.id
    user_status = get_user_status(user_id)
    current_mode = user_status.get("website_mode", "classic")

    # Toggle mode
    new_mode = "app" if current_mode == "classic" else "classic"

    # Save new mode
    if set_user_website_mode(user_id, new_mode):
        # Show notification message
        if new_mode == "app":
            message = i18n.get("feedback-switched-to-app")
            # "Switched to APP mode. GPRO Language setting will not be applied for URLs"
        else:
            message = i18n.get("feedback-switched-to-classic")
            # "Switched to Classic mode. GPRO Language will be used."

        await callback.answer(message, show_alert=True)

        # Refresh settings menu to update button and hide/show GPRO language
        await handle_settings_main(callback, i18n)
    else:
        await callback.answer(i18n.get("error-mode-switch-failed"), show_alert=True)
```

### 5. User Data Helper Functions

**File**: `notifications/user_data.py`

**New Function**:
```python
def set_user_website_mode(user_id: int, mode: str) -> bool:
    """Set user's website mode (classic or app)

    Args:
        user_id: Telegram user ID
        mode: "classic" or "app"

    Returns:
        bool: True if successful, False otherwise
    """
    if mode not in ["classic", "app"]:
        logger.warning(f"Invalid website mode: {mode}")
        return False

    user_status = get_user_status(user_id)
    user_status["website_mode"] = mode
    save_users_data()
    logger.info(f"User {user_id} switched to {mode} mode")
    return True

def get_user_website_mode(user_id: int) -> str:
    """Get user's website mode

    Returns:
        str: "classic" or "app" (defaults to "classic")
    """
    user_status = get_user_status(user_id)
    return user_status.get("website_mode", "classic")
```

**Export in `__init__.py`**:
```python
from .user_data import (
    # ... existing exports ...
    set_user_website_mode,
    get_user_website_mode,
)
```

### 6. Notification Message Updates

**Context**: Some notifications show messages like "Set your group in settings to personalize this link" when group is not set. For APP mode, some links don't support group personalization, so we need to adjust these messages.

**Files to Update**:
- Localization files (`locales/*/messages.ftl`) - may need separate messages for APP mode
- `notifications/sender.py` - notification functions

**Group Personalization by Notification Type**:

| Notification Type | Classic | APP | Show "add group" message? |
|-------------------|---------|-----|---------------------------|
| Quali Opens | No group | No group | **No** (neither support group) |
| Quali Results (Grid only) | Has group | Has group | **Yes** (both support group) |
| Race Live | Has group | Has group (fallback classic) | **Yes** (both support group) |
| Race Replay | Has group | **NO group** | **Conditional** (Classic: Yes, APP: No) |
| Race Results (Analysis) | No group | No group | **No** (neither support group) |
| Race Results (Summary) | Has group | Has group | **Yes** (both support group) |

**Note**: Q1/Q2 standings links removed from quali results notification in both modes - only starting grid is sent.

**Implementation**:
- For **Race Replay** notification in APP mode: Don't show "add group" message variant
- Keep existing logic for other notifications

**Update in `send_race_replay_notification()`**:
```python
async def send_race_replay_notification(
    bot: Bot, user_id: int, race_id: int, race_data: Dict, i18n=None
):
    user_status = get_user_status(user_id)
    group = user_status.get("group")
    website_mode = user_status.get("website_mode", "classic")

    # ... get UI language, track, etc ...

    # Generate replay link based on mode
    if website_mode == "app":
        replay_link = generate_app_race_replay_link()  # No group support
        # Use no-group message variant regardless of group setting
        message = get_text(
            "notif-race-replay-no-group",
            raceId=race_id,
            track=track,
            raceTime=race_time,
            replayLink=replay_link,
        )
    else:
        replay_link = generate_replay_link(group, gpro_lang)
        # Use group/no-group message based on group setting
        if group:
            message = get_text(
                "notif-race-replay",
                # ... with group ...
            )
        else:
            message = get_text(
                "notif-race-replay-no-group",
                # ... without group ...
            )
```

### 7. Localization Strings

**Files**: `locales/{lang}/messages.ftl` (all 12 languages)

**New Strings to Add**:

```fluent
# Website Mode Toggle
button-website-mode = Link type: {$mode}
website-mode-classic = Classic
feedback-switched-to-app = Switched to APP mode. GPRO Language setting will not be applied for URLs.
feedback-switched-to-classic = Switched to Classic mode. GPRO Language will be used.
error-mode-switch-failed = Failed to switch website mode. Please try again.
```

**Translation Notes**:
- `website-mode-classic` should be localized (e.g., "Clásico", "Classique", "Классический", etc.)
- "APP" remains "APP" in all languages (it's a proper name)
- Feedback messages should be fully translated

**Locales to Update** (12 total):
- `gb` (English) - write first
- `ru` (Russian)
- `br` (Brazilian Portuguese)
- `it` (Italian)
- `es` (Spanish)
- `fr` (French)
- `nl` (Dutch)
- `bg` (Bulgarian)
- `cz` (Czech)
- `in` (Hindi)
- `ua` (Ukrainian)
- `pt` (European Portuguese)

### 8. Testing Checklist

**Manual Testing**:
1. ✅ Toggle from Classic to APP mode
   - Verify GPRO Language button disappears
   - Verify notification message appears

2. ✅ Toggle from APP to Classic mode
   - Verify GPRO Language button reappears
   - Verify notification message appears

3. ✅ Send test notifications in APP mode (with group set):
   - Quali opens → office link (no group)
   - Quali results → starting grid link with group only
   - Race live → classic fallback (temp)
   - Race replay → replay link without group
   - Race results → analysis (no group) + summary (with group)

4. ✅ Send test notifications in APP mode (without group set):
   - Quali opens → office link
   - Quali results → starting grid base link
   - Race replay → no "add group" message

5. ✅ Verify existing users migration:
   - Load bot with existing users_data.json
   - Verify `website_mode: "classic"` added automatically

6. ✅ Test localization:
   - Switch UI language
   - Verify "Classic" translates correctly
   - Verify "APP" stays "APP"

## Implementation Order

1. **Data Layer** (user_data.py)
   - Add `website_mode` field and migration
   - Add getter/setter functions

2. **URL Generation** (sender.py)
   - Add APP URL generation functions
   - Add helper for group formatting

3. **Settings UI** (callbacks.py)
   - Update `build_settings_keyboard()`
   - Add toggle handler

4. **Notification Updates** (sender.py)
   - Update all `send_*_notification()` functions
   - Add conditional URL generation
   - Handle group personalization messages

5. **Localization** (messages.ftl)
   - Add English strings first
   - Translate to all 11 other languages

6. **Testing**
   - Manual testing with test account
   - Verify URL formats
   - Test mode switching
   - Test with/without group

## Edge Cases to Handle

1. **Live Race Link**: APP link not found yet
   - **Solution**: Use classic link as fallback for now
   - Add TODO comment in code

2. **Existing Users**: Migration for users without `website_mode`
   - **Solution**: Auto-add field with default "classic" in `get_user_status()`

3. **Invalid Mode Value**: If somehow set to invalid value
   - **Solution**: Validate in setter, fallback to "classic" in getter

4. **Q1/Q2 Links**: Removed from both Classic and APP modes
   - **Reason**: Users can easily navigate to Q1/Q2 from starting grid on the website interface
   - **Decision**: Send only starting grid link in quali results notification for both modes

## Files Modified Summary

**Core Logic**:
- `notifications/user_data.py` - Add website_mode field, getter/setter
- `notifications/sender.py` - Add APP URL generators, update notification senders
- `notifications/__init__.py` - Export new functions

**Handlers**:
- `handlers/callbacks.py` - Update settings keyboard, add toggle handler

**Localization** (12 files):
- `locales/gb/messages.ftl`
- `locales/ru/messages.ftl`
- `locales/br/messages.ftl`
- `locales/it/messages.ftl`
- `locales/es/messages.ftl`
- `locales/fr/messages.ftl`
- `locales/nl/messages.ftl`
- `locales/bg/messages.ftl`
- `locales/cz/messages.ftl`
- `locales/in/messages.ftl`
- `locales/ua/messages.ftl`
- `locales/pt/messages.ftl`

**Total Files**: ~16 files

## Estimated Complexity

- **Low Risk**: Data structure changes, localization
- **Medium Risk**: URL generation logic, settings UI
- **Testing Required**: All notification types with both modes
- **Reversibility**: High (toggle allows easy switch back)

## Future Enhancements

1. Find APP live race link when available
2. Consider adding preview of URLs in settings
3. Add deep link support if APP supports it
4. Monitor user adoption via metrics

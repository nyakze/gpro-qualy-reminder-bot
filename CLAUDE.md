# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GPRO Telegram bot that sends automatic qualification deadline notifications and provides race status/schedule commands for Grand Prix Racing Online (GPRO). Built with Aiogram 3.x, supports dual-language UI (English/Russian) and 31 GPRO languages for personalized race links.

## Development Commands

### Running the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot (main entry point)
python bot.py

# Kill existing notification checker (useful for debugging)
pkill -f bot.py
```

### Code Quality

```bash
# Format code
black .

# Lint and auto-fix
ruff check --fix .
```

### Deployment (systemd on Ubuntu)

```bash
# View logs
sudo journalctl -u gpro -f

# Restart service
sudo systemctl restart gpro

# Check status
sudo systemctl status gpro
```

### Testing & Debugging

```bash
# Watch user data changes
tail -f users_data.json

# Watch bot logs
tail -f gpro_bot.log

# View service logs
sudo journalctl -u gpro -f
```

## Architecture

### Core System Flow

1. **Startup** (`bot.py`):
   - Load environment config → Load user data → Load timezone search index → Load calendar cache → Setup i18n → Start handlers → Launch notification checker loop

2. **Notification System** (async background task):
   - Adaptive check interval: 5min normally, 1min when race approaching
   - API polling for quali opening detection (2-3.5h after previous race)
   - Weather data fetch when quali opens (with retry logic)
   - Notification windows: 48h, 24h, 2h, 10min before quali close + custom times + quali opens + race live + replay + results

3. **Handler Chain** (Aiogram 3.x):
   - User message → i18n middleware (determines UI language) → Router → Command/Callback/State handlers → Response

### Critical Data Flow Patterns

**User Data Persistence:**
- All user settings stored in `users_data.json` (in-memory dict + atomic file writes)
- Auto-migration pattern: Missing fields added on `get_user_status()` call
- CRITICAL: User ID keys are integers in memory but strings in JSON (type conversion on load/save)

**Calendar Management:**
- Two calendars: current season (`gpro_calendar.json`) and next season (`next_season_calendar.json`)
- Race IDs are sequential 1-17, re-numbered by date on API parse (not using GPRO's `idxReal`)
- Race timing: Always 19:00 UTC, quali closes 1.5h before race
- Weather data embedded in race entries, persisted to file after fetch

**Notification Deduplication:**
- In-memory `notify_history` dict: `{(race_id, label): timestamp}` or `{(user_id, race_id, label): timestamp}` for custom
- 30-day retention, cleaned on each check cycle
- Prevents duplicate sends within same notification window

### Module Structure

**`bot.py`** - Main entry point
- Initializes Bot, Dispatcher, i18n, handlers
- Launches notification checker as background task

**`config.py`** - Environment configuration
- Loads `.env` (BOT_TOKEN, GPRO_API_TOKEN, ADMIN_USER_ID)
- Supports comma-separated admin IDs
- Validates required tokens on import

**`gpro_calendar.py`** - GPRO API integration & calendar management
- Functions: `update_calendar()` (API fetch), `load_calendar_silent()` (cache only), `check_quali_status_from_api()`, `fetch_weather_from_api()`
- Global dicts: `race_calendar`, `next_season_calendar`
- Date parsing handles multiple formats including "Today" detection

**`i18n_setup.py`** - Internationalization
- FluentRuntimeCore with custom UserLanguageManager
- Locales in `locales/{en,ru}/*.ftl`
- UI language separate from GPRO link language (31 languages)

**`handlers/`** - Aiogram 3.x handlers
- `commands.py`: /start, /status, /calendar, /next, /settings, /update, /updatetz, /weather, /users
- `callbacks.py`: Button interactions (quali done, weather, notifications toggle, settings)
- `states.py`: FSM handlers for multi-step flows
- `onboarding.py`: New user language + group selection flow
- `__init__.py`: Router initialization, imports all handlers

**`notifications/`** - Notification system
- `checker.py`: Main loop with adaptive intervals, notification window checking, API polling logic
- `sender.py`: Send functions for each notification type (quali, opens, live, replay, results)
- `user_data.py`: User persistence, settings management, atomic writes
- `validation.py`: Custom notification validation (20min-70h range)

**`utils.py`** - Shared utilities
- Flag emoji generation, time formatting, URL builders, group name formatting

**`timezone_utils.py`** - Timezone conversion & management
- **Timezone data source**: Downloaded from Geoapify (IANA + Wikipedia data) via `/updatetz` command
- **timezone-info.json**: ~600 timezones with multi-language city names (auto-downloaded, committed to repo)
- **Search index**: Built at startup from timezone-info.json, supports city names in multiple languages
- get_user_timezone(): Get ZoneInfo object for user
- convert_to_user_tz(): Convert UTC datetime to user's timezone
- format_datetime_for_user(): Convert and format with timezone abbreviation
- get_timezone_display_name(): Human-readable names like "New York (EST)"
- fuzzy_search_timezones(): Rapidfuzz-based search with city names (including Cyrillic/non-Latin), countries, UTC offsets
- Automatic DST handling via Python's zoneinfo module
- POPULAR_TIMEZONES: Deprecated fallback if timezone-info.json not available

### Important Implementation Details

**Notification Timing Logic:**
- Standard windows use tolerance (±6min for 48h/24h, ±5min for 2h, ±2min for 10min)
- Custom notifications have ±5min tolerance
- Race live: Send 1min before to 5min after race start
- Quali opens: API polling every 10min from 2-3.5h post-race, fallback at 3.5h if not detected

**Weather Data Flow:**
- Fetched from Practice API when quali opens (either via API detection or fallback)
- Retry once on failure (5s delay)
- Cached in `race_calendar[race_id]['weather']` and persisted to file
- Available via Weather button in status message

**Onboarding Flow:**
- New users: Language selection → Group selection → Settings confirmation
- Uses FSM states (OnboardingStates.choosing_language, choosing_group)
- Sets both `ui_lang` (bot interface) and `gpro_lang` (GPRO links)

**Admin Commands:**
- `/update`: Fetch calendar from API (current + next season if published)
- `/updatetz`: Download timezone metadata from Geoapify and rebuild search index
- `/weather`: Manual weather fetch for testing
- `/users`: List all users with completion status
- Admin check: `user_id in ADMIN_USER_IDS` (set in config.py)

**Timezone Support:**
- Users can set their timezone via Settings → Timezone
- Text input → fuzzy search → inline keyboard selection flow
- All race times displayed in user's local timezone with abbreviation (e.g., "15.01 19:00 EST")
- DST handled automatically via Python's `zoneinfo` module
- Default timezone: UTC (backward compatible with existing users)
- Fuzzy search supports: city names in multiple languages ("москва", "tbilisi"), countries, UTC offsets ("utc+3")
- ~600 timezones from Geoapify dataset (downloaded via `/updatetz`, stored in timezone-info.json)
- Search index built at startup for fast fuzzy matching
- Conversion happens at display time, UTC stored in calendar
- Migration auto-adds 'timezone': 'UTC' field to existing users
- POPULAR_TIMEZONES fallback if timezone-info.json not available

### Testing Considerations

- Notification checker runs continuously - use `pkill` to reset state
- Calendar cache persists across restarts - delete JSON files to force refresh
- Weather data cached in calendar - remove from JSON or call `/weather` to re-fetch
- User data migrations happen automatically on first access after code changes
- Notification history is in-memory only - cleared on bot restart

### Common Gotchas

- User IDs are `int` in code but `str` in JSON - always convert on load/save
- Race IDs are sequential 1-17, NOT GPRO's original event IDs
- Notification labels must match exactly: "48h", "24h", "2h", "10min", "opens_soon", "race_live", "race_replay", "race_results", "custom_1", "custom_2"
- i18n context requires `await i18n.core.startup()` before use
- Atomic file writes use `.tmp` extension + `os.replace()` for crash safety
- API polling for quali opens is rate-limited (10min intervals) to avoid excessive calls

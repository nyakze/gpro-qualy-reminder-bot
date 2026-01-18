# AGENTS.md

This file provides guidance for agentic coding agents working in this repository.

## Project Overview

GPRO Telegram bot that sends automatic qualification deadline notifications for Grand Prix Racing Online. Built with Aiogram 3.x, supports 12-language UI and 31 GPRO link languages.

## Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot (main entry point)
python bot.py

# Kill existing process
pkill -f bot.py

# Format code
black .

# Lint and auto-fix
ruff check --fix .

# View logs
tail -f gpro_bot.log
journalctl -u gpro -f --output=cat  # if deployed

# Note: No automated test suite exists in this project
```

## Environment Setup

```bash
# Create .env file from .env.example
cp .env.example .env

# Install dependencies
pip install -r requirements.txt
```

Required `.env` variables:
- `TELEGRAM_BOT_TOKEN` - from @botfather
- `GPRO_API_TOKEN` - from https://app.gpro.net/apiaccess
- `ADMIN_USER_ID` - your Telegram ID (comma-separated for multiple admins)

## Code Style Guidelines

### Imports
- Use absolute imports for top-level modules: `from config import BOT_TOKEN`
- Use relative imports for intra-package modules: `from . import commands`
- Group imports: stdlib → third-party → local
- Alphabetize within groups

### Formatting
- 4-space indentation (no tabs)
- Line length: 88 characters (Black default)
- No trailing whitespace
- One blank line between function definitions

### Types
- Use type hints for function signatures
- Common patterns:
  - `Dict[str, Any]` for flexible dicts
  - `List[str]` for lists
  - `Optional[X]` or `X | None` for nullable values
  - `int` for user IDs in memory, convert to/from `str` for JSON

### Naming Conventions
- **Modules**: `snake_case` (e.g., `gpro_calendar.py`)
- **Classes**: `PascalCase` (e.g., `OnboardingStates`)
- **Functions/variables**: `snake_case` (e.g., `load_users_data`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BOT_TOKEN`, `USERS_FILE`)
- **Private functions**: leading underscore (e.g., `_get_timezone`)
- **Language codes**: Use GPRO format (`gb` not `en`, `ua` not `uk`)

### Error Handling
- Validate required config at module import: `if not BOT_TOKEN: raise ValueError(...)`
- Use logging for errors: `logger.error("message")`
- Wrap API calls in try/except with specific exception types
- Let exceptions propagate for unexpected errors; catch for recoverable cases
- User-facing errors: send Telegram message with context

### Async/Aiogram Patterns
- Use `async def` for handler functions
- Access state via `state: FSMContext` parameter
- Answer callbacks via `callback_query.answer()` or edit reply markup
- Use `MemoryStorage` for FSM (no Redis)
- Always `await` coroutines

### File Operations
- Use atomic writes for JSON: write to `.tmp` then `os.replace()`
- Define paths using `os.path.dirname(__file__)` for portability
- Global module-level dicts (e.g., `users_data`, `race_calendar`) for in-memory caching

### i18n
- Store translations in `locales/{code}/messages.ftl`
- UI language codes: `gb, ru, br, it, es, fr, nl, bg, cz, in, ua, pt`
- Use `await i18n.core.startup()` before accessing translations
- Map `ua` → `gb` for GPRO links (Ukrainian not supported)

### Key Conventions
- Race IDs: sequential 1-17 (not GPRO's original IDs)
- User IDs: `int` in memory, `str` in JSON
- Notification labels: `"48h"`, `"24h"`, `"2h"`, `"10min"`, `"opens_soon"`, `"race_live"`, `"race_replay"`, `"race_results"`, `"custom_1"`, `"custom_2"`
- Admin check: `user_id in ADMIN_USER_IDS`

### Snooze Feature
- **Snooze options**: +5m, +15m, +30m, +1h, +2h, +4h, +8h
- **Max snoozes**: 3 per notification type (72h, 48h, 24h, 2h, 10min, deadline)
- **Tolerance**: `SNOOZE_TOLERANCE_SECONDS = 120` - snoozes fire up to 2min late
- **Fast mode**: Checker switches to 60s interval when snooze is within 10min
- **Multiple snoozes**: User can snooze multiple times; each creates unique reminder
- **Storage**: Snoozes saved in `users_data.json` as `active_snoozes` dict

### Module Structure
- Add module docstring at file top: `"""Module description"""`
- Initialize module-level logger: `logger = logging.getLogger(__name__)`
- Define global module-level dicts for caching (e.g., `race_calendar`, `users_data`)
- Use `_SCRIPT_DIR` pattern for file paths: `os.path.dirname(os.path.abspath(__file__))`
- In `bot.py`: `sys.path.insert(0, ".")` for proper module imports

### Handler Patterns
- Register handlers with `@router.message()` or `@router.callback_query()` decorators
- Use filter objects: `Command("start")`, `F.data.startswith("prefix")`, `F.text & ~F.text.startswith("/")`
- Handler signature: `async def handler(event: Type, state: FSMContext, i18n: I18nContext)`
- Import router from local module: `from . import router`
- Clear FSM state with `await state.clear()` when flow completes

### Keyboard Building
- Use `InlineKeyboardMarkup(inline_keyboard=[[buttons], [buttons]])`
- Create buttons with `InlineKeyboardButton(text="Label", callback_data="data")`
- Build functions return `(keyboard, message_text)` tuples for reusability
- Use `callback_query.answer()` to acknowledge button presses
- Edit messages with `message.edit_text()` instead of sending new when updating

### Logging Patterns
- Use structured logging: `log_structured(logging.INFO, "message", key=value)` from `infra/logging`
- For non-structured logging: `logger.info("message")` with module-level logger
- Log new users with emoji marker: `logger.info(f"🆕 NEW user {user_id}")`
- Use appropriate levels: INFO for normal operations, WARNING for recoverable issues, ERROR for failures

### Logging Configuration
- **Console output**: Human-readable colored format with timestamps
  - `[HH:MM:SS] [LEVEL] message`
  - Colors: DEBUG (gray), INFO (green), WARNING (yellow), ERROR (red)
  - Colors auto-disable when piped/redirected
- **File output**: JSON format for parsing tools (unchanged)
- **Verbose mode**: Use `-v` or `--verbose` flag to show DEBUG logs in console
  - `python bot.py -v` enables debug logging
  - File logs always capture all levels regardless

### Startup Banner
The bot prints a banner after data is loaded showing:
- User count
- Race count
- Admin count
- Timezone count
- i18n language count

Use `set_startup_data(users_count=X, races=Y, ...)` in `bot.py` to populate banner data before `print_banner()` is called.

### Log Rotation
Settings defined in `infra/logging.py`:
- `LOG_MAX_BYTES = 1 * 1024 * 1024` (1 MB per file)
- `LOG_BACKUP_COUNT = 5` (5 rotating files)

## Architecture Summary

```
bot.py              → Entry point, dispatcher setup, middleware
infra/              → Logging, signal handlers, notification runner
config.py           → Environment config validation
gpro_calendar.py    → API integration, calendar cache
i18n_setup.py       → Fluent i18n middleware
timezone_utils.py   → Timezone conversion, fuzzy search
middleware/
    user_profile.py → Auto-update user profile on interactions
handlers/           → Command, callback, FSM handlers
notifications/      → Checker loop, senders, user data
utils.py            → Shared helpers (flags, formatting)
```

## Critical Data Patterns

- **User Data**: `users_data.json` with atomic writes; auto-migrate on access
- **Calendar**: `gpro_calendar.json` and `next_season_calendar.json`
- **Notification History**: In-memory `notify_history` dict with 30-day retention
- **Timezone Data**: Downloaded from Geoapify, stored in `timezone-info.json`

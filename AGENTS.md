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

# Run a specific test (pytest with file::test_name pattern)
pytest notifications/test_user_data.py::test_load_users_data -v
pytest handlers/tests/ -k "test_onboarding" -v

# Run all tests
pytest

# View logs
tail -f gpro_bot.log
journalctl -u gpro -f  # if deployed
```

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

## Architecture Summary

```
bot.py              → Entry point, dispatcher setup, middleware
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

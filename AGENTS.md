# AGENTS.md

Guidance for agentic coding agents working in this repository.

## Project Overview

GPRO Telegram bot for automatic qualification deadline notifications. Built with Aiogram 3.x, supports 12-language UI and 31 GPRO link languages.

## Essential Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot (main entry point)
python bot.py

# Kill existing process
pkill -f bot.py

# Format code (4-space indent, 88 char line length)
black .

# Lint with auto-fix
ruff check --fix .

# Type check
mypy .

# View logs
tail -f gpro_bot.log
journalctl -u gpro -f --output=cat  # if deployed
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run single test file
python -m pytest tests/test_timezone_utils.py -v

# Run single test class
python -m pytest tests/test_validation.py::TestGroupValidation -v

# Run single test
python -m pytest tests/test_validation.py::TestGroupValidation::test_valid_elite_group -v

# Run with coverage
python -m pytest tests/ --cov=.

# Run in background and watch
python -m pytest tests/ -v --tb=short
```

## Environment Setup

```bash
cp .env.example .env
pip install -r requirements.txt
```

Required `.env` variables:
- `TELEGRAM_BOT_TOKEN` - from @botfather
- `GPRO_API_TOKEN` - from https://app.gpro.net/apiaccess
- `ADMIN_USER_ID` - your Telegram ID (comma-separated for multiple admins)

## Code Style Guidelines

### Imports
- Absolute for top-level: `from config import BOT_TOKEN`
- Relative for intra-package: `from . import commands`
- Group: stdlib → third-party → local, alphabetized

### Formatting & Types
- 4-space indentation (no tabs), 88 char lines (Black default)
- Type hints for function signatures
- `Dict[str, Any]`, `List[str]`, `Optional[X]` or `X | None`
- User IDs: `int` in memory, `str` in JSON

### Naming Conventions
| Pattern | Convention | Example |
|---------|------------|---------|
| Modules | snake_case | `gpro_calendar.py` |
| Classes | PascalCase | `OnboardingStates` |
| Functions/variables | snake_case | `load_users_data()` |
| Constants | UPPER_SNAKE_CASE | `BOT_TOKEN` |
| Private functions | leading underscore | `_get_timezone()` |
| Language codes | GPRO format | `gb`, `ua` (not `en`, `uk`) |

### Error Handling
- Validate required config at import: `if not BOT_TOKEN: raise ValueError(...)`
- Use `logger.error()` for errors
- Wrap API calls in try/except with specific exceptions
- Let exceptions propagate for unexpected errors; catch for recoverable
- User-facing errors: send Telegram message with context

## Key Patterns

### Async/Aiogram
- Use `async def` for handlers
- State via `state: FSMContext` parameter
- Answer callbacks via `callback_query.answer()` or edit markup
- Always `await` coroutines

### File Operations
- Atomic JSON writes: write to `.tmp` then `os.replace()`
- Paths: `os.path.dirname(__file__)` for portability
- Global module-level dicts for in-memory caching

### Handlers
```python
@router.message(Command("start"))
async def handler(event: Type, state: FSMContext, i18n: I18nContext):
    ...
```
- Register with `@router.message()` or `@router.callback_query()`
- Use filters: `Command("start")`, `F.data.startswith("prefix")`
- Clear FSM with `await state.clear()` on flow completion

### Keyboard Building
```python
InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Label", callback_data="data")])
```
- Return `(keyboard, message_text)` tuples for reusability
- Edit messages with `message.edit_text()` not new sends

## Critical Conventions

- **Race IDs**: sequential 1-17 (not GPRO's original IDs)
- **Notification labels**: `"48h"`, `"24h"`, `"2h"`, `"10min"`, `"opens_soon"`, `"race_live"`, `"race_replay"`, `"race_results"`, `"custom_1"`, `"custom_2"`
- **Admin check**: `user_id in ADMIN_USER_IDS`
- **Snooze limits**: 3 per notification type, tolerance 120s, fast mode within 10min

## i18n

- Store translations in `locales/{code}/messages.ftl`
- UI languages: `gb, ru, br, it, es, fr, nl, bg, cz, in, ua, pt`
- Use `await i18n.core.startup()` before translations
- Map `ua` → `gb` for GPRO links

## Logging

- Structured: `log_structured(logging.INFO, "message", key=value)` from `infra/logging`
- Simple: `logger.info("message")` with module-level logger
- Verbose mode: `python bot.py -v` shows DEBUG in console
- File logs: JSON format, auto-rotates (1MB × 5 files)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail | Run `python -m pytest tests/ -v --tb=short` |
| Lint errors | Run `ruff check --fix .` then `black .` |
| Type errors | Run `mypy .` |
| Bot won't start | Check `gpro_bot.log` for errors |
| No calendar data | Verify `GPRO_API_TOKEN` in `.env` |
| Missing translations | Check `locales/{code}/messages.ftl` files |

## Module Structure

```
bot.py              → Entry point, dispatcher, middleware
infra/              → Logging, signals, notification runner
config.py           → Environment validation
gpro_calendar.py    → API integration, calendar cache
i18n_setup.py       → Fluent i18n middleware
timezone_utils.py   → Timezone, fuzzy search
middleware/         → User profile, rate limit
handlers/           → Command, callback, FSM handlers
notifications/      → Checker loop, senders
utils.py            → Helpers, formatting
tests/              → Pytest tests
```

## Critical Data

- **User Data**: `users_data.json`, atomic writes, auto-migrate
- **Calendar**: `gpro_calendar.json`, `next_season_calendar.json`
- **Notification History**: In-memory `notify_history`, 30-day retention
- **Timezone Data**: Geoapify, stored in `timezone-info.json`

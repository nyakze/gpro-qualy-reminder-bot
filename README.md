# GPRO Bot

Telegram bot for Grand Prix Racing Online (GPRO) that sends qualification deadline notifications and provides race status/schedule commands.

## 🚀 Public version
🌟 Public bot available: [@gproremindbot](https://t.me/gproremindbot). Feel free to give it a try!

## Features

### Notifications
- **Automatic qualifying notifications:** 72h, 48h, 24h, 2h, 10min before qualifying closes
- **Snooze notifications:** Postpone any qualifying notification (+5m, +15m, +30m, +1h, +2h, +4h, +8h). Stack up to 3 snoozes per notification type. Snoozed notifications can be snoozed again.
- **Custom notification times:** Set up to 2 custom notification times (20m-70h)
- **Qualifying open detection:** API-based detection when qualification opens (2-3.5h after race)
- **Race live notifications:** Get notified when race goes live
- **Replay notifications:** Get notified when race replay is available
- **Weather forecast:** Automatic weather data fetch when qualifying opens (Practice/Q1, Q2/Start, race quarters)
- **User control:** "✅ Qualifying Done" button stops notifications for that race

### Personalization
- **Interactive onboarding:** New users select language and group during /start
- **Multi-language support:** Bot UI in 12 languages (English, Russian, Brazilian Portuguese, Italian, Spanish, French, Dutch, Bulgarian, Czech, Hindi, Ukrainian, Portuguese) + 31 languages for GPRO links
- **Website mode toggle:** Switch between Classic GPRO (gpro.net) and APP (app.gpro.net) URLs in settings
- **Group settings:** Personalized race/replay links (set your group in settings)
- **Notification preferences:** Toggle individual notification types on/off
- **Timezone support:** Set your timezone for local time display with automatic DST handling (fuzzy search supports city names, abbreviations, UTC offsets)

### Commands
- `/start` - New users: interactive onboarding; existing users: main menu
- `/status` - Next race with full details, qualifying link, and weather button
- `/calendar` - Full season calendar with all 17 races
- `/next` - Next season calendar (when published)
- `/settings` - Configure language, group, and notification preferences

### Technical
- **API Integration:** Calendar, Office (qualifying detection), Practice (weather)
- **Smart caching:** Weather data cached to minimize API calls
- **Retry logic:** Automatic retry if weather fetch fails
- **Optimized notifications:** Adaptive check intervals based on race proximity
- **Multi-user support:** Persistent user data with atomic writes

## Quick Start

```bash
git clone https://github.com/nyakze/gpro-qualy-reminder-bot.git
cd gpro-qualy-reminder-bot
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Edit .env with TELEGRAM_BOT_TOKEN, GPRO_API_TOKEN, and ADMIN_USER_ID
python bot.py
```

## Documentation

For detailed documentation, see the [Wiki](https://github.com/nyakze/gpro-qualy-reminder-bot/wiki):

- **[User Guide](https://github.com/nyakze/gpro-qualy-reminder-bot/wiki/User-Guide)** - How notifications work, configuring settings, snooze feature, website mode
- **[Self-hosting Guide](https://github.com/nyakze/gpro-qualy-reminder-bot/wiki/Self-hosting-Guide)** - Quick start, tech stack, configuration, deployment, troubleshooting
- **[Development](https://github.com/nyakze/gpro-qualy-reminder-bot/wiki/Development)** - Architecture, adding features, debugging, code style guidelines

## API Integration

Uses GPRO Calendar API:
```
GET https://gpro.net/gb/backend/api/v2/Calendar
```
GPRO office API:
```
GET https://gpro.net/gb/backend/api/v2/office
```
GPRO Practice API:
```
GET https://gpro.net/gb/backend/api/v2/Practice
```



🗄️ Caches results in `gpro_calendar.json`. Requires GPRO API token (.env → GPRO_API_TOKEN)

## Data Attribution

### Timezone Data

This project uses timezone metadata from [Geoapify's Timezone Dataset](https://www.geoapify.com/download-timezones/#download-files), which combines data from multiple open sources:

- **IANA Time Zone Database**: Timezone identifiers and offset rules (Public Domain)
  - *"Unless specified below, all files in the tz code and data (including this LICENSE file) are in the public domain."*

- **Wikipedia**: Timezone textual metadata (Creative Commons BY-SA 3.0 / GFDL)
  - Used for city names and alternative names in multiple languages

The timezone dataset is downloaded via the `/updatetz` admin command and stored in `timezone-info.json`. This file should be committed to the repository for offline functionality.

**Attribution Requirements:**
- ✅ IANA timezone identifiers: Public domain (no attribution required)
- ✅ Wikipedia-derived metadata: CC BY-SA 3.0 / GFDL (attribution provided above)

We do not use OpenStreetMap geographic boundary data (ODbL) from the dataset.

## License
**Unlicense** - Free software, public domain. Use freely! ✨
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

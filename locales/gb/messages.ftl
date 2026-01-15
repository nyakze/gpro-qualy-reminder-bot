# GPRO Bot - English Translations

# =======================
# Commands & General
# =======================
start-welcome-new = 👋 <b>Welcome to GPRO Bot!</b>

    Let's get you set up. First, choose your preferred language for GPRO race links:

    🌍 <b>Select your language</b> (or skip to use English):

start-welcome-existing = 🏁 GPRO Bot LIVE!
    /status - Next race
    /calendar - Full season
    /next - Next season
    /settings - Preferences

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    What would you like to do?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendar
# =======================
no-races-scheduled = 🔔 No races scheduled
no-upcoming-qualifications = 🔔 No upcoming qualifications
next-season-not-published = 🌟 <b>Next season not published yet</b>

calendar-title-full = 🏁 <b>Full Season</b>
calendar-title-next = 🌟 <b>NEXT SEASON</b> ({ $count } races)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 <b>Group Selection</b>

    Choose your GPRO group to get personalized race links:

    Select a common group or enter your own:

onboard-group-custom = 🏁 <b>Group Selection (Optional)</b>

    Enter your group in one of these formats:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Numbers can be 1-3 digits.

    💡 <i>Your GPRO website language has been set to match your bot language. You can change it later in /settings</i>

onboard-complete = ✅ <b>Setup Complete!</b>

    🏁 <b>GPRO Bot is ready!</b>

    <b>Available commands:</b>
    /status - Next race
    /calendar - Full season
    /next - Next season
    /settings - Preferences

    💡 <i>You can change these settings anytime using /settings</i>

onboard-complete-with-group = ✅ <b>Setup Complete!</b>

    Group: <b>{ $group }</b>

    🏁 <b>GPRO Bot is ready!</b>

    <b>Available commands:</b>
    /status - Next race
    /calendar - Full season
    /next - Next season
    /settings - Preferences

# =======================
# Settings
# =======================
settings-title = ⚙️ <b>Settings</b>

    Configure your preferences:

settings-language-title = 🌍 <b>Language Settings</b>

    Current: { $language }

    Select your preferred language for GPRO race links:

ui-lang-menu-title = 💬 <b>Bot Language</b>

    Select bot interface language:

settings-group-title = 🏁 <b>Group Settings</b>

    Current group: <b>{ $group }</b>

    Enter your group in one of these formats:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Numbers can be 1-3 digits.

settings-group-set = ✅ <b>Group set to: { $group }</b>

    Race and replay notifications will include direct links to your group!

settings-notifications-title = 🔔 <b>Notification Settings</b>

    Click to toggle notifications on/off:
    ✅ = Enabled | ❌ = Disabled

    ℹ️ <i>These are global switches for all races. Use the 'Qualifying Done' button in notifications to disable a specific race.</i>

settings-custom-notif-title = ⏱️ <b>Custom Notifications</b>

    Set your own notification times ({ $min }m - { $max }h before qualifying closes).

    You can have up to 2 custom notifications.

    Click a slot to set or edit it.

settings-custom-notif-edit = ⏱️ <b>Custom Notification { $slot }</b>{ $current }

    Select a preset time or enter a custom time:

settings-custom-notif-current = Current:

settings-custom-notif-input = ⏱️ <b>Custom Notification { $slot }</b>

    Enter your custom notification time.

    <b>Accepted formats:</b>
    • <code>20m</code> or <code>45 minutes</code> (20m-70h)
    • <code>2h</code> or <code>12 hours</code>
    • <code>1h 30m</code> or <code>2h30m</code>

    <b>Examples:</b>
    • <code>20m</code> - 20 minutes before
    • <code>6h</code> - 6 hours before
    • <code>1h 30m</code> - 1 hour 30 minutes before

# =======================
# Buttons
# =======================
button-ui-language = 💬 Bot Language: { $language }
button-gpro-language = 🌍 GPRO Language: { $language }
button-language = 🌍 Language: { $language }
button-group = 🏁 Group: { $group }
button-notifications = 🔔 Notifications
button-custom-notifications = ⏱️ Custom Notifications
button-back = ◀ Back
button-back-to-settings = ◀ Back to Settings
button-back-to-notifications = ◀ Back to Notifications
button-back-to-custom = ◀ Back to Custom Notifications
button-back-custom-notif = ◀ Back to Custom Notifications
button-main-menu = 🏠 Main Menu
button-reset-group = 🔄 Reset Group
button-custom-slot-set = ⏱️ Custom { $slot }: { $time }
button-custom-slot-empty = ➕ Set Custom Notification { $slot }
button-previous = ◀ Previous
button-next = Next ▶
button-skip = ⏭️ Skip
button-reset-language = 🔄 Reset to Default (English)
button-enable-all = 🔔 Enable All Notifications
button-disable-all = 🔕 Disable All Notifications
button-enable-category = 🔔 Enable Category
button-disable-category = 🔕 Disable Category
button-quali-done = ✅ Qualifying Done
button-reenable-race = 🔄 Re-enable Race { $raceId } notifications
button-weather = 🌤️ Show Weather
button-enter-custom-group = ✏️ Enter Custom Group
button-enter-custom-time = ✏️ Enter Custom Time
button-disable-notification = 🔕 Disable This Notification
button-cancel = ❌ Cancel
button-got-it = ✅ Got it!
button-try-again = 🔄 Try Again

button-main-menu-status = 📊 Next Race
button-main-menu-calendar = 📅 Full Season
button-main-menu-next = 🌟 Next Season
button-main-menu-settings = ⚙️ Settings

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Set Custom Notification { $slot }
button-custom-notif-time = ⏱️ Custom { $slot }: { $time }

# =======================
# Notifications
# =======================
# Notification categories
notif-category-before-qualifying = Before Qualifying
notif-category-qualifying-events = Qualifying Events
notif-category-race-events = Race Events

# Individual notification labels
notif-label-72h = 3d before qualifying closes
notif-label-48h = 2d before qualifying closes
notif-label-24h = 1d before qualifying closes
notif-label-2h = 2h before qualifying closes
notif-label-10min = 10min before qualifying closes
notif-label-opens = Qualifying is open
notif-label-quali-results = Qualifying results available
notif-label-replay = Race replay available
notif-label-live = Race is live
notif-label-results = Race results available

notif-quali-closes = <b>Qualifying closes in { $time }!</b>
notif-quali-opens = <b>Qualifying is open</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifying deadline: { $qualiDeadline }</b>
    🏎 <b>Race: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Go to Qualifying</a>

    <i>Click the '✅ Qualifying Done' button to disable notifications for this race</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifying deadline: { $qualiDeadline }</b>
    🏎 <b>Race: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Go to Qualifying</a>

    ℹ️ <b>Automatic notifications disabled</b> for this race
    <i>Click the '🔄 Re-enable' button to re-enable notifications</i>

notif-quali-closed-title = <b>Qualifying is currently closed</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Qualifying closed: { $qualiDeadline }</b>
    🏎 <b>Race: { $raceTime }</b>

    ⏳ <i>Qualifying is currently closed. The next qualifying session will open after the current race is complete. Please wait for the race to be calculated.</i>

notif-race-live = 🏁 <b>Race #{ $raceId } is LIVE!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Watch Live Race</a>

notif-race-live-no-group = 🏁 <b>Race #{ $raceId } is LIVE!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Set your group in /settings for a direct link!

    🔗 <a href="{ $raceLink }">Watch Live Race</a>

notif-race-replay = 📺 <b>Race #{ $raceId } Replay Available</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Watch the race replay:

    🔗 <a href="{ $replayLink }">Watch Replay</a>

notif-race-replay-no-group = 📺 <b>Race #{ $raceId } Replay Available</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Watch the race replay:

    ⚠️ For personalized links, set your group in /settings!

    🔗 <a href="{ $replayLink }">Watch Replay</a>

notif-race-results = 📊 <b>Race #{ $raceId } Results Available</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Race results are now available:

    🔗 <a href="{ $analysisLink }">Race Analysis</a>
    🔗 <a href="{ $summaryLink }">Race Summary</a>

notif-race-results-no-group = 📊 <b>Race #{ $raceId } Results Available</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Race results are now available:

    🔗 <a href="{ $analysisLink }">Race Analysis</a>

    ⚠️ For personalized Race Summary, set your group in /settings!

notif-quali-results = 🏁 <b>Race #{ $raceId } Qualifying Results</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifying closed</b>
    🏎 <b>Race: { $raceTime }</b>

    Qualifying results are now available:

    🔗 <a href="{ $gridLink }">Starting Grid</a>

notif-quali-results-no-group = 🏁 <b>Race #{ $raceId } Qualifying Results</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifying closed</b>
    🏎 <b>Race: { $raceTime }</b>

    Qualifying results are now available:

    ⚠️ For personalized links, set your group in /settings!

    🔗 <a href="{ $gridLink }">Starting Grid</a>

# =======================
# New Season Reminder
# =======================
notif-category-season-prep = Season Preparation

notif-label-new-season-reminder = New season reminder

notif-new-season-reminder = 🌟 <b>New Season Starting!</b>

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Race: { $raceTime }</b>

    Your current group: <b>{ $group }</b>

    💡 If you've moved to a different group, please update it in /settings to receive personalized links!

notif-new-season-reminder-no-group = 🌟 <b>New Season Starting!</b>

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Race: { $raceTime }</b>

    ⚠️ You haven't set your group yet!

    💡 Set your group in /settings to receive personalized race links!

# =======================
# Weather
# =======================
weather-title = 🌤️ <b>Race Weather Forecast</b>
weather-practice-q1 = <b>Practice / Qualify 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Humidity: { $hum }%
weather-q2-start = <b>Qualify 2 / Race Start:</b> { $weather }
weather-race-conditions = <b>Race Conditions:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Humidity: { $hum }
    Rain probability: { $rain }
weather-not-available = ⚠️ Weather data not available
weather-cached = ℹ️ Weather already cached for <b>Race #{ $raceId }: { $track }</b>

    Use <code>/weather force</code> to force update.
    Use /status to see the notification with weather button.
weather-fetching = 🔄 Fetching weather for <b>Race #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Force updating weather for <b>Race #{ $raceId }: { $track }</b>...
weather-success = ✅ Weather data fetched for <b>Race #{ $raceId }: { $track }</b>

    Use /status to test the notification with weather button!
weather-failed = ❌ Failed to fetch weather data

    Check if GPRO API token is valid and Practice API is available.

# =======================
# Admin
# =======================
admin-only = ❌ Admin only
admin-calendar-updated = ✅ <b>Calendar</b>: { $count } races
    🔄 <b>{ $userCount } users</b> reset
admin-next-season-ready = 🌟 <b>Next season ready!</b> { $count } races
    Use /next to view
admin-next-season-not-published = ℹ️ <b>Next season not published</b>
admin-users-count = 📊 <b>{ $count } users</b>:
admin-users-none = 📊 <b>0 users</b> in database
admin-no-races = ❌ No races in calendar
admin-no-upcoming-races = ❌ No upcoming races found

# =======================
# Errors & Validation
# =======================
error-invalid-format = ❌ Invalid format!

    Please use:
    • <b>E</b> for Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Try again:

error-invalid-format-onboarding = ❌ Invalid format!

    Please use:
    • <b>E</b> for Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Try again or use /start to restart:

error-invalid-time = ❌ <b>Error:</b> { $error }

    Please try again with a valid format like: <code>2h</code>, <code>30m</code>, or <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Error:</b> { $error }

    Please try again.

error-invalid-race = ❌ Invalid race ID
error-invalid-page = ❌ Invalid page
error-invalid-language = ❌ Invalid language
error-invalid-category = ❌ Invalid category
error-invalid-slot = ❌ Invalid slot
error-invalid-data = ❌ Invalid data
error-reset-failed = ❌ Reset failed
error-race-not-found = ❌ Race not found
error-weather-not-available = ⚠️ Weather data not available yet
error-weather-send-failed = ❌ Failed to send weather

# =======================
# Feedback & Confirmations
# =======================
feedback-all-enabled = ✅ All notifications enabled!
feedback-all-disabled = ✅ All notifications disabled!
feedback-category-enabled = ✅ { $category } enabled!
feedback-category-disabled = ✅ { $category } disabled!
feedback-notif-enabled = ✅ { $label } enabled!
feedback-notif-disabled = ✅ { $label } disabled!
feedback-quali-done = ✅ Done!
feedback-race-marked-done = ✅ <i>Race marked done!</i>
feedback-reset = 🔄 Reset!
feedback-notifications-reset = 🔄 <i>Notifications reset!</i>
feedback-reenabled = 🔄 Re-enabled!
feedback-notifications-reenabled = 🔄 <i>Notifications re-enabled!</i>
feedback-language-set = ✅ Language set to { $language }
feedback-language-reset = ✅ Language reset to English
feedback-ui-language-set = ✅ Bot language set to { $language }
feedback-group-set = ✅ Group set to { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Custom notification { $slot } disabled
feedback-skip-language = ⏭️ Using default language (English)
feedback-skip-group = ⏭️ Skipped group selection
feedback-welcome = ✅ Welcome aboard!
feedback-weather-sent = 🌤️ Weather forecast sent!

# =======================
# Time Formatting
# =======================
# Weekday abbreviations (2-letter)
weekday-mon = Mo
weekday-tue = Tu
weekday-wed = We
weekday-thu = Th
weekday-fri = Fr
weekday-sat = Sa
weekday-sun = Su

time-minutes = { $minutes ->
    [one] { $minutes } minute
   *[other] { $minutes } minutes
}
time-hours = { $hours ->
    [one] { $hours } hour
   *[other] { $hours } hours
}
time-hours-minutes = { $hours ->
    [one] { $hours } hour
   *[other] { $hours } hours
} { $minutes ->
    [one] { $minutes } minute
   *[other] { $minutes } minutes
}
time-hours-minutes-short = { $hours }h{ $minutes }m
time-hours-short = { $hours }h
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }d{ $hours }h
time-days-hours-minutes-short = { $days }d{ $hours }h{ $minutes }m
time-days = { $days ->
    [one] { $days } day
   *[other] { $days } days
}
time-days-hours = { $days ->
    [one] { $days } day
   *[other] { $days } days
} { $hours ->
    [one] { $hours } hour
   *[other] { $hours } hours
}
time-months = { $months ->
    [one] { $months } month
   *[other] { $months } months
}
time-months-days = { $months ->
    [one] { $months } month
   *[other] { $months } months
} { $days ->
    [one] { $days } day
   *[other] { $days } days
}

# =======================
# Group Display
# =======================
group-not-set = Not set
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Custom Notification Messages
# =======================
custom-notif-set = Custom notification { $slot } set to { $time }
custom-notif-set-success = Custom notification { $slot } set to { $time }
custom-notif-not-set = Not set
custom-notif-min-error = Minimum time is 20 minutes
custom-notif-max-error = Maximum time is 70 hours
custom-notif-invalid-slot = Invalid slot (must be 0-{ $max })
custom-notif-empty-error = Time cannot be empty
custom-notif-invalid-format = Invalid format. Use: 2h, 30m, or 1h 30m
custom-notif-enter-time = Please enter a time
custom-notif-error-parsing = ❌ <b>Error:</b> { $error }

    Please try again with a valid format like: <code>2h</code>, <code>30m</code>, or <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Your custom notification has been set!
custom-notif-error-setting = ❌ <b>Error:</b> { $error }

    Please try again.

# =======================
# Validation
# =======================
validation-time-empty = Time cannot be empty
validation-time-min = Minimum time is 20 minutes
validation-time-max = Maximum time is 70 hours
validation-enter-time = Please enter a time
validation-invalid-format = Invalid format. Use: 2h, 30m, or 1h 30m
validation-invalid-slot = Invalid slot (must be 0-{ $maxSlots })

# =======================
# Notification Labels
# =======================
notif-label-72h = 3d before qualifying closes
notif-label-48h = 2d before qualifying closes
notif-label-24h = 1d before qualifying closes
notif-label-2h = 2h before qualifying closes
notif-label-10min = 10min before qualifying closes
notif-label-opens-soon = Qualifying is open
notif-label-quali-results = Qualifying results available
notif-label-race-replay = Race replay available
notif-label-race-live = Race is live
notif-label-race-results = Race results available

# =======================
# Notification Menu
# =======================
notif-menu-title = 🔔 <b>Notification Settings</b>

    Click to toggle notifications on/off:
    ✅ = Enabled | ❌ = Disabled

    ℹ️ <i>These are global switches for all races. Use the 'Qualifying Done' button in notifications to disable a specific race.</i>

# =======================
# Group Menu
# =======================
group-menu-title = 🏁 <b>Group Settings</b>

    Current group: <b>{ $groupDisplay }</b>

    Enter your group in one of these formats:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Numbers can be 1-3 digits.
group-reset-success = ✅ Group reset successfully

# =======================
# Language Menu
# =======================
lang-menu-title = 🌍 <b>Language Settings</b>

    Current: { $currentLang }

    Select your preferred language for GPRO race links:

# =======================
# Custom Notification Menu
# =======================
custom-notif-menu-title = ⏱️ <b>Custom Notifications</b>

    Set your own notification times ({ $minTime }m - { $maxTime }h before qualifying closes).

    You can have up to 2 custom notifications.

    Click a slot to set or edit it.

# =======================
# Weather
# =======================
weather-unavailable = ⚠️ Weather data not available
weather-title = 🌤️ <b>Race Weather Forecast</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Practice / Qualify 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Humidity: { $hum }%
weather-q2-race-start = <b>Qualify 2 / Race Start:</b> { $weather }
weather-race-conditions = <b>Race Conditions:</b>
weather-start-0h30m = <b>Start - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Temp: { $temp } • Humidity: { $hum }
weather-rain-prob = Rain probability: { $rain }

# Weather Conditions
weather-condition-sunny = Sunny
weather-condition-partially-cloudy = Partially Cloudy
weather-condition-cloudy = Cloudy
weather-condition-very-cloudy = Very Cloudy
weather-condition-rain = Rain

# =======================
# Timezone Settings
# =======================
button-timezone = ⏰ Timezone: { $timezone }
button-website-mode = 🌐 Link type: { $mode }
website-mode-classic = Classic
timezone-menu-title = ⏰ <b>Timezone Settings</b>

    Current timezone: <b>{ $timezone }</b>

    Type your timezone (city name, abbreviation, or UTC offset):

    Examples: <code>New York</code>, <code>PST</code>, <code>UTC+3</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Select your timezone:</b>

    Matches for "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Select your timezone:</b>

    Matches for "{ $query }" (Page { $page }/{ $total }):

timezone-set-success = ✅ <b>Timezone set!</b>

    { $timezone }

    Current time in your timezone: <b>{ $localTime }</b>

    All race times will now be shown in your local time.

button-reset-timezone = 🔄 Reset to UTC
feedback-timezone-set = ✅ Timezone updated
feedback-timezone-reset = ✅ Timezone reset to UTC
feedback-switched-to-app = APP mode enabled
feedback-switched-to-classic = Classic mode enabled
error-mode-switch-failed = ❌ Failed to switch website mode
error-timezone-not-found = ❌ No timezone found for "{ $query }"

    Try: city name (New York), abbreviation (PST), or UTC offset (UTC+3)
error-invalid-timezone = ❌ Invalid timezone

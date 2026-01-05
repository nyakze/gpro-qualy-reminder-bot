# GPRO Bot - Nederlandse Vertalingen

# =======================
# Commands & General
# =======================
start-welcome-new = 👋 <b>Welkom bij GPRO Bot!</b>

    Laten we je instellen. Kies eerst je voorkeurstaal voor GPRO race links:

    🌍 <b>Selecteer je taal</b> (of sla over om Engels te gebruiken):

start-welcome-existing = 🏁 GPRO Bot LIVE!
    /status - Volgende race
    /calendar - Volledig seizoen
    /next - Volgend seizoen
    /settings - Voorkeuren

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Wat wil je doen?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendar
# =======================
no-races-scheduled = 🔔 Geen races ingepland
no-upcoming-qualifications = 🔔 Geen aankomende kwalificaties
next-season-not-published = 🌟 <b>Volgend seizoen nog niet gepubliceerd</b>

calendar-title-full = 🏁 <b>Volledig Seizoen</b>
calendar-title-next = 🌟 <b>VOLGEND SEIZOEN</b> ({ $count } races)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 <b>Groep Selectie</b>

    Kies je GPRO groep om gepersonaliseerde race links te krijgen:

    Selecteer een veelvoorkomende groep of voer je eigen groep in:

onboard-group-custom = 🏁 <b>Groep Selectie (Optioneel)</b>

    Voer je groep in in een van deze formaten:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Nummers kunnen 1-3 cijfers zijn.

    💡 <i>Je GPRO website taal is ingesteld om overeen te komen met je bot taal. Je kunt dit later wijzigen in /settings</i>

onboard-complete = ✅ <b>Installatie Voltooid!</b>

    🏁 <b>GPRO Bot is klaar!</b>

    <b>Beschikbare commando's:</b>
    /status - Volgende race
    /calendar - Volledig seizoen
    /next - Volgend seizoen
    /settings - Voorkeuren

    💡 <i>Je kunt deze instellingen altijd wijzigen via /settings</i>

onboard-complete-with-group = ✅ <b>Installatie Voltooid!</b>

    Groep: <b>{ $group }</b>

    🏁 <b>GPRO Bot is klaar!</b>

    <b>Beschikbare commando's:</b>
    /status - Volgende race
    /calendar - Volledig seizoen
    /next - Volgend seizoen
    /settings - Voorkeuren

# =======================
# Settings
# =======================
settings-title = ⚙️ <b>Instellingen</b>

    Configureer je voorkeuren:

settings-language-title = 🌍 <b>Taalinstellingen</b>

    Huidig: { $language }

    Selecteer je voorkeurstaal voor GPRO race links:

ui-lang-menu-title = 💬 <b>Bot Taal</b>

    Selecteer interface taal van de bot:

settings-group-title = 🏁 <b>Groep Instellingen</b>

    Huidige groep: <b>{ $group }</b>

    Voer je groep in in een van deze formaten:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Nummers kunnen 1-3 cijfers zijn.

settings-group-set = ✅ <b>Groep ingesteld op: { $group }</b>

    Race en replay notificaties zullen directe links naar je groep bevatten!

settings-notifications-title = 🔔 <b>Notificatie Instellingen</b>

    Klik om notificaties aan/uit te zetten:
    ✅ = Ingeschakeld | ❌ = Uitgeschakeld

    ℹ️ <i>Dit zijn globale schakelaars voor alle races. Gebruik de '✅ Kwal Klaar' knop in notificaties om een specifieke race uit te schakelen.</i>

settings-custom-notif-title = ⏱️ <b>Aangepaste Notificaties</b>

    Stel je eigen notificatietijden in ({ $min }m - { $max }u voor sluiting kwalificatie).

    Je kunt maximaal 2 aangepaste notificaties hebben.

    Klik op een slot om deze in te stellen of te bewerken.

settings-custom-notif-edit = ⏱️ <b>Aangepaste Notificatie { $slot }</b>{ $current }

    Selecteer een vooraf ingestelde tijd of voer een aangepaste tijd in:

settings-custom-notif-current = Huidig:

settings-custom-notif-input = ⏱️ <b>Aangepaste Notificatie { $slot }</b>

    Voer je aangepaste notificatietijd in.

    <b>Geaccepteerde formaten:</b>
    • <code>20m</code> of <code>45 minuten</code> (20m-70u)
    • <code>2u</code> of <code>12 uur</code>
    • <code>1u 30m</code> of <code>2u30m</code>

    <b>Voorbeelden:</b>
    • <code>20m</code> - 20 minuten van tevoren
    • <code>6u</code> - 6 uur van tevoren
    • <code>1u 30m</code> - 1 uur en 30 minuten van tevoren

# =======================
# Buttons
# =======================
button-ui-language = 💬 Bot Taal: { $language }
button-gpro-language = 🌍 GPRO Taal: { $language }
button-language = 🌍 Taal: { $language }
button-group = 🏁 Groep: { $group }
button-notifications = 🔔 Notificaties
button-custom-notifications = ⏱️ Aangepaste Notificaties
button-back = ◀ Terug
button-back-to-settings = ◀ Terug naar Instellingen
button-back-to-notifications = ◀ Terug naar Notificaties
button-back-to-custom = ◀ Terug naar Aangepaste Notificaties
button-back-custom-notif = ◀ Terug naar Aangepaste Notificaties
button-main-menu = 🏠 Hoofdmenu
button-reset-group = 🔄 Reset Groep
button-custom-slot-set = ⏱️ Aangepast { $slot }: { $time }
button-custom-slot-empty = ➕ Stel Aangepaste Notificatie { $slot } in
button-previous = ◀ Vorige
button-next = Volgende ▶
button-skip = ⏭️ Overslaan
button-reset-language = 🔄 Reset naar Standaard (Engels)
button-enable-all = 🔔 Alle Notificaties Inschakelen
button-disable-all = 🔕 Alle Notificaties Uitschakelen
button-quali-done = ✅ Kwal Klaar
button-reenable-race = 🔄 Race { $raceId } notificaties opnieuw inschakelen
button-weather = 🌤️ Toon Weer
button-enter-custom-group = ✏️ Voer Aangepaste Groep in
button-enter-custom-time = ✏️ Voer Aangepaste Tijd in
button-disable-notification = 🔕 Schakel Deze Notificatie Uit
button-cancel = ❌ Annuleren
button-got-it = ✅ Begrepen!
button-try-again = 🔄 Probeer Opnieuw

button-main-menu-status = 📊 Volgende Race
button-main-menu-calendar = 📅 Volledig Seizoen
button-main-menu-next = 🌟 Volgend Seizoen
button-main-menu-settings = ⚙️ Instellingen

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Stel Aangepaste Notificatie { $slot } in
button-custom-notif-time = ⏱️ Aangepast { $slot }: { $time }

# =======================
# Notifications
# =======================
notif-label-72h = 3d voor sluiting kwalificatie
notif-label-48h = 2d voor sluiting kwalificatie
notif-label-24h = 1d voor sluiting kwalificatie
notif-label-2h = 2u voor sluiting kwalificatie
notif-label-10min = 10min voor sluiting kwalificatie
notif-label-opens = Kwalificatie is open
notif-label-replay = Race replay beschikbaar
notif-label-live = Race is live
notif-label-results = Race resultaten beschikbaar

notif-quali-closes = <b>Kwalificatie sluit over { $time }!</b>
notif-quali-opens = <b>Kwalificatie is open (of gaat binnenkort open)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Kwalificatie deadline: { $qualiDeadline }</b>
    🏎 <b>Race: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ga naar Kwalificatie</a>

    <i>Klik op de '✅ Kwal Klaar' knop om notificaties voor deze race uit te schakelen</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Race #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Kwalificatie deadline: { $qualiDeadline }</b>
    🏎 <b>Race: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ga naar Kwalificatie</a>

    ℹ️ <b>Automatische notificaties uitgeschakeld</b> voor deze race
    <i>Klik op de '🔄 Opnieuw inschakelen' knop om notificaties opnieuw in te schakelen</i>

notif-race-live = 🏁 <b>Race #{ $raceId } is LIVE!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Bekijk Live Race</a>

notif-race-live-no-group = 🏁 <b>Race #{ $raceId } is LIVE!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Stel je groep in via /settings voor een directe link!

    🔗 <a href="{ $raceLink }">Bekijk Live Race</a>

notif-race-replay = 📺 <b>Race #{ $raceId } Replay Beschikbaar</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Als de race al is berekend, is de replay hier beschikbaar:

    🔗 <a href="{ $replayLink }">Bekijk Replay</a>

notif-race-replay-no-group = 📺 <b>Race #{ $raceId } Replay Beschikbaar</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Als de race al is berekend, is de replay hier beschikbaar:

    ⚠️ Voor gepersonaliseerde links, stel je groep in via /settings!

    🔗 <a href="{ $replayLink }">Bekijk Replay</a>

notif-race-results = 📊 <b>Race #{ $raceId } Resultaten Beschikbaar</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Race resultaten zijn nu beschikbaar:

    🔗 <a href="{ $analysisLink }">Race Analyse</a>
    🔗 <a href="{ $summaryLink }">Race Samenvatting</a>

notif-race-results-no-group = 📊 <b>Race #{ $raceId } Resultaten Beschikbaar</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Race resultaten zijn nu beschikbaar:

    🔗 <a href="{ $analysisLink }">Race Analyse</a>

    ⚠️ Voor gepersonaliseerde Race Samenvatting, stel je groep in via /settings!

# =======================
# Weather
# =======================
weather-title = 🌤️ <b>Race Weer Voorspelling</b>
weather-practice-q1 = <b>Training / Kwalificatie 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Luchtvochtigheid: { $hum }%
weather-q2-start = <b>Kwalificatie 2 / Race Start:</b> { $weather }
weather-race-conditions = <b>Race Omstandigheden:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Luchtvochtigheid: { $hum }
    Regen kans: { $rain }
weather-not-available = ⚠️ Weergegevens niet beschikbaar
weather-cached = ℹ️ Weer al in cache voor <b>Race #{ $raceId }: { $track }</b>

    Gebruik <code>/weather force</code> om geforceerd bij te werken.
    Gebruik /status om de notificatie met weer knop te zien.
weather-fetching = 🔄 Weer ophalen voor <b>Race #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Geforceerd bijwerken weer voor <b>Race #{ $raceId }: { $track }</b>...
weather-success = ✅ Weergegevens opgehaald voor <b>Race #{ $raceId }: { $track }</b>

    Gebruik /status om de notificatie met weer knop te testen!
weather-failed = ❌ Ophalen weergegevens mislukt

    Controleer of GPRO API token geldig is en Practice API beschikbaar is.

# =======================
# Admin
# =======================
admin-only = ❌ Alleen admin
admin-calendar-updated = ✅ <b>Kalender</b>: { $count } races
    🔄 <b>{ $userCount } gebruikers</b> gereset
admin-next-season-ready = 🌟 <b>Volgend seizoen klaar!</b> { $count } races
    Gebruik /next om te bekijken
admin-next-season-not-published = ℹ️ <b>Volgend seizoen niet gepubliceerd</b>
admin-users-count = 📊 <b>{ $count } gebruikers</b>:
admin-users-none = 📊 <b>0 gebruikers</b> in database
admin-no-races = ❌ Geen races in kalender
admin-no-upcoming-races = ❌ Geen aankomende races gevonden

# =======================
# Errors & Validation
# =======================
error-invalid-format = ❌ Ongeldig formaat!

    Gebruik alsjeblieft:
    • <b>E</b> voor Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Probeer opnieuw:

error-invalid-format-onboarding = ❌ Ongeldig formaat!

    Gebruik alsjeblieft:
    • <b>E</b> voor Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Probeer opnieuw of gebruik /start om opnieuw te beginnen:

error-invalid-time = ❌ <b>Fout:</b> { $error }

    Probeer het alsjeblieft opnieuw met een geldig formaat zoals: <code>2u</code>, <code>30m</code>, of <code>1u 30m</code>

error-custom-notif-failed = ❌ <b>Fout:</b> { $error }

    Probeer het alsjeblieft opnieuw.

error-invalid-race = ❌ Ongeldig race ID
error-invalid-page = ❌ Ongeldige pagina
error-invalid-language = ❌ Ongeldige taal
error-invalid-slot = ❌ Ongeldig slot
error-invalid-data = ❌ Ongeldige gegevens
error-reset-failed = ❌ Reset mislukt
error-race-not-found = ❌ Race niet gevonden
error-weather-not-available = ⚠️ Weergegevens nog niet beschikbaar
error-weather-send-failed = ❌ Verzenden weer mislukt

# =======================
# Feedback & Confirmations
# =======================
feedback-all-enabled = ✅ Alle notificaties ingeschakeld!
feedback-all-disabled = ✅ Alle notificaties uitgeschakeld!
feedback-notif-enabled = ✅ { $label } ingeschakeld!
feedback-notif-disabled = ✅ { $label } uitgeschakeld!
feedback-quali-done = ✅ Klaar!
feedback-race-marked-done = ✅ <i>Race gemarkeerd als klaar!</i>
feedback-reset = 🔄 Reset!
feedback-notifications-reset = 🔄 <i>Notificaties gereset!</i>
feedback-reenabled = 🔄 Opnieuw ingeschakeld!
feedback-notifications-reenabled = 🔄 <i>Notificaties opnieuw ingeschakeld!</i>
feedback-language-set = ✅ Taal ingesteld op { $language }
feedback-language-reset = ✅ Taal gereset naar Engels
feedback-ui-language-set = ✅ Bot taal ingesteld op { $language }
feedback-group-set = ✅ Groep ingesteld op { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Aangepaste notificatie { $slot } uitgeschakeld
feedback-skip-language = ⏭️ Standaard taal gebruiken (Engels)
feedback-skip-group = ⏭️ Groep selectie overgeslagen
feedback-welcome = ✅ Welkom aan boord!
feedback-weather-sent = 🌤️ Weersverwachting verzonden!

# =======================
# Time Formatting
# =======================
# Weekday abbreviations (2-letter)
weekday-mon = Ma
weekday-tue = Di
weekday-wed = Wo
weekday-thu = Do
weekday-fri = Vr
weekday-sat = Za
weekday-sun = Zo

time-minutes = { $minutes ->
    [one] { $minutes } minuut
   *[other] { $minutes } minuten
}
time-hours = { $hours ->
    [one] { $hours } uur
   *[other] { $hours } uur
}
time-hours-minutes = { $hours ->
    [one] { $hours } uur
   *[other] { $hours } uur
} { $minutes ->
    [one] { $minutes } minuut
   *[other] { $minutes } minuten
}
time-hours-minutes-short = { $hours }u{ $minutes }m
time-hours-short = { $hours }u
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }d{ $hours }u
time-days-hours-minutes-short = { $days }d{ $hours }u{ $minutes }m
time-days = { $days ->
    [one] { $days } dag
   *[other] { $days } dagen
}
time-days-hours = { $days ->
    [one] { $days } dag
   *[other] { $days } dagen
} { $hours ->
    [one] { $hours } uur
   *[other] { $hours } uur
}
time-months = { $months ->
    [one] { $months } maand
   *[other] { $months } maanden
}
time-months-days = { $months ->
    [one] { $months } maand
   *[other] { $months } maanden
} { $days ->
    [one] { $days } dag
   *[other] { $days } dagen
}

# =======================
# Group Display
# =======================
group-not-set = Niet ingesteld
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Custom Notification Messages
# =======================
custom-notif-set = Aangepaste notificatie { $slot } ingesteld op { $time }
custom-notif-set-success = Aangepaste notificatie { $slot } ingesteld op { $time }
custom-notif-not-set = Niet ingesteld
custom-notif-min-error = Minimum tijd is 20 minuten
custom-notif-max-error = Maximum tijd is 70 uur
custom-notif-invalid-slot = Ongeldig slot (moet 0-{ $max } zijn)
custom-notif-empty-error = Tijd kan niet leeg zijn
custom-notif-invalid-format = Ongeldig formaat. Gebruik: 2u, 30m, of 1u 30m
custom-notif-enter-time = Voer alsjeblieft een tijd in
custom-notif-error-parsing = ❌ <b>Fout:</b> { $error }

    Probeer het alsjeblieft opnieuw met een geldig formaat zoals: <code>2u</code>, <code>30m</code>, of <code>1u 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Je aangepaste notificatie is ingesteld!
custom-notif-error-setting = ❌ <b>Fout:</b> { $error }

    Probeer het alsjeblieft opnieuw.

# =======================
# Validation
# =======================
validation-time-empty = Tijd kan niet leeg zijn
validation-time-min = Minimum tijd is 20 minuten
validation-time-max = Maximum tijd is 70 uur
validation-enter-time = Voer alsjeblieft een tijd in
validation-invalid-format = Ongeldig formaat. Gebruik: 2u, 30m, of 1u 30m
validation-invalid-slot = Ongeldig slot (moet 0-{ $maxSlots } zijn)

# =======================
# Notification Labels
# =======================
notif-label-72h = 3d voor sluiting kwalificatie
notif-label-48h = 2d voor sluiting kwalificatie
notif-label-24h = 1d voor sluiting kwalificatie
notif-label-2h = 2u voor sluiting kwalificatie
notif-label-10min = 10min voor sluiting kwalificatie
notif-label-opens-soon = Kwalificatie is open
notif-label-race-replay = Race replay beschikbaar
notif-label-race-live = Race is live
notif-label-race-results = Race resultaten beschikbaar

# =======================
# Notification Menu
# =======================
notif-menu-title = 🔔 <b>Notificatie Instellingen</b>

    Klik om notificaties aan/uit te zetten:
    ✅ = Ingeschakeld | ❌ = Uitgeschakeld

    ℹ️ <i>Dit zijn globale schakelaars voor alle races. Gebruik de '✅ Kwal Klaar' knop in notificaties om een specifieke race uit te schakelen.</i>

# =======================
# Group Menu
# =======================
group-menu-title = 🏁 <b>Groep Instellingen</b>

    Huidige groep: <b>{ $groupDisplay }</b>

    Voer je groep in in een van deze formaten:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Nummers kunnen 1-3 cijfers zijn.
group-reset-success = ✅ Groep succesvol gereset

# =======================
# Language Menu
# =======================
lang-menu-title = 🌍 <b>Taalinstellingen</b>

    Huidig: { $currentLang }

    Selecteer je voorkeurstaal voor GPRO race links:

# =======================
# Custom Notification Menu
# =======================
custom-notif-menu-title = ⏱️ <b>Aangepaste Notificaties</b>

    Stel je eigen notificatietijden in ({ $minTime }m - { $maxTime }u voor sluiting kwalificatie).

    Je kunt maximaal 2 aangepaste notificaties hebben.

    Klik op een slot om deze in te stellen of te bewerken.

# =======================
# Weather
# =======================
weather-unavailable = ⚠️ Weergegevens niet beschikbaar
weather-title = 🌤️ <b>Race Weer Voorspelling</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Training / Kwalificatie 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Luchtvochtigheid: { $hum }%
weather-q2-race-start = <b>Kwalificatie 2 / Race Start:</b> { $weather }
weather-race-conditions = <b>Race Omstandigheden:</b>
weather-start-0h30m = <b>Start - 0u30m:</b>
weather-0h30m-1h00m = <b>0u30m - 1u00m:</b>
weather-1h00m-1h30m = <b>1u00m - 1u30m:</b>
weather-1h30m-2h00m = <b>1u30m - 2u00m:</b>
weather-temp-hum-range = Temp: { $temp } • Luchtvochtigheid: { $hum }
weather-rain-prob = Regen kans: { $rain }

# Weather Conditions
weather-condition-sunny = Zonnig
weather-condition-partially-cloudy = Gedeeltelijk Bewolkt
weather-condition-cloudy = Bewolkt
weather-condition-very-cloudy = Zwaar Bewolkt
weather-condition-rain = Regen

# =======================
# Timezone Settings
# =======================
button-timezone = ⏰ Tijdzone: { $timezone }
timezone-menu-title = ⏰ <b>Tijdzone Instellingen</b>

    Huidige tijdzone: <b>{ $timezone }</b>

    Typ je tijdzone (stadsnaam, afkorting, of UTC offset):

    Voorbeelden: <code>Amsterdam</code>, <code>CET</code>, <code>UTC+1</code>, <code>Brussel</code>

timezone-select-matches = 🌍 <b>Selecteer je tijdzone:</b>

    Overeenkomsten voor "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Selecteer je tijdzone:</b>

    Overeenkomsten voor "{ $query }" (Pagina { $page }/{ $total }):

timezone-set-success = ✅ <b>Tijdzone ingesteld!</b>

    { $timezone }

    Huidige tijd in jouw tijdzone: <b>{ $localTime }</b>

    Alle race tijden worden nu in jouw lokale tijd weergegeven.

button-reset-timezone = 🔄 Reset naar UTC
feedback-timezone-set = ✅ Tijdzone bijgewerkt
feedback-timezone-reset = ✅ Tijdzone gereset naar UTC
error-timezone-not-found = ❌ Geen tijdzone gevonden voor "{ $query }"

    Probeer: stadsnaam (Amsterdam), afkorting (CET), of UTC offset (UTC+1)
error-invalid-timezone = ❌ Ongeldige tijdzone

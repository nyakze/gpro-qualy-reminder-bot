# GPRO Bot - Czech Translations

# =======================
# Commands & General
# =======================
start-welcome-new = 👋 <b>Vítejte v GPRO Botu!</b>

    Pojďme vás nastavit. Nejprve si zvolte preferovaný jazyk pro odkazy na GPRO závody:

    🌍 <b>Vyberte svůj jazyk</b> (nebo přeskočte a použijte angličtinu):

start-welcome-existing = 🏁 GPRO Bot AKTIVNÍ!
    /status - Příští závod
    /calendar - Celá sezóna
    /next - Příští sezóna
    /settings - Nastavení

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Co byste chtěli udělat?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendar
# =======================
no-races-scheduled = 🔔 Žádné závody nejsou naplánovány
no-upcoming-qualifications = 🔔 Žádné nadcházející kvalifikace
next-season-not-published = 🌟 <b>Příští sezóna ještě nebyla zveřejněna</b>

calendar-title-full = 🏁 <b>Celá sezóna</b>
calendar-title-next = 🌟 <b>PŘÍŠTÍ SEZÓNA</b> ({ $count } závodů)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 <b>Výběr skupiny</b>

    Vyberte svou GPRO skupinu pro personalizované odkazy na závody:

    Vyberte běžnou skupinu nebo zadejte vlastní:

onboard-group-custom = 🏁 <b>Výběr skupiny (volitelné)</b>

    Zadejte svou skupinu v jednom z těchto formátů:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Čísla mohou být 1-3místná.

    💡 <i>Váš jazyk GPRO webu byl nastaven podle jazyka botu. Můžete jej později změnit v /settings</i>

onboard-complete = ✅ <b>Nastavení dokončeno!</b>

    🏁 <b>GPRO Bot je připraven!</b>

    <b>Dostupné příkazy:</b>
    /status - Příští závod
    /calendar - Celá sezóna
    /next - Příští sezóna
    /settings - Nastavení

    💡 <i>Tato nastavení můžete kdykoli změnit pomocí /settings</i>

onboard-complete-with-group = ✅ <b>Nastavení dokončeno!</b>

    Skupina: <b>{ $group }</b>

    🏁 <b>GPRO Bot je připraven!</b>

    <b>Dostupné příkazy:</b>
    /status - Příští závod
    /calendar - Celá sezóna
    /next - Příští sezóna
    /settings - Nastavení

# =======================
# Settings
# =======================
settings-title = ⚙️ <b>Nastavení</b>

    Nastavte své preference:

settings-language-title = 🌍 <b>Nastavení jazyka</b>

    Aktuální: { $language }

    Vyberte svůj preferovaný jazyk pro odkazy na GPRO závody:

ui-lang-menu-title = 💬 <b>Jazyk botu</b>

    Vyberte jazyk rozhraní botu:

settings-group-title = 🏁 <b>Nastavení skupiny</b>

    Aktuální skupina: <b>{ $group }</b>

    Zadejte svou skupinu v jednom z těchto formátů:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Čísla mohou být 1-3místná.

settings-group-set = ✅ <b>Skupina nastavena na: { $group }</b>

    Oznámení o závodech a repríze budou obsahovat přímé odkazy na vaši skupinu!

settings-notifications-title = 🔔 <b>Nastavení oznámení</b>

    Kliknutím přepnete oznámení zapnuto/vypnuto:
    ✅ = Zapnuto | ❌ = Vypnuto

    ℹ️ <i>Toto jsou globální přepínače pro všechny závody. Použijte tlačítko 'Kvalifikace hotova' v oznámeních k zakázání konkrétního závodu.</i>

settings-custom-notif-title = ⏱️ <b>Vlastní oznámení</b>

    Nastavte si vlastní časy oznámení ({ $min }m - { $max }h před uzavřením kvalifikace).

    Můžete mít až 2 vlastní oznámení.

    Kliknutím na slot jej nastavíte nebo upravíte.

settings-custom-notif-edit = ⏱️ <b>Vlastní oznámení { $slot }</b>{ $current }

    Vyberte přednastavenou dobu nebo zadejte vlastní čas:

settings-custom-notif-current = Aktuální:

settings-custom-notif-input = ⏱️ <b>Vlastní oznámení { $slot }</b>

    Zadejte čas vlastního oznámení.

    <b>Akceptované formáty:</b>
    • <code>20m</code> nebo <code>45 minut</code> (20m-70h)
    • <code>2h</code> nebo <code>12 hodin</code>
    • <code>1h 30m</code> nebo <code>2h30m</code>

    <b>Příklady:</b>
    • <code>20m</code> - 20 minut předem
    • <code>6h</code> - 6 hodin předem
    • <code>1h 30m</code> - 1 hodina 30 minut předem

# =======================
# Buttons
# =======================
button-ui-language = 💬 Jazyk botu: { $language }
button-gpro-language = 🌍 Jazyk GPRO: { $language }
button-language = 🌍 Jazyk: { $language }
button-group = 🏁 Skupina: { $group }
button-notifications = 🔔 Oznámení
button-custom-notifications = ⏱️ Vlastní oznámení
button-back = ◀ Zpět
button-back-to-settings = ◀ Zpět do nastavení
button-back-to-notifications = ◀ Zpět k oznámením
button-back-to-custom = ◀ Zpět k vlastním oznámením
button-back-custom-notif = ◀ Zpět k vlastním oznámením
button-main-menu = 🏠 Hlavní nabídka
button-reset-group = 🔄 Resetovat skupinu
button-custom-slot-set = ⏱️ Vlastní { $slot }: { $time }
button-custom-slot-empty = ➕ Nastavit vlastní oznámení { $slot }
button-previous = ◀ Předchozí
button-next = Další ▶
button-skip = ⏭️ Přeskočit
button-reset-language = 🔄 Resetovat na výchozí (angličtinu)
button-enable-all = 🔔 Zapnout všechna oznámení
button-disable-all = 🔕 Vypnout všechna oznámení
button-enable-category = 🔔 Povolit kategorii
button-disable-category = 🔕 Zakázat kategorii
button-quali-done = ✅ Kvalifikace hotova
button-reenable-race = 🔄 Znovu zapnout oznámení závodu { $raceId }
button-weather = 🌤️ Zobrazit počasí
button-enter-custom-group = ✏️ Zadat vlastní skupinu
button-enter-custom-time = ✏️ Zadat vlastní čas
button-disable-notification = 🔕 Vypnout toto oznámení
button-cancel = ❌ Zrušit
button-got-it = ✅ Rozumím!
button-try-again = 🔄 Zkusit znovu

button-main-menu-status = 📊 Příští závod
button-main-menu-calendar = 📅 Celá sezóna
button-main-menu-next = 🌟 Příští sezóna
button-main-menu-settings = ⚙️ Nastavení

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Nastavit vlastní oznámení { $slot }
button-custom-notif-time = ⏱️ Vlastní { $slot }: { $time }

# =======================
# Notifications
# =======================
notif-category-before-qualifying = Před kvalifikací
notif-category-qualifying-events = Kvalifikační události
notif-category-race-events = Závodní události

notif-label-72h = 3 dny před uzavřením kvalifikace
notif-label-48h = 2 dny před uzavřením kvalifikace
notif-label-24h = 1 den před uzavřením kvalifikace
notif-label-2h = 2 hodiny před uzavřením kvalifikace
notif-label-10min = 10 minut před uzavřením kvalifikace
notif-label-opens = Kvalifikace je otevřena
notif-label-quali-results = Výsledky kvalifikace jsou k dispozici
notif-label-replay = Repríza závodu je dostupná
notif-label-live = Závod probíhá
notif-label-results = Výsledky závodu jsou dostupné

notif-quali-closes = <b>Kvalifikace se uzavře za { $time }!</b>
notif-quali-opens = <b>Kvalifikace je otevřena</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Závod č. { $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Uzávěrka kvalifikace: { $qualiDeadline }</b>
    🏎 <b>Závod: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Přejít na kvalifikaci</a>

    <i>Klikněte na tlačítko '✅ Kvalifikace hotova' pro vypnutí oznámení tohoto závodu</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Závod č. { $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Uzávěrka kvalifikace: { $qualiDeadline }</b>
    🏎 <b>Závod: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Přejít na kvalifikaci</a>

    ℹ️ <b>Automatická oznámení vypnuta</b> pro tento závod
    <i>Klikněte na tlačítko '🔄 Znovu zapnout' pro zapnutí oznámení</i>

notif-quali-closed-title = <b>Kvalifikace je momentálně uzavřena</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Závod č. { $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Kvalifikace uzavřena: { $qualiDeadline }</b>
    🏎 <b>Závod: { $raceTime }</b>

    ⏳ <i>Kvalifikace je momentálně uzavřena. Další kvalifikační session se otevře po dokončení aktuálního závodu. Počkejte prosím na vyhodnocení závodu.</i>

notif-race-live = 🏁 <b>Závod č. { $raceId } PROBÍHÁ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Sledovat závod naživo</a>

notif-race-live-no-group = 🏁 <b>Závod č. { $raceId } PROBÍHÁ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Nastavte svou skupinu v /settings pro přímý odkaz!

    🔗 <a href="{ $raceLink }">Sledovat závod naživo</a>

notif-race-replay = 📺 <b>Repríza závodu č. { $raceId } je dostupná</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Sledujte reprízu závodu:

    🔗 <a href="{ $replayLink }">Sledovat reprízu</a>

notif-race-replay-no-group = 📺 <b>Repríza závodu č. { $raceId } je dostupná</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Sledujte reprízu závodu:

    ⚠️ Pro personalizované odkazy nastavte svou skupinu v /settings!

    🔗 <a href="{ $replayLink }">Sledovat reprízu</a>

notif-race-results = 📊 <b>Výsledky závodu č. { $raceId } jsou dostupné</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Výsledky závodu jsou nyní dostupné:

    🔗 <a href="{ $analysisLink }">Analýza závodu</a>
    🔗 <a href="{ $summaryLink }">Souhrn závodu</a>

notif-race-results-no-group = 📊 <b>Výsledky závodu č. { $raceId } jsou dostupné</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Výsledky závodu jsou nyní dostupné:

    🔗 <a href="{ $analysisLink }">Analýza závodu</a>

    ⚠️ Pro personalizovaný souhrn závodu nastavte svou skupinu v /settings!

# =======================
# Weather



# =======================
weather-title = 🌤️ <b>Předpověď počasí pro závod</b>
weather-practice-q1 = <b>Trénink / Kvalifikace 1:</b> { $weather }
weather-temp-hum = Teplota: { $temp }°C • Vlhkost: { $hum }%
weather-q2-start = <b>Kvalifikace 2 / Start závodu:</b> { $weather }
weather-race-conditions = <b>Podmínky závodu:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Teplota: { $temp } • Vlhkost: { $hum }
    Pravděpodobnost deště: { $rain }
weather-not-available = ⚠️ Data o počasí nejsou dostupná
weather-cached = ℹ️ Počasí je již uloženo v mezipaměti pro <b>Závod č. { $raceId }: { $track }</b>

    Použijte <code>/weather force</code> pro vynucení aktualizace.
    Použijte /status pro zobrazení oznámení s tlačítkem počasí.
weather-fetching = 🔄 Načítání počasí pro <b>Závod č. { $raceId }: { $track }</b>...
weather-force-updating = 🔄 Vynucená aktualizace počasí pro <b>Závod č. { $raceId }: { $track }</b>...
weather-success = ✅ Data o počasí načtena pro <b>Závod č. { $raceId }: { $track }</b>

    Použijte /status pro testování oznámení s tlačítkem počasí!
weather-failed = ❌ Nepodařilo se načíst data o počasí

    Zkontrolujte, zda je GPRO API token platný a Practice API je dostupné.

# =======================
# Admin
# =======================
admin-only = ❌ Pouze pro administrátory
admin-calendar-updated = ✅ <b>Kalendář</b>: { $count } závodů
    🔄 <b>{ $userCount } uživatelů</b> resetováno
admin-next-season-ready = 🌟 <b>Příští sezóna je připravena!</b> { $count } závodů
    Použijte /next pro zobrazení
admin-next-season-not-published = ℹ️ <b>Příští sezóna nebyla zveřejněna</b>
admin-users-count = 📊 <b>{ $count } uživatelů</b>:
admin-users-none = 📊 <b>0 uživatelů</b> v databázi
admin-no-races = ❌ Žádné závody v kalendáři
admin-no-upcoming-races = ❌ Nebyly nalezeny žádné nadcházející závody

# =======================
# Errors & Validation
# =======================
error-invalid-format = ❌ Neplatný formát!

    Prosím použijte:
    • <b>E</b> pro Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> atd.

    Zkuste znovu:

error-invalid-format-onboarding = ❌ Neplatný formát!

    Prosím použijte:
    • <b>E</b> pro Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> atd.

    Zkuste znovu nebo použijte /start pro restart:

error-invalid-time = ❌ <b>Chyba:</b> { $error }

    Prosím zkuste znovu s platným formátem jako: <code>2h</code>, <code>30m</code>, nebo <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Chyba:</b> { $error }

    Prosím zkuste znovu.

error-invalid-race = ❌ Neplatné ID závodu
error-invalid-page = ❌ Neplatná stránka
error-invalid-language = ❌ Neplatný jazyk
error-invalid-category = ❌ Neplatná kategorie
error-invalid-slot = ❌ Neplatný slot
error-invalid-data = ❌ Neplatná data
error-reset-failed = ❌ Reset selhal
error-race-not-found = ❌ Závod nebyl nalezen
error-weather-not-available = ⚠️ Data o počasí ještě nejsou dostupná
error-weather-send-failed = ❌ Nepodařilo se odeslat počasí

# =======================
# Feedback & Confirmations
# =======================
feedback-all-enabled = ✅ Všechna oznámení zapnuta!
feedback-all-disabled = ✅ Všechna oznámení vypnuta!
feedback-category-enabled = ✅ { $category } povolena!
feedback-category-disabled = ✅ { $category } zakázána!
feedback-notif-enabled = ✅ { $label } zapnuto!
feedback-notif-disabled = ✅ { $label } vypnuto!
feedback-quali-done = ✅ Hotovo!
feedback-race-marked-done = ✅ <i>Závod označen jako dokončený!</i>
feedback-reset = 🔄 Resetováno!
feedback-notifications-reset = 🔄 <i>Oznámení resetována!</i>
feedback-reenabled = 🔄 Znovu zapnuto!
feedback-notifications-reenabled = 🔄 <i>Oznámení znovu zapnuta!</i>
feedback-language-set = ✅ Jazyk nastaven na { $language }
feedback-language-reset = ✅ Jazyk resetován na angličtinu
feedback-ui-language-set = ✅ Jazyk botu nastaven na { $language }
feedback-group-set = ✅ Skupina nastavena na { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Vlastní oznámení { $slot } vypnuto
feedback-skip-language = ⏭️ Používá se výchozí jazyk (angličtina)
feedback-skip-group = ⏭️ Výběr skupiny přeskočen
feedback-welcome = ✅ Vítejte na palubě!
feedback-weather-sent = 🌤️ Předpověď počasí odeslána!

# =======================
# Time Formatting
# =======================
# Weekday abbreviations (2-letter)
weekday-mon = Po
weekday-tue = Út
weekday-wed = St
weekday-thu = Čt
weekday-fri = Pá
weekday-sat = So
weekday-sun = Ne

time-minutes = { $minutes ->
    [one] { $minutes } minuta
    [few] { $minutes } minuty
   *[other] { $minutes } minut
}
time-hours = { $hours ->
    [one] { $hours } hodina
    [few] { $hours } hodiny
   *[other] { $hours } hodin
}
time-hours-minutes = { $hours ->
    [one] { $hours } hodina
    [few] { $hours } hodiny
   *[other] { $hours } hodin
} { $minutes ->
    [one] { $minutes } minuta
    [few] { $minutes } minuty
   *[other] { $minutes } minut
}
time-hours-minutes-short = { $hours }h{ $minutes }m
time-hours-short = { $hours }h
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }d{ $hours }h
time-days-hours-minutes-short = { $days }d{ $hours }h{ $minutes }m
time-days = { $days ->
    [one] { $days } den
    [few] { $days } dny
   *[other] { $days } dní
}
time-days-hours = { $days ->
    [one] { $days } den
    [few] { $days } dny
   *[other] { $days } dní
} { $hours ->
    [one] { $hours } hodina
    [few] { $hours } hodiny
   *[other] { $hours } hodin
}
time-months = { $months ->
    [one] { $months } měsíc
    [few] { $months } měsíce
   *[other] { $months } měsíců
}
time-months-days = { $months ->
    [one] { $months } měsíc
    [few] { $months } měsíce
   *[other] { $months } měsíců
} { $days ->
    [one] { $days } den
    [few] { $days } dny
   *[other] { $days } dní
}

# =======================
# Group Display
# =======================
group-not-set = Nenastaveno
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Custom Notification Messages
# =======================
custom-notif-set = Vlastní oznámení { $slot } nastaveno na { $time }
custom-notif-set-success = Vlastní oznámení { $slot } nastaveno na { $time }
custom-notif-not-set = Nenastaveno
custom-notif-min-error = Minimální čas je 20 minut
custom-notif-max-error = Maximální čas je 70 hodin
custom-notif-invalid-slot = Neplatný slot (musí být 0-{ $max })
custom-notif-empty-error = Čas nemůže být prázdný
custom-notif-invalid-format = Neplatný formát. Použijte: 2h, 30m, nebo 1h 30m
custom-notif-enter-time = Prosím zadejte čas
custom-notif-error-parsing = ❌ <b>Chyba:</b> { $error }

    Prosím zkuste znovu s platným formátem jako: <code>2h</code>, <code>30m</code>, nebo <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Vaše vlastní oznámení bylo nastaveno!
custom-notif-error-setting = ❌ <b>Chyba:</b> { $error }

    Prosím zkuste znovu.

# =======================
# Validation
# =======================
validation-time-empty = Čas nemůže být prázdný
validation-time-min = Minimální čas je 20 minut
validation-time-max = Maximální čas je 70 hodin
validation-enter-time = Prosím zadejte čas
validation-invalid-format = Neplatný formát. Použijte: 2h, 30m, nebo 1h 30m
validation-invalid-slot = Neplatný slot (musí být 0-{ $maxSlots })

# =======================
# Notification Labels
# =======================
notif-label-72h = 3 dny před uzavřením kvalifikace
notif-label-48h = 2 dny před uzavřením kvalifikace
notif-label-24h = 1 den před uzavřením kvalifikace
notif-label-2h = 2 hodiny před uzavřením kvalifikace
notif-label-10min = 10 minut před uzavřením kvalifikace
notif-label-opens-soon = Kvalifikace je otevřena
notif-label-quali-results = Výsledky kvalifikace jsou k dispozici
notif-label-race-replay = Repríza závodu je dostupná
notif-label-race-live = Závod probíhá
notif-label-race-results = Výsledky závodu jsou dostupné

# =======================
# Notification Menu
# =======================
notif-menu-title = 🔔 <b>Nastavení oznámení</b>

    Kliknutím přepnete oznámení zapnuto/vypnuto:
    ✅ = Zapnuto | ❌ = Vypnuto

    ℹ️ <i>Toto jsou globální přepínače pro všechny závody. Použijte tlačítko 'Kvalifikace hotova' v oznámeních k zakázání konkrétního závodu.</i>

# =======================
# Group Menu
# =======================
group-menu-title = 🏁 <b>Nastavení skupiny</b>

    Aktuální skupina: <b>{ $groupDisplay }</b>

    Zadejte svou skupinu v jednom z těchto formátů:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Čísla mohou být 1-3místná.
group-reset-success = ✅ Skupina úspěšně resetována

# =======================
# Language Menu
# =======================
lang-menu-title = 🌍 <b>Nastavení jazyka</b>

    Aktuální: { $currentLang }

    Vyberte svůj preferovaný jazyk pro odkazy na GPRO závody:

# =======================
# Custom Notification Menu
# =======================
custom-notif-menu-title = ⏱️ <b>Vlastní oznámení</b>

    Nastavte si vlastní časy oznámení ({ $minTime }m - { $maxTime }h před uzavřením kvalifikace).

    Můžete mít až 2 vlastní oznámení.

    Kliknutím na slot jej nastavíte nebo upravíte.

# =======================
# Weather



# =======================
weather-unavailable = ⚠️ Data o počasí nejsou dostupná
weather-title = 🌤️ <b>Předpověď počasí pro závod</b>
weather-race-header = Závod č. { $raceId }: { $track }
weather-practice-q1 = <b>Trénink / Kvalifikace 1:</b> { $weather }
weather-temp-hum = Teplota: { $temp }°C • Vlhkost: { $hum }%
weather-q2-race-start = <b>Kvalifikace 2 / Start závodu:</b> { $weather }
weather-race-conditions = <b>Podmínky závodu:</b>
weather-start-0h30m = <b>Start - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Teplota: { $temp } • Vlhkost: { $hum }
weather-rain-prob = Pravděpodobnost deště: { $rain }

# Weather Conditions
weather-condition-sunny = Slunečno
weather-condition-partially-cloudy = Polojasno
weather-condition-cloudy = Zataženo
weather-condition-very-cloudy = Velmi zataženo
weather-condition-rain = Déšť

# =======================
# Timezone Settings
# =======================
button-timezone = ⏰ Časové pásmo: { $timezone }
button-website-mode = 🌐 Typ odkazu: { $mode }
website-mode-classic = Klasický
timezone-menu-title = ⏰ <b>Nastavení časového pásma</b>

    Aktuální časové pásmo: <b>{ $timezone }</b>

    Zadejte své časové pásmo (název města, zkratka nebo UTC offset):

    Příklady: <code>Praha</code>, <code>CET</code>, <code>UTC+1</code>, <code>Londýn</code>

timezone-select-matches = 🌍 <b>Vyberte své časové pásmo:</b>

    Shody pro "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Vyberte své časové pásmo:</b>

    Shody pro "{ $query }" (Stránka { $page }/{ $total }):

timezone-set-success = ✅ <b>Časové pásmo nastaveno!</b>

    { $timezone }

    Aktuální čas ve vašem časovém pásmu: <b>{ $localTime }</b>

    Všechny časy závodů budou nyní zobrazeny ve vašem lokálním čase.

button-reset-timezone = 🔄 Resetovat na UTC
feedback-timezone-set = ✅ Časové pásmo aktualizováno
feedback-timezone-reset = ✅ Časové pásmo resetováno na UTC
feedback-switched-to-app = Režim APP aktivován
feedback-switched-to-classic = Klasický režim aktivován
error-mode-switch-failed = ❌ Nelze přepnout režim webové stránky
error-timezone-not-found = ❌ Nenalezeno žádné časové pásmo pro "{ $query }"

    Zkuste: název města (Praha), zkratka (CET), nebo UTC offset (UTC+1)
error-invalid-timezone = ❌ Neplatné časové pásmo

notif-quali-results = 🏁 <b>Výsledky kvalifikace - Závod #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Kvalifikace uzavřena</b>
    🏎 <b>Závod: { $raceTime }</b>

    Výsledky kvalifikace jsou k dispozici:

    🔗 <a href="{ $gridLink }">Startovní rošt</a>

notif-quali-results-no-group = 🏁 <b>Výsledky kvalifikace - Závod #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Kvalifikace uzavřena</b>
    🏎 <b>Závod: { $raceTime }</b>

    Výsledky kvalifikace jsou k dispozici:

    ⚠️ Pro personalizované odkazy nastavte svou skupinu v /settings!

    🔗 <a href="{ $gridLink }">Startovní rošt</a>

# =======================
# Připomínka nové sezóny
# =======================
notif-category-season-prep = Příprava na sezónu

notif-label-new-season-reminder = Připomínka nové sezóny

notif-new-season-reminder = 🌟 <b>Nová sezóna začíná!</b>

    🏁 <b>Závod #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Závod: { $raceTime }</b>

    Vaše aktuální skupina: <b>{ $group }</b>

    💡 Pokud jste přešli do jiné skupiny, aktualizujte ji v /settings pro personalizované odkazy!

notif-new-season-reminder-no-group = 🌟 <b>Nová sezóna začíná!</b>

    🏁 <b>Závod #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Závod: { $raceTime }</b>

    ⚠️ Ještě jste nenastavili svou skupinu!

    💡 Nastavte svou skupinu v /settings pro personalizované odkazy na závody!

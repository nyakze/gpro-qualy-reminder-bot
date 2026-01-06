# GPRO Bot - Traduzioni Italiane

# =======================
# Comandos & General
# =======================
start-welcome-new = 👋 <b>Benvenuto in GPRO Bot!</b>

    Iniziamo la configurazione. Prima scegli la tua lingua preferita per i link delle gare GPRO:

    🌍 <b>Seleziona la tua lingua</b> (o salta per usare l'inglese):

start-welcome-existing = 🏁 GPRO Bot ATTIVO!
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Cosa vorresti fare?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendario
# =======================
no-races-scheduled = 🔔 Nessuna gara programmata
no-upcoming-qualifications = 🔔 Nessuna qualifica programmata
next-season-not-published = 🌟 <b>La prossima stagione non è ancora stata pubblicata</b>

calendar-title-full = 🏁 <b>Stagione Completa</b>
calendar-title-next = 🌟 <b>PROSSIMA STAGIONE</b> ({ $count } gare)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 <b>Selezione Gruppo</b>

    Scegli il tuo gruppo GPRO per ricevere link personalizzati delle gare:

    Seleziona un gruppo comune o inserisci il tuo:

onboard-group-custom = 🏁 <b>Selezione Gruppo (Opzionale)</b>

    Inserisci il tuo gruppo in uno di questi formati:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.

    💡 <i>La lingua del sito GPRO è stata impostata per corrispondere alla lingua del bot. Puoi cambiarla in seguito in /settings</i>

onboard-complete = ✅ <b>Configurazione Completata!</b>

    🏁 <b>GPRO Bot è pronto!</b>

    <b>Comandi disponibili:</b>
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

    💡 <i>Puoi modificare queste impostazioni in qualsiasi momento usando /settings</i>

onboard-complete-with-group = ✅ <b>Configurazione Completata!</b>

    Gruppo: <b>{ $group }</b>

    🏁 <b>GPRO Bot è pronto!</b>

    <b>Comandi disponibili:</b>
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

# =======================
# Impostazioni
# =======================
settings-title = ⚙️ <b>Impostazioni</b>

    Configura le tue preferenze:

settings-language-title = 🌍 <b>Impostazioni Lingua</b>

    Attuale: { $language }

    Seleziona la tua lingua preferita per i link delle gare GPRO:

ui-lang-menu-title = 💬 <b>Lingua del Bot</b>

    Seleziona la lingua dell'interfaccia del bot:

settings-group-title = 🏁 <b>Impostazioni Gruppo</b>

    Gruppo attuale: <b>{ $group }</b>

    Inserisci il tuo gruppo in uno di questi formati:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.

settings-group-set = ✅ <b>Gruppo impostato su: { $group }</b>

    Le notifiche delle gare e dei replay includeranno link diretti al tuo gruppo!

settings-notifications-title = 🔔 <b>Impostazioni Notifiche</b>

    Clicca per attivare/disattivare le notifiche:
    ✅ = Attivo | ❌ = Disattivo

    ℹ️ <i>Questi sono interruttori globali per tutte le gare. Usa il pulsante 'Qualifica Completata' nelle notifiche per disabilitare una gara specifica.</i>

settings-custom-notif-title = ⏱️ <b>Notifiche Personalizzate</b>

    Imposta i tuoi orari di notifica ({ $min }m - { $max }h prima della chiusura delle qualifiche).

    Puoi avere fino a 2 notifiche personalizzate.

    Clicca su uno slot per impostarlo o modificarlo.

settings-custom-notif-edit = ⏱️ <b>Notifica Personalizzata { $slot }</b>{ $current }
settings-custom-notif-current = Current:

    Seleziona un orario predefinito o inserisci un orario personalizzato:

settings-custom-notif-input = ⏱️ <b>Notifica Personalizzata { $slot }</b>

    Inserisci il tuo orario di notifica personalizzato.

    <b>Formati accettati:</b>
    • <code>20m</code> o <code>45 minuti</code> (20m-70h)
    • <code>2h</code> o <code>12 ore</code>
    • <code>1h 30m</code> o <code>2h30m</code>

    <b>Esempi:</b>
    • <code>20m</code> - 20 minuti prima
    • <code>6h</code> - 6 ore prima
    • <code>1h 30m</code> - 1 ora e 30 minuti prima

# =======================
# Pulsanti
# =======================
button-ui-language = 💬 Lingua del Bot: { $language }
button-gpro-language = 🌍 Lingua GPRO: { $language }
button-language = 🌍 Lingua: { $language }
button-group = 🏁 Gruppo: { $group }
button-notifications = 🔔 Notifiche
button-custom-notifications = ⏱️ Notifiche Personalizzate
button-back = ◀ Indietro
button-back-to-settings = ◀ Torna alle Impostazioni
button-back-to-notifications = ◀ Torna alle Notifiche
button-back-to-custom = ◀ Torna alle Notifiche Personalizzate
button-back-custom-notif = ◀ Torna alle Notifiche Personalizzate
button-main-menu = 🏠 Menu Principale
button-reset-group = 🔄 Reimposta Gruppo
button-custom-slot-set = ⏱️ Personalizzata { $slot }: { $time }
button-custom-slot-empty = ➕ Imposta Notifica Personalizzata { $slot }
button-previous = ◀ Precedente
button-next = Successivo ▶
button-skip = ⏭️ Salta
button-reset-language = 🔄 Reimposta su Predefinito (Inglese)
button-enable-all = 🔔 Attiva Tutte le Notifiche
button-disable-all = 🔕 Disattiva Tutte le Notifiche
button-enable-category = 🔔 Attiva Categoria
button-disable-category = 🔕 Disattiva Categoria
button-quali-done = ✅ Qualifica Completata
button-reenable-race = 🔄 Riattiva notifiche Gara { $raceId }
button-weather = 🌤️ Mostra Meteo
button-enter-custom-group = ✏️ Inserisci Gruppo Personalizzato
button-enter-custom-time = ✏️ Inserisci Orario Personalizzato
button-disable-notification = 🔕 Disattiva Questa Notifica
button-cancel = ❌ Annulla
button-got-it = ✅ Capito!
button-try-again = 🔄 Riprova

button-main-menu-status = 📊 Prossima Gara
button-main-menu-calendar = 📅 Stagione Completa
button-main-menu-next = 🌟 Prossima Stagione
button-main-menu-settings = ⚙️ Impostazioni

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Imposta Notifica Personalizzata { $slot }
button-custom-notif-time = ⏱️ Personalizzata { $slot }: { $time }

# =======================
# Notifiche
# =======================
notif-category-before-qualifying = Prima delle Qualifiche
notif-category-qualifying-events = Eventi di Qualifica
notif-category-race-events = Eventi di Gara

notif-label-72h = 3g prima della chiusura qualifiche
notif-label-48h = 2g prima della chiusura qualifiche
notif-label-24h = 1g prima della chiusura qualifiche
notif-label-2h = 2h prima della chiusura qualifiche
notif-label-10min = 10min prima della chiusura qualifiche
notif-label-opens = Le qualifiche sono aperte
notif-label-quali-results = Risultati delle qualifiche disponibili
notif-label-replay = Replay della gara disponibile
notif-label-live = Gara in diretta
notif-label-results = Risultati della gara disponibili

notif-label-opens-soon = Le qualifiche sono aperte
notif-label-quali-results = Risultati delle qualifiche disponibili
notif-label-race-replay = Replay della gara disponibile
notif-label-race-live = Gara in diretta
notif-label-race-results = Risultati della gara disponibili

notif-quali-closes = <b>Le qualifiche chiudono tra { $time }!</b>
notif-quali-opens = <b>Le qualifiche sono aperte (o si apriranno presto)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Gara #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifiche chiudono: { $qualiDeadline }</b>
    🏎 <b>Gara: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Vai alle Qualifiche</a>

    <i>Clicca sul pulsante '✅ Qualifica Completata' per disattivare le notifiche di questa gara</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Gara #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifiche chiudono: { $qualiDeadline }</b>
    🏎 <b>Gara: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Vai alle Qualifiche</a>

    ℹ️ <b>Notifiche automatiche disabilitate</b> per questa gara
    <i>Clicca sul pulsante '🔄 Riattiva' per riattivare le notifiche</i>

notif-race-live = 🏁 <b>Gara #{ $raceId } è IN DIRETTA!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Guarda la Gara in Diretta</a>

notif-race-live-no-group = 🏁 <b>Gara #{ $raceId } è IN DIRETTA!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Imposta il tuo gruppo in /settings per un link diretto!

    🔗 <a href="{ $raceLink }">Guarda la Gara in Diretta</a>

notif-race-replay = 📺 <b>Replay Gara #{ $raceId } Disponibile</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Se la gara è già stata calcolata, il replay è disponibile qui:

    🔗 <a href="{ $replayLink }">Guarda il Replay</a>

notif-race-replay-no-group = 📺 <b>Replay Gara #{ $raceId } Disponibile</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Se la gara è già stata calcolata, il replay è disponibile qui:

    ⚠️ Per link personalizzati, imposta il tuo gruppo in /settings!

    🔗 <a href="{ $replayLink }">Guarda il Replay</a>

notif-race-results = 📊 <b>Risultati Gara #{ $raceId } Disponibili</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    I risultati della gara sono ora disponibili:

    🔗 <a href="{ $analysisLink }">Analisi della Gara</a>
    🔗 <a href="{ $summaryLink }">Riepilogo della Gara</a>

notif-race-results-no-group = 📊 <b>Risultati Gara #{ $raceId } Disponibili</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    I risultati della gara sono ora disponibili:

    🔗 <a href="{ $analysisLink }">Analisi della Gara</a>

    ⚠️ Per il Riepilogo Gara personalizzato, imposta il tuo gruppo in /settings!

# =======================
# Meteo
# =======================
weather-title = 🌤️ <b>Previsioni Meteo Gara</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Prova / Qualifica 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Umidità: { $hum }%
weather-q2-start = <b>Qualifica 2 / Partenza Gara:</b> { $weather }
weather-q2-race-start = <b>Qualifica 2 / Partenza Gara:</b> { $weather }
weather-race-conditions = <b>Condizioni di Gara:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Umidità: { $hum }
    Probabilità di pioggia: { $rain }
weather-not-available = ⚠️ Dati meteo non disponibili
weather-unavailable = ⚠️ Dati meteo non disponibili
weather-cached = ℹ️ Meteo già in cache per <b>Gara #{ $raceId }: { $track }</b>

    Usa <code>/weather force</code> per forzare l'aggiornamento.
    Usa /status per vedere la notifica con il pulsante meteo.
weather-fetching = 🔄 Recupero meteo per <b>Gara #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Aggiornamento forzato meteo per <b>Gara #{ $raceId }: { $track }</b>...
weather-success = ✅ Dati meteo recuperati per <b>Gara #{ $raceId }: { $track }</b>

    Usa /status per testare la notifica con il pulsante meteo!
weather-failed = ❌ Impossibile recuperare i dati meteo

    Verifica che il token API GPRO sia valido e che l'API di Prova sia disponibile.

weather-start-0h30m = <b>Partenza - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Temp: { $temp } • Umidità: { $hum }
weather-rain-prob = Probabilità di pioggia: { $rain }

# Condizioni Meteorologiche
weather-condition-sunny = Soleggiato
weather-condition-partially-cloudy = Parzialmente Nuvoloso
weather-condition-cloudy = Nuvoloso
weather-condition-very-cloudy = Coperto
weather-condition-rain = Pioggia

# =======================
# Admin
# =======================
admin-only = ❌ Solo admin
admin-calendar-updated = ✅ <b>Calendario</b>: { $count } gare
    🔄 <b>{ $userCount } utenti</b> reimpostati
admin-next-season-ready = 🌟 <b>Prossima stagione pronta!</b> { $count } gare
    Usa /next per visualizzare
admin-next-season-not-published = ℹ️ <b>Prossima stagione non pubblicata</b>
admin-users-count = 📊 <b>{ $count } utenti</b>:
admin-users-none = 📊 <b>0 utenti</b> nel database
admin-no-races = ❌ Nessuna gara nel calendario
admin-no-upcoming-races = ❌ Nessuna gara futura trovata

# =======================
# Errori & Validazione
# =======================
error-invalid-format = ❌ Formato non valido!

    Per favore usa:
    • <b>E</b> per Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> ecc.

    Riprova:

error-invalid-format-onboarding = ❌ Formato non valido!

    Per favore usa:
    • <b>E</b> per Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> ecc.

    Riprova o usa /start per ricominciare:

error-invalid-time = ❌ <b>Errore:</b> { $error }

    Per favore riprova con un formato valido come: <code>2h</code>, <code>30m</code>, o <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Errore:</b> { $error }

    Per favore riprova.

error-invalid-race = ❌ ID gara non valido
error-invalid-page = ❌ Pagina non valida
error-invalid-language = ❌ Lingua non valida
error-invalid-category = ❌ Categoria non valida
error-invalid-slot = ❌ Slot non valido
error-invalid-data = ❌ Dati non validi
error-reset-failed = ❌ Reimpostazione fallita
error-race-not-found = ❌ Gara non trovata
error-weather-not-available = ⚠️ Dati meteo non ancora disponibili
error-weather-send-failed = ❌ Impossibile inviare il meteo

# =======================
# Feedback & Conferme
# =======================
feedback-all-enabled = ✅ Tutte le notifiche attivate!
feedback-all-disabled = ✅ Tutte le notifiche disattivate!
feedback-category-enabled = ✅ { $category } attivata!
feedback-category-disabled = ✅ { $category } disattivata!
feedback-notif-enabled = ✅ { $label } attivata!
feedback-notif-disabled = ✅ { $label } disattivata!
feedback-quali-done = ✅ Fatto!
feedback-race-marked-done = ✅ <i>Gara segnata come completata!</i>
feedback-reset = 🔄 Reimpostato!
feedback-notifications-reset = 🔄 <i>Notifiche reimpostate!</i>
feedback-reenabled = 🔄 Riattivato!
feedback-notifications-reenabled = 🔄 <i>Notifiche riattivate!</i>
feedback-language-set = ✅ Lingua impostata su { $language }
feedback-language-reset = ✅ Lingua reimpostata su inglese
feedback-ui-language-set = ✅ Lingua del bot impostata su { $language }
feedback-group-set = ✅ Gruppo impostato su { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notifica personalizzata { $slot } disattivata
feedback-skip-language = ⏭️ Uso della lingua predefinita (inglese)
feedback-skip-group = ⏭️ Selezione gruppo saltata
feedback-welcome = ✅ Benvenuto!
feedback-weather-sent = 🌤️ Previsioni meteo inviate!

# =======================
# Formattazione Tempo
# =======================
# Abbreviazioni giorni della settimana (2 lettere)
weekday-mon = Lu
weekday-tue = Ma
weekday-wed = Me
weekday-thu = Gi
weekday-fri = Ve
weekday-sat = Sa
weekday-sun = Do

time-minutes = { $minutes ->
    [one] { $minutes } minuto
   *[other] { $minutes } minuti
}
time-hours = { $hours ->
    [one] { $hours } ora
   *[other] { $hours } ore
}
time-hours-minutes = { $hours ->
    [one] { $hours } ora
   *[other] { $hours } ore
} { $minutes ->
    [one] { $minutes } minuto
   *[other] { $minutes } minuti
}
time-hours-minutes-short = { $hours }h{ $minutes }m
time-hours-short = { $hours }h
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }g{ $hours }h
time-days-hours-minutes-short = { $days }g{ $hours }h{ $minutes }m
time-days = { $days ->
    [one] { $days } giorno
   *[other] { $days } giorni
}
time-days-hours = { $days ->
    [one] { $days } giorno
   *[other] { $days } giorni
} { $hours ->
    [one] { $hours } ora
   *[other] { $hours } ore
}
time-months = { $months ->
    [one] { $months } mese
   *[other] { $months } mesi
}
time-months-days = { $months ->
    [one] { $months } mese
   *[other] { $months } mesi
} { $days ->
    [one] { $days } giorno
   *[other] { $days } giorni
}

# =======================
# Visualizzazione Gruppo
# =======================
group-not-set = Non impostato
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Messaggi Notifica Personalizzata
# =======================
custom-notif-set = Notifica personalizzata { $slot } impostata su { $time }
custom-notif-set-success = Notifica personalizzata { $slot } impostata su { $time }
custom-notif-not-set = Non impostata
custom-notif-min-error = Il tempo minimo è di 20 minuti
custom-notif-max-error = Il tempo massimo è di 70 ore
custom-notif-invalid-slot = Slot non valido (deve essere 0-{ $max })
custom-notif-empty-error = Il tempo non può essere vuoto
custom-notif-invalid-format = Formato non valido. Usa: 2h, 30m, o 1h 30m
custom-notif-enter-time = Per favore inserisci un tempo
custom-notif-error-parsing = ❌ <b>Errore:</b> { $error }

    Per favore riprova con un formato valido come: <code>2h</code>, <code>30m</code>, o <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    La tua notifica personalizzata è stata impostata!
custom-notif-error-setting = ❌ <b>Errore:</b> { $error }

    Per favore riprova.

# =======================
# Validazione
# =======================
validation-time-empty = Il tempo non può essere vuoto
validation-time-min = Il tempo minimo è di 20 minuti
validation-time-max = Il tempo massimo è di 70 ore
validation-enter-time = Per favore inserisci un tempo
validation-invalid-format = Formato non valido. Usa: 2h, 30m, o 1h 30m
validation-invalid-slot = Slot non valido (deve essere 0-{ $maxSlots })

# =======================
# Menu Notifiche
# =======================
notif-menu-title = 🔔 <b>Impostazioni Notifiche</b>

    Clicca per attivare/disattivare le notifiche:
    ✅ = Attivo | ❌ = Disattivo

    ℹ️ <i>Questi sono interruttori globali per tutte le gare. Usa il pulsante 'Qualifica Completata' nelle notifiche per disabilitare una gara specifica.</i>

# =======================
# Menu Gruppo
# =======================
group-menu-title = 🏁 <b>Impostazioni Gruppo</b>

    Gruppo attuale: <b>{ $groupDisplay }</b>

    Inserisci il tuo gruppo in uno di questi formati:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.
group-reset-success = ✅ Gruppo reimpostato con successo

# =======================
# Menu Lingua
# =======================
lang-menu-title = 🌍 <b>Impostazioni Lingua</b>

    Attuale: { $currentLang }

    Seleziona la tua lingua preferita per i link delle gare GPRO:

# =======================
# Menu Notifiche Personalizzate
# =======================
custom-notif-menu-title = ⏱️ <b>Notifiche Personalizzate</b>

    Imposta i tuoi orari di notifica ({ $minTime }m - { $maxTime }h prima della chiusura delle qualifiche).

    Puoi avere fino a 2 notifiche personalizzate.

    Clicca su uno slot per impostarlo o modificarlo.

# =======================
# Impostazioni Fuso Orario
# =======================
button-timezone = ⏰ Fuso orario: { $timezone }
timezone-menu-title = ⏰ <b>Impostazioni Fuso Orario</b>

    Fuso orario attuale: <b>{ $timezone }</b>

    Digita il tuo fuso orario (nome città in inglese, abbreviazione o offset UTC):

    Esempi: <code>Rome</code>, <code>New York</code>, <code>UTC+1</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Seleziona il tuo fuso orario:</b>

    Corrispondenze per "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Seleziona il tuo fuso orario:</b>

    Corrispondenze per "{ $query }" (Pagina { $page }/{ $total }):

timezone-set-success = ✅ <b>Fuso orario impostato!</b>

    { $timezone }

    Ora attuale nel tuo fuso orario: <b>{ $localTime }</b>

    Tutti gli orari delle gare saranno mostrati nel tuo orario locale.

button-reset-timezone = 🔄 Ripristina UTC
feedback-timezone-set = ✅ Fuso orario aggiornato
feedback-timezone-reset = ✅ Fuso orario ripristinato a UTC
error-timezone-not-found = ❌ Nessun fuso orario trovato per "{ $query }"

    Prova: nome città in inglese (Rome), abbreviazione (CET), o offset UTC (UTC+1)
error-invalid-timezone = ❌ Fuso orario non valido



notif-quali-results = 🏁 <b>Risultati Qualifiche - Gara #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifiche chiuse: { $qualiClose }</b>
    🏎 <b>Gara: { $raceTime }</b>

    Risultati delle qualifiche disponibili:

    🔗 <a href="{ $q12Link }">Classifica Q1 e Q2</a>
    🔗 <a href="{ $gridLink }">Griglia di Partenza</a>

notif-quali-results-no-group = 🏁 <b>Risultati Qualifiche - Gara #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifiche chiuse: { $qualiClose }</b>
    🏎 <b>Gara: { $raceTime }</b>

    Risultati delle qualifiche disponibili:

    ⚠️ Per link personalizzati, imposta il tuo gruppo in /settings!

    🔗 <a href="{ $q12Link }">Classifica Q1 e Q2</a>
    🔗 <a href="{ $gridLink }">Griglia di Partenza</a>

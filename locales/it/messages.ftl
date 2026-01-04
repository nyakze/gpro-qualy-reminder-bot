# GPRO Bot - Traduzioni Italiane

# =======================
# Comandos & General
# =======================
start-welcome-new = 👋 **Benvenuto in GPRO Bot!**

    Iniziamo la configurazione. Prima scegli la tua lingua preferita per i link delle gare GPRO:

    🌍 **Seleziona la tua lingua** (o salta per usare l'inglese):

start-welcome-existing = 🏁 GPRO Bot ATTIVO!
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

start-welcome-existing-buttons = 🏁 **GPRO Bot**

    Cosa vorresti fare?

bot-live = 🏁 **GPRO Bot**

# =======================
# Status & Calendario
# =======================
no-races-scheduled = 🔔 Nessuna gara programmata
no-upcoming-qualifications = 🔔 Nessuna qualifica programmata
next-season-not-published = 🌟 **La prossima stagione non è ancora stata pubblicata**

calendar-title-full = 🏁 **Stagione Completa**
calendar-title-next = 🌟 **PROSSIMA STAGIONE** ({ $count } gare)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 **Selezione Gruppo**

    Scegli il tuo gruppo GPRO per ricevere link personalizzati delle gare:

    Seleziona un gruppo comune o inserisci il tuo:

onboard-group-custom = 🏁 **Gruppo Personalizzato**

    Inserisci il tuo gruppo in uno di questi formati:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.

onboard-complete = ✅ **Configurazione Completata!**

    🏁 **GPRO Bot è pronto!**

    **Comandi disponibili:**
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

    💡 *Puoi modificare queste impostazioni in qualsiasi momento usando /settings*

onboard-complete-with-group = ✅ **Configurazione Completata!**

    Gruppo: **{ $group }**

    🏁 **GPRO Bot è pronto!**

    **Comandi disponibili:**
    /status - Prossima gara
    /calendar - Stagione completa
    /next - Prossima stagione
    /settings - Preferenze

# =======================
# Impostazioni
# =======================
settings-title = ⚙️ **Impostazioni**

    Configura le tue preferenze:

settings-language-title = 🌍 **Impostazioni Lingua**

    Attuale: { $language }

    Seleziona la tua lingua preferita per i link delle gare GPRO:

ui-lang-menu-title = 💬 **Lingua del Bot**

    Seleziona la lingua dell'interfaccia del bot:

settings-group-title = 🏁 **Impostazioni Gruppo**

    Gruppo attuale: **{ $group }**

    Inserisci il tuo gruppo in uno di questi formati:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.

settings-group-set = ✅ **Gruppo impostato su: { $group }**

    Le notifiche delle gare e dei replay includeranno link diretti al tuo gruppo!

settings-notifications-title = 🔔 **Impostazioni Notifiche**

    Clicca per attivare/disattivare le notifiche:
    ✅ = Attivo | ❌ = Disattivo

    ℹ️ *Questi sono interruttori globali per tutte le gare. Usa il pulsante 'Qualifica Completata' nelle notifiche per disabilitare una gara specifica.*

settings-custom-notif-title = ⏱️ **Notifiche Personalizzate**

    Imposta i tuoi orari di notifica ({ $min }m - { $max }h prima della chiusura delle qualifiche).

    Puoi avere fino a 2 notifiche personalizzate.

    Clicca su uno slot per impostarlo o modificarlo.

settings-custom-notif-edit = ⏱️ **Notifica Personalizzata { $slot }**{ $current }

    Seleziona un orario predefinito o inserisci un orario personalizzato:

settings-custom-notif-input = ⏱️ **Notifica Personalizzata { $slot }**

    Inserisci il tuo orario di notifica personalizzato.

    **Formati accettati:**
    • `20m` o `45 minuti` (20m-70h)
    • `2h` o `12 ore`
    • `1h 30m` o `2h30m`

    **Esempi:**
    • `20m` - 20 minuti prima
    • `6h` - 6 ore prima
    • `1h 30m` - 1 ora e 30 minuti prima

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
notif-label-72h = 3g prima della chiusura qualifiche
notif-label-48h = 2g prima della chiusura qualifiche
notif-label-24h = 1g prima della chiusura qualifiche
notif-label-2h = 2h prima della chiusura qualifiche
notif-label-10min = 10min prima della chiusura qualifiche
notif-label-opens = Le qualifiche sono aperte
notif-label-replay = Replay della gara disponibile
notif-label-live = Gara in diretta
notif-label-results = Risultati della gara disponibili

notif-label-opens-soon = Le qualifiche sono aperte
notif-label-race-replay = Replay della gara disponibile
notif-label-race-live = Gara in diretta
notif-label-race-results = Risultati della gara disponibili

notif-quali-closes = **Le qualifiche chiudono tra { $time }!**
notif-quali-opens = **Le qualifiche sono aperte (o si apriranno presto)**

notif-quali-message = { $emoji } { $title }

    🏁 **Gara #{ $raceId }**
    📍 **{ $track }**
    📅 **Qualifiche: { $qualiDeadline } | Gara: { $raceTime }**

    🔗 [Vai alle Qualifiche]({ $qualiLink })

    Clicca sul pulsante per disabilitare le notifiche per questa gara

notif-quali-message-disabled = { $emoji } { $title }

    🏁 **Gara #{ $raceId }**
    📍 **{ $track }**
    📅 **Qualifiche: { $qualiDeadline } | Gara: { $raceTime }**

    🔗 [Vai alle Qualifiche]({ $qualiLink })

    ℹ️ **Notifiche automatiche disabilitate** per questa gara
    Clicca sul pulsante per riattivare le notifiche

notif-race-live = 🏁 **Gara #{ $raceId } è IN DIRETTA!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    🔗 [Guarda la Gara in Diretta]({ $raceLink })

notif-race-live-no-group = 🏁 **Gara #{ $raceId } è IN DIRETTA!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    ⚠️ Imposta il tuo gruppo in /settings per un link diretto!

    🔗 [Guarda la Gara in Diretta]({ $raceLink })

notif-race-replay = 📺 **Replay Gara #{ $raceId } Disponibile**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Se la gara è già stata calcolata, il replay è disponibile qui:

    🔗 [Guarda il Replay]({ $replayLink })

notif-race-replay-no-group = 📺 **Replay Gara #{ $raceId } Disponibile**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Se la gara è già stata calcolata, il replay è disponibile qui:

    ⚠️ Per link personalizzati, imposta il tuo gruppo in /settings!

    🔗 [Guarda il Replay]({ $replayLink })

notif-race-results = 📊 **Risultati Gara #{ $raceId } Disponibili**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    I risultati della gara sono ora disponibili:

    🔗 [Analisi della Gara]({ $analysisLink })
    🔗 [Riepilogo della Gara]({ $summaryLink })

notif-race-results-no-group = 📊 **Risultati Gara #{ $raceId } Disponibili**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    I risultati della gara sono ora disponibili:

    🔗 [Analisi della Gara]({ $analysisLink })

    ⚠️ Per il Riepilogo Gara personalizzato, imposta il tuo gruppo in /settings!

# =======================
# Meteo
# =======================
weather-title = 🌤️ **Previsioni Meteo Gara**
weather-practice-q1 = **Prova / Qualifica 1:** { $weather }
weather-temp-hum = Temp: { $temp }°C • Umidità: { $hum }%
weather-q2-start = **Qualifica 2 / Partenza Gara:** { $weather }
weather-q2-race-start = **Qualifica 2 / Partenza Gara:** { $weather }
weather-race-conditions = **Condizioni di Gara:**
weather-quarter = **{ $label }:**
weather-race-quarter = Temp: { $temp } • Umidità: { $hum }
    Probabilità di pioggia: { $rain }
weather-not-available = ⚠️ Dati meteo non disponibili
weather-unavailable = ⚠️ Dati meteo non disponibili
weather-cached = ℹ️ Meteo già in cache per **Gara #{ $raceId }: { $track }**

    Usa `/weather force` per forzare l'aggiornamento.
    Usa /status per vedere la notifica con il pulsante meteo.
weather-fetching = 🔄 Recupero meteo per **Gara #{ $raceId }: { $track }**...
weather-force-updating = 🔄 Aggiornamento forzato meteo per **Gara #{ $raceId }: { $track }**...
weather-success = ✅ Dati meteo recuperati per **Gara #{ $raceId }: { $track }**

    Usa /status per testare la notifica con il pulsante meteo!
weather-failed = ❌ Impossibile recuperare i dati meteo

    Verifica che il token API GPRO sia valido e che l'API di Prova sia disponibile.

weather-start-0h30m = **Partenza - 0h30m:**
weather-0h30m-1h00m = **0h30m - 1h00m:**
weather-1h00m-1h30m = **1h00m - 1h30m:**
weather-1h30m-2h00m = **1h30m - 2h00m:**
weather-temp-hum-range = Temp: { $temp } • Umidità: { $hum }
weather-rain-prob = Probabilità di pioggia: { $rain }

# =======================
# Admin
# =======================
admin-only = ❌ Solo admin
admin-calendar-updated = ✅ **Calendario**: { $count } gare
    🔄 **{ $userCount } utenti** reimpostati
admin-next-season-ready = 🌟 **Prossima stagione pronta!** { $count } gare
    Usa /next per visualizzare
admin-next-season-not-published = ℹ️ **Prossima stagione non pubblicata**
admin-users-count = 📊 **{ $count } utenti**:
admin-users-none = 📊 **0 utenti** nel database
admin-no-races = ❌ Nessuna gara nel calendario
admin-no-upcoming-races = ❌ Nessuna gara futura trovata

# =======================
# Errori & Validazione
# =======================
error-invalid-format = ❌ Formato non valido!

    Per favore usa:
    • **E** per Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** ecc.

    Riprova:

error-invalid-format-onboarding = ❌ Formato non valido!

    Per favore usa:
    • **E** per Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** ecc.

    Riprova o usa /start per ricominciare:

error-invalid-time = ❌ **Errore:** { $error }

    Per favore riprova con un formato valido come: `2h`, `30m`, o `1h 30m`

error-custom-notif-failed = ❌ **Errore:** { $error }

    Per favore riprova.

error-invalid-race = ❌ ID gara non valido
error-invalid-page = ❌ Pagina non valida
error-invalid-language = ❌ Lingua non valida
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
feedback-notif-enabled = ✅ { $label } attivata!
feedback-notif-disabled = ✅ { $label } disattivata!
feedback-quali-done = ✅ Fatto!
feedback-race-marked-done = ✅ *Gara segnata come completata!*
feedback-reset = 🔄 Reimpostato!
feedback-notifications-reset = 🔄 *Notifiche reimpostate!*
feedback-reenabled = 🔄 Riattivato!
feedback-notifications-reenabled = 🔄 *Notifiche riattivate!*
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
custom-notif-error-parsing = ❌ **Errore:** { $error }

    Per favore riprova con un formato valido come: `2h`, `30m`, o `1h 30m`
custom-notif-success = ✅ **{ $message }**

    La tua notifica personalizzata è stata impostata!
custom-notif-error-setting = ❌ **Errore:** { $error }

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
notif-menu-title = 🔔 **Impostazioni Notifiche**

    Clicca per attivare/disattivare le notifiche:
    ✅ = Attivo | ❌ = Disattivo

    ℹ️ *Questi sono interruttori globali per tutte le gare. Usa il pulsante 'Qualifica Completata' nelle notifiche per disabilitare una gara specifica.*

# =======================
# Menu Gruppo
# =======================
group-menu-title = 🏁 **Impostazioni Gruppo**

    Gruppo attuale: **{ $groupDisplay }**

    Inserisci il tuo gruppo in uno di questi formati:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    I numeri possono avere da 1 a 3 cifre.
group-reset-success = ✅ Gruppo reimpostato con successo

# =======================
# Menu Lingua
# =======================
lang-menu-title = 🌍 **Impostazioni Lingua**

    Attuale: { $currentLang }

    Seleziona la tua lingua preferita per i link delle gare GPRO:

# =======================
# Menu Notifiche Personalizzate
# =======================
custom-notif-menu-title = ⏱️ **Notifiche Personalizzate**

    Imposta i tuoi orari di notifica ({ $minTime }m - { $maxTime }h prima della chiusura delle qualifiche).

    Puoi avere fino a 2 notifiche personalizzate.

    Clicca su uno slot per impostarlo o modificarlo.

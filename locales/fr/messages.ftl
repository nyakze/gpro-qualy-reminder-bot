# GPRO Bot - Traductions Françaises

# =======================
# Commandes & Général
# =======================
start-welcome-new = 👋 <b>Bienvenue sur GPRO Bot !</b>

    Commençons la configuration. Choisissez d'abord votre langue préférée pour les liens de courses GPRO :

    🌍 <b>Sélectionnez votre langue</b> (ou passez pour utiliser l'anglais) :

start-welcome-onboarding = 👋 <b>Bienvenue sur GPRO Bot !</b>

    Choisissez la langue du bot :

start-welcome-existing = 🏁 GPRO Bot ACTIF !
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Que souhaitez-vous faire ?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Statut & Calendrier
# =======================
no-races-scheduled = 🔔 Aucune course programmée
no-upcoming-qualifications = 🔔 Aucune qualification programmée
next-season-not-published = 🌟 <b>La prochaine saison n'a pas encore été publiée</b>

calendar-title-full = 🏁 <b>Saison Complète</b>
calendar-title-next = 🌟 <b>PROCHAINE SAISON</b> ({ $count } courses)

# =======================
# Intégration
# =======================
onboard-group-title = 🏁 <b>Sélection de Groupe</b>

    Choisissez votre groupe GPRO pour recevoir des liens de courses personnalisés :

    Sélectionnez un groupe commun ou saisissez le vôtre :

onboard-group-custom = 🏁 <b>Sélection du Groupe (Optionnel)</b>

    Saisissez votre groupe dans l'un de ces formats :
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.

    💡 <i>La langue du site GPRO a été définie pour correspondre à la langue du bot. Vous pouvez la modifier ultérieurement dans /settings</i>

onboard-complete = ✅ <b>Configuration Terminée !</b>

    🏁 <b>GPRO Bot est prêt !</b>

    <b>Commandes disponibles :</b>
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

    💡 <i>Vous pouvez modifier ces paramètres à tout moment en utilisant /settings</i>

onboard-complete-with-group = ✅ <b>Configuration Terminée !</b>

    Groupe : <b>{ $group }</b>

    🏁 <b>GPRO Bot est prêt !</b>

    <b>Commandes disponibles :</b>
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

# =======================
# Paramètres
# =======================
settings-title = ⚙️ <b>Paramètres</b>

    Configurez vos préférences :

settings-language-title = 🌍 <b>Paramètres de Langue</b>

    Actuel : { $language }

    Sélectionnez votre langue préférée pour les liens de courses GPRO :

ui-lang-menu-title = 💬 <b>Langue du Bot</b>

    Sélectionnez la langue de l'interface du bot :

settings-group-title = 🏁 <b>Paramètres de Groupe</b>

    Groupe actuel : <b>{ $group }</b>

    Saisissez votre groupe dans l'un de ces formats :
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.

settings-group-set = ✅ <b>Groupe défini sur : { $group }</b>

    Les notifications de courses et de rediffusions incluront des liens directs vers votre groupe !

settings-notifications-title = 🔔 <b>Paramètres de Notifications</b>

    Cliquez pour activer/désactiver les notifications :
    ✅ = Activé | ❌ = Désactivé

    ℹ️ <i>Ce sont des interrupteurs globaux pour toutes les courses. Utilisez le bouton 'Qualifications Terminées' dans les notifications pour désactiver une course spécifique.</i>

settings-custom-notif-title = ⏱️ <b>Notifications Personnalisées</b>

    Définissez vos propres horaires de notification ({ $min }m - { $max }h avant la fermeture des qualifications).

    Vous pouvez avoir jusqu'à 2 notifications personnalisées.

    Cliquez sur un emplacement pour le configurer ou le modifier.

settings-custom-notif-edit = ⏱️ <b>Notification Personnalisée { $slot }</b>{ $current }
settings-custom-notif-current = Current:

    Sélectionnez un horaire prédéfini ou saisissez un horaire personnalisé :

settings-custom-notif-input = ⏱️ <b>Notification Personnalisée { $slot }</b>

    Saisissez votre horaire de notification personnalisé.

    <b>Formats acceptés :</b>
    • <code>20m</code> ou <code>45 minutes</code> (20m-70h)
    • <code>2h</code> ou <code>12 heures</code>
    • <code>1h 30m</code> ou <code>2h30m</code>

    <b>Exemples :</b>
    • <code>20m</code> - 20 minutes avant
    • <code>6h</code> - 6 heures avant
    • <code>1h 30m</code> - 1 heure et 30 minutes avant

# =======================
# Boutons
# =======================
button-ui-language = 💬 Langue du Bot : { $language }
button-gpro-language = 🌍 Langue GPRO : { $language }
button-language = 🌍 Langue : { $language }
button-group = 🏁 Groupe : { $group }
button-notifications = 🔔 Notifications
button-custom-notifications = ⏱️ Notifications Personnalisées
button-back = ◀ Retour
button-back-to-settings = ◀ Retour aux Paramètres
button-back-to-notifications = ◀ Retour aux Notifications
button-back-to-custom = ◀ Retour aux Notifications Personnalisées
button-back-custom-notif = ◀ Retour aux Notifications Personnalisées
button-main-menu = 🏠 Menu Principal
button-reset-group = 🔄 Réinitialiser le Groupe
button-custom-slot-set = ⏱️ Personnalisée { $slot } : { $time }
button-custom-slot-empty = ➕ Définir Notification Personnalisée { $slot }
button-previous = ◀ Précédent
button-next = Suivant ▶
button-skip = ⏭️ Passer
button-reset-language = 🔄 Réinitialiser par Défaut (Anglais)
button-enable-all = 🔔 Activer Toutes les Notifications
button-disable-all = 🔕 Désactiver Toutes les Notifications
button-enable-category = 🔔 Activer la Catégorie
button-disable-category = 🔕 Désactiver la Catégorie
button-quali-done = ✅ Qualifications Terminées
button-reenable-race = 🔄 Réactiver les notifications de la Course { $raceId }
button-weather = 🌤️ Afficher la Météo
button-snooze-5m = 🔔🔁 +5m
button-snooze-15m = 🔔🔁 +15m
button-snooze-30m = 🔔🔁 +30m
button-snooze-1h = 🔔🔁 +1h
button-snooze-2h = 🔔🔁 +2h
button-snooze-4h = 🔔🔁 +4h
button-snooze-8h = 🔔🔁 +8h
button-enter-custom-group = ✏️ Saisir un Groupe Personnalisé
button-enter-custom-time = ✏️ Saisir un Horaire Personnalisé
button-disable-notification = 🔕 Désactiver Cette Notification
button-cancel = ❌ Annuler
button-got-it = ✅ Compris !
button-try-again = 🔄 Réessayer

button-main-menu-status = 📊 Prochaine Course
button-main-menu-calendar = 📅 Saison Complète
button-main-menu-next = 🌟 Prochaine Saison
button-main-menu-settings = ⚙️ Paramètres

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Définir Notification Personnalisée { $slot }
button-custom-notif-time = ⏱️ Personnalisée { $slot } : { $time }

# =======================
# Notifications
# =======================
notif-category-before-qualifying = Avant les Qualifications
notif-category-qualifying-events = Événements de Qualification
notif-category-race-events = Événements de Course

notif-label-72h = 3j avant la fermeture des qualifications
notif-label-48h = 2j avant la fermeture des qualifications
notif-label-24h = 1j avant la fermeture des qualifications
notif-label-2h = 2h avant la fermeture des qualifications
notif-label-10min = 10min avant la fermeture des qualifications
notif-label-opens = Les qualifications sont ouvertes
notif-label-quali-results = Résultats des qualifications disponibles
notif-label-replay = Rediffusion de la course disponible
notif-label-live = Course en direct
notif-label-results = Résultats de la course disponibles

notif-label-opens-soon = Les qualifications sont ouvertes
notif-label-quali-results = Résultats des qualifications disponibles
notif-label-race-replay = Rediffusion de la course disponible
notif-label-race-live = Course en direct
notif-label-race-results = Résultats de la course disponibles

notif-quali-closes = <b>Les qualifications ferment dans { $time } !</b>
notif-quali-opens = <b>Les qualifications sont ouvertes</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifications ferment : { $qualiDeadline }</b>
    🏎 <b>Course : { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Aller aux Qualifications</a>

    <i>Cliquez sur le bouton '✅ Qualifications Terminées' pour désactiver les notifications de cette course</i>

notif-snooze-title = <b>Rappel (reporté)</b>

notif-snooze-message = { $emoji } { $title }

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifications ferment : { $qualiDeadline }</b>
    🏎 <b>Course : { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Aller aux Qualifications</a>

    <i>Cliquez sur le bouton '✅ Qualifications Terminées' pour désactiver les notifications de cette course</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Qualifications ferment : { $qualiDeadline }</b>
    🏎 <b>Course : { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Aller aux Qualifications</a>

    ℹ️ <b>Notifications automatiques désactivées</b> pour cette course
    <i>Cliquez sur le bouton '🔄 Réactiver' pour réactiver les notifications</i>

notif-quali-closed-title = <b>Qualifications actuellement fermées</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Qualifications fermées : { $qualiDeadline }</b>
    🏎 <b>Course : { $raceTime }</b>

    ⏳ <i>Les qualifications sont actuellement fermées. La prochaine session de qualifications s'ouvrira après la fin de la course en cours. Veuillez attendre le calcul de la course.</i>

notif-race-live = 🏁 <b>La Course #{ $raceId } est EN DIRECT !</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Regarder la Course en Direct</a>

notif-race-live-no-group = 🏁 <b>La Course #{ $raceId } est EN DIRECT !</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Définissez votre groupe dans /settings pour un lien direct !

    🔗 <a href="{ $raceLink }">Regarder la Course en Direct</a>

notif-race-replay = 📺 <b>Rediffusion de la Course #{ $raceId } Disponible</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Regardez la rediffusion de la course :

    🔗 <a href="{ $replayLink }">Regarder la Rediffusion</a>

notif-race-replay-no-group = 📺 <b>Rediffusion de la Course #{ $raceId } Disponible</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Regardez la rediffusion de la course :

    ⚠️ Pour des liens personnalisés, définissez votre groupe dans /settings !

    🔗 <a href="{ $replayLink }">Regarder la Rediffusion</a>

notif-race-results = 📊 <b>Résultats de la Course #{ $raceId } Disponibles</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Les résultats de la course sont maintenant disponibles :

    🔗 <a href="{ $analysisLink }">Analyse de la Course</a>
    🔗 <a href="{ $summaryLink }">Résumé de la Course</a>

notif-race-results-no-group = 📊 <b>Résultats de la Course #{ $raceId } Disponibles</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Les résultats de la course sont maintenant disponibles :

    🔗 <a href="{ $analysisLink }">Analyse de la Course</a>

    ⚠️ Pour le Résumé de Course personnalisé, définissez votre groupe dans /settings !

# =======================
# Météo
# =======================
weather-title = 🌤️ <b>Prévisions Météo de la Course</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Essais / Qualifications 1 :</b> { $weather }
weather-temp-hum = Temp : { $temp }°C • Hum : { $hum }%
weather-q2-start = <b>Qualifications 2 / Départ Course :</b> { $weather }
weather-q2-race-start = <b>Qualifications 2 / Départ Course :</b> { $weather }
weather-race-conditions = <b>Conditions de Course :</b>
weather-quarter = <b>{ $label } :</b>
weather-race-quarter = Temp : { $temp } • Humidité : { $hum }
    Probabilité de pluie : { $rain }
weather-not-available = ⚠️ Données météo non disponibles
weather-unavailable = ⚠️ Données météo non disponibles
weather-cached = ℹ️ Météo déjà en cache pour <b>Course #{ $raceId } : { $track }</b>

    Utilisez <code>/weather force</code> pour forcer la mise à jour.
    Utilisez /status pour voir la notification avec le bouton météo.
weather-fetching = 🔄 Récupération de la météo pour <b>Course #{ $raceId } : { $track }</b>...
weather-force-updating = 🔄 Mise à jour forcée de la météo pour <b>Course #{ $raceId } : { $track }</b>...
weather-success = ✅ Données météo récupérées pour <b>Course #{ $raceId } : { $track }</b>

    Utilisez /status pour tester la notification avec le bouton météo !
weather-failed = ❌ Impossible de récupérer les données météo

    Vérifiez que le jeton API GPRO est valide et que l'API d'Essais est disponible.

weather-start-0h30m = <b>Départ - 0h30m :</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m :</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m :</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m :</b>
weather-temp-hum-range = Temp : { $temp } • Hum : { $hum }
weather-rain-prob = Probabilité de pluie : { $rain }

# Conditions Météorologiques
weather-condition-sunny = Ensoleillé
weather-condition-partially-cloudy = Partiellement Nuageux
weather-condition-cloudy = Nuageux
weather-condition-very-cloudy = Très couvert
weather-condition-rain = Pluie

# =======================
# Admin
# =======================
admin-only = ❌ Administrateur uniquement
admin-calendar-updated = ✅ <b>Calendrier</b> : { $count } courses
    🔄 <b>{ $userCount } utilisateurs</b> réinitialisés
admin-next-season-ready = 🌟 <b>Prochaine saison prête !</b> { $count } courses
    Utilisez /next pour visualiser
admin-next-season-not-published = ℹ️ <b>Prochaine saison non publiée</b>
admin-users-count = 📊 <b>{ $count } utilisateurs</b> :
admin-users-none = 📊 <b>0 utilisateur</b> dans la base de données
admin-no-races = ❌ Aucune course dans le calendrier
admin-no-upcoming-races = ❌ Aucune course future trouvée

# =======================
# Erreurs & Validation
# =======================
error-invalid-format = ❌ Format invalide !

    Veuillez utiliser :
    • <b>E</b> pour Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Réessayez :

error-invalid-format-onboarding = ❌ Format invalide !

    Veuillez utiliser :
    • <b>E</b> pour Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Réessayez ou utilisez /start pour recommencer :

error-invalid-time = ❌ <b>Erreur :</b> { $error }

    Veuillez réessayer avec un format valide comme : <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Erreur :</b> { $error }

    Veuillez réessayer.

error-invalid-race = ❌ ID de course invalide
error-invalid-page = ❌ Page invalide
error-invalid-language = ❌ Langue invalide
error-invalid-category = ❌ Catégorie invalide
error-invalid-slot = ❌ Emplacement invalide
error-invalid-data = ❌ Données invalides
error-reset-failed = ❌ Réinitialisation échouée
error-race-not-found = ❌ Course non trouvée
error-weather-not-available = ⚠️ Données météo pas encore disponibles
error-weather-send-failed = ❌ Impossible d'envoyer la météo

# =======================
# Retours & Confirmations
# =======================
feedback-all-enabled = ✅ Toutes les notifications activées !
feedback-all-disabled = ✅ Toutes les notifications désactivées !
feedback-category-enabled = ✅ { $category } activée !
feedback-category-disabled = ✅ { $category } désactivée !
feedback-notif-enabled = ✅ { $label } activée !
feedback-notif-disabled = ✅ { $label } désactivée !
feedback-quali-done = ✅ Terminé !
feedback-race-marked-done = ✅ <i>Course marquée comme terminée !</i>
feedback-reset = 🔄 Réinitialisé !
feedback-notifications-reset = 🔄 <i>Notifications réinitialisées !</i>
feedback-reenabled = 🔄 Réactivé !
feedback-notifications-reenabled = 🔄 <i>Notifications réactivées !</i>
feedback-language-set = ✅ Langue définie sur { $language }
feedback-language-reset = ✅ Langue réinitialisée à { $language }
feedback-ui-language-set = ✅ Langue du bot définie sur { $language }
feedback-group-set = ✅ Groupe défini sur { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notification personnalisée { $slot } désactivée
feedback-skip-language = ⏭️ Utilisation de la langue détectée automatiquement: { $language }
feedback-skip-group = ⏭️ Sélection de groupe passée
feedback-welcome = ✅ Bienvenue !
feedback-weather-sent = 🌤️ Prévisions météo envoyées !
snooze-confirmed = 🔁⏰ Rappel déplacé à { $time }
snooze-max-reached = 🔁❌ Limite de report atteinte (3/3)
snooze-past-deadline = 🔁❌ Impossible de reporter au-delà du délai
snooze-past-next = 🔁❌ Prochain rappel dans { $minutes }min

# =======================
# Format de Temps
# =======================
# Abréviations des jours de la semaine (2 lettres)
weekday-mon = Lu
weekday-tue = Ma
weekday-wed = Me
weekday-thu = Je
weekday-fri = Ve
weekday-sat = Sa
weekday-sun = Di

time-minutes = { $minutes ->
    [one] { $minutes } minute
   *[other] { $minutes } minutes
}
time-hours = { $hours ->
    [one] { $hours } heure
   *[other] { $hours } heures
}
time-hours-minutes = { $hours ->
    [one] { $hours } heure
   *[other] { $hours } heures
} { $minutes ->
    [one] { $minutes } minute
   *[other] { $minutes } minutes
}
time-hours-minutes-short = { $hours }h{ $minutes }m
time-hours-short = { $hours }h
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }j{ $hours }h
time-days-hours-minutes-short = { $days }j{ $hours }h{ $minutes }m
time-days = { $days ->
    [one] { $days } jour
   *[other] { $days } jours
}
time-days-hours = { $days ->
    [one] { $days } jour
   *[other] { $days } jours
} { $hours ->
    [one] { $hours } heure
   *[other] { $hours } heures
}
time-months = { $months ->
    [one] { $months } mois
   *[other] { $months } mois
}
time-months-days = { $months ->
    [one] { $months } mois
   *[other] { $months } mois
} { $days ->
    [one] { $days } jour
   *[other] { $days } jours
}

# =======================
# Affichage de Groupe
# =======================
group-not-set = Non défini
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Messages de Notification Personnalisée
# =======================
custom-notif-set = Notification personnalisée { $slot } définie sur { $time }
custom-notif-set-success = Notification personnalisée { $slot } définie sur { $time }
custom-notif-not-set = Non définie
custom-notif-min-error = Le temps minimum est de 20 minutes
custom-notif-max-error = Le temps maximum est de 70 heures
custom-notif-invalid-slot = Emplacement invalide (doit être 0-{ $max })
custom-notif-empty-error = Le temps ne peut pas être vide
custom-notif-invalid-format = Format invalide. Utilisez : 2h, 30m, ou 1h 30m
custom-notif-enter-time = Veuillez saisir un temps
custom-notif-error-parsing = ❌ <b>Erreur :</b> { $error }

    Veuillez réessayer avec un format valide comme : <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Votre notification personnalisée a été définie !
custom-notif-error-setting = ❌ <b>Erreur :</b> { $error }

    Veuillez réessayer.

# =======================
# Validation
# =======================
validation-time-empty = Le temps ne peut pas être vide
validation-time-min = Le temps minimum est de 20 minutes
validation-time-max = Le temps maximum est de 70 heures
validation-enter-time = Veuillez saisir un temps
validation-invalid-format = Format invalide. Utilisez : 2h, 30m, ou 1h 30m
validation-invalid-slot = Emplacement invalide (doit être 0-{ $maxSlots })
validation-group-invalid-format = Format de groupe invalide. Utilisez : E, M1-5, P1-25, A1-80, R1-150
validation-group-e-no-numbers = Le groupe Elite n'a pas de groupes numérotés (utilisez 'E')
validation-group-range-m = Le groupe Master doit être 1-5
validation-group-range-p = Le groupe Pro doit être 1-25
validation-group-range-a = Le groupe Amateur doit être 1-80
validation-group-range-r = Le groupe Rookie doit être 1-150

# =======================
# Menu de Notifications
# =======================
notif-menu-title = 🔔 <b>Paramètres de Notifications</b>

    Cliquez pour activer/désactiver les notifications :
    ✅ = Activé | ❌ = Désactivé

    ℹ️ <i>Ce sont des interrupteurs globaux pour toutes les courses. Utilisez le bouton 'Qualifications Terminées' dans les notifications pour désactiver une course spécifique.</i>

# =======================
# Menu de Groupe
# =======================
group-menu-title = 🏁 <b>Paramètres de Groupe</b>

    Groupe actuel : <b>{ $groupDisplay }</b>

    Saisissez votre groupe dans l'un de ces formats :
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.
group-reset-success = ✅ Groupe réinitialisé avec succès

# =======================
# Menu de Langue
# =======================
lang-menu-title = 🌍 <b>Paramètres de Langue</b>

    Actuel : { $currentLang }

    Sélectionnez votre langue préférée pour les liens de courses GPRO :

# =======================
# Menu de Notifications Personnalisées
# =======================
custom-notif-menu-title = ⏱️ <b>Notifications Personnalisées</b>

    Définissez vos propres horaires de notification ({ $minTime }m - { $maxTime }h avant la fermeture des qualifications).

    Vous pouvez avoir jusqu'à 2 notifications personnalisées.

    Cliquez sur un emplacement pour le configurer ou le modifier.

# =======================
# Paramètres de Fuseau Horaire
# =======================
button-timezone = ⏰ Fuseau horaire: { $timezone }
button-website-mode = 🌐 Type de lien: { $mode }
website-mode-classic = Classique
timezone-menu-title = ⏰ <b>Paramètres de Fuseau Horaire</b>

    Fuseau horaire actuel: <b>{ $timezone }</b>

    Tapez votre fuseau horaire (nom de ville en anglais, abréviation ou décalage UTC):

    Exemples: <code>Paris</code>, <code>New York</code>, <code>UTC+1</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Sélectionnez votre fuseau horaire:</b>

    Correspondances pour "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Sélectionnez votre fuseau horaire:</b>

    Correspondances pour "{ $query }" (Page { $page }/{ $total }):

timezone-set-success = ✅ <b>Fuseau horaire défini!</b>

    { $timezone }

    Heure actuelle dans votre fuseau horaire: <b>{ $localTime }</b>

    Tous les horaires des courses seront affichés dans votre heure locale.

button-reset-timezone = 🔄 Réinitialiser à UTC
feedback-timezone-set = ✅ Fuseau horaire mis à jour
feedback-timezone-reset = ✅ Fuseau horaire réinitialisé à UTC
feedback-switched-to-app = Mode APP activé
feedback-switched-to-classic = Mode Classique activé
error-mode-switch-failed = ❌ Échec du changement de mode de site web
error-timezone-not-found = ❌ Aucun fuseau horaire trouvé pour "{ $query }"

    Essayez: nom de ville en anglais (Paris), abréviation (CET), ou décalage UTC (UTC+1)
error-invalid-timezone = ❌ Fuseau horaire invalide



notif-quali-results = 🏁 <b>Résultats des Qualifications - Course #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifications fermées</b>
    🏎 <b>Course: { $raceTime }</b>

    Résultats des qualifications disponibles:

    🔗 <a href="{ $gridLink }">Grille de Départ</a>

notif-quali-results-no-group = 🏁 <b>Résultats des Qualifications - Course #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualifications fermées</b>
    🏎 <b>Course: { $raceTime }</b>

    Résultats des qualifications disponibles:

    ⚠️ Pour des liens personnalisés, configurez votre groupe dans /settings!

    🔗 <a href="{ $gridLink }">Grille de Départ</a>

# =======================
# Rappel Nouvelle Saison
# =======================
notif-category-season-prep = Préparation Saison

notif-label-new-season-reminder = Rappel nouvelle saison

notif-new-season-reminder = 🌟 <b>Nouvelle Saison Commence!</b>

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Course: { $raceTime }</b>

    Votre groupe actuel: <b>{ $group }</b>

    💡 Si vous avez changé de groupe, mettez-le à jour dans /settings pour recevoir des liens personnalisés!

notif-new-season-reminder-no-group = 🌟 <b>Nouvelle Saison Commence!</b>

    🏁 <b>Course #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Course: { $raceTime }</b>

    ⚠️ Vous n'avez pas encore configuré votre groupe!

    💡 Configurez votre groupe dans /settings pour recevoir des liens de course personnalisés!

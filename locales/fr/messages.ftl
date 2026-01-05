# GPRO Bot - Traductions Françaises

# =======================
# Commandes & Général
# =======================
start-welcome-new = 👋 **Bienvenue sur GPRO Bot !**

    Commençons la configuration. Choisissez d'abord votre langue préférée pour les liens de courses GPRO :

    🌍 **Sélectionnez votre langue** (ou passez pour utiliser l'anglais) :

start-welcome-existing = 🏁 GPRO Bot ACTIF !
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

start-welcome-existing-buttons = 🏁 **GPRO Bot**

    Que souhaitez-vous faire ?

bot-live = 🏁 **GPRO Bot**

# =======================
# Statut & Calendrier
# =======================
no-races-scheduled = 🔔 Aucune course programmée
no-upcoming-qualifications = 🔔 Aucune qualification programmée
next-season-not-published = 🌟 **La prochaine saison n'a pas encore été publiée**

calendar-title-full = 🏁 **Saison Complète**
calendar-title-next = 🌟 **PROCHAINE SAISON** ({ $count } courses)

# =======================
# Intégration
# =======================
onboard-group-title = 🏁 **Sélection de Groupe**

    Choisissez votre groupe GPRO pour recevoir des liens de courses personnalisés :

    Sélectionnez un groupe commun ou saisissez le vôtre :

onboard-group-custom = 🏁 **Sélection du Groupe (Optionnel)**

    Saisissez votre groupe dans l'un de ces formats :
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.

    💡 *La langue du site GPRO a été définie pour correspondre à la langue du bot. Vous pouvez la modifier ultérieurement dans /settings*

onboard-complete = ✅ **Configuration Terminée !**

    🏁 **GPRO Bot est prêt !**

    **Commandes disponibles :**
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

    💡 *Vous pouvez modifier ces paramètres à tout moment en utilisant /settings*

onboard-complete-with-group = ✅ **Configuration Terminée !**

    Groupe : **{ $group }**

    🏁 **GPRO Bot est prêt !**

    **Commandes disponibles :**
    /status - Prochaine course
    /calendar - Saison complète
    /next - Prochaine saison
    /settings - Préférences

# =======================
# Paramètres
# =======================
settings-title = ⚙️ **Paramètres**

    Configurez vos préférences :

settings-language-title = 🌍 **Paramètres de Langue**

    Actuel : { $language }

    Sélectionnez votre langue préférée pour les liens de courses GPRO :

ui-lang-menu-title = 💬 **Langue du Bot**

    Sélectionnez la langue de l'interface du bot :

settings-group-title = 🏁 **Paramètres de Groupe**

    Groupe actuel : **{ $group }**

    Saisissez votre groupe dans l'un de ces formats :
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.

settings-group-set = ✅ **Groupe défini sur : { $group }**

    Les notifications de courses et de rediffusions incluront des liens directs vers votre groupe !

settings-notifications-title = 🔔 **Paramètres de Notifications**

    Cliquez pour activer/désactiver les notifications :
    ✅ = Activé | ❌ = Désactivé

    ℹ️ *Ce sont des interrupteurs globaux pour toutes les courses. Utilisez le bouton 'Qualifications Terminées' dans les notifications pour désactiver une course spécifique.*

settings-custom-notif-title = ⏱️ **Notifications Personnalisées**

    Définissez vos propres horaires de notification ({ $min }m - { $max }h avant la fermeture des qualifications).

    Vous pouvez avoir jusqu'à 2 notifications personnalisées.

    Cliquez sur un emplacement pour le configurer ou le modifier.

settings-custom-notif-edit = ⏱️ **Notification Personnalisée { $slot }**{ $current }

    Sélectionnez un horaire prédéfini ou saisissez un horaire personnalisé :

settings-custom-notif-input = ⏱️ **Notification Personnalisée { $slot }**

    Saisissez votre horaire de notification personnalisé.

    **Formats acceptés :**
    • `20m` ou `45 minutes` (20m-70h)
    • `2h` ou `12 heures`
    • `1h 30m` ou `2h30m`

    **Exemples :**
    • `20m` - 20 minutes avant
    • `6h` - 6 heures avant
    • `1h 30m` - 1 heure et 30 minutes avant

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
button-quali-done = ✅ Qualifications Terminées
button-reenable-race = 🔄 Réactiver les notifications de la Course { $raceId }
button-weather = 🌤️ Afficher la Météo
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
notif-label-72h = 3j avant la fermeture des qualifications
notif-label-48h = 2j avant la fermeture des qualifications
notif-label-24h = 1j avant la fermeture des qualifications
notif-label-2h = 2h avant la fermeture des qualifications
notif-label-10min = 10min avant la fermeture des qualifications
notif-label-opens = Les qualifications sont ouvertes
notif-label-replay = Rediffusion de la course disponible
notif-label-live = Course en direct
notif-label-results = Résultats de la course disponibles

notif-label-opens-soon = Les qualifications sont ouvertes
notif-label-race-replay = Rediffusion de la course disponible
notif-label-race-live = Course en direct
notif-label-race-results = Résultats de la course disponibles

notif-quali-closes = **Les qualifications ferment dans { $time } !**
notif-quali-opens = **Les qualifications sont ouvertes (ou vont s'ouvrir bientôt)**

notif-quali-message = { $emoji } { $title }

    🏁 **Course #{ $raceId }**
    📍 **{ $track }**
    📅 **Qualifications : { $qualiDeadline } | Course : { $raceTime }**

    🔗 [Aller aux Qualifications]({ $qualiLink })

    Cliquez sur le bouton pour désactiver les notifications pour cette course

notif-quali-message-disabled = { $emoji } { $title }

    🏁 **Course #{ $raceId }**
    📍 **{ $track }**
    📅 **Qualifications : { $qualiDeadline } | Course : { $raceTime }**

    🔗 [Aller aux Qualifications]({ $qualiLink })

    ℹ️ **Notifications automatiques désactivées** pour cette course
    Cliquez sur le bouton pour réactiver les notifications

notif-race-live = 🏁 **La Course #{ $raceId } est EN DIRECT !**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    🔗 [Regarder la Course en Direct]({ $raceLink })

notif-race-live-no-group = 🏁 **La Course #{ $raceId } est EN DIRECT !**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    ⚠️ Définissez votre groupe dans /settings pour un lien direct !

    🔗 [Regarder la Course en Direct]({ $raceLink })

notif-race-replay = 📺 **Rediffusion de la Course #{ $raceId } Disponible**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Si la course a déjà été calculée, la rediffusion est disponible ici :

    🔗 [Regarder la Rediffusion]({ $replayLink })

notif-race-replay-no-group = 📺 **Rediffusion de la Course #{ $raceId } Disponible**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Si la course a déjà été calculée, la rediffusion est disponible ici :

    ⚠️ Pour des liens personnalisés, définissez votre groupe dans /settings !

    🔗 [Regarder la Rediffusion]({ $replayLink })

notif-race-results = 📊 **Résultats de la Course #{ $raceId } Disponibles**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Les résultats de la course sont maintenant disponibles :

    🔗 [Analyse de la Course]({ $analysisLink })
    🔗 [Résumé de la Course]({ $summaryLink })

notif-race-results-no-group = 📊 **Résultats de la Course #{ $raceId } Disponibles**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Les résultats de la course sont maintenant disponibles :

    🔗 [Analyse de la Course]({ $analysisLink })

    ⚠️ Pour le Résumé de Course personnalisé, définissez votre groupe dans /settings !

# =======================
# Météo
# =======================
weather-title = 🌤️ **Prévisions Météo de la Course**
weather-practice-q1 = **Essais / Qualifications 1 :** { $weather }
weather-temp-hum = Temp : { $temp }°C • Humidité : { $hum }%
weather-q2-start = **Qualifications 2 / Départ Course :** { $weather }
weather-q2-race-start = **Qualifications 2 / Départ Course :** { $weather }
weather-race-conditions = **Conditions de Course :**
weather-quarter = **{ $label } :**
weather-race-quarter = Temp : { $temp } • Humidité : { $hum }
    Probabilité de pluie : { $rain }
weather-not-available = ⚠️ Données météo non disponibles
weather-unavailable = ⚠️ Données météo non disponibles
weather-cached = ℹ️ Météo déjà en cache pour **Course #{ $raceId } : { $track }**

    Utilisez `/weather force` pour forcer la mise à jour.
    Utilisez /status pour voir la notification avec le bouton météo.
weather-fetching = 🔄 Récupération de la météo pour **Course #{ $raceId } : { $track }**...
weather-force-updating = 🔄 Mise à jour forcée de la météo pour **Course #{ $raceId } : { $track }**...
weather-success = ✅ Données météo récupérées pour **Course #{ $raceId } : { $track }**

    Utilisez /status pour tester la notification avec le bouton météo !
weather-failed = ❌ Impossible de récupérer les données météo

    Vérifiez que le jeton API GPRO est valide et que l'API d'Essais est disponible.

weather-start-0h30m = **Départ - 0h30m :**
weather-0h30m-1h00m = **0h30m - 1h00m :**
weather-1h00m-1h30m = **1h00m - 1h30m :**
weather-1h30m-2h00m = **1h30m - 2h00m :**
weather-temp-hum-range = Temp : { $temp } • Humidité : { $hum }
weather-rain-prob = Probabilité de pluie : { $rain }

# =======================
# Admin
# =======================
admin-only = ❌ Administrateur uniquement
admin-calendar-updated = ✅ **Calendrier** : { $count } courses
    🔄 **{ $userCount } utilisateurs** réinitialisés
admin-next-season-ready = 🌟 **Prochaine saison prête !** { $count } courses
    Utilisez /next pour visualiser
admin-next-season-not-published = ℹ️ **Prochaine saison non publiée**
admin-users-count = 📊 **{ $count } utilisateurs** :
admin-users-none = 📊 **0 utilisateur** dans la base de données
admin-no-races = ❌ Aucune course dans le calendrier
admin-no-upcoming-races = ❌ Aucune course future trouvée

# =======================
# Erreurs & Validation
# =======================
error-invalid-format = ❌ Format invalide !

    Veuillez utiliser :
    • **E** pour Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Réessayez :

error-invalid-format-onboarding = ❌ Format invalide !

    Veuillez utiliser :
    • **E** pour Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Réessayez ou utilisez /start pour recommencer :

error-invalid-time = ❌ **Erreur :** { $error }

    Veuillez réessayer avec un format valide comme : `2h`, `30m`, ou `1h 30m`

error-custom-notif-failed = ❌ **Erreur :** { $error }

    Veuillez réessayer.

error-invalid-race = ❌ ID de course invalide
error-invalid-page = ❌ Page invalide
error-invalid-language = ❌ Langue invalide
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
feedback-notif-enabled = ✅ { $label } activée !
feedback-notif-disabled = ✅ { $label } désactivée !
feedback-quali-done = ✅ Terminé !
feedback-race-marked-done = ✅ *Course marquée comme terminée !*
feedback-reset = 🔄 Réinitialisé !
feedback-notifications-reset = 🔄 *Notifications réinitialisées !*
feedback-reenabled = 🔄 Réactivé !
feedback-notifications-reenabled = 🔄 *Notifications réactivées !*
feedback-language-set = ✅ Langue définie sur { $language }
feedback-language-reset = ✅ Langue réinitialisée à l'anglais
feedback-ui-language-set = ✅ Langue du bot définie sur { $language }
feedback-group-set = ✅ Groupe défini sur { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notification personnalisée { $slot } désactivée
feedback-skip-language = ⏭️ Utilisation de la langue par défaut (anglais)
feedback-skip-group = ⏭️ Sélection de groupe passée
feedback-welcome = ✅ Bienvenue !
feedback-weather-sent = 🌤️ Prévisions météo envoyées !

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
custom-notif-error-parsing = ❌ **Erreur :** { $error }

    Veuillez réessayer avec un format valide comme : `2h`, `30m`, ou `1h 30m`
custom-notif-success = ✅ **{ $message }**

    Votre notification personnalisée a été définie !
custom-notif-error-setting = ❌ **Erreur :** { $error }

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

# =======================
# Menu de Notifications
# =======================
notif-menu-title = 🔔 **Paramètres de Notifications**

    Cliquez pour activer/désactiver les notifications :
    ✅ = Activé | ❌ = Désactivé

    ℹ️ *Ce sont des interrupteurs globaux pour toutes les courses. Utilisez le bouton 'Qualifications Terminées' dans les notifications pour désactiver une course spécifique.*

# =======================
# Menu de Groupe
# =======================
group-menu-title = 🏁 **Paramètres de Groupe**

    Groupe actuel : **{ $groupDisplay }**

    Saisissez votre groupe dans l'un de ces formats :
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Les numéros peuvent comporter de 1 à 3 chiffres.
group-reset-success = ✅ Groupe réinitialisé avec succès

# =======================
# Menu de Langue
# =======================
lang-menu-title = 🌍 **Paramètres de Langue**

    Actuel : { $currentLang }

    Sélectionnez votre langue préférée pour les liens de courses GPRO :

# =======================
# Menu de Notifications Personnalisées
# =======================
custom-notif-menu-title = ⏱️ **Notifications Personnalisées**

    Définissez vos propres horaires de notification ({ $minTime }m - { $maxTime }h avant la fermeture des qualifications).

    Vous pouvez avoir jusqu'à 2 notifications personnalisées.

    Cliquez sur un emplacement pour le configurer ou le modifier.

# =======================
# Paramètres de Fuseau Horaire
# =======================
button-timezone = ⏰ Fuseau horaire: { $timezone }
timezone-menu-title = ⏰ **Paramètres de Fuseau Horaire**

    Fuseau horaire actuel: **{ $timezone }**

    Tapez votre fuseau horaire (nom de ville en anglais, abréviation ou décalage UTC):

    Exemples: `Paris`, `New York`, `UTC+1`, `London`

timezone-select-matches = 🌍 **Sélectionnez votre fuseau horaire:**

    Correspondances pour "{ $query }":

timezone-select-matches-paginated = 🌍 **Sélectionnez votre fuseau horaire:**

    Correspondances pour "{ $query }" (Page { $page }/{ $total }):

timezone-set-success = ✅ **Fuseau horaire défini!**

    { $timezone }

    Heure actuelle dans votre fuseau horaire: **{ $localTime }**

    Tous les horaires des courses seront affichés dans votre heure locale.

button-reset-timezone = 🔄 Réinitialiser à UTC
feedback-timezone-set = ✅ Fuseau horaire mis à jour
feedback-timezone-reset = ✅ Fuseau horaire réinitialisé à UTC
error-timezone-not-found = ❌ Aucun fuseau horaire trouvé pour "{ $query }"

    Essayez: nom de ville en anglais (Paris), abréviation (CET), ou décalage UTC (UTC+1)
error-invalid-timezone = ❌ Fuseau horaire invalide

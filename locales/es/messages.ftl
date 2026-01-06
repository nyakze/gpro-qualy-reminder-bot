# GPRO Bot - Traducciones en Español

# =======================
# Comandos & General
# =======================
start-welcome-new = 👋 <b>¡Bienvenido a GPRO Bot!</b>

    Vamos a configurar todo. Primero elige tu idioma preferido para los enlaces de carreras de GPRO:

    🌍 <b>Selecciona tu idioma</b> (o omite para usar inglés):

start-welcome-existing = 🏁 ¡GPRO Bot ACTIVO!
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    ¿Qué te gustaría hacer?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Estado & Calendario
# =======================
no-races-scheduled = 🔔 No hay carreras programadas
no-upcoming-qualifications = 🔔 No hay clasificaciones programadas
next-season-not-published = 🌟 <b>La próxima temporada aún no se ha publicado</b>

calendar-title-full = 🏁 <b>Temporada Completa</b>
calendar-title-next = 🌟 <b>PRÓXIMA TEMPORADA</b> ({ $count } carreras)

# =======================
# Incorporación
# =======================
onboard-group-title = 🏁 <b>Selección de Grupo</b>

    Elige tu grupo GPRO para recibir enlaces personalizados de carreras:

    Selecciona un grupo común o ingresa el tuyo:

onboard-group-custom = 🏁 <b>Selección de Grupo (Opcional)</b>

    Ingresa tu grupo en uno de estos formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.

    💡 <i>El idioma del sitio GPRO se ha configurado para coincidir con el idioma del bot. Puedes cambiarlo más tarde en /settings</i>

onboard-complete = ✅ <b>¡Configuración Completada!</b>

    🏁 <b>¡GPRO Bot está listo!</b>

    <b>Comandos disponibles:</b>
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

    💡 <i>Puedes cambiar estas configuraciones en cualquier momento usando /settings</i>

onboard-complete-with-group = ✅ <b>¡Configuración Completada!</b>

    Grupo: <b>{ $group }</b>

    🏁 <b>¡GPRO Bot está listo!</b>

    <b>Comandos disponibles:</b>
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

# =======================
# Configuración
# =======================
settings-title = ⚙️ <b>Configuración</b>

    Configura tus preferencias:

settings-language-title = 🌍 <b>Configuración de Idioma</b>

    Actual: { $language }

    Selecciona tu idioma preferido para los enlaces de carreras de GPRO:

ui-lang-menu-title = 💬 <b>Idioma del Bot</b>

    Selecciona el idioma de la interfaz del bot:

settings-group-title = 🏁 <b>Configuración de Grupo</b>

    Grupo actual: <b>{ $group }</b>

    Ingresa tu grupo en uno de estos formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.

settings-group-set = ✅ <b>Grupo establecido en: { $group }</b>

    ¡Las notificaciones de carreras y repeticiones incluirán enlaces directos a tu grupo!

settings-notifications-title = 🔔 <b>Configuración de Notificaciones</b>

    Haz clic para activar/desactivar notificaciones:
    ✅ = Activado | ❌ = Desactivado

    ℹ️ <i>Estos son interruptores globales para todas las carreras. Usa el botón 'Clasificación Completada' en las notificaciones para desactivar una carrera específica.</i>

settings-custom-notif-title = ⏱️ <b>Notificaciones Personalizadas</b>

    Establece tus propios horarios de notificación ({ $min }m - { $max }h antes del cierre de la clasificación).

    Puedes tener hasta 2 notificaciones personalizadas.

    Haz clic en un espacio para configurarlo o editarlo.

settings-custom-notif-edit = ⏱️ <b>Notificación Personalizada { $slot }</b>{ $current }
settings-custom-notif-current = Current:

    Selecciona un horario predefinido o ingresa un horario personalizado:

settings-custom-notif-input = ⏱️ <b>Notificación Personalizada { $slot }</b>

    Ingresa tu horario de notificación personalizado.

    <b>Formatos aceptados:</b>
    • <code>20m</code> o <code>45 minutos</code> (20m-70h)
    • <code>2h</code> o <code>12 horas</code>
    • <code>1h 30m</code> o <code>2h30m</code>

    <b>Ejemplos:</b>
    • <code>20m</code> - 20 minutos antes
    • <code>6h</code> - 6 horas antes
    • <code>1h 30m</code> - 1 hora y 30 minutos antes

# =======================
# Botones
# =======================
button-ui-language = 💬 Idioma del Bot: { $language }
button-gpro-language = 🌍 Idioma GPRO: { $language }
button-language = 🌍 Idioma: { $language }
button-group = 🏁 Grupo: { $group }
button-notifications = 🔔 Notificaciones
button-custom-notifications = ⏱️ Notificaciones Personalizadas
button-back = ◀ Atrás
button-back-to-settings = ◀ Volver a Configuración
button-back-to-notifications = ◀ Volver a Notificaciones
button-back-to-custom = ◀ Volver a Notificaciones Personalizadas
button-back-custom-notif = ◀ Volver a Notificaciones Personalizadas
button-main-menu = 🏠 Menú Principal
button-reset-group = 🔄 Restablecer Grupo
button-custom-slot-set = ⏱️ Personalizada { $slot }: { $time }
button-custom-slot-empty = ➕ Establecer Notificación Personalizada { $slot }
button-previous = ◀ Anterior
button-next = Siguiente ▶
button-skip = ⏭️ Omitir
button-reset-language = 🔄 Restablecer a Predeterminado (Inglés)
button-enable-all = 🔔 Activar Todas las Notificaciones
button-disable-all = 🔕 Desactivar Todas las Notificaciones
button-quali-done = ✅ Clasificación Completada
button-reenable-race = 🔄 Reactivar notificaciones de la Carrera { $raceId }
button-weather = 🌤️ Mostrar Clima
button-enter-custom-group = ✏️ Ingresar Grupo Personalizado
button-enter-custom-time = ✏️ Ingresar Horario Personalizado
button-disable-notification = 🔕 Desactivar Esta Notificación
button-cancel = ❌ Cancelar
button-got-it = ✅ ¡Entendido!
button-try-again = 🔄 Intentar de Nuevo

button-main-menu-status = 📊 Próxima Carrera
button-main-menu-calendar = 📅 Temporada Completa
button-main-menu-next = 🌟 Próxima Temporada
button-main-menu-settings = ⚙️ Configuración

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Establecer Notificación Personalizada { $slot }
button-custom-notif-time = ⏱️ Personalizada { $slot }: { $time }

# =======================
# Notificaciones
# =======================
notif-label-72h = 3d antes del cierre de la clasificación
notif-label-48h = 2d antes del cierre de la clasificación
notif-label-24h = 1d antes del cierre de la clasificación
notif-label-2h = 2h antes del cierre de la clasificación
notif-label-10min = 10min antes del cierre de la clasificación
notif-label-opens = La clasificación está abierta
notif-label-quali-results = Resultados de clasificación disponibles
notif-label-replay = Repetición de la carrera disponible
notif-label-live = Carrera en vivo
notif-label-results = Resultados de la carrera disponibles

notif-label-opens-soon = La clasificación está abierta
notif-label-quali-results = Resultados de clasificación disponibles
notif-label-race-replay = Repetición de la carrera disponible
notif-label-race-live = Carrera en vivo
notif-label-race-results = Resultados de la carrera disponibles

notif-quali-closes = <b>¡La clasificación cierra en { $time }!</b>
notif-quali-opens = <b>La clasificación está abierta (o se abrirá pronto)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Carrera #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Clasificación cierra: { $qualiDeadline }</b>
    🏎 <b>Carrera: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir a la Clasificación</a>

    <i>Haz clic en el botón '✅ Clasificación Completada' para desactivar las notificaciones de esta carrera</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Carrera #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Clasificación cierra: { $qualiDeadline }</b>
    🏎 <b>Carrera: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir a la Clasificación</a>

    ℹ️ <b>Notificaciones automáticas desactivadas</b> para esta carrera
    <i>Haz clic en el botón '🔄 Reactivar' para reactivar las notificaciones</i>

notif-race-live = 🏁 <b>¡La Carrera #{ $raceId } está EN VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Ver Carrera en Vivo</a>

notif-race-live-no-group = 🏁 <b>¡La Carrera #{ $raceId } está EN VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ ¡Establece tu grupo en /settings para un enlace directo!

    🔗 <a href="{ $raceLink }">Ver Carrera en Vivo</a>

notif-race-replay = 📺 <b>Repetición de la Carrera #{ $raceId } Disponible</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Si la carrera ya se ha calculado, la repetición está disponible aquí:

    🔗 <a href="{ $replayLink }">Ver Repetición</a>

notif-race-replay-no-group = 📺 <b>Repetición de la Carrera #{ $raceId } Disponible</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Si la carrera ya se ha calculado, la repetición está disponible aquí:

    ⚠️ ¡Para enlaces personalizados, establece tu grupo en /settings!

    🔗 <a href="{ $replayLink }">Ver Repetición</a>

notif-race-results = 📊 <b>Resultados de la Carrera #{ $raceId } Disponibles</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Los resultados de la carrera ya están disponibles:

    🔗 <a href="{ $analysisLink }">Análisis de la Carrera</a>
    🔗 <a href="{ $summaryLink }">Resumen de la Carrera</a>

notif-race-results-no-group = 📊 <b>Resultados de la Carrera #{ $raceId } Disponibles</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Los resultados de la carrera ya están disponibles:

    🔗 <a href="{ $analysisLink }">Análisis de la Carrera</a>

    ⚠️ ¡Para el Resumen de Carrera personalizado, establece tu grupo en /settings!

# =======================
# Clima
# =======================
weather-title = 🌤️ <b>Pronóstico del Clima de la Carrera</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Práctica / Clasificación 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Humedad: { $hum }%
weather-q2-start = <b>Clasificación 2 / Inicio de Carrera:</b> { $weather }
weather-q2-race-start = <b>Clasificación 2 / Inicio de Carrera:</b> { $weather }
weather-race-conditions = <b>Condiciones de Carrera:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Humedad: { $hum }
    Probabilidad de lluvia: { $rain }
weather-not-available = ⚠️ Datos del clima no disponibles
weather-unavailable = ⚠️ Datos del clima no disponibles
weather-cached = ℹ️ Clima ya en caché para <b>Carrera #{ $raceId }: { $track }</b>

    Usa <code>/weather force</code> para forzar la actualización.
    Usa /status para ver la notificación con el botón del clima.
weather-fetching = 🔄 Obteniendo clima para <b>Carrera #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Forzando actualización del clima para <b>Carrera #{ $raceId }: { $track }</b>...
weather-success = ✅ Datos del clima obtenidos para <b>Carrera #{ $raceId }: { $track }</b>

    ¡Usa /status para probar la notificación con el botón del clima!
weather-failed = ❌ No se pudieron obtener los datos del clima

    Verifica que el token de la API de GPRO sea válido y que la API de Práctica esté disponible.

weather-start-0h30m = <b>Inicio - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Temp: { $temp } • Humedad: { $hum }
weather-rain-prob = Probabilidad de lluvia: { $rain }

# Condiciones Meteorológicas
weather-condition-sunny = Soleado
weather-condition-partially-cloudy = Parcialmente Nublado
weather-condition-cloudy = Nublado
weather-condition-very-cloudy = Cubierto
weather-condition-rain = Lluvia

# =======================
# Admin
# =======================
admin-only = ❌ Solo admin
admin-calendar-updated = ✅ <b>Calendario</b>: { $count } carreras
    🔄 <b>{ $userCount } usuarios</b> restablecidos
admin-next-season-ready = 🌟 <b>¡Próxima temporada lista!</b> { $count } carreras
    Usa /next para ver
admin-next-season-not-published = ℹ️ <b>Próxima temporada no publicada</b>
admin-users-count = 📊 <b>{ $count } usuarios</b>:
admin-users-none = 📊 <b>0 usuarios</b> en la base de datos
admin-no-races = ❌ No hay carreras en el calendario
admin-no-upcoming-races = ❌ No se encontraron carreras futuras

# =======================
# Errores & Validación
# =======================
error-invalid-format = ❌ ¡Formato inválido!

    Por favor usa:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Inténtalo de nuevo:

error-invalid-format-onboarding = ❌ ¡Formato inválido!

    Por favor usa:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Inténtalo de nuevo o usa /start para reiniciar:

error-invalid-time = ❌ <b>Error:</b> { $error }

    Por favor inténtalo de nuevo con un formato válido como: <code>2h</code>, <code>30m</code>, o <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Error:</b> { $error }

    Por favor inténtalo de nuevo.

error-invalid-race = ❌ ID de carrera inválido
error-invalid-page = ❌ Página inválida
error-invalid-language = ❌ Idioma inválido
error-invalid-slot = ❌ Espacio inválido
error-invalid-data = ❌ Datos inválidos
error-reset-failed = ❌ Restablecimiento fallido
error-race-not-found = ❌ Carrera no encontrada
error-weather-not-available = ⚠️ Datos del clima aún no disponibles
error-weather-send-failed = ❌ No se pudo enviar el clima

# =======================
# Retroalimentación & Confirmaciones
# =======================
feedback-all-enabled = ✅ ¡Todas las notificaciones activadas!
feedback-all-disabled = ✅ ¡Todas las notificaciones desactivadas!
feedback-notif-enabled = ✅ ¡{ $label } activada!
feedback-notif-disabled = ✅ ¡{ $label } desactivada!
feedback-quali-done = ✅ ¡Hecho!
feedback-race-marked-done = ✅ <i>¡Carrera marcada como completada!</i>
feedback-reset = 🔄 ¡Restablecido!
feedback-notifications-reset = 🔄 <i>¡Notificaciones restablecidas!</i>
feedback-reenabled = 🔄 ¡Reactivado!
feedback-notifications-reenabled = 🔄 <i>¡Notificaciones reactivadas!</i>
feedback-language-set = ✅ Idioma establecido en { $language }
feedback-language-reset = ✅ Idioma restablecido a inglés
feedback-ui-language-set = ✅ Idioma del bot establecido en { $language }
feedback-group-set = ✅ Grupo establecido en { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notificación personalizada { $slot } desactivada
feedback-skip-language = ⏭️ Usando idioma predeterminado (inglés)
feedback-skip-group = ⏭️ Selección de grupo omitida
feedback-welcome = ✅ ¡Bienvenido!
feedback-weather-sent = 🌤️ ¡Pronóstico del clima enviado!

# =======================
# Formato de Tiempo
# =======================
# Abreviaciones de días de la semana (2 letras)
weekday-mon = Lu
weekday-tue = Ma
weekday-wed = Mi
weekday-thu = Ju
weekday-fri = Vi
weekday-sat = Sá
weekday-sun = Do

time-minutes = { $minutes ->
    [one] { $minutes } minuto
   *[other] { $minutes } minutos
}
time-hours = { $hours ->
    [one] { $hours } hora
   *[other] { $hours } horas
}
time-hours-minutes = { $hours ->
    [one] { $hours } hora
   *[other] { $hours } horas
} { $minutes ->
    [one] { $minutes } minuto
   *[other] { $minutes } minutos
}
time-hours-minutes-short = { $hours }h{ $minutes }m
time-hours-short = { $hours }h
time-minutes-short = { $minutes }m
time-days-hours-short = { $days }d{ $hours }h
time-days-hours-minutes-short = { $days }d{ $hours }h{ $minutes }m
time-days = { $days ->
    [one] { $days } día
   *[other] { $days } días
}
time-days-hours = { $days ->
    [one] { $days } día
   *[other] { $days } días
} { $hours ->
    [one] { $hours } hora
   *[other] { $hours } horas
}
time-months = { $months ->
    [one] { $months } mes
   *[other] { $months } meses
}
time-months-days = { $months ->
    [one] { $months } mes
   *[other] { $months } meses
} { $days ->
    [one] { $days } día
   *[other] { $days } días
}

# =======================
# Visualización de Grupo
# =======================
group-not-set = No establecido
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Mensajes de Notificación Personalizada
# =======================
custom-notif-set = Notificación personalizada { $slot } establecida en { $time }
custom-notif-set-success = Notificación personalizada { $slot } establecida en { $time }
custom-notif-not-set = No establecida
custom-notif-min-error = El tiempo mínimo es de 20 minutos
custom-notif-max-error = El tiempo máximo es de 70 horas
custom-notif-invalid-slot = Espacio inválido (debe ser 0-{ $max })
custom-notif-empty-error = El tiempo no puede estar vacío
custom-notif-invalid-format = Formato inválido. Usa: 2h, 30m, o 1h 30m
custom-notif-enter-time = Por favor ingresa un tiempo
custom-notif-error-parsing = ❌ <b>Error:</b> { $error }

    Por favor inténtalo de nuevo con un formato válido como: <code>2h</code>, <code>30m</code>, o <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    ¡Tu notificación personalizada ha sido establecida!
custom-notif-error-setting = ❌ <b>Error:</b> { $error }

    Por favor inténtalo de nuevo.

# =======================
# Validación
# =======================
validation-time-empty = El tiempo no puede estar vacío
validation-time-min = El tiempo mínimo es de 20 minutos
validation-time-max = El tiempo máximo es de 70 horas
validation-enter-time = Por favor ingresa un tiempo
validation-invalid-format = Formato inválido. Usa: 2h, 30m, o 1h 30m
validation-invalid-slot = Espacio inválido (debe ser 0-{ $maxSlots })

# =======================
# Menú de Notificaciones
# =======================
notif-menu-title = 🔔 <b>Configuración de Notificaciones</b>

    Haz clic para activar/desactivar notificaciones:
    ✅ = Activado | ❌ = Desactivado

    ℹ️ <i>Estos son interruptores globales para todas las carreras. Usa el botón 'Clasificación Completada' en las notificaciones para desactivar una carrera específica.</i>

# =======================
# Menú de Grupo
# =======================
group-menu-title = 🏁 <b>Configuración de Grupo</b>

    Grupo actual: <b>{ $groupDisplay }</b>

    Ingresa tu grupo en uno de estos formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.
group-reset-success = ✅ Grupo restablecido con éxito

# =======================
# Menú de Idioma
# =======================
lang-menu-title = 🌍 <b>Configuración de Idioma</b>

    Actual: { $currentLang }

    Selecciona tu idioma preferido para los enlaces de carreras de GPRO:

# =======================
# Menú de Notificaciones Personalizadas
# =======================
custom-notif-menu-title = ⏱️ <b>Notificaciones Personalizadas</b>

    Establece tus propios horarios de notificación ({ $minTime }m - { $maxTime }h antes del cierre de la clasificación).

    Puedes tener hasta 2 notificaciones personalizadas.

    Haz clic en un espacio para configurarlo o editarlo.

# =======================
# Configuración de Zona Horaria
# =======================
button-timezone = ⏰ Zona horaria: { $timezone }
timezone-menu-title = ⏰ <b>Configuración de Zona Horaria</b>

    Zona horaria actual: <b>{ $timezone }</b>

    Escribe tu zona horaria (nombre de ciudad en inglés, abreviatura o desplazamiento UTC):

    Ejemplos: <code>Madrid</code>, <code>New York</code>, <code>UTC+1</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Selecciona tu zona horaria:</b>

    Coincidencias para "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Selecciona tu zona horaria:</b>

    Coincidencias para "{ $query }" (Página { $page }/{ $total }):

timezone-set-success = ✅ <b>¡Zona horaria configurada!</b>

    { $timezone }

    Hora actual en tu zona horaria: <b>{ $localTime }</b>

    Todos los horarios de las carreras se mostrarán en tu hora local.

button-reset-timezone = 🔄 Restablecer a UTC
feedback-timezone-set = ✅ Zona horaria actualizada
feedback-timezone-reset = ✅ Zona horaria restablecida a UTC
error-timezone-not-found = ❌ No se encontró zona horaria para "{ $query }"

    Intenta: nombre de ciudad en inglés (Madrid), abreviatura (CET), o desplazamiento UTC (UTC+1)
error-invalid-timezone = ❌ Zona horaria inválida



notif-quali-results = 🏁 <b>Resultados de Clasificación - Carrera #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Clasificación cerrada: { $qualiClose }</b>
    🏎 <b>Carrera: { $raceTime }</b>

    Resultados de clasificación disponibles:

    🔗 <a href="{ $q12Link }">Clasificación Q1 y Q2</a>
    🔗 <a href="{ $gridLink }">Parrilla de Salida</a>

notif-quali-results-no-group = 🏁 <b>Resultados de Clasificación - Carrera #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Clasificación cerrada: { $qualiClose }</b>
    🏎 <b>Carrera: { $raceTime }</b>

    Resultados de clasificación disponibles:

    ⚠️ Para enlaces personalizados, configura tu grupo en /settings!

    🔗 <a href="{ $q12Link }">Clasificación Q1 y Q2</a>
    🔗 <a href="{ $gridLink }">Parrilla de Salida</a>

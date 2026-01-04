# GPRO Bot - Traducciones en Español

# =======================
# Comandos & General
# =======================
start-welcome-new = 👋 **¡Bienvenido a GPRO Bot!**

    Vamos a configurar todo. Primero elige tu idioma preferido para los enlaces de carreras de GPRO:

    🌍 **Selecciona tu idioma** (o omite para usar inglés):

start-welcome-existing = 🏁 ¡GPRO Bot ACTIVO!
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

start-welcome-existing-buttons = 🏁 **GPRO Bot**

    ¿Qué te gustaría hacer?

bot-live = 🏁 **GPRO Bot**

# =======================
# Estado & Calendario
# =======================
no-races-scheduled = 🔔 No hay carreras programadas
no-upcoming-qualifications = 🔔 No hay clasificaciones programadas
next-season-not-published = 🌟 **La próxima temporada aún no se ha publicado**

calendar-title-full = 🏁 **Temporada Completa**
calendar-title-next = 🌟 **PRÓXIMA TEMPORADA** ({ $count } carreras)

# =======================
# Incorporación
# =======================
onboard-group-title = 🏁 **Selección de Grupo**

    Elige tu grupo GPRO para recibir enlaces personalizados de carreras:

    Selecciona un grupo común o ingresa el tuyo:

onboard-group-custom = 🏁 **Selección de Grupo (Opcional)**

    Ingresa tu grupo en uno de estos formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.

    💡 *El idioma del sitio GPRO se ha configurado para coincidir con el idioma del bot. Puedes cambiarlo más tarde en /settings*

onboard-complete = ✅ **¡Configuración Completada!**

    🏁 **¡GPRO Bot está listo!**

    **Comandos disponibles:**
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

    💡 *Puedes cambiar estas configuraciones en cualquier momento usando /settings*

onboard-complete-with-group = ✅ **¡Configuración Completada!**

    Grupo: **{ $group }**

    🏁 **¡GPRO Bot está listo!**

    **Comandos disponibles:**
    /status - Próxima carrera
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferencias

# =======================
# Configuración
# =======================
settings-title = ⚙️ **Configuración**

    Configura tus preferencias:

settings-language-title = 🌍 **Configuración de Idioma**

    Actual: { $language }

    Selecciona tu idioma preferido para los enlaces de carreras de GPRO:

ui-lang-menu-title = 💬 **Idioma del Bot**

    Selecciona el idioma de la interfaz del bot:

settings-group-title = 🏁 **Configuración de Grupo**

    Grupo actual: **{ $group }**

    Ingresa tu grupo en uno de estos formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.

settings-group-set = ✅ **Grupo establecido en: { $group }**

    ¡Las notificaciones de carreras y repeticiones incluirán enlaces directos a tu grupo!

settings-notifications-title = 🔔 **Configuración de Notificaciones**

    Haz clic para activar/desactivar notificaciones:
    ✅ = Activado | ❌ = Desactivado

    ℹ️ *Estos son interruptores globales para todas las carreras. Usa el botón 'Clasificación Completada' en las notificaciones para desactivar una carrera específica.*

settings-custom-notif-title = ⏱️ **Notificaciones Personalizadas**

    Establece tus propios horarios de notificación ({ $min }m - { $max }h antes del cierre de la clasificación).

    Puedes tener hasta 2 notificaciones personalizadas.

    Haz clic en un espacio para configurarlo o editarlo.

settings-custom-notif-edit = ⏱️ **Notificación Personalizada { $slot }**{ $current }

    Selecciona un horario predefinido o ingresa un horario personalizado:

settings-custom-notif-input = ⏱️ **Notificación Personalizada { $slot }**

    Ingresa tu horario de notificación personalizado.

    **Formatos aceptados:**
    • `20m` o `45 minutos` (20m-70h)
    • `2h` o `12 horas`
    • `1h 30m` o `2h30m`

    **Ejemplos:**
    • `20m` - 20 minutos antes
    • `6h` - 6 horas antes
    • `1h 30m` - 1 hora y 30 minutos antes

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
notif-label-replay = Repetición de la carrera disponible
notif-label-live = Carrera en vivo
notif-label-results = Resultados de la carrera disponibles

notif-label-opens-soon = La clasificación está abierta
notif-label-race-replay = Repetición de la carrera disponible
notif-label-race-live = Carrera en vivo
notif-label-race-results = Resultados de la carrera disponibles

notif-quali-closes = **¡La clasificación cierra en { $time }!**
notif-quali-opens = **La clasificación está abierta (o se abrirá pronto)**

notif-quali-message = { $emoji } { $title }

    🏁 **Carrera #{ $raceId }**
    📍 **{ $track }**
    📅 **Clasificación: { $qualiDeadline } | Carrera: { $raceTime }**

    🔗 [Ir a la Clasificación]({ $qualiLink })

    Haz clic en el botón para desactivar las notificaciones de esta carrera

notif-quali-message-disabled = { $emoji } { $title }

    🏁 **Carrera #{ $raceId }**
    📍 **{ $track }**
    📅 **Clasificación: { $qualiDeadline } | Carrera: { $raceTime }**

    🔗 [Ir a la Clasificación]({ $qualiLink })

    ℹ️ **Notificaciones automáticas desactivadas** para esta carrera
    Haz clic en el botón para reactivar las notificaciones

notif-race-live = 🏁 **¡La Carrera #{ $raceId } está EN VIVO!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    🔗 [Ver Carrera en Vivo]({ $raceLink })

notif-race-live-no-group = 🏁 **¡La Carrera #{ $raceId } está EN VIVO!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    ⚠️ ¡Establece tu grupo en /settings para un enlace directo!

    🔗 [Ver Carrera en Vivo]({ $raceLink })

notif-race-replay = 📺 **Repetición de la Carrera #{ $raceId } Disponible**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Si la carrera ya se ha calculado, la repetición está disponible aquí:

    🔗 [Ver Repetición]({ $replayLink })

notif-race-replay-no-group = 📺 **Repetición de la Carrera #{ $raceId } Disponible**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Si la carrera ya se ha calculado, la repetición está disponible aquí:

    ⚠️ ¡Para enlaces personalizados, establece tu grupo en /settings!

    🔗 [Ver Repetición]({ $replayLink })

notif-race-results = 📊 **Resultados de la Carrera #{ $raceId } Disponibles**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Los resultados de la carrera ya están disponibles:

    🔗 [Análisis de la Carrera]({ $analysisLink })
    🔗 [Resumen de la Carrera]({ $summaryLink })

notif-race-results-no-group = 📊 **Resultados de la Carrera #{ $raceId } Disponibles**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Los resultados de la carrera ya están disponibles:

    🔗 [Análisis de la Carrera]({ $analysisLink })

    ⚠️ ¡Para el Resumen de Carrera personalizado, establece tu grupo en /settings!

# =======================
# Clima
# =======================
weather-title = 🌤️ **Pronóstico del Clima de la Carrera**
weather-practice-q1 = **Práctica / Clasificación 1:** { $weather }
weather-temp-hum = Temp: { $temp }°C • Humedad: { $hum }%
weather-q2-start = **Clasificación 2 / Inicio de Carrera:** { $weather }
weather-q2-race-start = **Clasificación 2 / Inicio de Carrera:** { $weather }
weather-race-conditions = **Condiciones de Carrera:**
weather-quarter = **{ $label }:**
weather-race-quarter = Temp: { $temp } • Humedad: { $hum }
    Probabilidad de lluvia: { $rain }
weather-not-available = ⚠️ Datos del clima no disponibles
weather-unavailable = ⚠️ Datos del clima no disponibles
weather-cached = ℹ️ Clima ya en caché para **Carrera #{ $raceId }: { $track }**

    Usa `/weather force` para forzar la actualización.
    Usa /status para ver la notificación con el botón del clima.
weather-fetching = 🔄 Obteniendo clima para **Carrera #{ $raceId }: { $track }**...
weather-force-updating = 🔄 Forzando actualización del clima para **Carrera #{ $raceId }: { $track }**...
weather-success = ✅ Datos del clima obtenidos para **Carrera #{ $raceId }: { $track }**

    ¡Usa /status para probar la notificación con el botón del clima!
weather-failed = ❌ No se pudieron obtener los datos del clima

    Verifica que el token de la API de GPRO sea válido y que la API de Práctica esté disponible.

weather-start-0h30m = **Inicio - 0h30m:**
weather-0h30m-1h00m = **0h30m - 1h00m:**
weather-1h00m-1h30m = **1h00m - 1h30m:**
weather-1h30m-2h00m = **1h30m - 2h00m:**
weather-temp-hum-range = Temp: { $temp } • Humedad: { $hum }
weather-rain-prob = Probabilidad de lluvia: { $rain }

# =======================
# Admin
# =======================
admin-only = ❌ Solo admin
admin-calendar-updated = ✅ **Calendario**: { $count } carreras
    🔄 **{ $userCount } usuarios** restablecidos
admin-next-season-ready = 🌟 **¡Próxima temporada lista!** { $count } carreras
    Usa /next para ver
admin-next-season-not-published = ℹ️ **Próxima temporada no publicada**
admin-users-count = 📊 **{ $count } usuarios**:
admin-users-none = 📊 **0 usuarios** en la base de datos
admin-no-races = ❌ No hay carreras en el calendario
admin-no-upcoming-races = ❌ No se encontraron carreras futuras

# =======================
# Errores & Validación
# =======================
error-invalid-format = ❌ ¡Formato inválido!

    Por favor usa:
    • **E** para Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Inténtalo de nuevo:

error-invalid-format-onboarding = ❌ ¡Formato inválido!

    Por favor usa:
    • **E** para Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Inténtalo de nuevo o usa /start para reiniciar:

error-invalid-time = ❌ **Error:** { $error }

    Por favor inténtalo de nuevo con un formato válido como: `2h`, `30m`, o `1h 30m`

error-custom-notif-failed = ❌ **Error:** { $error }

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
feedback-race-marked-done = ✅ *¡Carrera marcada como completada!*
feedback-reset = 🔄 ¡Restablecido!
feedback-notifications-reset = 🔄 *¡Notificaciones restablecidas!*
feedback-reenabled = 🔄 ¡Reactivado!
feedback-notifications-reenabled = 🔄 *¡Notificaciones reactivadas!*
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
custom-notif-error-parsing = ❌ **Error:** { $error }

    Por favor inténtalo de nuevo con un formato válido como: `2h`, `30m`, o `1h 30m`
custom-notif-success = ✅ **{ $message }**

    ¡Tu notificación personalizada ha sido establecida!
custom-notif-error-setting = ❌ **Error:** { $error }

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
notif-menu-title = 🔔 **Configuración de Notificaciones**

    Haz clic para activar/desactivar notificaciones:
    ✅ = Activado | ❌ = Desactivado

    ℹ️ *Estos son interruptores globales para todas las carreras. Usa el botón 'Clasificación Completada' en las notificaciones para desactivar una carrera específica.*

# =======================
# Menú de Grupo
# =======================
group-menu-title = 🏁 **Configuración de Grupo**

    Grupo actual: **{ $groupDisplay }**

    Ingresa tu grupo en uno de estos formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Los números pueden tener de 1 a 3 dígitos.
group-reset-success = ✅ Grupo restablecido con éxito

# =======================
# Menú de Idioma
# =======================
lang-menu-title = 🌍 **Configuración de Idioma**

    Actual: { $currentLang }

    Selecciona tu idioma preferido para los enlaces de carreras de GPRO:

# =======================
# Menú de Notificaciones Personalizadas
# =======================
custom-notif-menu-title = ⏱️ **Notificaciones Personalizadas**

    Establece tus propios horarios de notificación ({ $minTime }m - { $maxTime }h antes del cierre de la clasificación).

    Puedes tener hasta 2 notificaciones personalizadas.

    Haz clic en un espacio para configurarlo o editarlo.

# =======================
# Configuración de Zona Horaria
# =======================
button-timezone = ⏰ Zona horaria: { $timezone }
timezone-menu-title = ⏰ **Configuración de Zona Horaria**

    Zona horaria actual: **{ $timezone }**

    Escribe tu zona horaria (nombre de ciudad, abreviatura o desplazamiento UTC):

    Ejemplos: `Madrid`, `CET`, `UTC+1`, `Buenos Aires`

timezone-select-matches = 🌍 **Selecciona tu zona horaria:**

    Coincidencias para "{ $query }":

timezone-set-success = ✅ **¡Zona horaria configurada!**

    { $timezone }

    Hora actual en tu zona horaria: **{ $localTime }**

    Todos los horarios de las carreras se mostrarán en tu hora local.

button-reset-timezone = 🔄 Restablecer a UTC
feedback-timezone-set = ✅ Zona horaria actualizada
feedback-timezone-reset = ✅ Zona horaria restablecida a UTC
error-timezone-not-found = ❌ No se encontró zona horaria para "{ $query }"

    Intenta: nombre de ciudad (Madrid), abreviatura (CET), o desplazamiento UTC (UTC+1)
error-invalid-timezone = ❌ Zona horaria inválida

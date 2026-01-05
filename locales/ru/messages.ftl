# GPRO Bot - Русские переводы

# =======================
# Команды и общее
# =======================
start-welcome-new = 👋 **Добро пожаловать в GPRO Bot!**

    Давайте настроим бота. Сначала выберите предпочитаемый язык для ссылок на GPRO:

    🌍 **Выберите язык** (или пропустите для английского):

start-welcome-existing = 🏁 GPRO Bot РАБОТАЕТ!
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

start-welcome-existing-buttons = 🏁 **GPRO Bot**

    Что хотите сделать?

bot-live = 🏁 **GPRO Bot**

# =======================
# Статус и календарь
# =======================
no-races-scheduled = 🔔 Нет запланированных гонок
no-upcoming-qualifications = 🔔 Нет предстоящих квалификаций
next-season-not-published = 🌟 **Следующий сезон ещё не опубликован**

calendar-title-full = 🏁 **Весь сезон**
calendar-title-next = 🌟 **СЛЕДУЮЩИЙ СЕЗОН** ({ $count } гонок)

# =======================
# Онбординг
# =======================
onboard-group-title = 🏁 **Выбор группы**

    Выберите вашу группу в GPRO для персонализированных ссылок:

    Выберите готовый вариант или введите свой:

onboard-group-custom = 🏁 **Выбор группы (Необязательно)**

    Введите группу в одном из этих форматов:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Номер может быть от 1 до 3 цифр.

    💡 *Язык сайта GPRO установлен соответствующим языку бота. Вы можете изменить его позже в /settings*

onboard-complete = ✅ **Настройка завершена!**

    🏁 **GPRO Bot готов к работе!**

    **Доступные команды:**
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

    💡 *Вы можете изменить эти настройки в любое время через /settings*

onboard-complete-with-group = ✅ **Настройка завершена!**

    Группа: **{ $group }**

    🏁 **GPRO Bot готов к работе!**

    **Доступные команды:**
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

# =======================
# Настройки
# =======================
settings-title = ⚙️ **Настройки**

    Настройте ваши предпочтения:

settings-language-title = 🌍 **Настройки языка**

    Текущий: { $language }

    Выберите предпочитаемый язык для ссылок на GPRO:

ui-lang-menu-title = 💬 **Язык бота**

    Выберите язык интерфейса бота:

settings-group-title = 🏁 **Настройки группы**

    Текущая группа: **{ $group }**

    Введите группу в одном из этих форматов:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Номер может быть от 1 до 3 цифр.

settings-group-set = ✅ **Группа установлена: { $group }**

    Уведомления о гонках и реплеях будут содержать прямые ссылки на вашу группу!

settings-notifications-title = 🔔 **Настройки уведомлений**

    Нажмите для включения/отключения уведомлений:
    ✅ = Включено | ❌ = Отключено

    ℹ️ *Это глобальные переключатели для всех гонок. Используйте кнопку 'Проехал квалификацию' в уведомлениях для отключения конкретной гонки.*

settings-custom-notif-title = ⏱️ **Кастомные уведомления**

    Установите свои времена уведомлений ({ $min }м - { $max }ч до закрытия квалификации).

    Можно создать до 2 кастомных уведомлений.

    Нажмите на слот для настройки.

settings-custom-notif-edit = ⏱️ **Кастомное уведомление { $slot }**{ $current }

    Выберите готовое время или введите своё:

settings-custom-notif-input = ⏱️ **Кастомное уведомление { $slot }**

    Введите время для уведомления.

    **Поддерживаемые форматы:**
    • `20m` или `45 минут` (20м-70ч)
    • `2h` или `12 часов`
    • `1h 30m` или `2ч30м`

    **Примеры:**
    • `20m` - за 20 минут
    • `6h` - за 6 часов
    • `1h 30m` - за 1 час 30 минут

# =======================
# Кнопки
# =======================
button-ui-language = 💬 Язык бота: { $language }
button-gpro-language = 🌍 Язык GPRO: { $language }
button-language = 🌍 Язык: { $language }
button-group = 🏁 Группа: { $group }
button-notifications = 🔔 Уведомления
button-custom-notifications = ⏱️ Кастомные уведомления
button-back = ◀ Назад
button-back-to-settings = ◀ Назад к настройкам
button-back-to-notifications = ◀ Назад к уведомлениям
button-back-to-custom = ◀ Назад к кастомным
button-back-custom-notif = ◀ Назад к кастомным
button-main-menu = 🏠 Главное меню
button-reset-group = 🔄 Сбросить группу
button-custom-slot-set = ⏱️ Кастомное { $slot }: { $time }
button-custom-slot-empty = ➕ Установить кастомное { $slot }
button-previous = ◀ Назад
button-next = Далее ▶
button-skip = ⏭️ Пропустить
button-reset-language = 🔄 Сбросить на английский
button-enable-all = 🔔 Включить все уведомления
button-disable-all = 🔕 Отключить все уведомления
button-quali-done = ✅ Проехал квалификацию
button-reenable-race = 🔄 Включить уведомления для гонки { $raceId }
button-weather = 🌤️ Показать погоду
button-enter-custom-group = ✏️ Ввести свою группу
button-enter-custom-time = ✏️ Ввести своё время
button-disable-notification = 🔕 Отключить это уведомление
button-cancel = ❌ Отмена
button-got-it = ✅ Понятно!
button-try-again = 🔄 Попробовать снова

button-main-menu-status = 📊 Следующая гонка
button-main-menu-calendar = 📅 Весь сезон
button-main-menu-next = 🌟 Следующий сезон
button-main-menu-settings = ⚙️ Настройки

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Создать уведомление { $slot }
button-custom-notif-time = ⏱️ Кастом { $slot }: { $time }

# =======================
# Уведомления
# =======================
notif-label-72h = За 3 дня до закрытия квалификации
notif-label-48h = За 2 дня до закрытия квалификации
notif-label-24h = За 1 день до закрытия квалификации
notif-label-2h = За 2ч до закрытия квалификации
notif-label-10min = За 10мин до закрытия квалификации
notif-label-opens = Квалификация открыта
notif-label-replay = Доступен реплей гонки
notif-label-live = Гонка в прямом эфире
notif-label-results = Доступны результаты гонки

notif-quali-closes = **Квалификация закроется через { $time }!**
notif-quali-opens = **Квалификация открыта (или скоро откроется)**

notif-quali-message = { $emoji } { $title }

    🏁 **Гонка #{ $raceId }**
    📍 **{ $track }**
    📅 **Квалификация: { $qualiDeadline } | Гонка: { $raceTime }**

    🔗 [Перейти к квалификации]({ $qualiLink })

    Нажмите кнопку для отключения уведомлений об этой гонке

notif-quali-message-disabled = { $emoji } { $title }

    🏁 **Гонка #{ $raceId }**
    📍 **{ $track }**
    📅 **Квалификация: { $qualiDeadline } | Гонка: { $raceTime }**

    🔗 [Перейти к квалификации]({ $qualiLink })

    ℹ️ **Автоматические уведомления отключены** для этой гонки
    Нажмите кнопку для включения

notif-race-live = 🏁 **Гонка #{ $raceId } в ПРЯМОМ ЭФИРЕ!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    🔗 [Смотреть гонку]({ $raceLink })

notif-race-live-no-group = 🏁 **Гонка #{ $raceId } в ПРЯМОМ ЭФИРЕ!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    ⚠️ Укажите группу в /settings для прямой ссылки!

    🔗 [Смотреть гонку]({ $raceLink })

notif-race-replay = 📺 **Доступен реплей гонки #{ $raceId }**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Если гонка уже рассчитана, реплей доступен здесь:

    🔗 [Смотреть реплей]({ $replayLink })

notif-race-replay-no-group = 📺 **Доступен реплей гонки #{ $raceId }**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Если гонка уже рассчитана, реплей доступен здесь:

    ⚠️ Для персональных ссылок укажите группу в /settings!

    🔗 [Смотреть реплей]({ $replayLink })

notif-race-results = 📊 **Доступны результаты гонки #{ $raceId }**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Результаты гонки доступны:

    🔗 [Анализ гонки]({ $analysisLink })
    🔗 [Сводка гонки]({ $summaryLink })

notif-race-results-no-group = 📊 **Доступны результаты гонки #{ $raceId }**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Результаты гонки доступны:

    🔗 [Анализ гонки]({ $analysisLink })

    ⚠️ Для персональной сводки укажите группу в /settings!

# =======================
# Погода
# =======================
weather-title = 🌤️ **Прогноз погоды на гонку**
weather-practice-q1 = **Практика / Квалификация 1:** { $weather }
weather-temp-hum = Темп: { $temp }°C • Влажность: { $hum }%
weather-q2-start = **Квалификация 2 / Старт гонки:** { $weather }
weather-race-conditions = **Условия гонки:**
weather-quarter = **{ $label }:**
weather-race-quarter = Темп: { $temp } • Влажность: { $hum }
    Вероятность дождя: { $rain }
weather-not-available = ⚠️ Данные о погоде недоступны
weather-cached = ℹ️ Погода уже загружена для **Гонки #{ $raceId }: { $track }**

    Используйте `/weather force` для принудительного обновления.
    Используйте /status для просмотра уведомления с кнопкой погоды.
weather-fetching = 🔄 Загрузка погоды для **Гонки #{ $raceId }: { $track }**...
weather-force-updating = 🔄 Принудительное обновление погоды для **Гонки #{ $raceId }: { $track }**...
weather-success = ✅ Погода загружена для **Гонки #{ $raceId }: { $track }**

    Используйте /status для проверки уведомления с кнопкой погоды!
weather-failed = ❌ Не удалось загрузить погоду

    Проверьте, что GPRO API токен действителен и Practice API доступен.

# =======================
# Админ
# =======================
admin-only = ❌ Только для админов
admin-calendar-updated = ✅ **Календарь**: { $count } гонок
    🔄 **{ $userCount } пользователей** сброшено
admin-next-season-ready = 🌟 **Следующий сезон готов!** { $count } гонок
    Используйте /next для просмотра
admin-next-season-not-published = ℹ️ **Следующий сезон не опубликован**
admin-users-count = 📊 **{ $count } пользователей**:
admin-users-none = 📊 **0 пользователей** в базе
admin-no-races = ❌ Нет гонок в календаре
admin-no-upcoming-races = ❌ Нет предстоящих гонок

# =======================
# Ошибки и валидация
# =======================
error-invalid-format = ❌ Неверный формат!

    Используйте:
    • **E** для Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** и т.д.

    Попробуйте снова:

error-invalid-format-onboarding = ❌ Неверный формат!

    Используйте:
    • **E** для Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** и т.д.

    Попробуйте снова или используйте /start для перезапуска:

error-invalid-time = ❌ **Ошибка:** { $error }

    Попробуйте снова с правильным форматом: `2h`, `30m` или `1h 30m`

error-custom-notif-failed = ❌ **Ошибка:** { $error }

    Попробуйте снова.

error-invalid-race = ❌ Неверный ID гонки
error-invalid-page = ❌ Неверная страница
error-invalid-language = ❌ Неверный язык
error-invalid-slot = ❌ Неверный слот
error-invalid-data = ❌ Неверные данные
error-reset-failed = ❌ Сброс не удался
error-race-not-found = ❌ Гонка не найдена
error-weather-not-available = ⚠️ Данные о погоде пока недоступны
error-weather-send-failed = ❌ Не удалось отправить погоду

# =======================
# Обратная связь и подтверждения
# =======================
feedback-all-enabled = ✅ Все уведомления включены!
feedback-all-disabled = ✅ Все уведомления отключены!
feedback-notif-enabled = ✅ { $label } включено!
feedback-notif-disabled = ✅ { $label } отключено!
feedback-quali-done = ✅ Готово!
feedback-race-marked-done = ✅ *Гонка отмечена как завершенная!*
feedback-reset = 🔄 Сброшено!
feedback-notifications-reset = 🔄 *Уведомления сброшены!*
feedback-reenabled = 🔄 Включено заново!
feedback-notifications-reenabled = 🔄 *Уведомления включены заново!*
feedback-language-set = ✅ Язык установлен: { $language }
feedback-language-reset = ✅ Язык сброшен на английский
feedback-ui-language-set = ✅ Язык бота установлен: { $language }
feedback-group-set = ✅ Группа установлена: { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Кастомное уведомление { $slot } отключено
feedback-skip-language = ⏭️ Используется язык по умолчанию (английский)
feedback-skip-group = ⏭️ Выбор группы пропущен
feedback-welcome = ✅ Добро пожаловать!
feedback-weather-sent = 🌤️ Прогноз погоды отправлен!

# =======================
# Форматирование времени
# =======================
# Сокращения дней недели (2 буквы)
weekday-mon = Пн
weekday-tue = Вт
weekday-wed = Ср
weekday-thu = Чт
weekday-fri = Пт
weekday-sat = Сб
weekday-sun = Вс

time-minutes = { $minutes } { $minutes ->
    [one] минута
    [few] минуты
   *[many] минут
}
time-hours = { $hours } { $hours ->
    [one] час
    [few] часа
   *[many] часов
}
time-hours-minutes = { $hours } { $hours ->
    [one] час
    [few] часа
   *[many] часов
} { $minutes } { $minutes ->
    [one] минута
    [few] минуты
   *[many] минут
}
time-hours-minutes-short = { $hours }ч{ $minutes }м
time-days = { $days } { $days ->
    [one] день
    [few] дня
   *[many] дней
}
time-days-hours = { $days } { $days ->
    [one] день
    [few] дня
   *[many] дней
} { $hours } { $hours ->
    [one] час
    [few] часа
   *[many] часов
}
time-months = { $months } { $months ->
    [one] месяц
    [few] месяца
   *[many] месяцев
}
time-months-days = { $months } { $months ->
    [one] месяц
    [few] месяца
   *[many] месяцев
} { $days } { $days ->
    [one] день
    [few] дня
   *[many] дней
}

# =======================
# Отображение группы
# =======================
group-not-set = Не установлена
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Сообщения кастомных уведомлений
# =======================
custom-notif-set = Кастомное уведомление { $slot } установлено на { $time }
custom-notif-set-success = Кастомное уведомление { $slot } установлено на { $time }
custom-notif-not-set = Не установлено
custom-notif-min-error = Минимальное время 20 минут
custom-notif-max-error = Максимальное время 70 часов
custom-notif-invalid-slot = Неверный слот (должен быть 0-{ $max })
custom-notif-empty-error = Время не может быть пустым
custom-notif-invalid-format = Неверный формат. Используйте: 2ч, 30м или 1ч 30м
custom-notif-enter-time = Пожалуйста, введите время
custom-notif-error-parsing = ❌ **Ошибка:** { $error }

    Пожалуйста, попробуйте снова с корректным форматом: `2ч`, `30м` или `1ч 30м`
custom-notif-success = ✅ **{ $message }**

    Ваше кастомное уведомление установлено!
custom-notif-error-setting = ❌ **Ошибка:** { $error }

    Пожалуйста, попробуйте снова.

# =======================
# Валидация
# =======================
validation-time-empty = Время не может быть пустым
validation-time-min = Минимальное время 20 минут
validation-time-max = Максимальное время 70 часов
validation-enter-time = Пожалуйста, введите время
validation-invalid-format = Неверный формат. Используйте: 2ч, 30м или 1ч 30м
validation-invalid-slot = Неверный слот (должен быть 0-{ $maxSlots })

# =======================
# Названия уведомлений
# =======================
notif-label-72h = 3 дня до закрытия квалификации
notif-label-48h = 2 дня до закрытия квалификации
notif-label-24h = 1 день до закрытия квалификации
notif-label-2h = 2ч до закрытия квалификации
notif-label-10min = 10мин до закрытия квалификации
notif-label-opens-soon = Квалификация открыта
notif-label-race-replay = Доступен повтор гонки
notif-label-race-live = Гонка началась
notif-label-race-results = Доступны результаты гонки

# =======================
# Меню уведомлений
# =======================
notif-menu-title = 🔔 **Настройки уведомлений**

    Нажмите, чтобы включить/выключить уведомления:
    ✅ = Включено | ❌ = Выключено

    ℹ️ *Это глобальные переключатели для всех гонок. Используйте кнопку 'Проехал квалификацию' в уведомлениях, чтобы отключить конкретную гонку.*

# =======================
# Меню группы
# =======================
group-menu-title = 🏁 **Настройки группы**

    Текущая группа: **{ $groupDisplay }**

    Введите вашу группу в одном из форматов:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Номер может быть 1-3 цифры.
group-reset-success = ✅ Группа успешно сброшена

# =======================
# Меню языка
# =======================
lang-menu-title = 🌍 **Настройки языка**

    Текущий: { $currentLang }

    Выберите предпочитаемый язык для ссылок GPRO:

# =======================
# Меню кастомных уведомлений
# =======================
custom-notif-menu-title = ⏱️ **Кастомные уведомления**

    Установите свои времена уведомлений ({ $minTime }м - { $maxTime }ч до закрытия квалификации).

    Вы можете иметь до 2 кастомных уведомлений.

    Нажмите на слот, чтобы установить или изменить.

# =======================
# Погода
# =======================
weather-unavailable = ⚠️ Данные о погоде недоступны
weather-title = 🌤️ **Прогноз погоды на гонку**
weather-practice-q1 = **Практика / Квалификация 1:** { $weather }
weather-temp-hum = Температура: { $temp }°C • Влажность: { $hum }%
weather-q2-race-start = **Квалификация 2 / Старт гонки:** { $weather }
weather-race-conditions = **Условия гонки:**
weather-start-0h30m = **Старт - 0ч30м:**
weather-0h30m-1h00m = **0ч30м - 1ч00м:**
weather-1h00m-1h30m = **1ч00м - 1ч30м:**
weather-1h30m-2h00m = **1ч30м - 2ч00м:**
weather-temp-hum-range = Температура: { $temp } • Влажность: { $hum }
weather-rain-prob = Вероятность дождя: { $rain }

# =======================
# Настройки часового пояса
# =======================
button-timezone = ⏰ Часовой пояс: { $timezone }
timezone-menu-title = ⏰ **Настройки часового пояса**

    Текущий часовой пояс: **{ $timezone }**

    Введите ваш часовой пояс (название города на английском, аббревиатуру или смещение UTC):

    Примеры: `Moscow`, `New York`, `UTC+3`, `London`

timezone-select-matches = 🌍 **Выберите ваш часовой пояс:**

    Найдено для "{ $query }":

timezone-set-success = ✅ **Часовой пояс установлен!**

    { $timezone }

    Текущее время в вашем часовом поясе: **{ $localTime }**

    Все времена гонок теперь будут отображаться в вашем местном времени.

button-reset-timezone = 🔄 Сбросить на UTC
feedback-timezone-set = ✅ Часовой пояс обновлён
feedback-timezone-reset = ✅ Часовой пояс сброшен на UTC
error-timezone-not-found = ❌ Часовой пояс не найден для "{ $query }"

    Попробуйте: название города на английском (Moscow), аббревиатуру (MSK), или смещение UTC (UTC+3)
error-invalid-timezone = ❌ Неверный часовой пояс

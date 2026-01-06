# GPRO Bot - Русские переводы

# =======================
# Команды и общее
# =======================
start-welcome-new = 👋 <b>Добро пожаловать в GPRO Bot!</b>

    Давайте настроим бота. Сначала выберите предпочитаемый язык для ссылок на GPRO:

    🌍 <b>Выберите язык</b> (или пропустите для английского):

start-welcome-existing = 🏁 GPRO Bot РАБОТАЕТ!
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Что хотите сделать?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Статус и календарь
# =======================
no-races-scheduled = 🔔 Нет запланированных гонок
no-upcoming-qualifications = 🔔 Нет предстоящих квалификаций
next-season-not-published = 🌟 <b>Следующий сезон ещё не опубликован</b>

calendar-title-full = 🏁 <b>Весь сезон</b>
calendar-title-next = 🌟 <b>СЛЕДУЮЩИЙ СЕЗОН</b> ({ $count } гонок)

# =======================
# Онбординг
# =======================
onboard-group-title = 🏁 <b>Выбор группы</b>

    Выберите вашу группу в GPRO для персонализированных ссылок:

    Выберите готовый вариант или введите свой:

onboard-group-custom = 🏁 <b>Выбор группы (Необязательно)</b>

    Введите группу в одном из этих форматов:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер может быть от 1 до 3 цифр.

    💡 <i>Язык сайта GPRO установлен соответствующим языку бота. Вы можете изменить его позже в /settings</i>

onboard-complete = ✅ <b>Настройка завершена!</b>

    🏁 <b>GPRO Bot готов к работе!</b>

    <b>Доступные команды:</b>
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

    💡 <i>Вы можете изменить эти настройки в любое время через /settings</i>

onboard-complete-with-group = ✅ <b>Настройка завершена!</b>

    Группа: <b>{ $group }</b>

    🏁 <b>GPRO Bot готов к работе!</b>

    <b>Доступные команды:</b>
    /status - Следующая гонка
    /calendar - Весь сезон
    /next - Следующий сезон
    /settings - Настройки

# =======================
# Настройки
# =======================
settings-title = ⚙️ <b>Настройки</b>

    Настройте ваши предпочтения:

settings-language-title = 🌍 <b>Настройки языка</b>

    Текущий: { $language }

    Выберите предпочитаемый язык для ссылок на GPRO:

ui-lang-menu-title = 💬 <b>Язык бота</b>

    Выберите язык интерфейса бота:

settings-group-title = 🏁 <b>Настройки группы</b>

    Текущая группа: <b>{ $group }</b>

    Введите группу в одном из этих форматов:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер может быть от 1 до 3 цифр.

settings-group-set = ✅ <b>Группа установлена: { $group }</b>

    Уведомления о гонках и реплеях будут содержать прямые ссылки на вашу группу!

settings-notifications-title = 🔔 <b>Настройки уведомлений</b>

    Нажмите для включения/отключения уведомлений:
    ✅ = Включено | ❌ = Отключено

    ℹ️ <i>Это глобальные переключатели для всех гонок. Используйте кнопку 'Проехал квалификацию' в уведомлениях для отключения конкретной гонки.</i>

settings-custom-notif-title = ⏱️ <b>Кастомные уведомления</b>

    Установите свои времена уведомлений ({ $min }м - { $max }ч до закрытия квалификации).

    Можно создать до 2 кастомных уведомлений.

    Нажмите на слот для настройки.

settings-custom-notif-edit = ⏱️ <b>Кастомное уведомление { $slot }</b>{ $current }

    Выберите готовое время или введите своё:

settings-custom-notif-current = Текущее:

settings-custom-notif-input = ⏱️ <b>Кастомное уведомление { $slot }</b>

    Введите время для уведомления.

    <b>Поддерживаемые форматы:</b>
    • <code>20m</code> или <code>45 минут</code> (20м-70ч)
    • <code>2h</code> или <code>12 часов</code>
    • <code>1h 30m</code> или <code>2ч30м</code>

    <b>Примеры:</b>
    • <code>20m</code> - за 20 минут
    • <code>6h</code> - за 6 часов
    • <code>1h 30m</code> - за 1 час 30 минут

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
button-enable-category = 🔔 Включить категорию
button-disable-category = 🔕 Отключить категорию
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
# Категории уведомлений
notif-category-before-qualifying = Перед квалификацией
notif-category-qualifying-events = События квалификации
notif-category-race-events = События гонки

# Отдельные уведомления
notif-label-72h = За 3 дня до закрытия квалификации
notif-label-48h = За 2 дня до закрытия квалификации
notif-label-24h = За 1 день до закрытия квалификации
notif-label-2h = За 2ч до закрытия квалификации
notif-label-10min = За 10мин до закрытия квалификации
notif-label-opens = Квалификация открыта
notif-label-quali-results = Результаты квалификации доступны
notif-label-replay = Доступен реплей гонки
notif-label-live = Гонка в прямом эфире
notif-label-results = Доступны результаты гонки

notif-quali-closes = <b>Квалификация закроется через { $time }!</b>
notif-quali-opens = <b>Квалификация открыта (или скоро откроется)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Гонка #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Квал. закрывается: { $qualiDeadline }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Перейти к квалификации</a>

    <i>Нажмите кнопку '✅ Проехал квалификацию', чтобы отключить уведомления для этой гонки</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Гонка #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Квал. закрывается: { $qualiDeadline }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Перейти к квалификации</a>

    ℹ️ <b>Автоматические уведомления отключены</b> для этой гонки
    <i>Нажмите кнопку '🔄 Включить' для включения уведомлений</i>

notif-quali-closed-title = <b>Квалификация сейчас закрыта</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Гонка #{ $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Квалификация закрыта: { $qualiDeadline }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    ⏳ <i>Квалификация сейчас закрыта. Следующая квалификация откроется после завершения текущей гонки. Пожалуйста, подождите, пока гонка будет рассчитана.</i>

notif-race-live = 🏁 <b>Гонка #{ $raceId } в ПРЯМОМ ЭФИРЕ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Смотреть гонку</a>

notif-race-live-no-group = 🏁 <b>Гонка #{ $raceId } в ПРЯМОМ ЭФИРЕ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Укажите группу в /settings для прямой ссылки!

    🔗 <a href="{ $raceLink }">Смотреть гонку</a>

notif-race-replay = 📺 <b>Доступен реплей гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Если гонка уже рассчитана, реплей доступен здесь:

    🔗 <a href="{ $replayLink }">Смотреть реплей</a>

notif-race-replay-no-group = 📺 <b>Доступен реплей гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Если гонка уже рассчитана, реплей доступен здесь:

    ⚠️ Для персональных ссылок укажите группу в /settings!

    🔗 <a href="{ $replayLink }">Смотреть реплей</a>

notif-race-results = 📊 <b>Доступны результаты гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Результаты гонки доступны:

    🔗 <a href="{ $analysisLink }">Анализ гонки</a>
    🔗 <a href="{ $summaryLink }">Сводка гонки</a>

notif-race-results-no-group = 📊 <b>Доступны результаты гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Результаты гонки доступны:

    🔗 <a href="{ $analysisLink }">Анализ гонки</a>

    ⚠️ Для персональной сводки укажите группу в /settings!

# =======================
# Погода
# =======================
weather-title = 🌤️ <b>Прогноз погоды на гонку</b>
weather-practice-q1 = <b>Практика / Квалификация 1:</b> { $weather }
weather-temp-hum = Темп: { $temp }°C • Влажность: { $hum }%
weather-q2-start = <b>Квалификация 2 / Старт гонки:</b> { $weather }
weather-race-conditions = <b>Условия гонки:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Темп: { $temp } • Влажность: { $hum }
    Вероятность дождя: { $rain }
weather-not-available = ⚠️ Данные о погоде недоступны
weather-cached = ℹ️ Погода уже загружена для <b>Гонки #{ $raceId }: { $track }</b>

    Используйте <code>/weather force</code> для принудительного обновления.
    Используйте /status для просмотра уведомления с кнопкой погоды.
weather-fetching = 🔄 Загрузка погоды для <b>Гонки #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Принудительное обновление погоды для <b>Гонки #{ $raceId }: { $track }</b>...
weather-success = ✅ Погода загружена для <b>Гонки #{ $raceId }: { $track }</b>

    Используйте /status для проверки уведомления с кнопкой погоды!
weather-failed = ❌ Не удалось загрузить погоду

    Проверьте, что GPRO API токен действителен и Practice API доступен.

# =======================
# Админ
# =======================
admin-only = ❌ Только для админов
admin-calendar-updated = ✅ <b>Календарь</b>: { $count } гонок
    🔄 <b>{ $userCount } пользователей</b> сброшено
admin-next-season-ready = 🌟 <b>Следующий сезон готов!</b> { $count } гонок
    Используйте /next для просмотра
admin-next-season-not-published = ℹ️ <b>Следующий сезон не опубликован</b>
admin-users-count = 📊 <b>{ $count } пользователей</b>:
admin-users-none = 📊 <b>0 пользователей</b> в базе
admin-no-races = ❌ Нет гонок в календаре
admin-no-upcoming-races = ❌ Нет предстоящих гонок

# =======================
# Ошибки и валидация
# =======================
error-invalid-format = ❌ Неверный формат!

    Используйте:
    • <b>E</b> для Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> и т.д.

    Попробуйте снова:

error-invalid-format-onboarding = ❌ Неверный формат!

    Используйте:
    • <b>E</b> для Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> и т.д.

    Попробуйте снова или используйте /start для перезапуска:

error-invalid-time = ❌ <b>Ошибка:</b> { $error }

    Попробуйте снова с правильным форматом: <code>2h</code>, <code>30m</code> или <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Ошибка:</b> { $error }

    Попробуйте снова.

error-invalid-race = ❌ Неверный ID гонки
error-invalid-page = ❌ Неверная страница
error-invalid-language = ❌ Неверный язык
error-invalid-category = ❌ Неверная категория
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
feedback-category-enabled = ✅ { $category } включена!
feedback-category-disabled = ✅ { $category } отключена!
feedback-notif-enabled = ✅ { $label } включено!
feedback-notif-disabled = ✅ { $label } отключено!
feedback-quali-done = ✅ Готово!
feedback-race-marked-done = ✅ <i>Гонка отмечена как завершенная!</i>
feedback-reset = 🔄 Сброшено!
feedback-notifications-reset = 🔄 <i>Уведомления сброшены!</i>
feedback-reenabled = 🔄 Включено заново!
feedback-notifications-reenabled = 🔄 <i>Уведомления включены заново!</i>
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
time-hours-short = { $hours }ч
time-minutes-short = { $minutes }м
time-days-hours-short = { $days }д{ $hours }ч
time-days-hours-minutes-short = { $days }д{ $hours }ч{ $minutes }м
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
custom-notif-error-parsing = ❌ <b>Ошибка:</b> { $error }

    Пожалуйста, попробуйте снова с корректным форматом: <code>2ч</code>, <code>30м</code> или <code>1ч 30м</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Ваше кастомное уведомление установлено!
custom-notif-error-setting = ❌ <b>Ошибка:</b> { $error }

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
notif-label-quali-results = Результаты квалификации доступны
notif-label-race-replay = Доступен повтор гонки
notif-label-race-live = Гонка началась
notif-label-race-results = Доступны результаты гонки

# =======================
# Меню уведомлений
# =======================
notif-menu-title = 🔔 <b>Настройки уведомлений</b>

    Нажмите, чтобы включить/выключить уведомления:
    ✅ = Включено | ❌ = Выключено

    ℹ️ <i>Это глобальные переключатели для всех гонок. Используйте кнопку 'Проехал квалификацию' в уведомлениях, чтобы отключить конкретную гонку.</i>

# =======================
# Меню группы
# =======================
group-menu-title = 🏁 <b>Настройки группы</b>

    Текущая группа: <b>{ $groupDisplay }</b>

    Введите вашу группу в одном из форматов:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер может быть 1-3 цифры.
group-reset-success = ✅ Группа успешно сброшена

# =======================
# Меню языка
# =======================
lang-menu-title = 🌍 <b>Настройки языка</b>

    Текущий: { $currentLang }

    Выберите предпочитаемый язык для ссылок GPRO:

# =======================
# Меню кастомных уведомлений
# =======================
custom-notif-menu-title = ⏱️ <b>Кастомные уведомления</b>

    Установите свои времена уведомлений ({ $minTime }м - { $maxTime }ч до закрытия квалификации).

    Вы можете иметь до 2 кастомных уведомлений.

    Нажмите на слот, чтобы установить или изменить.

# =======================
# Погода
# =======================
weather-unavailable = ⚠️ Данные о погоде недоступны
weather-title = 🌤️ <b>Прогноз погоды на гонку</b>
weather-race-header = Гонка #{ $raceId }: { $track }
weather-practice-q1 = <b>Практика / Квалификация 1:</b> { $weather }
weather-temp-hum = Температура: { $temp }°C • Влажность: { $hum }%
weather-q2-race-start = <b>Квалификация 2 / Старт гонки:</b> { $weather }
weather-race-conditions = <b>Условия гонки:</b>
weather-start-0h30m = <b>Старт - 0ч30м:</b>
weather-0h30m-1h00m = <b>0ч30м - 1ч00м:</b>
weather-1h00m-1h30m = <b>1ч00м - 1ч30м:</b>
weather-1h30m-2h00m = <b>1ч30м - 2ч00м:</b>
weather-temp-hum-range = Температура: { $temp } • Влажность: { $hum }
weather-rain-prob = Вероятность дождя: { $rain }

# Погодные условия
weather-condition-sunny = Солнечно
weather-condition-partially-cloudy = Переменная облачность
weather-condition-cloudy = Облачно
weather-condition-very-cloudy = Пасмурно
weather-condition-rain = Дождь

# =======================
# Настройки часового пояса
# =======================
button-timezone = ⏰ Часовой пояс: { $timezone }
button-website-mode = 🌐 Тип ссылок: { $mode }
website-mode-classic = Классический
timezone-menu-title = ⏰ <b>Настройки часового пояса</b>

    Текущий часовой пояс: <b>{ $timezone }</b>

    Введите ваш часовой пояс (название города на английском, аббревиатуру или смещение UTC):

    Примеры: <code>Moscow</code>, <code>New York</code>, <code>UTC+3</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Выберите ваш часовой пояс:</b>

    Найдено для "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Выберите ваш часовой пояс:</b>

    Найдено для "{ $query }" (Страница { $page }/{ $total }):

timezone-set-success = ✅ <b>Часовой пояс установлен!</b>

    { $timezone }

    Текущее время в вашем часовом поясе: <b>{ $localTime }</b>

    Все времена гонок теперь будут отображаться в вашем местном времени.

button-reset-timezone = 🔄 Сбросить на UTC
feedback-timezone-set = ✅ Часовой пояс обновлён
feedback-timezone-reset = ✅ Часовой пояс сброшен на UTC
feedback-switched-to-app = Режим APP включён
feedback-switched-to-classic = Классический режим включён
error-mode-switch-failed = ❌ Не удалось переключить режим сайта
error-timezone-not-found = ❌ Часовой пояс не найден для "{ $query }"

    Попробуйте: название города на английском (Moscow), аббревиатуру (MSK), или смещение UTC (UTC+3)
error-invalid-timezone = ❌ Неверный часовой пояс



notif-quali-results = 🏁 <b>Результаты квалификации гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Квалификация закрыта: { $qualiClose }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    Результаты квалификации доступны:

    🔗 <a href="{ $gridLink }">Стартовая решётка</a>

notif-quali-results-no-group = 🏁 <b>Результаты квалификации гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Квалификация закрыта: { $qualiClose }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    Результаты квалификации доступны:

    ⚠️ Для персональных ссылок укажите группу в /settings!

    🔗 <a href="{ $gridLink }">Стартовая решётка</a>

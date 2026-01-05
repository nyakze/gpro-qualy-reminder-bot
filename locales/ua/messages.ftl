# GPRO Bot - Ukrainian Translations

# =======================
# Commands & General
# =======================
start-welcome-new = 👋 <b>Ласкаво просимо до GPRO Bot!</b>

    Давайте налаштуємо бота. Спочатку оберіть бажану мову для посилань на гонки GPRO:

    🌍 <b>Виберіть мову</b> (або пропустіть, щоб використовувати англійську):

start-welcome-existing = 🏁 GPRO Bot АКТИВНИЙ!
    /status - Наступна гонка
    /calendar - Повний сезон
    /next - Наступний сезон
    /settings - Налаштування

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Що ви бажаєте зробити?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendar
# =======================
no-races-scheduled = 🔔 Гонки не заплановані
no-upcoming-qualifications = 🔔 Немає майбутніх кваліфікацій
next-season-not-published = 🌟 <b>Наступний сезон ще не опубліковано</b>

calendar-title-full = 🏁 <b>Повний Сезон</b>
calendar-title-next = 🌟 <b>НАСТУПНИЙ СЕЗОН</b> ({ $count } гонок)

# =======================
# Onboarding
# =======================
onboard-group-title = 🏁 <b>Вибір Групи</b>

    Оберіть вашу групу GPRO для отримання персоналізованих посилань на гонки:

    Виберіть популярну групу або введіть власну:

onboard-group-custom = 🏁 <b>Вибір Групи (Опціонально)</b>

    Введіть вашу групу в одному з цих форматів:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер може містити 1-3 цифри.

    💡 <i>Мова вашого веб-сайту GPRO встановлена відповідно до мови бота. Ви можете змінити її пізніше в /settings</i>

onboard-complete = ✅ <b>Налаштування Завершено!</b>

    🏁 <b>GPRO Bot готовий!</b>

    <b>Доступні команди:</b>
    /status - Наступна гонка
    /calendar - Повний сезон
    /next - Наступний сезон
    /settings - Налаштування

    💡 <i>Ви можете змінити ці налаштування будь-коли через /settings</i>

onboard-complete-with-group = ✅ <b>Налаштування Завершено!</b>

    Група: <b>{ $group }</b>

    🏁 <b>GPRO Bot готовий!</b>

    <b>Доступні команди:</b>
    /status - Наступна гонка
    /calendar - Повний сезон
    /next - Наступний сезон
    /settings - Налаштування

# =======================
# Settings
# =======================
settings-title = ⚙️ <b>Налаштування</b>

    Налаштуйте свої параметри:

settings-language-title = 🌍 <b>Налаштування Мови</b>

    Поточна: { $language }

    Виберіть бажану мову для посилань на гонки GPRO:

ui-lang-menu-title = 💬 <b>Мова Бота</b>

    Виберіть мову інтерфейсу бота:

settings-group-title = 🏁 <b>Налаштування Групи</b>

    Поточна група: <b>{ $group }</b>

    Введіть вашу групу в одному з цих форматів:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер може містити 1-3 цифри.

settings-group-set = ✅ <b>Групу встановлено: { $group }</b>

    Сповіщення про гонки та повтори включатимуть прямі посилання на вашу групу!

settings-notifications-title = 🔔 <b>Налаштування Сповіщень</b>

    Натисніть, щоб увімкнути/вимкнути сповіщення:
    ✅ = Увімкнено | ❌ = Вимкнено

    ℹ️ <i>Це глобальні перемикачі для всіх гонок. Використовуйте кнопку 'Кваліфікація Завершена' у сповіщеннях, щоб вимкнути конкретну гонку.</i>

settings-custom-notif-title = ⏱️ <b>Користувацькі Сповіщення</b>

    Встановіть власний час сповіщень (від { $min }хв до { $max }год до закриття кваліфікації).

    Ви можете мати до 2 користувацьких сповіщень.

    Натисніть на слот, щоб встановити або відредагувати його.

settings-custom-notif-edit = ⏱️ <b>Користувацьке Сповіщення { $slot }</b>{ $current }

    Виберіть попередньо встановлений час або введіть свій:

settings-custom-notif-current = Поточне:

settings-custom-notif-input = ⏱️ <b>Користувацьке Сповіщення { $slot }</b>

    Введіть час для вашого користувацького сповіщення.

    <b>Прийнятні формати:</b>
    • <code>20m</code> або <code>45 minutes</code> (20хв-70год)
    • <code>2h</code> або <code>12 hours</code>
    • <code>1h 30m</code> або <code>2h30m</code>

    <b>Приклади:</b>
    • <code>20m</code> - 20 хвилин до закриття
    • <code>6h</code> - 6 годин до закриття
    • <code>1h 30m</code> - 1 година 30 хвилин до закриття

# =======================
# Buttons
# =======================
button-ui-language = 💬 Мова Бота: { $language }
button-gpro-language = 🌍 Мова GPRO: { $language }
button-language = 🌍 Мова: { $language }
button-group = 🏁 Група: { $group }
button-notifications = 🔔 Сповіщення
button-custom-notifications = ⏱️ Користувацькі Сповіщення
button-back = ◀ Назад
button-back-to-settings = ◀ Назад до Налаштувань
button-back-to-notifications = ◀ Назад до Сповіщень
button-back-to-custom = ◀ Назад до Користувацьких Сповіщень
button-back-custom-notif = ◀ Назад до Користувацьких Сповіщень
button-main-menu = 🏠 Головне Меню
button-reset-group = 🔄 Скинути Групу
button-custom-slot-set = ⏱️ Користувацьке { $slot }: { $time }
button-custom-slot-empty = ➕ Встановити Користувацьке Сповіщення { $slot }
button-previous = ◀ Попередня
button-next = Наступна ▶
button-skip = ⏭️ Пропустити
button-reset-language = 🔄 Скинути до Початкової (Англійська)
button-enable-all = 🔔 Увімкнути Всі Сповіщення
button-disable-all = 🔕 Вимкнути Всі Сповіщення
button-quali-done = ✅ Кваліфікація Завершена
button-reenable-race = 🔄 Увімкнути знову сповіщення Гонки { $raceId }
button-weather = 🌤️ Показати Погоду
button-enter-custom-group = ✏️ Ввести Власну Групу
button-enter-custom-time = ✏️ Ввести Власний Час
button-disable-notification = 🔕 Вимкнути Це Сповіщення
button-cancel = ❌ Скасувати
button-got-it = ✅ Зрозуміло!
button-try-again = 🔄 Спробувати Знову

button-main-menu-status = 📊 Наступна Гонка
button-main-menu-calendar = 📅 Повний Сезон
button-main-menu-next = 🌟 Наступний Сезон
button-main-menu-settings = ⚙️ Налаштування

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Встановити Користувацьке Сповіщення { $slot }
button-custom-notif-time = ⏱️ Користувацьке { $slot }: { $time }

# =======================
# Notifications
# =======================
notif-label-72h = 3д до закриття кваліфікації
notif-label-48h = 2д до закриття кваліфікації
notif-label-24h = 1д до закриття кваліфікації
notif-label-2h = 2год до закриття кваліфікації
notif-label-10min = 10хв до закриття кваліфікації
notif-label-opens = Кваліфікація відкрита
notif-label-replay = Доступний повтор гонки
notif-label-live = Гонка в прямому ефірі
notif-label-results = Доступні результати гонки

notif-quali-closes = <b>Кваліфікація закривається через { $time }!</b>
notif-quali-opens = <b>Кваліфікація відкрита (або відкривається найближчим часом)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Гонка #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Дедлайн кваліфікації: { $qualiDeadline }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Перейти до Кваліфікації</a>

    <i>Натисніть кнопку '✅ Кваліфікація Завершена', щоб вимкнути сповіщення для цієї гонки</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Гонка #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Дедлайн кваліфікації: { $qualiDeadline }</b>
    🏎 <b>Гонка: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Перейти до Кваліфікації</a>

    ℹ️ <b>Автоматичні сповіщення вимкнено</b> для цієї гонки
    <i>Натисніть кнопку '🔄 Увімкнути знову', щоб відновити сповіщення</i>

notif-race-live = 🏁 <b>Гонка #{ $raceId } В ПРЯМОМУ ЕФІРІ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Дивитися Гонку в Прямому Ефірі</a>

notif-race-live-no-group = 🏁 <b>Гонка #{ $raceId } В ПРЯМОМУ ЕФІРІ!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Встановіть вашу групу в /settings для прямого посилання!

    🔗 <a href="{ $raceLink }">Дивитися Гонку в Прямому Ефірі</a>

notif-race-replay = 📺 <b>Доступний Повтор Гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Якщо гонка вже була розрахована, повтор доступний тут:

    🔗 <a href="{ $replayLink }">Дивитися Повтор</a>

notif-race-replay-no-group = 📺 <b>Доступний Повтор Гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Якщо гонка вже була розрахована, повтор доступний тут:

    ⚠️ Для персоналізованих посилань встановіть вашу групу в /settings!

    🔗 <a href="{ $replayLink }">Дивитися Повтор</a>

notif-race-results = 📊 <b>Доступні Результати Гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Результати гонки тепер доступні:

    🔗 <a href="{ $analysisLink }">Аналіз Гонки</a>
    🔗 <a href="{ $summaryLink }">Підсумки Гонки</a>

notif-race-results-no-group = 📊 <b>Доступні Результати Гонки #{ $raceId }</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Результати гонки тепер доступні:

    🔗 <a href="{ $analysisLink }">Аналіз Гонки</a>

    ⚠️ Для персоналізованих Підсумків Гонки встановіть вашу групу в /settings!

# =======================
# Weather
# =======================
weather-title = 🌤️ <b>Прогноз Погоди для Гонки</b>
weather-practice-q1 = <b>Практика / Кваліфікація 1:</b> { $weather }
weather-temp-hum = Темп: { $temp }°C • Вологість: { $hum }%
weather-q2-start = <b>Кваліфікація 2 / Старт Гонки:</b> { $weather }
weather-race-conditions = <b>Умови Гонки:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Темп: { $temp } • Вологість: { $hum }
    Ймовірність дощу: { $rain }
weather-not-available = ⚠️ Дані про погоду недоступні
weather-cached = ℹ️ Погода вже кешована для <b>Гонки #{ $raceId }: { $track }</b>

    Використовуйте <code>/weather force</code> для примусового оновлення.
    Використовуйте /status, щоб побачити сповіщення з кнопкою погоди.
weather-fetching = 🔄 Отримання погоди для <b>Гонки #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Примусове оновлення погоди для <b>Гонки #{ $raceId }: { $track }</b>...
weather-success = ✅ Дані про погоду отримано для <b>Гонки #{ $raceId }: { $track }</b>

    Використовуйте /status, щоб перевірити сповіщення з кнопкою погоди!
weather-failed = ❌ Не вдалося отримати дані про погоду

    Перевірте, чи дійсний токен GPRO API і чи доступний Practice API.

# =======================
# Admin
# =======================
admin-only = ❌ Тільки для адміністраторів
admin-calendar-updated = ✅ <b>Календар</b>: { $count } гонок
    🔄 <b>{ $userCount } користувачів</b> скинуто
admin-next-season-ready = 🌟 <b>Наступний сезон готовий!</b> { $count } гонок
    Використовуйте /next для перегляду
admin-next-season-not-published = ℹ️ <b>Наступний сезон не опубліковано</b>
admin-users-count = 📊 <b>{ $count } користувачів</b>:
admin-users-none = 📊 <b>0 користувачів</b> у базі даних
admin-no-races = ❌ Немає гонок у календарі
admin-no-upcoming-races = ❌ Не знайдено майбутніх гонок

# =======================
# Errors & Validation
# =======================
error-invalid-format = ❌ Невірний формат!

    Будь ласка, використовуйте:
    • <b>E</b> для Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> тощо.

    Спробуйте знову:

error-invalid-format-onboarding = ❌ Невірний формат!

    Будь ласка, використовуйте:
    • <b>E</b> для Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> тощо.

    Спробуйте знову або використовуйте /start для перезапуску:

error-invalid-time = ❌ <b>Помилка:</b> { $error }

    Будь ласка, спробуйте знову з правильним форматом, наприклад: <code>2h</code>, <code>30m</code> або <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Помилка:</b> { $error }

    Будь ласка, спробуйте знову.

error-invalid-race = ❌ Невірний ID гонки
error-invalid-page = ❌ Невірна сторінка
error-invalid-language = ❌ Невірна мова
error-invalid-slot = ❌ Невірний слот
error-invalid-data = ❌ Невірні дані
error-reset-failed = ❌ Скидання не вдалося
error-race-not-found = ❌ Гонку не знайдено
error-weather-not-available = ⚠️ Дані про погоду ще недоступні
error-weather-send-failed = ❌ Не вдалося надіслати погоду

# =======================
# Feedback & Confirmations
# =======================
feedback-all-enabled = ✅ Всі сповіщення увімкнено!
feedback-all-disabled = ✅ Всі сповіщення вимкнено!
feedback-notif-enabled = ✅ { $label } увімкнено!
feedback-notif-disabled = ✅ { $label } вимкнено!
feedback-quali-done = ✅ Готово!
feedback-race-marked-done = ✅ <i>Гонку позначено як завершену!</i>
feedback-reset = 🔄 Скинуто!
feedback-notifications-reset = 🔄 <i>Сповіщення скинуто!</i>
feedback-reenabled = 🔄 Увімкнено знову!
feedback-notifications-reenabled = 🔄 <i>Сповіщення увімкнено знову!</i>
feedback-language-set = ✅ Мову встановлено на { $language }
feedback-language-reset = ✅ Мову скинуто до Англійської
feedback-ui-language-set = ✅ Мову бота встановлено на { $language }
feedback-group-set = ✅ Групу встановлено на { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Користувацьке сповіщення { $slot } вимкнено
feedback-skip-language = ⏭️ Використовується мова за замовчуванням (Англійська)
feedback-skip-group = ⏭️ Вибір групи пропущено
feedback-welcome = ✅ Ласкаво просимо на борт!
feedback-weather-sent = 🌤️ Прогноз погоди надіслано!

# =======================
# Time Formatting
# =======================
# Weekday abbreviations (2-letter)
weekday-mon = Пн
weekday-tue = Вт
weekday-wed = Ср
weekday-thu = Чт
weekday-fri = Пт
weekday-sat = Сб
weekday-sun = Нд

time-minutes = { $minutes ->
    [one] { $minutes } хвилина
    [few] { $minutes } хвилини
   *[other] { $minutes } хвилин
}
time-hours = { $hours ->
    [one] { $hours } година
    [few] { $hours } години
   *[other] { $hours } годин
}
time-hours-minutes = { $hours ->
    [one] { $hours } година
    [few] { $hours } години
   *[other] { $hours } годин
} { $minutes ->
    [one] { $minutes } хвилина
    [few] { $minutes } хвилини
   *[other] { $minutes } хвилин
}
time-hours-minutes-short = { $hours }год{ $minutes }хв
time-hours-short = { $hours }год
time-minutes-short = { $minutes }хв
time-days-hours-short = { $days }д{ $hours }год
time-days-hours-minutes-short = { $days }д{ $hours }год{ $minutes }хв
time-days = { $days ->
    [one] { $days } день
    [few] { $days } дні
   *[other] { $days } днів
}
time-days-hours = { $days ->
    [one] { $days } день
    [few] { $days } дні
   *[other] { $days } днів
} { $hours ->
    [one] { $hours } година
    [few] { $hours } години
   *[other] { $hours } годин
}
time-months = { $months ->
    [one] { $months } місяць
    [few] { $months } місяці
   *[other] { $months } місяців
}
time-months-days = { $months ->
    [one] { $months } місяць
    [few] { $months } місяці
   *[other] { $months } місяців
} { $days ->
    [one] { $days } день
    [few] { $days } дні
   *[other] { $days } днів
}

# =======================
# Group Display
# =======================
group-not-set = Не встановлено
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Custom Notification Messages
# =======================
custom-notif-set = Користувацьке сповіщення { $slot } встановлено на { $time }
custom-notif-set-success = Користувацьке сповіщення { $slot } встановлено на { $time }
custom-notif-not-set = Не встановлено
custom-notif-min-error = Мінімальний час - 20 хвилин
custom-notif-max-error = Максимальний час - 70 годин
custom-notif-invalid-slot = Невірний слот (має бути 0-{ $max })
custom-notif-empty-error = Час не може бути порожнім
custom-notif-invalid-format = Невірний формат. Використовуйте: 2h, 30m або 1h 30m
custom-notif-enter-time = Будь ласка, введіть час
custom-notif-error-parsing = ❌ <b>Помилка:</b> { $error }

    Будь ласка, спробуйте знову з правильним форматом, наприклад: <code>2h</code>, <code>30m</code> або <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Ваше користувацьке сповіщення встановлено!
custom-notif-error-setting = ❌ <b>Помилка:</b> { $error }

    Будь ласка, спробуйте знову.

# =======================
# Validation
# =======================
validation-time-empty = Час не може бути порожнім
validation-time-min = Мінімальний час - 20 хвилин
validation-time-max = Максимальний час - 70 годин
validation-enter-time = Будь ласка, введіть час
validation-invalid-format = Невірний формат. Використовуйте: 2h, 30m або 1h 30m
validation-invalid-slot = Невірний слот (має бути 0-{ $maxSlots })

# =======================
# Notification Labels
# =======================
notif-label-72h = 3д до закриття кваліфікації
notif-label-48h = 2д до закриття кваліфікації
notif-label-24h = 1д до закриття кваліфікації
notif-label-2h = 2год до закриття кваліфікації
notif-label-10min = 10хв до закриття кваліфікації
notif-label-opens-soon = Кваліфікація відкрита
notif-label-race-replay = Доступний повтор гонки
notif-label-race-live = Гонка в прямому ефірі
notif-label-race-results = Доступні результати гонки

# =======================
# Notification Menu
# =======================
notif-menu-title = 🔔 <b>Налаштування Сповіщень</b>

    Натисніть, щоб увімкнути/вимкнути сповіщення:
    ✅ = Увімкнено | ❌ = Вимкнено

    ℹ️ <i>Це глобальні перемикачі для всіх гонок. Використовуйте кнопку 'Кваліфікація Завершена' у сповіщеннях, щоб вимкнути конкретну гонку.</i>

# =======================
# Group Menu
# =======================
group-menu-title = 🏁 <b>Налаштування Групи</b>

    Поточна група: <b>{ $groupDisplay }</b>

    Введіть вашу групу в одному з цих форматів:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Номер може містити 1-3 цифри.
group-reset-success = ✅ Групу успішно скинуто

# =======================
# Language Menu
# =======================
lang-menu-title = 🌍 <b>Налаштування Мови</b>

    Поточна: { $currentLang }

    Виберіть бажану мову для посилань на гонки GPRO:

# =======================
# Custom Notification Menu
# =======================
custom-notif-menu-title = ⏱️ <b>Користувацькі Сповіщення</b>

    Встановіть власний час сповіщень (від { $minTime }хв до { $maxTime }год до закриття кваліфікації).

    Ви можете мати до 2 користувацьких сповіщень.

    Натисніть на слот, щоб встановити або відредагувати його.

# =======================
# Weather
# =======================
weather-unavailable = ⚠️ Дані про погоду недоступні
weather-title = 🌤️ <b>Прогноз Погоди для Гонки</b>
weather-race-header = Гонка #{ $raceId }: { $track }
weather-practice-q1 = <b>Практика / Кваліфікація 1:</b> { $weather }
weather-temp-hum = Темп: { $temp }°C • Вологість: { $hum }%
weather-q2-race-start = <b>Кваліфікація 2 / Старт Гонки:</b> { $weather }
weather-race-conditions = <b>Умови Гонки:</b>
weather-start-0h30m = <b>Старт - 0год30хв:</b>
weather-0h30m-1h00m = <b>0год30хв - 1год00хв:</b>
weather-1h00m-1h30m = <b>1год00хв - 1год30хв:</b>
weather-1h30m-2h00m = <b>1год30хв - 2год00хв:</b>
weather-temp-hum-range = Темп: { $temp } • Вологість: { $hum }
weather-rain-prob = Ймовірність дощу: { $rain }

# Weather Conditions
weather-condition-sunny = Сонячно
weather-condition-partially-cloudy = Мінлива хмарність
weather-condition-cloudy = Хмарно
weather-condition-very-cloudy = Дуже хмарно
weather-condition-rain = Дощ

# =======================
# Timezone Settings
# =======================
button-timezone = ⏰ Часовий пояс: { $timezone }
timezone-menu-title = ⏰ <b>Налаштування Часового Поясу</b>

    Поточний часовий пояс: <b>{ $timezone }</b>

    Введіть ваш часовий пояс (назва міста, абревіатура або зміщення UTC):

    Приклади: <code>Київ</code>, <code>EET</code>, <code>UTC+2</code>, <code>Лондон</code>

timezone-select-matches = 🌍 <b>Виберіть ваш часовий пояс:</b>

    Збіги для "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Виберіть ваш часовий пояс:</b>

    Збіги для "{ $query }" (Сторінка { $page }/{ $total }):

timezone-set-success = ✅ <b>Часовий пояс встановлено!</b>

    { $timezone }

    Поточний час у вашому часовому поясі: <b>{ $localTime }</b>

    Тепер весь час гонок відображатиметься у вашому місцевому часі.

button-reset-timezone = 🔄 Скинути до UTC
feedback-timezone-set = ✅ Часовий пояс оновлено
feedback-timezone-reset = ✅ Часовий пояс скинуто до UTC
error-timezone-not-found = ❌ Не знайдено часовий пояс для "{ $query }"

    Спробуйте: назву міста (Київ), абревіатуру (EET) або зміщення UTC (UTC+2)
error-invalid-timezone = ❌ Невірний часовий пояс

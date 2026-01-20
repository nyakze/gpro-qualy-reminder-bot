
# GPRO Bot - Български превод

# =======================
# Команди и Основни
# =======================
start-welcome-new = 👋 <b>Добре дошли в GPRO Bot!</b>

    Нека ви настроим. Първо, изберете предпочитания език за връзки към състезания в GPRO:

    🌍 <b>Изберете вашия език</b> (или пропуснете, за да използвате английски):

start-welcome-existing = 🏁 GPRO Bot АКТИВЕН!
    /status - Следващо състезание
    /calendar - Пълен сезон
    /next - Следващ сезон
    /settings - Настройки

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    Какво бихте искали да направите?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Статус и Календар
# =======================
no-races-scheduled = 🔔 Няма планирани състезания
no-upcoming-qualifications = 🔔 Няма предстоящи квалификации
next-season-not-published = 🌟 <b>Следващият сезон все още не е публикуван</b>

calendar-title-full = 🏁 <b>Пълен сезон</b>
calendar-title-next = 🌟 <b>СЛЕДВАЩ СЕЗОН</b> ({ $count } състезания)

# =======================
# Първоначална настройка
# =======================
onboard-group-title = 🏁 <b>Избор на група</b>

    Изберете вашата GPRO група, за да получавате персонализирани връзки към състезания:

    Изберете обща група или въведете своя:

onboard-group-custom = 🏁 <b>Избор на група (по избор)</b>

    Въведете вашата група в един от следните формати:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Числата могат да бъдат от 1 до 3 цифри.

    💡 <i>Езикът на вашия GPRO уебсайт е зададен да съответства на езика на бота. Можете да го промените по-късно в /settings</i>

onboard-complete = ✅ <b>Настройката е завършена!</b>

    🏁 <b>GPRO Bot е готов!</b>

    <b>Налични команди:</b>
    /status - Следващо състезание
    /calendar - Пълен сезон
    /next - Следващ сезон
    /settings - Настройки

    💡 <i>Можете да променяте тези настройки по всяко време с /settings</i>

onboard-complete-with-group = ✅ <b>Настройката е завършена!</b>

    Група: <b>{ $group }</b>

    🏁 <b>GPRO Bot е готов!</b>

    <b>Налични команди:</b>
    /status - Следващо състезание
    /calendar - Пълен сезон
    /next - Следващ сезон
    /settings - Настройки

# =======================
# Настройки
# =======================
settings-title = ⚙️ <b>Настройки</b>

    Конфигурирайте вашите предпочитания:

settings-language-title = 🌍 <b>Езикови настройки</b>

    Текущ: { $language }

    Изберете предпочитания език за връзки към състезания в GPRO:

ui-lang-menu-title = 💬 <b>Език на бота</b>

    Изберете език на интерфейса на бота:

settings-group-title = 🏁 <b>Настройки на групата</b>

    Текуща група: <b>{ $group }</b>

    Въведете вашата група в един от следните формати:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Числата могат да бъдат от 1 до 3 цифри.

settings-group-set = ✅ <b>Групата е зададена на: { $group }</b>

    Известията за състезания и повторения ще включват директни връзки към вашата група!

settings-notifications-title = 🔔 <b>Настройки на известията</b>

    Щракнете, за да включите/изключите известията:
    ✅ = Активни | ❌ = Неактивни

    ℹ️ <i>Това са глобални превключватели за всички състезания. Използвайте бутона 'Квалификацията е готова' в известията, за да деактивирате конкретно състезание.</i>

settings-custom-notif-title = ⏱️ <b>Персонализирани известия</b>

    Задайте свои собствени времена за известия ({ $min }m - { $max }h преди затваряне на квалификацията).

    Можете да имате до 2 персонализирани известия.

    Щракнете върху слот, за да го зададете или редактирате.

settings-custom-notif-edit = ⏱️ <b>Персонализирано известие { $slot }</b>{ $current }

    Изберете предварително зададено време или въведете персонализирано време:

settings-custom-notif-current = Текущо:

settings-custom-notif-input = ⏱️ <b>Персонализирано известие { $slot }</b>

    Въведете вашето персонализирано време за известие.

    <b>Приемани формати:</b>
    • <code>20m</code> или <code>45 minutes</code> (20m-70h)
    • <code>2h</code> или <code>12 hours</code>
    • <code>1h 30m</code> или <code>2h30m</code>

    <b>Примери:</b>
    • <code>20m</code> - 20 минути преди
    • <code>6h</code> - 6 часа преди
    • <code>1h 30m</code> - 1 час и 30 минути преди

# =======================
# Бутони
# =======================
button-ui-language = 💬 Език на бота: { $language }
button-gpro-language = 🌍 GPRO език: { $language }
button-language = 🌍 Език: { $language }
button-group = 🏁 Група: { $group }
button-notifications = 🔔 Известия
button-custom-notifications = ⏱️ Персонализирани известия
button-back = ◀ Назад
button-back-to-settings = ◀ Назад към настройките
button-back-to-notifications = ◀ Назад към известията
button-back-to-custom = ◀ Назад към персонализираните известия
button-back-custom-notif = ◀ Назад към персонализираните известия
button-main-menu = 🏠 Главно меню
button-reset-group = 🔄 Нулиране на групата
button-custom-slot-set = ⏱️ Персонализирано { $slot }: { $time }
button-custom-slot-empty = ➕ Задаване на персонализирано известие { $slot }
button-previous = ◀ Предишна
button-next = Следваща ▶
button-skip = ⏭️ Пропусни
button-reset-language = 🔄 Нулиране до подразбиране (английски)
button-enable-all = 🔔 Активиране на всички известия
button-disable-all = 🔕 Деактивиране на всички известия
button-enable-category = 🔔 Активиране на категорията
button-disable-category = 🔕 Деактивиране на категорията
button-quali-done = ✅ Квалификацията е готова
button-reenable-race = 🔄 Повторно активиране на известия за състезание { $raceId }
button-weather = 🌤️ Показване на времето
button-snooze-5m = 🔔🔁 +5м
button-snooze-15m = 🔔🔁 +15м
button-snooze-30m = 🔔🔁 +30м
button-snooze-1h = 🔔🔁 +1ч
button-snooze-2h = 🔔🔁 +2ч
button-snooze-4h = 🔔🔁 +4ч
button-snooze-8h = 🔔🔁 +8ч
button-enter-custom-group = ✏️ Въвеждане на персонализирана група
button-enter-custom-time = ✏️ Въвеждане на персонализирано време
button-disable-notification = 🔕 Деактивиране на това известие
button-cancel = ❌ Отказ
button-got-it = ✅ Разбрано!
button-try-again = 🔄 Опитайте отново

button-main-menu-status = 📊 Следващо състезание
button-main-menu-calendar = 📅 Пълен сезон
button-main-menu-next = 🌟 Следващ сезон
button-main-menu-settings = ⚙️ Настройки

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Задаване на персонализирано известие { $slot }
button-custom-notif-time = ⏱️ Персонализирано { $slot }: { $time }

# =======================
# Известия
# =======================
notif-category-before-qualifying = Преди квалификацията
notif-category-qualifying-events = Събития от квалификацията
notif-category-race-events = Гонкови събития

notif-label-72h = 3д преди затваряне на квалификацията
notif-label-48h = 2д преди затваряне на квалификацията
notif-label-24h = 1д преди затваряне на квалификацията
notif-label-2h = 2ч преди затваряне на квалификацията
notif-label-10min = 10мин преди затваряне на квалификацията
notif-label-opens = Квалификацията е отворена
notif-label-quali-results = Резултати от квалификацията налични
notif-label-replay = Повторение на състезанието е налично
notif-label-live = Състезанието е на живо
notif-label-results = Резултатите от състезанието са налични

notif-quali-closes = <b>Квалификацията се затваря след { $time }!</b>
notif-quali-opens = <b>Квалификацията е отворена</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Краен срок за квал.: { $qualiDeadline }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Към квалификацията</a>

    <i>Натиснете бутона '✅ Квалификацията е готова', за да деактивирате известията за това състезание</i>

notif-snooze-title = <b>Напомняне (отложено)</b>

notif-snooze-message = { $emoji } { $title }

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Краен срок за квал.: { $qualiDeadline }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Към квалификацията</a>

    <i>Натиснете бутона '✅ Квалификацията е готова', за да деактивирате известията за това състезание</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Краен срок за квал.: { $qualiDeadline }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Към квалификацията</a>

    ℹ️ <b>Автоматичните известия са деактивирани</b> за това състезание
    <i>Натиснете бутона '🔄 Повторно активиране', за да активирате отново известията</i>

notif-quali-closed-title = <b>Квалификацията е затворена в момента</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Квалификацията приключи: { $qualiDeadline }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    ⏳ <i>Квалификацията е затворена в момента. Следващата сесия за квалификация ще се отвори след приключване на настоящото състезание. Моля, изчакайте изчисляването на състезанието.</i>

notif-race-live = 🏁 <b>Състезание #{ $raceId } е НА ЖИВО!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Гледайте състезанието на живо</a>

notif-race-live-no-group = 🏁 <b>Състезание #{ $raceId } е НА ЖИВО!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Задайте вашата група в /settings за директна връзка!

    🔗 <a href="{ $raceLink }">Гледайте състезанието на живо</a>

notif-race-replay = 📺 <b>Повторение на състезание #{ $raceId } е налично</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Гледайте повторението на състезанието:

    🔗 <a href="{ $replayLink }">Гледайте повторението</a>

notif-race-replay-no-group = 📺 <b>Повторение на състезание #{ $raceId } е налично</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Гледайте повторението на състезанието:

    ⚠️ За персонализирани връзки, задайте вашата група в /settings!

    🔗 <a href="{ $replayLink }">Гледайте повторението</a>

notif-race-results = 📊 <b>Резултати от състезание #{ $raceId } са налични</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Резултатите от състезанието са вече налични:

    🔗 <a href="{ $analysisLink }">Анализ на състезанието</a>
    🔗 <a href="{ $summaryLink }">Обобщение на състезанието</a>

notif-race-results-no-group = 📊 <b>Резултати от състезание #{ $raceId } са налични</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Резултатите от състезанието са вече налични:

    🔗 <a href="{ $analysisLink }">Анализ на състезанието</a>

    ⚠️ За персонализирано обобщение, задайте вашата група в /settings!

# =======================
# Време
# =======================
weather-title = 🌤️ <b>Прогноза за времето на състезанието</b>
weather-practice-q1 = <b>Тренировка / Квалификация 1:</b> { $weather }
weather-temp-hum = Темп: { $temp }°C • Влаж: { $hum }%
weather-q2-start = <b>Квалификация 2 / Начало на състезанието:</b> { $weather }
weather-race-conditions = <b>Условия по време на състезанието:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Температура: { $temp } • Влажност: { $hum }
    Вероятност за дъжд: { $rain }
weather-not-available = ⚠️ Данните за времето не са налични
weather-cached = ℹ️ Времето вече е кеширано за <b>Състезание #{ $raceId }: { $track }</b>

    Използвайте <code>/weather force</code>, за да принудите актуализация.
    Използвайте /status, за да видите известието с бутон за времето.
weather-fetching = 🔄 Извличане на данни за времето за <b>Състезание #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Принудителна актуализация на времето за <b>Състезание #{ $raceId }: { $track }</b>...
weather-success = ✅ Данните за времето са извлечени за <b>Състезание #{ $raceId }: { $track }</b>

    Използвайте /status, за да тествате известието с бутон за времето!
weather-failed = ❌ Неуспешно извличане на данни за времето

    Проверете дали GPRO API токенът е валиден и дали Practice API е достъпен.

# =======================
# Администраторски
# =======================
admin-only = ❌ Само за администратори
admin-calendar-updated = ✅ <b>Календар</b>: { $count } състезания
    🔄 <b>{ $userCount } потребители</b> нулирани
admin-next-season-ready = 🌟 <b>Следващият сезон е готов!</b> { $count } състезания
    Използвайте /next за преглед
admin-next-season-not-published = ℹ️ <b>Следващият сезон не е публикуван</b>
admin-users-count = 📊 <b>{ $count } потребители</b>:
admin-users-none = 📊 <b>0 потребители</b> в базата данни
admin-no-races = ❌ Няма състезания в календара
admin-no-upcoming-races = ❌ Не са намерени предстоящи състезания

# =======================
# Грешки и валидация
# =======================
error-invalid-format = ❌ Невалиден формат!

    Моля, използвайте:
    • <b>E</b> за Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> и др.

    Опитайте отново:

error-invalid-format-onboarding = ❌ Невалиден формат!

    Моля, използвайте:
    • <b>E</b> за Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> и др.

    Опитайте отново или използвайте /start за рестартиране:

error-invalid-time = ❌ <b>Грешка:</b> { $error }

    Моля, опитайте отново с валиден формат като: <code>2h</code>, <code>30m</code>, или <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Грешка:</b> { $error }

    Моля, опитайте отново.

error-invalid-race = ❌ Невалиден идентификатор на състезание
error-invalid-page = ❌ Невалидна страница
error-invalid-language = ❌ Невалиден език
error-invalid-category = ❌ Невалидна категория
error-invalid-slot = ❌ Невалиден слот
error-invalid-data = ❌ Невалидни данни
error-reset-failed = ❌ Нулирането е неуспешно
error-race-not-found = ❌ Състезанието не е намерено
error-weather-not-available = ⚠️ Данните за времето все още не са налични
error-weather-send-failed = ❌ Неуспешно изпращане на данни за времето

# =======================
# Обратна връзка и потвърждения
# =======================
feedback-all-enabled = ✅ Всички известия са активирани!
feedback-all-disabled = ✅ Всички известия са деактивирани!
feedback-category-enabled = ✅ { $category } активирана!
feedback-category-disabled = ✅ { $category } деактивирана!
feedback-notif-enabled = ✅ { $label } активирано!
feedback-notif-disabled = ✅ { $label } деактивирано!
feedback-quali-done = ✅ Готово!
feedback-race-marked-done = ✅ <i>Състезанието е маркирано като готово!</i>
feedback-reset = 🔄 Нулирано!
feedback-notifications-reset = 🔄 <i>Известията са нулирани!</i>
feedback-reenabled = 🔄 Повторно активирано!
feedback-notifications-reenabled = 🔄 <i>Известията са повторно активирани!</i>
feedback-language-set = ✅ Езикът е зададен на { $language }
feedback-language-reset = ✅ Езикът е нулиран до английски
feedback-ui-language-set = ✅ Езикът на бота е зададен на { $language }
feedback-group-set = ✅ Групата е зададена на { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Персонализирано известие { $slot } деактивирано
feedback-skip-language = ⏭️ Използване на език по подразбиране (английски)
feedback-skip-group = ⏭️ Изборът на група е пропуснат
feedback-welcome = ✅ Добре дошли на борда!
feedback-weather-sent = 🌤️ Прогноза за времето е изпратена!
snooze-confirmed = 🔁⏰ Напомняне преместено в { $time }
snooze-max-reached = 🔁❌ Лимитът за отлагане е достигнат (3/3)
snooze-past-deadline = 🔁❌ Не може да се отлага след крайния срок
snooze-past-next = 🔁❌ Следващо напомняне след { $minutes }мин

# =======================
# Форматиране на време
# =======================
# Съкращения за дни от седмицата (2 букви)
weekday-mon = Пн
weekday-tue = Вт
weekday-wed = Ср
weekday-thu = Чт
weekday-fri = Пт
weekday-sat = Сб
weekday-sun = Нд

time-minutes = { $minutes ->
    [one] { $minutes } минута
   *[other] { $minutes } минути
}
time-hours = { $hours ->
    [one] { $hours } час
   *[other] { $hours } часа
}
time-hours-minutes = { $hours ->
    [one] { $hours } час
   *[other] { $hours } часа
} { $minutes ->
    [one] { $minutes } минута
   *[other] { $minutes } минути
}
time-hours-minutes-short = { $hours }ч{ $minutes }м
time-hours-short = { $hours }ч
time-minutes-short = { $minutes }м
time-days-hours-short = { $days }д{ $hours }ч
time-days-hours-minutes-short = { $days }д{ $hours }ч{ $minutes }м
time-days = { $days ->
    [one] { $days } ден
   *[other] { $days } дни
}
time-days-hours = { $days ->
    [one] { $days } ден
   *[other] { $days } дни
} { $hours ->
    [one] { $hours } час
   *[other] { $hours } часа
}
time-months = { $months ->
    [one] { $months } месец
   *[other] { $months } месеца
}
time-months-days = { $months ->
    [one] { $months } месец
   *[other] { $months } месеца
} { $days ->
    [one] { $days } ден
   *[other] { $days } дни
}

# =======================
# Показване на група
# =======================
group-not-set = Не е зададена
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Съобщения за персонализирани известия
# =======================
custom-notif-set = Персонализирано известие { $slot } зададено на { $time }
custom-notif-set-success = Персонализирано известие { $slot } зададено на { $time }
custom-notif-not-set = Не е зададено
custom-notif-min-error = Минималното време е 20 минути
custom-notif-max-error = Максималното време е 70 часа
custom-notif-invalid-slot = Невалиден слот (трябва да бъде 0-{ $max })
custom-notif-empty-error = Времето не може да бъде празно
custom-notif-invalid-format = Невалиден формат. Използвайте: 2h, 30m, или 1h 30m
custom-notif-enter-time = Моля, въведете време
custom-notif-error-parsing = ❌ <b>Грешка:</b> { $error }

    Моля, опитайте отново с валиден формат като: <code>2h</code>, <code>30m</code>, или <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Вашето персонализирано известие е зададено!
custom-notif-error-setting = ❌ <b>Грешка:</b> { $error }

    Моля, опитайте отново.

# =======================
# Валидация
# =======================
validation-time-empty = Времето не може да бъде празно
validation-time-min = Минималното време е 20 минути
validation-time-max = Максималното време е 70 часа
validation-enter-time = Моля, въведете време
validation-invalid-format = Невалиден формат. Използвайте: 2h, 30m, или 1h 30m
validation-invalid-slot = Невалиден слот (трябва да бъде 0-{ $maxSlots })
validation-group-invalid-format = Невалиден формат на групата. Използвайте: E, M1-5, P1-25, A1-80, R1-150
validation-group-e-no-numbers = Elite групата няма номерирани групи (използвайте 'E')
validation-group-range-m = Master групата трябва да бъде 1-5
validation-group-range-p = Pro групата трябва да бъде 1-25
validation-group-range-a = Amateur групата трябва да бъде 1-80
validation-group-range-r = Rookie групата трябва да бъде 1-150

# =======================
# Етикети на известия
# =======================
notif-label-72h = 3д преди затваряне на квалификацията
notif-label-48h = 2д преди затваряне на квалификацията
notif-label-24h = 1д преди затваряне на квалификацията
notif-label-2h = 2ч преди затваряне на квалификацията
notif-label-10min = 10мин преди затваряне на квалификацията
notif-label-opens-soon = Квалификацията е отворена
notif-label-quali-results = Резултати от квалификацията налични
notif-label-race-replay = Повторение на състезанието е налично
notif-label-race-live = Състезанието е на живо
notif-label-race-results = Резултатите от състезанието са налични

# =======================
# Меню за известия
# =======================
notif-menu-title = 🔔 <b>Настройки на известията</b>

    Щракнете, за да включите/изключите известията:
    ✅ = Активни | ❌ = Неактивни

    ℹ️ <i>Това са глобални превключватели за всички състезания. Използвайте бутона 'Квалификацията е готова' в известията, за да деактивирате конкретно състезание.</i>

# =======================
# Меню за група
# =======================
group-menu-title = 🏁 <b>Настройки на групата</b>

    Текуща група: <b>{ $groupDisplay }</b>

    Въведете вашата група в един от следните формати:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Числата могат да бъдат от 1 до 3 цифри.
group-reset-success = ✅ Групата е нулирана успешно

# =======================
# Езиково меню
# =======================
lang-menu-title = 🌍 <b>Езикови настройки</b>

    Текущ: { $currentLang }

    Изберете предпочитания език за връзки към състезания в GPRO:

# =======================
# Меню за персонализирани известия
# =======================
custom-notif-menu-title = ⏱️ <b>Персонализирани известия</b>

    Задайте свои собствени времена за известия ({ $minTime }m - { $maxTime }h преди затваряне на квалификацията).

    Можете да имате до 2 персонализирани известия.

    Щракнете върху слот, за да го зададете или редактирате.

# =======================
# Време
# =======================
weather-unavailable = ⚠️ Данните за времето не са налични
weather-title = 🌤️ <b>Прогноза за времето на състезанието</b>
weather-race-header = Състезание #{ $raceId }: { $track }
weather-practice-q1 = <b>Тренировка / Квалификация 1:</b> { $weather }
weather-temp-hum = Темп: { $temp }°C • Влаж: { $hum }%
weather-q2-race-start = <b>Квалификация 2 / Начало на състезанието:</b> { $weather }
weather-race-conditions = <b>Условия по време на състезанието:</b>
weather-start-0h30m = <b>Начало - 0ч30м:</b>
weather-0h30m-1h00m = <b>0ч30м - 1ч00м:</b>
weather-1h00m-1h30m = <b>1ч00м - 1ч30м:</b>
weather-1h30m-2h00m = <b>1ч30м - 2ч00м:</b>
weather-temp-hum-range = Темп: { $temp } • Влаж: { $hum }
weather-rain-prob = Вероятност за дъжд: { $rain }

# Метеорологични условия
weather-condition-sunny = Слънчево
weather-condition-partially-cloudy = Частично облачно
weather-condition-cloudy = Облачно
weather-condition-very-cloudy = Много облачно
weather-condition-rain = Дъжд

# =======================
# Настройки за часова зона
# =======================
button-timezone = ⏰ Часова зона: { $timezone }
button-website-mode = 🌐 Тип връзка: { $mode }
website-mode-classic = Класически
timezone-menu-title = ⏰ <b>Настройки за часова зона</b>

    Текуща часова зона: <b>{ $timezone }</b>

    Въведете вашата часова зона (име на град, съкращение или UTC отместване):

    Примери: <code>София</code>, <code>EET</code>, <code>UTC+2</code>, <code>Лондон</code>

timezone-select-matches = 🌍 <b>Изберете вашата часова зона:</b>

    Съвпадения за "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Изберете вашата часова зона:</b>

    Съвпадения за "{ $query }" (Страница { $page }/{ $total }):

timezone-set-success = ✅ <b>Часовата зона е зададена!</b>

    { $timezone }

    Текущо време във вашата часова зона: <b>{ $localTime }</b>

    Всички времена на състезанията вече ще бъдат показани в локалното ви време.

button-reset-timezone = 🔄 Нулиране до UTC
feedback-timezone-set = ✅ Часовата зона е актуализирана
feedback-timezone-reset = ✅ Часовата зона е нулирана до UTC
feedback-switched-to-app = Режим APP активиран
feedback-switched-to-classic = Класически режим активиран
error-mode-switch-failed = ❌ Неуспешно превключване на режим на уебсайта
error-timezone-not-found = ❌ Не е намерена часова зона за "{ $query }"

    Опитайте: име на град (София), съкращение (EET), или UTC отместване (UTC+2)
error-invalid-timezone = ❌ Невалидна часова зона



notif-quali-results = 🏁 <b>Резултати от квалификацията - Състезание #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Квалификация приключена</b>
    🏎 <b>Състезание: { $raceTime }</b>

    Резултати от квалификацията налични:

    🔗 <a href="{ $gridLink }">Стартова решетка</a>

notif-quali-results-no-group = 🏁 <b>Резултати от квалификацията - Състезание #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Квалификация приключена</b>
    🏎 <b>Състезание: { $raceTime }</b>

    Резултати от квалификацията налични:

    ⚠️ За персонализирани връзки, задайте вашата група в /settings!

    🔗 <a href="{ $gridLink }">Стартова решетка</a>

# =======================
# Напомняне за нов сезон
# =======================
notif-category-season-prep = Подготовка за сезон

notif-label-new-season-reminder = Напомняне за нов сезон

notif-new-season-reminder = 🌟 <b>Започва нов сезон!</b>

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    Вашата текуща група: <b>{ $group }</b>

    💡 Ако сте преминали в друга група, моля актуализирайте я в /settings, за да получавате персонализирани връзки!

notif-new-season-reminder-no-group = 🌟 <b>Започва нов сезон!</b>

    🏁 <b>Състезание #{ $raceId }</b>
    📍 <b>{ $track }</b>
    🏎 <b>Състезание: { $raceTime }</b>

    ⚠️ Все още не сте задали група!

    💡 Задайте вашата група в /settings, за да получавате персонализирани връзки за състезания!

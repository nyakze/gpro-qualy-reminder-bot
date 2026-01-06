# GPRO Bot - Traduções em Português (Portugal)

# =======================
# Comandos e Geral
# =======================
start-welcome-new = 👋 <b>Bem-vindo ao GPRO Bot!</b>

    Vamos configurar. Primeiro, escolhe o teu idioma preferido para os links das corridas GPRO:

    🌍 <b>Seleciona o teu idioma</b> (ou salta para usar inglês):

start-welcome-existing = 🏁 GPRO Bot AO VIVO!
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferências

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    O que desejas fazer?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Estado e Calendário
# =======================
no-races-scheduled = 🔔 Sem corridas agendadas
no-upcoming-qualifications = 🔔 Sem qualificações futuras
next-season-not-published = 🌟 <b>Próxima temporada ainda não publicada</b>

calendar-title-full = 🏁 <b>Temporada Completa</b>
calendar-title-next = 🌟 <b>PRÓXIMA TEMPORADA</b> ({ $count } corridas)

# =======================
# Configuração Inicial
# =======================
onboard-group-title = 🏁 <b>Seleção de Grupo</b>

    Escolhe o teu grupo GPRO para obteres links personalizados:

    Seleciona um grupo comum ou introduz o teu próprio:

onboard-group-custom = 🏁 <b>Seleção de Grupo (Opcional)</b>

    Introduz o teu grupo num destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter 1-3 dígitos.

    💡 <i>O idioma do site GPRO foi definido para corresponder ao idioma do bot. Podes alterá-lo mais tarde em /settings</i>

onboard-complete = ✅ <b>Configuração Concluída!</b>

    🏁 <b>GPRO Bot está pronto!</b>

    <b>Comandos disponíveis:</b>
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferências

    💡 <i>Podes alterar estas configurações a qualquer momento usando /settings</i>

onboard-complete-with-group = ✅ <b>Configuração Concluída!</b>

    Grupo: <b>{ $group }</b>

    🏁 <b>GPRO Bot está pronto!</b>

    <b>Comandos disponíveis:</b>
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Preferências

# =======================
# Definições
# =======================
settings-title = ⚙️ <b>Definições</b>

    Configura as tuas preferências:

settings-language-title = 🌍 <b>Definições de Idioma</b>

    Atual: { $language }

    Seleciona o teu idioma preferido para os links das corridas GPRO:

ui-lang-menu-title = 💬 <b>Idioma do Bot</b>

    Seleciona o idioma da interface do bot:

settings-group-title = 🏁 <b>Definições de Grupo</b>

    Grupo atual: <b>{ $group }</b>

    Introduz o teu grupo num destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter 1-3 dígitos.

settings-group-set = ✅ <b>Grupo definido para: { $group }</b>

    As notificações de corrida e repetição incluirão links diretos para o teu grupo!

settings-notifications-title = 🔔 <b>Definições de Notificações</b>

    Clica para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ <i>Estes são interruptores globais para todas as corridas. Usa o botão 'Qualificação Feita' nas notificações para desativar uma corrida específica.</i>

settings-custom-notif-title = ⏱️ <b>Notificações Personalizadas</b>

    Define os teus próprios horários de notificação ({ $min }m - { $max }h antes do fecho da qualificação).

    Podes ter até 2 notificações personalizadas.

    Clica numa ranhura para definir ou editar.

settings-custom-notif-edit = ⏱️ <b>Notificação Personalizada { $slot }</b>{ $current }

    Seleciona um horário predefinido ou introduz um horário personalizado:

settings-custom-notif-current = Atual:

settings-custom-notif-input = ⏱️ <b>Notificação Personalizada { $slot }</b>

    Introduz o horário da tua notificação personalizada.

    <b>Formatos aceites:</b>
    • <code>20m</code> ou <code>45 minutos</code> (20m-70h)
    • <code>2h</code> ou <code>12 horas</code>
    • <code>1h 30m</code> ou <code>2h30m</code>

    <b>Exemplos:</b>
    • <code>20m</code> - 20 minutos antes
    • <code>6h</code> - 6 horas antes
    • <code>1h 30m</code> - 1 hora e 30 minutos antes

# =======================
# Botões
# =======================
button-ui-language = 💬 Idioma do Bot: { $language }
button-gpro-language = 🌍 Idioma GPRO: { $language }
button-language = 🌍 Idioma: { $language }
button-group = 🏁 Grupo: { $group }
button-notifications = 🔔 Notificações
button-custom-notifications = ⏱️ Notificações Personalizadas
button-back = ◀ Voltar
button-back-to-settings = ◀ Voltar às Definições
button-back-to-notifications = ◀ Voltar às Notificações
button-back-to-custom = ◀ Voltar às Notificações Personalizadas
button-back-custom-notif = ◀ Voltar às Notificações Personalizadas
button-main-menu = 🏠 Menu Principal
button-reset-group = 🔄 Redefinir Grupo
button-custom-slot-set = ⏱️ Personalizada { $slot }: { $time }
button-custom-slot-empty = ➕ Definir Notificação Personalizada { $slot }
button-previous = ◀ Anterior
button-next = Seguinte ▶
button-skip = ⏭️ Saltar
button-reset-language = 🔄 Redefinir para Padrão (Inglês)
button-enable-all = 🔔 Ativar Todas as Notificações
button-disable-all = 🔕 Desativar Todas as Notificações
button-enable-category = 🔔 Ativar Categoria
button-disable-category = 🔕 Desativar Categoria
button-quali-done = ✅ Qualificação Feita
button-reenable-race = 🔄 Reativar notificações Corrida { $raceId }
button-weather = 🌤️ Mostrar Meteorologia
button-enter-custom-group = ✏️ Introduzir Grupo Personalizado
button-enter-custom-time = ✏️ Introduzir Horário Personalizado
button-disable-notification = 🔕 Desativar Esta Notificação
button-cancel = ❌ Cancelar
button-got-it = ✅ Entendido!
button-try-again = 🔄 Tentar Novamente

button-main-menu-status = 📊 Próxima Corrida
button-main-menu-calendar = 📅 Temporada Completa
button-main-menu-next = 🌟 Próxima Temporada
button-main-menu-settings = ⚙️ Definições

button-group-elite = Elite
button-group-master3 = Master 3
button-group-pro15 = Pro 15
button-group-amateur42 = Amateur 42
button-group-rookie11 = Rookie 11

button-set-custom-notif = ➕ Definir Notificação Personalizada { $slot }
button-custom-notif-time = ⏱️ Personalizada { $slot }: { $time }

# =======================
# Notificações
# =======================
notif-category-before-qualifying = Antes da Qualificação
notif-category-qualifying-events = Eventos de Qualificação
notif-category-race-events = Eventos de Corrida

notif-label-72h = 3d antes do fecho da qualificação
notif-label-48h = 2d antes do fecho da qualificação
notif-label-24h = 1d antes do fecho da qualificação
notif-label-2h = 2h antes do fecho da qualificação
notif-label-10min = 10min antes do fecho da qualificação
notif-label-opens = Qualificação aberta
notif-label-quali-results = Resultados da qualificação disponíveis
notif-label-replay = Repetição da corrida disponível
notif-label-live = Corrida ao vivo
notif-label-results = Resultados da corrida disponíveis

notif-quali-closes = <b>Qualificação fecha em { $time }!</b>
notif-quali-opens = <b>Qualificação está aberta</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Corrida #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Prazo de qualificação: { $qualiDeadline }</b>
    🏎 <b>Corrida: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir para Qualificação</a>

    <i>Clica no botão '✅ Qualificação Feita' para desativar notificações desta corrida</i>

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Corrida #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Prazo de qualificação: { $qualiDeadline }</b>
    🏎 <b>Corrida: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir para Qualificação</a>

    ℹ️ <b>Notificações automáticas desativadas</b> para esta corrida
    <i>Clica no botão '🔄 Reativar' para reativar notificações</i>

notif-quali-closed-title = <b>Qualificação está fechada atualmente</b>

notif-quali-closed-message = { $emoji } { $title }

    🏁 <b>Corrida #{ $raceId }</b>
    📍 <b>{ $track }</b>
    ⏰ <b>Qualificação encerrada: { $qualiDeadline }</b>
    🏎 <b>Corrida: { $raceTime }</b>

    ⏳ <i>A qualificação está fechada atualmente. A próxima sessão de qualificação abrirá após a conclusão da corrida atual. Por favor aguarde que a corrida seja calculada.</i>

notif-race-live = 🏁 <b>Corrida #{ $raceId } está AO VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Ver Corrida Ao Vivo</a>

notif-race-live-no-group = 🏁 <b>Corrida #{ $raceId } está AO VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Define o teu grupo em /settings para um link direto!

    🔗 <a href="{ $raceLink }">Ver Corrida Ao Vivo</a>

notif-race-replay = 📺 <b>Repetição da Corrida #{ $raceId } Disponível</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Vê a repetição da corrida:

    🔗 <a href="{ $replayLink }">Ver Repetição</a>

notif-race-replay-no-group = 📺 <b>Repetição da Corrida #{ $raceId } Disponível</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Vê a repetição da corrida:

    ⚠️ Para links personalizados, define o teu grupo em /settings!

    🔗 <a href="{ $replayLink }">Ver Repetição</a>

notif-race-results = 📊 <b>Resultados da Corrida #{ $raceId } Disponíveis</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Os resultados da corrida estão agora disponíveis:

    🔗 <a href="{ $analysisLink }">Análise da Corrida</a>
    🔗 <a href="{ $summaryLink }">Resumo da Corrida</a>

notif-race-results-no-group = 📊 <b>Resultados da Corrida #{ $raceId } Disponíveis</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Os resultados da corrida estão agora disponíveis:

    🔗 <a href="{ $analysisLink }">Análise da Corrida</a>

    ⚠️ Para Resumo da Corrida personalizado, define o teu grupo em /settings!

# =======================
# Meteorologia
# =======================
weather-title = 🌤️ <b>Previsão Meteorológica da Corrida</b>
weather-practice-q1 = <b>Treinos / Qualificação 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Humidade: { $hum }%
weather-q2-start = <b>Qualificação 2 / Início da Corrida:</b> { $weather }
weather-race-conditions = <b>Condições da Corrida:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Humidade: { $hum }
    Probabilidade de chuva: { $rain }
weather-not-available = ⚠️ Dados meteorológicos não disponíveis
weather-cached = ℹ️ Meteorologia já em cache para <b>Corrida #{ $raceId }: { $track }</b>

    Usa <code>/weather force</code> para forçar atualização.
    Usa /status para ver a notificação com o botão de meteorologia.
weather-fetching = 🔄 A obter meteorologia para <b>Corrida #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 A forçar atualização da meteorologia para <b>Corrida #{ $raceId }: { $track }</b>...
weather-success = ✅ Dados meteorológicos obtidos para <b>Corrida #{ $raceId }: { $track }</b>

    Usa /status para testar a notificação com o botão de meteorologia!
weather-failed = ❌ Falha ao obter dados meteorológicos

    Verifica se o token da API GPRO é válido e se a API de Treinos está disponível.

# =======================
# Administração
# =======================
admin-only = ❌ Apenas administrador
admin-calendar-updated = ✅ <b>Calendário</b>: { $count } corridas
    🔄 <b>{ $userCount } utilizadores</b> redefinidos
admin-next-season-ready = 🌟 <b>Próxima temporada pronta!</b> { $count } corridas
    Usa /next para visualizar
admin-next-season-not-published = ℹ️ <b>Próxima temporada não publicada</b>
admin-users-count = 📊 <b>{ $count } utilizadores</b>:
admin-users-none = 📊 <b>0 utilizadores</b> na base de dados
admin-no-races = ❌ Sem corridas no calendário
admin-no-upcoming-races = ❌ Sem corridas futuras encontradas

# =======================
# Erros e Validação
# =======================
error-invalid-format = ❌ Formato inválido!

    Por favor usa:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Tenta novamente:

error-invalid-format-onboarding = ❌ Formato inválido!

    Por favor usa:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Tenta novamente ou usa /start para recomeçar:

error-invalid-time = ❌ <b>Erro:</b> { $error }

    Por favor tenta novamente com um formato válido como: <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Erro:</b> { $error }

    Por favor tenta novamente.

error-invalid-race = ❌ ID de corrida inválido
error-invalid-page = ❌ Página inválida
error-invalid-language = ❌ Idioma inválido
error-invalid-category = ❌ Categoria inválida
error-invalid-slot = ❌ Ranhura inválida
error-invalid-data = ❌ Dados inválidos
error-reset-failed = ❌ Redefinição falhou
error-race-not-found = ❌ Corrida não encontrada
error-weather-not-available = ⚠️ Dados meteorológicos ainda não disponíveis
error-weather-send-failed = ❌ Falha ao enviar meteorologia

# =======================
# Feedback e Confirmações
# =======================
feedback-all-enabled = ✅ Todas as notificações ativadas!
feedback-all-disabled = ✅ Todas as notificações desativadas!
feedback-category-enabled = ✅ { $category } ativada!
feedback-category-disabled = ✅ { $category } desativada!
feedback-notif-enabled = ✅ { $label } ativada!
feedback-notif-disabled = ✅ { $label } desativada!
feedback-quali-done = ✅ Feito!
feedback-race-marked-done = ✅ <i>Corrida marcada como feita!</i>
feedback-reset = 🔄 Redefinido!
feedback-notifications-reset = 🔄 <i>Notificações redefinidas!</i>
feedback-reenabled = 🔄 Reativado!
feedback-notifications-reenabled = 🔄 <i>Notificações reativadas!</i>
feedback-language-set = ✅ Idioma definido para { $language }
feedback-language-reset = ✅ Idioma redefinido para Inglês
feedback-ui-language-set = ✅ Idioma do bot definido para { $language }
feedback-group-set = ✅ Grupo definido para { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notificação personalizada { $slot } desativada
feedback-skip-language = ⏭️ A usar idioma padrão (Inglês)
feedback-skip-group = ⏭️ Seleção de grupo saltada
feedback-welcome = ✅ Bem-vindo a bordo!
feedback-weather-sent = 🌤️ Previsão meteorológica enviada!

# =======================
# Formatação de Tempo
# =======================
# Abreviaturas de dias da semana (2 letras)
weekday-mon = Seg
weekday-tue = Ter
weekday-wed = Qua
weekday-thu = Qui
weekday-fri = Sex
weekday-sat = Sáb
weekday-sun = Dom

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
    [one] { $days } dia
   *[other] { $days } dias
}
time-days-hours = { $days ->
    [one] { $days } dia
   *[other] { $days } dias
} { $hours ->
    [one] { $hours } hora
   *[other] { $hours } horas
}
time-months = { $months ->
    [one] { $months } mês
   *[other] { $months } meses
}
time-months-days = { $months ->
    [one] { $months } mês
   *[other] { $months } meses
} { $days ->
    [one] { $days } dia
   *[other] { $days } dias
}

# =======================
# Exibição de Grupo
# =======================
group-not-set = Não definido
group-elite = Elite
group-master = Master - { $number }
group-pro = Pro - { $number }
group-amateur = Amateur - { $number }
group-rookie = Rookie - { $number }

# =======================
# Mensagens de Notificações Personalizadas
# =======================
custom-notif-set = Notificação personalizada { $slot } definida para { $time }
custom-notif-set-success = Notificação personalizada { $slot } definida para { $time }
custom-notif-not-set = Não definida
custom-notif-min-error = Tempo mínimo é 20 minutos
custom-notif-max-error = Tempo máximo é 70 horas
custom-notif-invalid-slot = Ranhura inválida (deve ser 0-{ $max })
custom-notif-empty-error = Tempo não pode estar vazio
custom-notif-invalid-format = Formato inválido. Usa: 2h, 30m, ou 1h 30m
custom-notif-enter-time = Por favor introduz um horário
custom-notif-error-parsing = ❌ <b>Erro:</b> { $error }

    Por favor tenta novamente com um formato válido como: <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    A tua notificação personalizada foi definida!
custom-notif-error-setting = ❌ <b>Erro:</b> { $error }

    Por favor tenta novamente.

# =======================
# Validação
# =======================
validation-time-empty = Tempo não pode estar vazio
validation-time-min = Tempo mínimo é 20 minutos
validation-time-max = Tempo máximo é 70 horas
validation-enter-time = Por favor introduz um horário
validation-invalid-format = Formato inválido. Usa: 2h, 30m, ou 1h 30m
validation-invalid-slot = Ranhura inválida (deve ser 0-{ $maxSlots })

# =======================
# Etiquetas de Notificações
# =======================
notif-label-72h = 3d antes do fecho da qualificação
notif-label-48h = 2d antes do fecho da qualificação
notif-label-24h = 1d antes do fecho da qualificação
notif-label-2h = 2h antes do fecho da qualificação
notif-label-10min = 10min antes do fecho da qualificação
notif-label-opens-soon = Qualificação aberta
notif-label-quali-results = Resultados da qualificação disponíveis
notif-label-race-replay = Repetição da corrida disponível
notif-label-race-live = Corrida ao vivo
notif-label-race-results = Resultados da corrida disponíveis

# =======================
# Menu de Notificações
# =======================
notif-menu-title = 🔔 <b>Definições de Notificações</b>

    Clica para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ <i>Estes são interruptores globais para todas as corridas. Usa o botão 'Qualificação Feita' nas notificações para desativar uma corrida específica.</i>

# =======================
# Menu de Grupo
# =======================
group-menu-title = 🏁 <b>Definições de Grupo</b>

    Grupo atual: <b>{ $groupDisplay }</b>

    Introduz o teu grupo num destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter 1-3 dígitos.
group-reset-success = ✅ Grupo redefinido com sucesso

# =======================
# Menu de Idioma
# =======================
lang-menu-title = 🌍 <b>Definições de Idioma</b>

    Atual: { $currentLang }

    Seleciona o teu idioma preferido para os links das corridas GPRO:

# =======================
# Menu de Notificações Personalizadas
# =======================
custom-notif-menu-title = ⏱️ <b>Notificações Personalizadas</b>

    Define os teus próprios horários de notificação ({ $minTime }m - { $maxTime }h antes do fecho da qualificação).

    Podes ter até 2 notificações personalizadas.

    Clica numa ranhura para definir ou editar.

# =======================
# Meteorologia
# =======================
weather-unavailable = ⚠️ Dados meteorológicos não disponíveis
weather-title = 🌤️ <b>Previsão Meteorológica da Corrida</b>
weather-race-header = Corrida #{ $raceId }: { $track }
weather-practice-q1 = <b>Treinos / Qualificação 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Humidade: { $hum }%
weather-q2-race-start = <b>Qualificação 2 / Início da Corrida:</b> { $weather }
weather-race-conditions = <b>Condições da Corrida:</b>
weather-start-0h30m = <b>Início - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Temp: { $temp } • Humidade: { $hum }
weather-rain-prob = Probabilidade de chuva: { $rain }

# Condições Meteorológicas
weather-condition-sunny = Ensolarado
weather-condition-partially-cloudy = Parcialmente Nublado
weather-condition-cloudy = Nublado
weather-condition-very-cloudy = Muito Nublado
weather-condition-rain = Chuva

# =======================
# Definições de Fuso Horário
# =======================
button-timezone = ⏰ Fuso Horário: { $timezone }
button-website-mode = 🌐 Tipo de ligação: { $mode }
website-mode-classic = Clássico
timezone-menu-title = ⏰ <b>Definições de Fuso Horário</b>

    Fuso horário atual: <b>{ $timezone }</b>

    Escreve o teu fuso horário (nome da cidade, abreviatura ou desvio UTC):

    Exemplos: <code>Lisboa</code>, <code>WET</code>, <code>UTC+0</code>, <code>Londres</code>

timezone-select-matches = 🌍 <b>Seleciona o teu fuso horário:</b>

    Resultados para "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Seleciona o teu fuso horário:</b>

    Resultados para "{ $query }" (Página { $page }/{ $total }):

timezone-set-success = ✅ <b>Fuso horário definido!</b>

    { $timezone }

    Hora atual no teu fuso horário: <b>{ $localTime }</b>

    Todos os horários das corridas serão agora mostrados na tua hora local.

button-reset-timezone = 🔄 Redefinir para UTC
feedback-timezone-set = ✅ Fuso horário atualizado
feedback-timezone-reset = ✅ Fuso horário redefinido para UTC
feedback-switched-to-app = Modo APP ativado
feedback-switched-to-classic = Modo Clássico ativado
error-mode-switch-failed = ❌ Falha ao alterar o modo do site
error-timezone-not-found = ❌ Nenhum fuso horário encontrado para "{ $query }"

    Tenta: nome da cidade (Lisboa), abreviatura (WET), ou desvio UTC (UTC+0)
error-invalid-timezone = ❌ Fuso horário inválido



notif-quali-results = 🏁 <b>Resultados da Qualificação - Corrida #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualificação encerrada</b>
    🏎 <b>Corrida: { $raceTime }</b>

    Resultados da qualificação disponíveis:

    🔗 <a href="{ $gridLink }">Grelha de Partida</a>

notif-quali-results-no-group = 🏁 <b>Resultados da Qualificação - Corrida #{ $raceId }</b>

    📍 <b>{ $track }</b>
    ✅ <b>Qualificação encerrada</b>
    🏎 <b>Corrida: { $raceTime }</b>

    Resultados da qualificação disponíveis:

    ⚠️ Para ligações personalizadas, configure o seu grupo em /settings!

    🔗 <a href="{ $gridLink }">Grelha de Partida</a>

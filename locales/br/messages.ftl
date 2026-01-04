# GPRO Bot - Traduções em Português (Brasil)

# =======================
# Comandos & Geral
# =======================
start-welcome-new = 👋 **Bem-vindo ao GPRO Bot!**

    Vamos configurar tudo. Primeiro, escolha seu idioma preferido para os links de corrida do GPRO:

    🌍 **Selecione seu idioma** (ou pule para usar inglês):

start-welcome-existing = 🏁 GPRO Bot ATIVO!
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

start-welcome-existing-buttons = 🏁 **GPRO Bot**

    O que você gostaria de fazer?

bot-live = 🏁 **GPRO Bot**

# =======================
# Status & Calendário
# =======================
no-races-scheduled = 🔔 Nenhuma corrida agendada
no-upcoming-qualifications = 🔔 Nenhuma classificação programada
next-season-not-published = 🌟 **A próxima temporada ainda não foi publicada**

calendar-title-full = 🏁 **Temporada Completa**
calendar-title-next = 🌟 **PRÓXIMA TEMPORADA** ({ $count } corridas)

# =======================
# Integração (Onboarding)
# =======================
onboard-group-title = 🏁 **Seleção de Grupo**

    Escolha seu grupo GPRO para receber links personalizados de corrida:

    Selecione um grupo comum ou informe o seu:

onboard-group-custom = 🏁 **Grupo Personalizado**

    Informe seu grupo em um destes formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.

onboard-complete = ✅ **Configuração Concluída!**

    🏁 **GPRO Bot está pronto!**

    **Comandos disponíveis:**
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

    💡 *Você pode alterar essas configurações a qualquer momento usando /settings*

onboard-complete-with-group = ✅ **Configuração Concluída!**

    Grupo: **{ $group }**

    🏁 **GPRO Bot está pronto!**

    **Comandos disponíveis:**
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

# =======================
# Configurações
# =======================
settings-title = ⚙️ **Configurações**

    Configure suas preferências:

settings-language-title = 🌍 **Configurações de Idioma**

    Atual: { $language }

    Selecione seu idioma preferido para os links de corrida GPRO:

ui-lang-menu-title = 💬 **Idioma do Bot**

    Selecione o idioma da interface do bot:

settings-group-title = 🏁 **Configurações de Grupo**

    Grupo atual: **{ $group }**

    Informe seu grupo em um destes formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.

settings-group-set = ✅ **Grupo definido para: { $group }**

    As notificações de corrida e replay incluirão links diretos para seu grupo!

settings-notifications-title = 🔔 **Configurações de Notificações**

    Clique para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ *Estas são chaves globais para todas as corridas. Use o botão 'Classificação Concluída' nas notificações para desativar uma corrida específica.*

settings-custom-notif-title = ⏱️ **Notificações Personalizadas**

    Defina seus próprios horários de notificação ({ $min }m - { $max }h antes do fechamento da classificação).

    Você pode ter até 2 notificações personalizadas.

    Clique em um slot para configurar ou editar.

settings-custom-notif-edit = ⏱️ **Notificação Personalizada { $slot }**{ $current }

    Selecione um horário predefinido ou informe um horário personalizado:

settings-custom-notif-input = ⏱️ **Notificação Personalizada { $slot }**

    Informe seu horário de notificação personalizado.

    **Formatos aceitos:**
    • `20m` ou `45 minutos` (20m-70h)
    • `2h` ou `12 horas`
    • `1h 30m` ou `2h30m`

    **Exemplos:**
    • `20m` - 20 minutos antes
    • `6h` - 6 horas antes
    • `1h 30m` - 1 hora e 30 minutos antes

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
button-back-to-settings = ◀ Voltar para Configurações
button-back-to-notifications = ◀ Voltar para Notificações
button-back-to-custom = ◀ Voltar para Notificações Personalizadas
button-back-custom-notif = ◀ Voltar para Notificações Personalizadas
button-main-menu = 🏠 Menu Principal
button-reset-group = 🔄 Redefinir Grupo
button-custom-slot-set = ⏱️ Personalizada { $slot }: { $time }
button-custom-slot-empty = ➕ Definir Notificação Personalizada { $slot }
button-previous = ◀ Anterior
button-next = Próximo ▶
button-skip = ⏭️ Pular
button-reset-language = 🔄 Redefinir para Padrão (Inglês)
button-enable-all = 🔔 Ativar Todas as Notificações
button-disable-all = 🔕 Desativar Todas as Notificações
button-quali-done = ✅ Classificação Concluída
button-reenable-race = 🔄 Reativar notificações da Corrida { $raceId }
button-weather = 🌤️ Mostrar Clima
button-enter-custom-group = ✏️ Informar Grupo Personalizado
button-enter-custom-time = ✏️ Informar Horário Personalizado
button-disable-notification = 🔕 Desativar Esta Notificação
button-cancel = ❌ Cancelar
button-got-it = ✅ Entendi!
button-try-again = 🔄 Tentar Novamente

button-main-menu-status = 📊 Próxima Corrida
button-main-menu-calendar = 📅 Temporada Completa
button-main-menu-next = 🌟 Próxima Temporada
button-main-menu-settings = ⚙️ Configurações

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
notif-label-72h = 3d antes do fechamento da classificação
notif-label-48h = 2d antes do fechamento da classificação
notif-label-24h = 1d antes do fechamento da classificação
notif-label-2h = 2h antes do fechamento da classificação
notif-label-10min = 10min antes do fechamento da classificação
notif-label-opens = Classificação está aberta
notif-label-replay = Replay da corrida disponível
notif-label-live = Corrida está ao vivo
notif-label-results = Resultados da corrida disponíveis

notif-label-opens-soon = Classificação está aberta
notif-label-race-replay = Replay da corrida disponível
notif-label-race-live = Corrida está ao vivo
notif-label-race-results = Resultados da corrida disponíveis

notif-quali-closes = **Classificação fecha em { $time }!**
notif-quali-opens = **Classificação está aberta (ou abrirá em breve)**

notif-quali-message = { $emoji } { $title }

    🏁 **Corrida #{ $raceId }**
    📍 **{ $track }**
    📅 **Classificação: { $qualiDeadline } | Corrida: { $raceTime }**

    🔗 [Ir para Classificação]({ $qualiLink })

    Clique no botão para desativar notificações desta corrida

notif-quali-message-disabled = { $emoji } { $title }

    🏁 **Corrida #{ $raceId }**
    📍 **{ $track }**
    📅 **Classificação: { $qualiDeadline } | Corrida: { $raceTime }**

    🔗 [Ir para Classificação]({ $qualiLink })

    ℹ️ **Notificações automáticas desativadas** para esta corrida
    Clique no botão para reativar notificações

notif-race-live = 🏁 **Corrida #{ $raceId } está AO VIVO!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    🔗 [Assistir Corrida ao Vivo]({ $raceLink })

notif-race-live-no-group = 🏁 **Corrida #{ $raceId } está AO VIVO!**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    ⚠️ Defina seu grupo em /settings para um link direto!

    🔗 [Assistir Corrida ao Vivo]({ $raceLink })

notif-race-replay = 📺 **Replay da Corrida #{ $raceId } Disponível**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Se a corrida já foi calculada, o replay está disponível aqui:

    🔗 [Assistir Replay]({ $replayLink })

notif-race-replay-no-group = 📺 **Replay da Corrida #{ $raceId } Disponível**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Se a corrida já foi calculada, o replay está disponível aqui:

    ⚠️ Para links personalizados, defina seu grupo em /settings!

    🔗 [Assistir Replay]({ $replayLink })

notif-race-results = 📊 **Resultados da Corrida #{ $raceId } Disponíveis**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Os resultados da corrida agora estão disponíveis:

    🔗 [Análise da Corrida]({ $analysisLink })
    🔗 [Resumo da Corrida]({ $summaryLink })

notif-race-results-no-group = 📊 **Resultados da Corrida #{ $raceId } Disponíveis**

    📍 **{ $track }**
    🕐 **{ $raceTime }**

    Os resultados da corrida agora estão disponíveis:

    🔗 [Análise da Corrida]({ $analysisLink })

    ⚠️ Para Resumo da Corrida personalizado, defina seu grupo em /settings!

# =======================
# Clima
# =======================
weather-title = 🌤️ **Previsão do Clima da Corrida**
weather-practice-q1 = **Treino / Classificação 1:** { $weather }
weather-temp-hum = Temp: { $temp }°C • Umidade: { $hum }%
weather-q2-start = **Classificação 2 / Largada da Corrida:** { $weather }
weather-q2-race-start = **Classificação 2 / Largada da Corrida:** { $weather }
weather-race-conditions = **Condições da Corrida:**
weather-quarter = **{ $label }:**
weather-race-quarter = Temp: { $temp } • Umidade: { $hum }
    Probabilidade de chuva: { $rain }
weather-not-available = ⚠️ Dados do clima não disponíveis
weather-unavailable = ⚠️ Dados do clima não disponíveis
weather-cached = ℹ️ Clima já em cache para **Corrida #{ $raceId }: { $track }**

    Use `/weather force` para forçar atualização.
    Use /status para ver a notificação com botão do clima.
weather-fetching = 🔄 Buscando clima para **Corrida #{ $raceId }: { $track }**...
weather-force-updating = 🔄 Forçando atualização do clima para **Corrida #{ $raceId }: { $track }**...
weather-success = ✅ Dados do clima obtidos para **Corrida #{ $raceId }: { $track }**

    Use /status para testar a notificação com botão do clima!
weather-failed = ❌ Falha ao obter dados do clima

    Verifique se o token da API GPRO é válido e se a API de Treino está disponível.

weather-start-0h30m = **Largada - 0h30m:**
weather-0h30m-1h00m = **0h30m - 1h00m:**
weather-1h00m-1h30m = **1h00m - 1h30m:**
weather-1h30m-2h00m = **1h30m - 2h00m:**
weather-temp-hum-range = Temp: { $temp } • Umidade: { $hum }
weather-rain-prob = Probabilidade de chuva: { $rain }

# =======================
# Admin
# =======================
admin-only = ❌ Somente admin
admin-calendar-updated = ✅ **Calendário**: { $count } corridas
    🔄 **{ $userCount } usuários** redefinidos
admin-next-season-ready = 🌟 **Próxima temporada pronta!** { $count } corridas
    Use /next para visualizar
admin-next-season-not-published = ℹ️ **Próxima temporada não publicada**
admin-users-count = 📊 **{ $count } usuários**:
admin-users-none = 📊 **0 usuários** no banco de dados
admin-no-races = ❌ Nenhuma corrida no calendário
admin-no-upcoming-races = ❌ Nenhuma corrida futura encontrada

# =======================
# Erros & Validação
# =======================
error-invalid-format = ❌ Formato inválido!

    Por favor use:
    • **E** para Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Tente novamente:

error-invalid-format-onboarding = ❌ Formato inválido!

    Por favor use:
    • **E** para Elite
    • **M3** (Master 3)
    • **P15**, **A42**, **R11** etc.

    Tente novamente ou use /start para reiniciar:

error-invalid-time = ❌ **Erro:** { $error }

    Por favor tente novamente com um formato válido como: `2h`, `30m`, ou `1h 30m`

error-custom-notif-failed = ❌ **Erro:** { $error }

    Por favor tente novamente.

error-invalid-race = ❌ ID de corrida inválido
error-invalid-page = ❌ Página inválida
error-invalid-language = ❌ Idioma inválido
error-invalid-slot = ❌ Slot inválido
error-invalid-data = ❌ Dados inválidos
error-reset-failed = ❌ Falha ao redefinir
error-race-not-found = ❌ Corrida não encontrada
error-weather-not-available = ⚠️ Dados do clima ainda não disponíveis
error-weather-send-failed = ❌ Falha ao enviar clima

# =======================
# Feedback & Confirmações
# =======================
feedback-all-enabled = ✅ Todas as notificações ativadas!
feedback-all-disabled = ✅ Todas as notificações desativadas!
feedback-notif-enabled = ✅ { $label } ativada!
feedback-notif-disabled = ✅ { $label } desativada!
feedback-quali-done = ✅ Concluído!
feedback-race-marked-done = ✅ *Corrida marcada como concluída!*
feedback-reset = 🔄 Redefinido!
feedback-notifications-reset = 🔄 *Notificações redefinidas!*
feedback-reenabled = 🔄 Reativado!
feedback-notifications-reenabled = 🔄 *Notificações reativadas!*
feedback-language-set = ✅ Idioma definido para { $language }
feedback-language-reset = ✅ Idioma redefinido para inglês
feedback-ui-language-set = ✅ Idioma do bot definido para { $language }
feedback-group-set = ✅ Grupo definido para { $group }
feedback-custom-notif-set = ✅ { $message }
feedback-custom-notif-disabled = ✅ Notificação personalizada { $slot } desativada
feedback-skip-language = ⏭️ Usando idioma padrão (inglês)
feedback-skip-group = ⏭️ Seleção de grupo pulada
feedback-welcome = ✅ Bem-vindo!
feedback-weather-sent = 🌤️ Previsão do clima enviada!

# =======================
# Formatação de Tempo
# =======================
# Abreviações dos dias da semana (2 letras)
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
# Mensagens de Notificação Personalizada
# =======================
custom-notif-set = Notificação personalizada { $slot } definida para { $time }
custom-notif-set-success = Notificação personalizada { $slot } definida para { $time }
custom-notif-not-set = Não definida
custom-notif-min-error = O tempo mínimo é de 20 minutos
custom-notif-max-error = O tempo máximo é de 70 horas
custom-notif-invalid-slot = Slot inválido (deve ser 0-{ $max })
custom-notif-empty-error = O tempo não pode ficar vazio
custom-notif-invalid-format = Formato inválido. Use: 2h, 30m, ou 1h 30m
custom-notif-enter-time = Por favor informe um tempo
custom-notif-error-parsing = ❌ **Erro:** { $error }

    Por favor tente novamente com um formato válido como: `2h`, `30m`, ou `1h 30m`
custom-notif-success = ✅ **{ $message }**

    Sua notificação personalizada foi definida!
custom-notif-error-setting = ❌ **Erro:** { $error }

    Por favor tente novamente.

# =======================
# Validação
# =======================
validation-time-empty = O tempo não pode ficar vazio
validation-time-min = O tempo mínimo é de 20 minutos
validation-time-max = O tempo máximo é de 70 horas
validation-enter-time = Por favor informe um tempo
validation-invalid-format = Formato inválido. Use: 2h, 30m, ou 1h 30m
validation-invalid-slot = Slot inválido (deve ser 0-{ $maxSlots })

# =======================
# Menu de Notificações
# =======================
notif-menu-title = 🔔 **Configurações de Notificações**

    Clique para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ *Estas são chaves globais para todas as corridas. Use o botão 'Classificação Concluída' nas notificações para desativar uma corrida específica.*

# =======================
# Menu de Grupo
# =======================
group-menu-title = 🏁 **Configurações de Grupo**

    Grupo atual: **{ $groupDisplay }**

    Informe seu grupo em um destes formatos:
    • **E** (Elite)
    • **M3** (Master 3)
    • **P15** (Pro 15)
    • **A42** (Amateur 42)
    • **R11** (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.
group-reset-success = ✅ Grupo redefinido com sucesso

# =======================
# Menu de Idioma
# =======================
lang-menu-title = 🌍 **Configurações de Idioma**

    Atual: { $currentLang }

    Selecione seu idioma preferido para os links de corrida GPRO:

# =======================
# Menu de Notificações Personalizadas
# =======================
custom-notif-menu-title = ⏱️ **Notificações Personalizadas**

    Defina seus próprios horários de notificação ({ $minTime }m - { $maxTime }h antes do fechamento da classificação).

    Você pode ter até 2 notificações personalizadas.

    Clique em um slot para configurar ou editar.

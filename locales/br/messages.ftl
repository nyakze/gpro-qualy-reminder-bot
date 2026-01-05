# GPRO Bot - Traduções em Português (Brasil)

# =======================
# Comandos & Geral
# =======================
start-welcome-new = 👋 <b>Bem-vindo ao GPRO Bot!</b>

    Vamos configurar tudo. Primeiro, escolha seu idioma preferido para os links de corrida do GPRO:

    🌍 <b>Selecione seu idioma</b> (ou pule para usar inglês):

start-welcome-existing = 🏁 GPRO Bot ATIVO!
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

start-welcome-existing-buttons = 🏁 <b>GPRO Bot</b>

    O que você gostaria de fazer?

bot-live = 🏁 <b>GPRO Bot</b>

# =======================
# Status & Calendário
# =======================
no-races-scheduled = 🔔 Nenhuma corrida agendada
no-upcoming-qualifications = 🔔 Nenhuma classificação programada
next-season-not-published = 🌟 <b>A próxima temporada ainda não foi publicada</b>

calendar-title-full = 🏁 <b>Temporada Completa</b>
calendar-title-next = 🌟 <b>PRÓXIMA TEMPORADA</b> ({ $count } corridas)

# =======================
# Integração (Onboarding)
# =======================
onboard-group-title = 🏁 <b>Seleção de Grupo</b>

    Escolha seu grupo GPRO para receber links personalizados de corrida:

    Selecione um grupo comum ou informe o seu:

onboard-group-custom = 🏁 <b>Seleção de Grupo (Opcional)</b>

    Informe seu grupo em um destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.

    💡 <i>O idioma do site GPRO foi definido para corresponder ao idioma do bot. Você pode alterá-lo mais tarde em /settings</i>

onboard-complete = ✅ <b>Configuração Concluída!</b>

    🏁 <b>GPRO Bot está pronto!</b>

    <b>Comandos disponíveis:</b>
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

    💡 <i>Você pode alterar essas configurações a qualquer momento usando /settings</i>

onboard-complete-with-group = ✅ <b>Configuração Concluída!</b>

    Grupo: <b>{ $group }</b>

    🏁 <b>GPRO Bot está pronto!</b>

    <b>Comandos disponíveis:</b>
    /status - Próxima corrida
    /calendar - Temporada completa
    /next - Próxima temporada
    /settings - Configurações

# =======================
# Configurações
# =======================
settings-title = ⚙️ <b>Configurações</b>

    Configure suas preferências:

settings-language-title = 🌍 <b>Configurações de Idioma</b>

    Atual: { $language }

    Selecione seu idioma preferido para os links de corrida GPRO:

ui-lang-menu-title = 💬 <b>Idioma do Bot</b>

    Selecione o idioma da interface do bot:

settings-group-title = 🏁 <b>Configurações de Grupo</b>

    Grupo atual: <b>{ $group }</b>

    Informe seu grupo em um destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.

settings-group-set = ✅ <b>Grupo definido para: { $group }</b>

    As notificações de corrida e replay incluirão links diretos para seu grupo!

settings-notifications-title = 🔔 <b>Configurações de Notificações</b>

    Clique para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ <i>Estas são chaves globais para todas as corridas. Use o botão 'Classificação Concluída' nas notificações para desativar uma corrida específica.</i>

settings-custom-notif-title = ⏱️ <b>Notificações Personalizadas</b>

    Defina seus próprios horários de notificação ({ $min }m - { $max }h antes do fechamento da classificação).

    Você pode ter até 2 notificações personalizadas.

    Clique em um slot para configurar ou editar.

settings-custom-notif-edit = ⏱️ <b>Notificação Personalizada { $slot }</b>{ $current }
settings-custom-notif-current = Current:

    Selecione um horário predefinido ou informe um horário personalizado:

settings-custom-notif-input = ⏱️ <b>Notificação Personalizada { $slot }</b>

    Informe seu horário de notificação personalizado.

    <b>Formatos aceitos:</b>
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

notif-quali-closes = <b>Classificação fecha em { $time }!</b>
notif-quali-opens = <b>Classificação está aberta (ou abrirá em breve)</b>

notif-quali-message = { $emoji } { $title }

    🏁 <b>Corrida #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Classificação fecha: { $qualiDeadline }</b>
    🏎 <b>Corrida: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir para Classificação</a>

    Clique no botão para desativar notificações desta corrida

notif-quali-message-disabled = { $emoji } { $title }

    🏁 <b>Corrida #{ $raceId }</b>
    📍 <b>{ $track }</b>
    📅 <b>Classificação fecha: { $qualiDeadline }</b>
    🏎 <b>Corrida: { $raceTime }</b>

    🔗 <a href="{ $qualiLink }">Ir para Classificação</a>

    ℹ️ <b>Notificações automáticas desativadas</b> para esta corrida
    Clique no botão para reativar notificações

notif-race-live = 🏁 <b>Corrida #{ $raceId } está AO VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    🔗 <a href="{ $raceLink }">Assistir Corrida ao Vivo</a>

notif-race-live-no-group = 🏁 <b>Corrida #{ $raceId } está AO VIVO!</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    ⚠️ Defina seu grupo em /settings para um link direto!

    🔗 <a href="{ $raceLink }">Assistir Corrida ao Vivo</a>

notif-race-replay = 📺 <b>Replay da Corrida #{ $raceId } Disponível</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Se a corrida já foi calculada, o replay está disponível aqui:

    🔗 <a href="{ $replayLink }">Assistir Replay</a>

notif-race-replay-no-group = 📺 <b>Replay da Corrida #{ $raceId } Disponível</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Se a corrida já foi calculada, o replay está disponível aqui:

    ⚠️ Para links personalizados, defina seu grupo em /settings!

    🔗 <a href="{ $replayLink }">Assistir Replay</a>

notif-race-results = 📊 <b>Resultados da Corrida #{ $raceId } Disponíveis</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Os resultados da corrida agora estão disponíveis:

    🔗 <a href="{ $analysisLink }">Análise da Corrida</a>
    🔗 <a href="{ $summaryLink }">Resumo da Corrida</a>

notif-race-results-no-group = 📊 <b>Resultados da Corrida #{ $raceId } Disponíveis</b>

    📍 <b>{ $track }</b>
    🕐 <b>{ $raceTime }</b>

    Os resultados da corrida agora estão disponíveis:

    🔗 <a href="{ $analysisLink }">Análise da Corrida</a>

    ⚠️ Para Resumo da Corrida personalizado, defina seu grupo em /settings!

# =======================
# Clima
# =======================
weather-title = 🌤️ <b>Previsão do Clima da Corrida</b>
weather-race-header = Race #{ $raceId }: { $track }
weather-practice-q1 = <b>Treino / Classificação 1:</b> { $weather }
weather-temp-hum = Temp: { $temp }°C • Umidade: { $hum }%
weather-q2-start = <b>Classificação 2 / Largada da Corrida:</b> { $weather }
weather-q2-race-start = <b>Classificação 2 / Largada da Corrida:</b> { $weather }
weather-race-conditions = <b>Condições da Corrida:</b>
weather-quarter = <b>{ $label }:</b>
weather-race-quarter = Temp: { $temp } • Umidade: { $hum }
    Probabilidade de chuva: { $rain }
weather-not-available = ⚠️ Dados do clima não disponíveis
weather-unavailable = ⚠️ Dados do clima não disponíveis
weather-cached = ℹ️ Clima já em cache para <b>Corrida #{ $raceId }: { $track }</b>

    Use <code>/weather force</code> para forçar atualização.
    Use /status para ver a notificação com botão do clima.
weather-fetching = 🔄 Buscando clima para <b>Corrida #{ $raceId }: { $track }</b>...
weather-force-updating = 🔄 Forçando atualização do clima para <b>Corrida #{ $raceId }: { $track }</b>...
weather-success = ✅ Dados do clima obtidos para <b>Corrida #{ $raceId }: { $track }</b>

    Use /status para testar a notificação com botão do clima!
weather-failed = ❌ Falha ao obter dados do clima

    Verifique se o token da API GPRO é válido e se a API de Treino está disponível.

weather-start-0h30m = <b>Largada - 0h30m:</b>
weather-0h30m-1h00m = <b>0h30m - 1h00m:</b>
weather-1h00m-1h30m = <b>1h00m - 1h30m:</b>
weather-1h30m-2h00m = <b>1h30m - 2h00m:</b>
weather-temp-hum-range = Temp: { $temp } • Umidade: { $hum }
weather-rain-prob = Probabilidade de chuva: { $rain }

# Condições Meteorológicas
weather-condition-sunny = Ensolarado
weather-condition-partially-cloudy = Parcialmente Nublado
weather-condition-cloudy = Nublado
weather-condition-very-cloudy = Encoberto
weather-condition-rain = Chuva

# =======================
# Admin
# =======================
admin-only = ❌ Somente admin
admin-calendar-updated = ✅ <b>Calendário</b>: { $count } corridas
    🔄 <b>{ $userCount } usuários</b> redefinidos
admin-next-season-ready = 🌟 <b>Próxima temporada pronta!</b> { $count } corridas
    Use /next para visualizar
admin-next-season-not-published = ℹ️ <b>Próxima temporada não publicada</b>
admin-users-count = 📊 <b>{ $count } usuários</b>:
admin-users-none = 📊 <b>0 usuários</b> no banco de dados
admin-no-races = ❌ Nenhuma corrida no calendário
admin-no-upcoming-races = ❌ Nenhuma corrida futura encontrada

# =======================
# Erros & Validação
# =======================
error-invalid-format = ❌ Formato inválido!

    Por favor use:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Tente novamente:

error-invalid-format-onboarding = ❌ Formato inválido!

    Por favor use:
    • <b>E</b> para Elite
    • <b>M3</b> (Master 3)
    • <b>P15</b>, <b>A42</b>, <b>R11</b> etc.

    Tente novamente ou use /start para reiniciar:

error-invalid-time = ❌ <b>Erro:</b> { $error }

    Por favor tente novamente com um formato válido como: <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>

error-custom-notif-failed = ❌ <b>Erro:</b> { $error }

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
feedback-race-marked-done = ✅ <i>Corrida marcada como concluída!</i>
feedback-reset = 🔄 Redefinido!
feedback-notifications-reset = 🔄 <i>Notificações redefinidas!</i>
feedback-reenabled = 🔄 Reativado!
feedback-notifications-reenabled = 🔄 <i>Notificações reativadas!</i>
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
custom-notif-error-parsing = ❌ <b>Erro:</b> { $error }

    Por favor tente novamente com um formato válido como: <code>2h</code>, <code>30m</code>, ou <code>1h 30m</code>
custom-notif-success = ✅ <b>{ $message }</b>

    Sua notificação personalizada foi definida!
custom-notif-error-setting = ❌ <b>Erro:</b> { $error }

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
notif-menu-title = 🔔 <b>Configurações de Notificações</b>

    Clique para ativar/desativar notificações:
    ✅ = Ativado | ❌ = Desativado

    ℹ️ <i>Estas são chaves globais para todas as corridas. Use o botão 'Classificação Concluída' nas notificações para desativar uma corrida específica.</i>

# =======================
# Menu de Grupo
# =======================
group-menu-title = 🏁 <b>Configurações de Grupo</b>

    Grupo atual: <b>{ $groupDisplay }</b>

    Informe seu grupo em um destes formatos:
    • <b>E</b> (Elite)
    • <b>M3</b> (Master 3)
    • <b>P15</b> (Pro 15)
    • <b>A42</b> (Amateur 42)
    • <b>R11</b> (Rookie 11)

    Os números podem ter de 1 a 3 dígitos.
group-reset-success = ✅ Grupo redefinido com sucesso

# =======================
# Menu de Idioma
# =======================
lang-menu-title = 🌍 <b>Configurações de Idioma</b>

    Atual: { $currentLang }

    Selecione seu idioma preferido para os links de corrida GPRO:

# =======================
# Menu de Notificações Personalizadas
# =======================
custom-notif-menu-title = ⏱️ <b>Notificações Personalizadas</b>

    Defina seus próprios horários de notificação ({ $minTime }m - { $maxTime }h antes do fechamento da classificação).

    Você pode ter até 2 notificações personalizadas.

    Clique em um slot para configurar ou editar.

# =======================
# Configurações de Fuso Horário
# =======================
button-timezone = ⏰ Fuso horário: { $timezone }
timezone-menu-title = ⏰ <b>Configurações de Fuso Horário</b>

    Fuso horário atual: <b>{ $timezone }</b>

    Digite seu fuso horário (nome da cidade em inglês, abreviação ou deslocamento UTC):

    Exemplos: <code>Sao Paulo</code>, <code>New York</code>, <code>UTC-3</code>, <code>London</code>

timezone-select-matches = 🌍 <b>Selecione seu fuso horário:</b>

    Correspondências para "{ $query }":

timezone-select-matches-paginated = 🌍 <b>Selecione seu fuso horário:</b>

    Correspondências para "{ $query }" (Página { $page }/{ $total }):

timezone-set-success = ✅ <b>Fuso horário definido!</b>

    { $timezone }

    Horário atual no seu fuso horário: <b>{ $localTime }</b>

    Todos os horários das corridas serão exibidos no seu horário local.

button-reset-timezone = 🔄 Redefinir para UTC
feedback-timezone-set = ✅ Fuso horário atualizado
feedback-timezone-reset = ✅ Fuso horário redefinido para UTC
error-timezone-not-found = ❌ Nenhum fuso horário encontrado para "{ $query }"

    Tente: nome da cidade em inglês (Sao Paulo), abreviação (BRT), ou deslocamento UTC (UTC-3)
error-invalid-timezone = ❌ Fuso horário inválido

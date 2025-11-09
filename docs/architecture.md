# Architecture Overview

This document summarises the IST-detector bot architecture using the C4 model. It highlights the actors that interact with the system, the deployed containers, and the key software components.

## Level 1 – System Context

The bot acts as a gateway between end-users, the Robokassa payment platform and the operations team receiving service requests.

```plantuml
@startuml Context
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "Клиент Telegram", "Запускает диалог и оформляет заявку")
System_Boundary(bot, "IST-detector Bot") {
  System(telegram_bot, "Telegram Bot", "aiogram", "Обрабатывает диалог и генерирует платежные ссылки")
}
System_Ext(robokassa, "Robokassa", "Принимает оплату за услуги")
System_Ext(email_gateway, "SMTP сервер", "Отправляет уведомления операторам")
Person_Ext(operators, "Операторы SOC", "Обрабатывают заявки клиентов")

Rel(user, telegram_bot, "Отправляет сообщения")
Rel(telegram_bot, robokassa, "Направляет клиента на оплату")
Rel(telegram_bot, email_gateway, "Отправляет уведомления")
Rel(email_gateway, operators, "Доставляет e-mail уведомления")
@enduml
```

## Level 2 – Container Diagram

The solution is deployed as a single Python container that depends on external services.

```plantuml
@startuml Containers
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "Клиент Telegram")
System_Boundary(bot, "IST-detector") {
  Container(webhook, "Telegram Bot", "Python 3.11 / aiogram", "Обрабатывает команды, сохраняет состояние пользователя, создает ссылки Robokassa")
}
Container_Ext(telegram_api, "Telegram Bot API", "https", "Получает и доставляет обновления")
Container_Ext(robokassa, "Robokassa", "https", "Обработка платежей")
Container_Ext(smtp, "SMTP сервер", "smtps", "Отправка уведомлений операторам")

Rel(user, telegram_api, "Отправляет сообщения", "HTTPS")
Rel(telegram_api, webhook, "Передает обновления", "HTTPS")
Rel(webhook, robokassa, "Формирует ссылки оплаты", "HTTPS")
Rel(webhook, smtp, "Шлет уведомления", "SMTPS")
@enduml
```

## Level 3 – Component Diagram

Internally the bot is organised into distinct modules to keep the conversation logic maintainable.

```plantuml
@startuml Components
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

Container(webhook, "Telegram Bot", "Python/aiogram") {
  Component(loader, "loader", "Инициализация бота, загрузка настроек")
  Component(handlers, "handlers.services", "Основной сценарий диалога и генерация платежей")
  Component(keyboards, "keyboards.choise_buttons", "Формирование клавиатур")
  Component(catalog, "service_catalog", "Справочник услуг и тарифов")
  Component(config, "config", "Загрузка конфигурации через Pydantic")
}
Container_Ext(telegram_api, "Telegram Bot API")
Container_Ext(robokassa, "Robokassa")
Container_Ext(smtp, "SMTP")
Person(user, "Клиент Telegram")

Rel(user, handlers, "Сообщения/команды")
Rel(handlers, keyboards, "Получение клавиатур")
Rel(handlers, catalog, "Выбор услуг")
Rel(handlers, config, "Настройки SMTP/Robokassa")
Rel(handlers, robokassa, "Ссылки на оплату")
Rel(handlers, smtp, "Уведомления по e-mail")
Rel(loader, config, "Получает токены")
Rel(loader, handlers, "Передает Dispatcher")
@enduml
```

> PlantUML sources are provided so diagrams can be rendered if needed. Replace the remote include with a local copy when generating diagrams offline.

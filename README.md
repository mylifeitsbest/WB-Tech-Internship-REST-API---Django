<div align="center">

  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=26&pause=1000&color=F8D800&center=true&vCenter=true&width=700&lines=%F0%9F%9B%8D%EF%B8%8F+MARKETFLOW+E-COMMERCE+API;%E2%9A%A1+DJANGO+REST+FRAMEWORK+%2B+POSTGRESQL;%F0%9F%94%92+CONCURRENT+ORDER+PROCESSING" alt="Typing SVG" />

  <p align="center">
    <b>Масштабируемый REST API сервис интернет-магазина с изолированным слоем сервисов, JWT-авторизацией и транзакционным контролем склада</b>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Django-4+-092E20?style=flat-square&logo=django&logoColor=white" alt="Django" />
    <img src="https://img.shields.io/badge/DRF-REST_Framework-red?style=flat-square&logo=django&logoColor=white" alt="DRF" />
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/Swagger-OpenAPI_3.0-85EA2D?style=flat-square&logo=swagger&logoColor=black" alt="Swagger" />
  </p>

</div>

---

### 📌 О проекте

**MarketFlow** — полнофункциональный e-commerce бэкенд-сервис, спроектированный с учетом требований к надежности финансовых операций и параллельной обработке заказов. Сервис решает ключевые задачи онлайн-ритейла: управление каталогом, корзинами, балансом пользователей и атомарным резервированием товарных остатков при высоких нагрузках.

---

### 🛡️ Архитектурные паттерны & Особенности

* 🧱 **Изоляция бизнес-логики (Services Layer):** контроллеры (`views.py`) остаются тонкими — все транзакции и операции проводятся через выделенный слой `services.py`.
* 🔒 **Гарантия ACID и защита от Race Conditions:** оформление покупок выполняется строго внутри `@transaction.atomic` с пессимистической блокировкой строк инвентаря через `select_for_update()`. Исключает овербукинг и покупку товаров «в минус».
* 🔑 **Безопасность и сессии:** JWT-авторизация (Access / Refresh токены) на базе `simplejwt` с разграничением прав доступа (RBAC).
* 📜 **Аудит и логирование:** запись всех ключевых событий и финансовых транзакций в консоль и физический файл `orders.log`.
* 📖 **OpenAPI 3.0 Спецификация:** автогенерация документации и песочницы Swagger UI с помощью `drf-spectacular`.

---

### 🔄 Механика безопасного заказа (Transactional Flow)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Клиент (Mobile/Web)
    participant API as Orders API (DRF)
    participant Service as OrderService (services.py)
    participant DB as PostgreSQL (ACID)

    Client->>API: POST /api/orders/create/
    API->>Service: create_order(user, cart)
    critical Транзакционный блок (@transaction.atomic)
        Service->>DB: select_for_update() (Блокировка остатков на складе)
        Service->>DB: Валидация баланса кошелька и остатков
        Service->>DB: Списание баланса + Уменьшение остатка склада
        Service->>DB: Создание записи Order & OrderItems
        Service->>DB: Очистка корзины (Cart.clear())
    end
    Service-->>API: Объект созданного заказа
    API-->>Client: 201 Created (Детали заказа)

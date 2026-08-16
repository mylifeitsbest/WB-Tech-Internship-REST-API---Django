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
```

---

### 🛠️ Стек технологий

| Слой | Стек | Назначение |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.11+, Django 4+, DRF | Ядро API, сериализаторы, permissions |
| **Database** | PostgreSQL, Django ORM | Реляционное хранилище с ACID-гарантиями |
| **Auth** | JWT (simplejwt) | Безопасная аутентификация |
| **Docs** | drf-spectacular (Swagger UI) | Интерактивная песочница и OpenAPI схема |
| **DevOps & Tests** | Docker, Docker Compose, unittest | Контейнеризация и интеграционные тесты |

---

### 📄 Эндпоинты API

| Метод | Эндпоинт | Описание | Доступ |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/register/` | Регистрация нового пользователя | Public |
| `POST` | `/api/token/` | Получение пары JWT-токенов | Public |
| `GET` | `/api/users/profile/` | Просмотр профиля и баланса | Authenticated |
| `POST` | `/api/users/balance/topup/` | Пополнение внутреннего кошелька | Authenticated |
| `GET` | `/api/products/` | Каталог товаров магазина | Public |
| `POST` | `/api/products/` | Создание новой товарной позиции | Staff / Admin |
| `GET` | `/api/cart/` | Просмотр состава корзины | Authenticated |
| `POST` | `/api/cart/` | Добавление товара в корзину | Authenticated |
| `POST` | `/api/orders/create/` | Оформление заказа и списание средств | Authenticated |
| `GET` | `/api/docs/` | Интерактивный Swagger UI | Public |

---

### 🚀 Быстрый старт в Docker

#### 1. Подготовка конфигурации (.env)

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=production_ready_django_secret_key_12345
DEBUG=True
ALLOWED_HOSTS=*

DB_NAME=marketflow_db
DB_USER=postgres
DB_PASSWORD=postgres_secure_pass
DB_HOST=db
DB_PORT=5432
```

#### 2. Сборка и запуск сервисов

```bash
docker compose up --build
```

- **API:** `http://localhost:8000/api/`
- **Swagger UI:** `http://localhost:8000/api/docs/`

---

### 🧪 Запуск автоматических тестов

Интеграционные тесты покрывают критические сценарии: конкурентные покупки, нехватку денег на балансе и дефицит остатков на складе:

```bash
docker compose exec web python manage.py test
```

---

### 📂 Структура проекта

```plaintext
├── config/                  # Конфигурация Django и глобальный роутинг
│   ├── settings.py          # Базовые настройки, JWT, логи, spectacular
│   ├── urls.py              # Реестр маршрутов API
│   ├── wsgi.py              # WSGI-конфиг
│   └── asgi.py              # ASGI-конфиг
├── apps/                    # Бизнес-модули
│   ├── users/               # Модель пользователя, баланс, профили
│   ├── products/            # Каталог, категории, остатки на складе
│   └── orders/              # Корзина, транзакции и слой services.py
├── tests/                   # Интеграционные тесты
├── Dockerfile               # Контейнеризация Django API
├── docker-compose.yml       # Оркестрация web-сервиса и PostgreSQL
└── manage.py                # CLI-менеджер Django
```

# CryptoMonitor

**Система мониторинга цен криптовалют на основе CoinGecko API**

---

## Описание

Проект состоит из двух основных компонентов:

1. **API-сервер** на FastAPI (Python) для управления списком монет и получения исторических и текущих данных о ценах.
2. **Crawler** — асинхронный воркер, который периодически (каждую минуту) опрашивает CoinGecko API и сохраняет данные в базу.

Данные хранятся в PostgreSQL, Redis используется для очередей (опционально).

---

## Особенности

* Хранение истории цен, объема торгов и изменения за 24ч.
* CRUD для управления «coin» (добавление/удаление криптовалют).
* REST API с эндпоинтами:

  * `GET /api/v1/coins/` — список монет
  * `POST /api/v1/coins/` — добавить монету
  * `DELETE /api/v1/coins/{id}` — удалить монету
  * `GET /api/v1/coins/{id}/prices` — исторические данные
  * `GET /api/v1/coins/{id}/prices/latest` — текущая цена
* Crawler: автономно собирает и обновляет данные без дубликатов.
* Тесты на pytest для CRUD и API-интеграции.
* Поддержка локального запуска и контейнеризации через Docker Compose.

---

## Структура проекта

```
crypto_monitor/
├── .env                    # конфигурация (DB, Redis, JWT)
├── requirements.txt        # зависимости Python
├── docker-compose.yml      # контейнеры: PostgreSQL, Redis, API, Crawler
├── sql/
│   └── init_schema.sql     # SQL-скрипт инициализации БД
├── app/
│   ├── main.py             # FastAPI-приложение
│   ├── config.py           # загрузка .env
│   ├── database.py         # создание асинхронной сессии
│   ├── models.py           # SQLAlchemy-модели
│   ├── schemas.py          # Pydantic-схемы
│   ├── crud.py             # операции с БД
│   ├── api/
│   │   ├── coins.py        # роуты для /coins
│   │   └── prices.py       # роуты для /coins/{id}/prices
│   └── crawler/
│       └── crawler.py      # асинхронный воркер
└── tests/
    ├── conftest.py         # фикстуры pytest
    ├── test_coins.py       # CRUD-тесты
    └── test_prices.py      # тесты интеграции
```

---

## Пререквизиты

* Python 3.9+
* PostgreSQL
* Redis
* Docker & Docker Compose (рекомендуется)

---

## Установка и запуск локально

1. Клонируйте репозиторий:

   ```bash
   git clone <repo_url> && cd CryptoMonitor
   ```
2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\\Scripts\\activate   # Windows
   ```
3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```
4. Настройте `.env` в корне:

   ```ini
   DATABASE_URL=postgresql+asyncpg://crypto_user:password@localhost:5432/cryptodb
   REDIS_URL=redis://localhost:6379/0
   SECRET_KEY=<openssl rand -hex 32>
   ```
5. Поднимите PostgreSQL и Redis (локально или через Docker):

   ```bash
   docker run -d --name cryptodb -e POSTGRES_USER=crypto_user \
     -e POSTGRES_PASSWORD=your_password -e POSTGRES_DB=cryptodb -p 5432:5432 postgres:14-alpine
   docker run -d --name cryptoredis -p 6379:6379 redis:6-alpine
   ```
6. Инициализация схемы:

   ```bash
   psql postgresql://crypto_user:your_password@localhost:5432/cryptodb \
     -f sql/init_schema.sql
   ```
7. Запуск API-сервера:

   ```bash
   uvicorn app.main:app --reload
   ```
8. Запуск краулера (в другом терминале):

   ```bash
   python -m app.crawler.crawler
   ```

---

## Запуск через Docker Compose

1. Проверьте `docker-compose.yml` на корректность настроек.
2. Запустите все сервисы:

   ```bash
   docker-compose up -d --build
   ```
3. API доступен на `http://localhost:8000`.
4. Логи:

   ```bash
   docker-compose logs -f api
   docker-compose logs -f crawler
   ```

---

## Тестирование

Запустите тесты командой:

```bash
pytest -q
```

---



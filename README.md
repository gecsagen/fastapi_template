# Установка
1. **Создание виртуального окружения, установка зависимостей, создание БД:**
    `python -m venv .venv`
    `pip install -r requirements.txt`
    `docker-compose -f docker-compose-local.yaml up -d`

2. **Создание и применение миграций:**
**Создаем базу alembic: **
`alembic init migrations`
**Меняем путь к БД в файле алембика (alembic.ini): **
`sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres`
**Импортируем модели в env .py**
`from main import Base`
`target_metadata = Base.metadata`
**Создаем первую миграцию **
`alembic revision --autogenerate -m "comment"`
**Применяем миграции: **
`alembic upgrade heads`

3. **Запуск проекта:**
`uvicorn main:app --port 8000  --reload`

# Структура проекта:
**main.py **-- *API роутеры, и запуск API*
**requirements.txt **-- *зависимости проекта*
**session.py **-- *создание сессии БД и движка БД*
**settings.py** -- *настройки БД и хэширования*
**security.py **-- *работа с токенами*
**.gitignore** -- *ингорируемые файлы и папки при коммитах*
**docker-compose-local.yaml** -- *докер для БД*
**user/api_login.py** -- *эндпоинт создания токена*
**user/api **-- *эндпоинты пользователя*
**user/dals.py** -- *методы работы с пользователем через БД*
**user/hashing.py **-- *методы валидации и хэширования паролей*
**user/models.py** -- *ORM модели *
**user/schemas.py** -- *pydantic модели для валидации данных*
**user/services.py** -- *сервисный слой (обертки для методов работы с БД,
для каждого метода открывается новая сессия с БД)*
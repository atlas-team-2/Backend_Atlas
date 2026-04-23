# Проект: «Атлас народов»

Проект представляет собой веб-платформу для изучения народов России.  
Пользователь может выбрать регион и увидеть народы, проживающие на его территории.  
Также пользователь может выбрать конкретный народ и перейти к статье с информацией о нём.  
Платформа позволяет создавать новые материалы, редактировать существующие статьи и предлагать правки.  
В статье отображается мини-карта, на которой показаны все регионы проживания выбранного народа.

## Состав команды и роли

- **@AzalinaF** — Backend Developer
- **@asilya18** — Backend Developer
- **@Guzykkkk** — Frontend Developer
- **@Kami00613** — Frontend Developer
- **@somerealsanua** — Frontend Developer

## Используемые технологии

- FastAPI
- SQLModel
- PostgreSQL
- asyncpg
- Pydantic Settings
- Uvicorn
- uv

## Переменные окружения

Для настройки проекта используются переменные окружения.  
Пример заполнения находится в файле `.env.example`.

| Название переменной | Тип | Описание | Значение по умолчанию |
|---|---|---|---|
| DB_SCHEMA | string | Схема подключения к базе данных | postgresql+asyncpg |
| APP_NAME | string | Название приложения | Atlas Naroda API |
| APP_VERSION | string | Версия приложения | 1.0.0 |
| APP_DESCRIPTION | string | Описание приложения | API для проекта Атлас народа |
| DB_HOST | string | Хост PostgreSQL | localhost |
| DB_PORT | int | Порт PostgreSQL | 5432 |
| DB_NAME | string | Имя базы данных | atlas_db |
| DB_USER | string | Пользователь PostgreSQL | postgres |
| DB_PASSWORD | string | Пароль PostgreSQL | postgres |

## Файл `.env.example`

В проекте присутствует файл `.env.example` со всеми необходимыми переменными среды и значениями по умолчанию.

## Работа с миграциями (Alembic)

Для управления структурой базы данных используется Alembic.

### Создание новой миграции
uv run alembic revision --autogenerate -m "описание изменений"

### Применение миграций
uv run alembic upgrade head

### Откат миграций
uv run alembic downgrade -1

### Просмотр истории миграций
uv run alembic history

### Проверка текущего состояния
uv run alembic current


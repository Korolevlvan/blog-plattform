# Blog Platform API

Бэкенд для лабораторной работы 1: FastAPI + SQLAlchemy + Alembic + PostgreSQL + JWT + Docker.

## Что реализовано

- CRUD для статей
- регистрация, логин, получение и обновление текущего пользователя
- комментарии к статьям
- JWT-аутентификация через `Authorization: Bearer <token>`
- PostgreSQL как основная база данных
- миграции Alembic
- Dockerfile и `docker-compose.yaml`
- healthchecks для приложения и БД
- профиль `dev` для запуска только PostgreSQL
- GitHub Actions для публикации в GHCR и автодеплоя на Render через deploy hook

## Структура проекта

```text
├── src/
│   ├── controllers/
│   ├── core/
│   ├── db/
│   ├── dependencies/
│   ├── models/
│   ├── routes/
│   └── schemas/
├── migrations/
├── .github/workflows/
├── docker/
├── Dockerfile
├── docker-compose.yaml
├── .env.example
├── alembic.ini
├── main.py
└── README.md
```

## Быстрый старт

### 1. Подготовка окружения

Скопируйте `.env.example` в `.env`:

```bash
cp .env.example .env
```

### 2. Сборка и запуск

```bash
docker compose up --build
```

Приложение будет доступно по адресу:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Healthcheck: `http://localhost:8000/health`

### 3. Только PostgreSQL для локальной разработки

```bash
docker compose --profile dev up db-dev -d
```

## Основные эндпоинты

### Пользователи

- `POST /api/users` — регистрация
- `POST /api/users/login` — логин
- `GET /api/user` — текущий пользователь
- `PUT /api/user` — обновление текущего пользователя

### Статьи

- `POST /api/articles` — создать статью
- `GET /api/articles` — список статей
- `GET /api/articles/{slug}` — получить статью
- `PUT /api/articles/{slug}` — обновить статью
- `DELETE /api/articles/{slug}` — удалить статью

### Комментарии

- `POST /api/articles/{slug}/comments` — добавить комментарий
- `GET /api/articles/{slug}/comments` — список комментариев
- `DELETE /api/articles/{slug}/comments/{comment_id}` — удалить комментарий

## Пример сценария тестирования

### Регистрация

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "secret123",
    "bio": "My bio",
    "image_url": "https://example.com/avatar.png"
  }'
```

### Логин

```bash
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secret123"
  }'
```

### Создание статьи

```bash
curl -X POST http://localhost:8000/api/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{
    "title": "My First Article",
    "description": "Short description",
    "body": "Full article body",
    "tagList": ["fastapi", "python"]
  }'
```

### Добавление комментария

```bash
curl -X POST http://localhost:8000/api/articles/my-first-article/comments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d '{"body": "Great article!"}'
```

## GitHub Actions и GHCR

Перед пушем в GitHub:

1. Включите **Read and write permissions** в `Settings -> Actions -> General`.
2. Убедитесь, что пакет GHCR наследует доступ от репозитория.
3. Запушьте код в ветку `main`.

Образ будет опубликован как:

```text
ghcr.io/<github_username>/<repository>:latest
```

## Автодеплой на Render

1. Создайте Web Service на Render.
2. Выберите деплой из Docker Registry.
3. Укажите образ `ghcr.io/<github_username>/<repository>:latest`.
4. Добавьте переменные окружения из `.env`.
5. Создайте deploy hook и сохраните его в GitHub Secret `RENDER_DEPLOY_HOOK_URL`.

После этого workflow будет автоматически публиковать образ и триггерить деплой.

## Ссылки для README после реального деплоя

После публикации замените плейсхолдеры на реальные ссылки:

- Deployed app: `https://<your-service>.onrender.com`
- Swagger UI: `https://<your-service>.onrender.com/docs`

# API для Yatube

`api_final_yatube` — REST API для социальной платформы Yatube. Проект позволяет получать, создавать, редактировать и удалять публикации и комментарии, просматривать сообщества, а также подписываться на авторов. Аутентификация построена на JWT-токенах.

## Возможности

- публикации: список, просмотр, создание, редактирование и удаление;
- комментарии: вложенные маршруты для работы с комментариями к постам;
- сообщества: просмотр списка и деталей;
- подписки: подписка на авторов и поиск по своим подпискам;
- JWT-аутентификация через `/api/v1/jwt/`.

## Стек

- Python 3.12
- Django 5
- Django REST framework
- Simple JWT
- Pytest

## Установка

1. Клонируйте репозиторий и перейдите в него:

```bash
git clone <repo_url>
cd api-final-yatube
```

2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Выполните миграции:

```bash
python yatube_api/manage.py migrate
```

5. Запустите сервер:

```bash
python yatube_api/manage.py runserver
```

Документация Redoc будет доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).

## Примеры запросов

Получить JWT-токен:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"username":"TestUser","password":"1234567"}'
```

Ответ:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

Получить список публикаций:

```bash
curl http://127.0.0.1:8000/api/v1/posts/
```

Ответ:

```json
[
  {
    "id": 1,
    "author": "TestUser",
    "text": "Первый пост",
    "pub_date": "2026-06-19T12:00:00Z",
    "image": null,
    "group": 1
  }
]
```

Создать публикацию:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/posts/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Новый пост","group":1}'
```

Ответ:

```json
{
  "id": 2,
  "author": "TestUser",
  "text": "Новый пост",
  "pub_date": "2026-06-19T12:30:00Z",
  "image": null,
  "group": 1
}
```

Получить комментарии к посту:

```bash
curl http://127.0.0.1:8000/api/v1/posts/1/comments/
```

Ответ:

```json
[
  {
    "id": 1,
    "author": "TestUser",
    "text": "Первый комментарий",
    "created": "2026-06-19T12:40:00Z",
    "post": 1
  }
]
```

Подписаться на автора:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/follow/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"following":"TestUserAnother"}'
```

Ответ:

```json
{
  "user": "TestUser",
  "following": "TestUserAnother"
}
```

## Автор

Максим

- GitHub: [minozis](https://github.com/minozis)

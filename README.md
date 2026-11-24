# BookNest API

REST API для управления книгами и авторами на FastAPI.

## Запуск проекта
1. Создать виртуальное окружение: `python -m venv venv`
2. Активировать: `.\venv\Scripts\Activate.ps1`
3. Установить зависимости: `python -m pip install -r requirements.txt`
4. Запустить сервер: `uvicorn app.main:app --reload`

## Документация
После запуска документация Swagger UI доступна по адресу: http://127.0.0.1:8000/docs
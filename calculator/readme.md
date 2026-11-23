# Credit Calculator

Микросервис расчета кредитных предложений и параметров кредита.

## Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

## Настройка

Скопируйте файл с примером конфигурации и при необходимости измените параметры:

```bash
cp .env.example .env
```

## Запуск

Из директории `calculator`:

```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу http://127.0.0.1:8000

## Swagger

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Тесты

Из директории `calculator`:

```bash
pytest
```

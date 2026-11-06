# Инвест-ферма: Django-бэкенд

## Запуск
```
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env         # Linux/Mac: cp .env.example .env
```
Откройте `.env` и впишите свой ключ в `AI_API_KEY` (и свой `DJANGO_SECRET_KEY`).
```
python manage.py makemigrations game
python manage.py migrate
python manage.py runserver
```
Сайт: http://127.0.0.1:8000/  Админка: `python manage.py createsuperuser`, затем /admin/

## API
- `GET  /api/market/` — котировки (симулятор в game/market.py)
- `GET/POST /api/state/` — загрузка и сохранение фермы игрока (по сессии)
- `POST /api/ai/` — вопрос ИИ-аналитику `{question, context}`; ключ хранится только на сервере

## Для продакшена
DJANGO_DEBUG=0, свой SECRET_KEY, ALLOWED_HOSTS, HTTPS, gunicorn; добавьте авторизацию вместо сессий.
Реальные котировки: заменить _step()/_init() в game/market.py запросом к API биржи.

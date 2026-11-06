"""Обращение к ИИ-агенту. Ключ берётся из настроек (.env) и никогда не попадает в браузер."""
import requests
from django.conf import settings

SYSTEM = (
    "Ты ИИ-аналитик учебной игры про российский рынок акций. Отвечай по-русски, кратко "
    "(до 5 предложений), опираясь на переданные данные. Цены симулированные. "
    "Не давай инвестиционных рекомендаций, напоминай о диверсификации."
)


class AIError(Exception):
    pass


def ask_ai(question, context):
    if not settings.AI_API_KEY:
        raise AIError("AI_API_KEY не задан в файле .env")
    try:
        r = requests.post(
            settings.AI_API_URL,
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": settings.AI_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": f"Данные: {context}\nВопрос: {question}"},
                ],
            },
            timeout=40,
        )
    except requests.RequestException as e:
        raise AIError(f"Сервис ИИ недоступен: {e.__class__.__name__}")
    if r.status_code != 200:
        raise AIError(f"Сервис ИИ вернул HTTP {r.status_code}")
    try:
        return r.json()["choices"][0]["message"]["content"] or "Пустой ответ."
    except (KeyError, IndexError, ValueError):
        raise AIError("Неожиданный формат ответа ИИ")

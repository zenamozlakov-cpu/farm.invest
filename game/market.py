"""Симулятор рынка (учебные данные). Для реальных котировок замените _step() запросом к API биржи."""
import random
import time
from django.core.cache import cache

STOCKS = {
    "SBER": ("Сбербанк", "Банки", 310, 4.6),
    "VTBR": ("ВТБ", "Банки", 80, 2.8),
    "GAZP": ("Газпром", "Нефть и газ", 128, 3.9),
    "LKOH": ("Лукойл", "Нефть и газ", 7100, 6.1),
    "ROSN": ("Роснефть", "Нефть и газ", 430, 4.2),
    "YDEX": ("Яндекс", "Технологии", 4200, 18),
    "MTSS": ("МТС", "Технологии", 230, 7.4),
    "GMKN": ("Норникель", "Металлы", 135, 8.2),
}
TICK_SECONDS = 3
HISTORY = 60


def _init():
    data = {}
    for t, (_, _, p, _) in STOCKS.items():
        x, h = p * random.uniform(0.9, 1.1), []
        for _ in range(HISTORY):
            x *= 1 + random.uniform(-0.01, 0.01)
            h.append(round(x, 2))
        data[t] = h
    return {"history": data, "ts": time.time()}


def _step(state):
    for h in state["history"].values():
        h.append(round(h[-1] * (1 + random.uniform(-0.006, 0.006)), 2))
        del h[0]


def get_market():
    state = cache.get("market") or _init()
    steps = min(int((time.time() - state["ts"]) // TICK_SECONDS), 20)
    for _ in range(steps):
        _step(state)
    if steps:
        state["ts"] = time.time()
    cache.set("market", state, None)
    return [
        {"t": t, "name": n, "sector": s, "pe": pe, "history": state["history"][t], "price": state["history"][t][-1]}
        for t, (n, s, _, pe) in STOCKS.items()
    ]

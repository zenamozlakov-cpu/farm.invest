from django.db import models


class GameState(models.Model):
    """Сохранённая ферма игрока (привязана к сессии браузера)."""
    session_key = models.CharField(max_length=64, unique=True)
    cash = models.FloatField(default=1_000_000)
    positions = models.JSONField(default=dict)  # {"SBER": {"q": 10, "avg": 300.5, "x": 10, "y": 20, "placed": 1}}
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session_key[:8]}… cash={self.cash:.0f}"

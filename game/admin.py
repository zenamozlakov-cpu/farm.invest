from django.contrib import admin
from .models import GameState

@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    list_display = ("session_key", "cash", "updated")

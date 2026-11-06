from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/market/", views.market),
    path("api/state/", views.state),
    path("api/ai/", views.ai),
]

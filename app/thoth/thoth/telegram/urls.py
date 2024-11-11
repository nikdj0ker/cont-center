from django.urls import path

from .api.views import BotWebhook

urlpatterns = [
    path("", BotWebhook.as_view(), name="telegram"),
]

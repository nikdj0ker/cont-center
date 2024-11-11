import logging

from django.http import HttpResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from thoth.telegram.models import Bot, UserBot
from thoth.telegram.utils import message_processing

from .serializers import BotSerializer, UserBotSerializer


logger = logging.getLogger("telegram")


class BotWebhook(GenericViewSet, CreateModelMixin):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    def create(self, request, *args, **kwargs):
        return message_processing(request)


class UserBotWebhook(GenericViewSet, CreateModelMixin):
    queryset = UserBot.objects.all()
    serializer_class = UserBotSerializer

    def create(self, request, *args, **kwargs):
        return message_processing(request)

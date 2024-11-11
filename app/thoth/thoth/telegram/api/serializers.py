from rest_framework import serializers

from thoth.telegram.models import Bot, UserBot


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = [
            "bot_name",
            "owner",
        ]


class UserBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBot
        fields = [
            "userbot_name",
            "owner",
        ]

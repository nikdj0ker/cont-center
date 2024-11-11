from django.conf import settings
from django.db import models

from thoth.bitrix.models import AppInstance
from thoth.bitrix.models import Line


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    user_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    source = models.ForeignKey('Reklama_Source', on_delete=models.CASCADE, null=True)
    campaign = models.ForeignKey('Reklama_Campaign', on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False)
    first_use = models.DateTimeField()
    last_use = models.DateTimeField()

    def __str__(self):
        return f"{self.user_name}"


class Reklama_Source(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    link = models.CharField(max_length=255, null=True)
    note = models.TextField(null=True)


class Reklama_Campaign(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    source = models.ForeignKey('Reklama_Source', on_delete=models.CASCADE)
    adv_link = models.CharField(max_length=255, null=True)
    adv = models.ForeignKey('Reklama_Adv', on_delete=models.CASCADE)
    money = models.BigIntegerField(null=True)
    start = models.DateField(null=True)
    end = models.DateField(null=True)
    note = models.TextField(null=True)


class Reklama_Adv(models.Model):
    text = models.TextField()


class Bot(models.Model):
    bot_name = models.CharField(max_length=255, unique=True, editable=True)
    bot_token = models.CharField(max_length=255)
    sms_service = models.BooleanField(default=False)
    old_sms_service = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app_instance = models.ForeignKey(AppInstance, on_delete=models.SET_NULL, null=True)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.bot_name}"


class UserBot(models.Model):
    userbot_name = models.CharField(max_length=255, unique=True, editable=True)
    api_id = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    sms_service = models.BooleanField(default=False)
    old_sms_service = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app_instance = models.ForeignKey(AppInstance, on_delete=models.SET_NULL, null=True)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.userbot_name}"

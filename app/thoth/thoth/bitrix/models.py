import uuid

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


class App(models.Model):
    APP_NAME = [
        ("olx", "olx"),
        ("waba", "waba"),
        ("telegram", "telegram"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="apps", blank=True, null=True
    )
    name = models.CharField(max_length=255, blank=True, choices=APP_NAME)
    connector = models.BooleanField(default=False)
    client_id = models.CharField(max_length=255, blank=True, unique=True)
    client_secret = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def get_instances(self):
        return self.installations.all()


class Bitrix(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user_id = models.CharField(max_length=255, blank=True, null=True)
    client_endpoint = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.domain

    def get_instances(self):
        return self.installations.all()


class AppInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name="installations")
    portal = models.ForeignKey(
        Bitrix, on_delete=models.CASCADE, related_name="installations"
    )
    auth_status = models.CharField(max_length=1)
    access_token = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    application_token = models.CharField(max_length=255, blank=True)
    storage_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.app.name} on {self.portal.domain}"


class Line(models.Model):
    line_id = models.CharField(max_length=50)
    app_instance = models.ForeignKey(
        "AppInstance", on_delete=models.CASCADE, related_name="lines", null=True
    )

    def __str__(self):
        return f"Line {self.line_id} for AppInstance {self.app_instance}"


class VerificationCode(models.Model):
    portal = models.OneToOneField(Bitrix, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()

from rest_framework import serializers
from olx.models import OlxApp, OlxUser

class OlxAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlxApp
        fields = ['owner', 'client_domain', 'client_id', 'client_secret', 'authorization_link']

class OlxUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlxUser
        fields = ['olxapp', 'bitrix', 'olx_id', 'email', 'name', 'phone', 'access_token', 'refresh_token']

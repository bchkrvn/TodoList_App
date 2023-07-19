from rest_framework import serializers
from django.conf import settings


class BotVerifySerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=settings.TOKEN_LENGTH * 2)

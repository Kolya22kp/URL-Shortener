from rest_framework import serializers
from .models import ShortenedURL
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortenedURLSerializer(serializers.ModelSerializer):
    """Сериалайзер для сокращенных ссылок"""
    class Meta:
        model = ShortenedURL
        fields = ['id', 'original_url', 'short_code', 'created_at', 'click_count']
        read_only_fields = ['short_code', 'created_at', 'click_count']

    def validate_original_url(self, value):
        """Функция для валидации ссылки"""
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid URL")
        return value
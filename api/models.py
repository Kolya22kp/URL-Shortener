from django.db import models
import random
import string, logging

class ShortenedURL(models.Model):
    """Модель сокращенных ссылок"""
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    def generate_short_code(self):
        """Генерация случайного кода длиной 6 символов"""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(6))

    def save(self, *args, **kwargs):
        """Сохранение кода сокращенной ссылки"""
        if not self.short_code:
            self.short_code = self.generate_short_code()
            while ShortenedURL.objects.filter(short_code=self.short_code).exists():
                self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)
        logging.info(f"Создана ссылка с кодом {self.short_code}. Оригинальная ссылка: {self.original_url[25:]}...")

    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
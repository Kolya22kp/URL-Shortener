from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ShortenedURL
import logging

# Отключаем логирование во время тестов
logging.disable(logging.CRITICAL)


class ShortenedURLModelTest(TestCase):
    def test_create_short_url(self):
        """Тест создания короткой ссылки"""
        url = ShortenedURL.objects.create(original_url="https://www.example.com")
        self.assertIsNotNone(url.short_code)
        self.assertEqual(url.click_count, 0)

    def test_unique_short_codes(self):
        """Тест уникальности коротких кодов"""
        url1 = ShortenedURL.objects.create(original_url="https://www.example1.com")
        url2 = ShortenedURL.objects.create(original_url="https://www.example2.com")
        url3 = ShortenedURL.objects.create(original_url="https://www.example3.com")
        self.assertNotEqual(url1.short_code, url2.short_code)


class ShortURLAPITest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('create_short_url')
        self.test_url = "https://www.example.com"

    def test_create_short_url(self):
        """Тест API создания короткой ссылки"""
        data = {'original_url': self.test_url}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('short_code', response.data)

    def test_redirect_url(self):
        """Тест редиректа по короткой ссылке"""
        # Сначала создаем короткую ссылку
        url_obj = ShortenedURL.objects.create(original_url=self.test_url)

        # Тестируем редирект
        redirect_url = reverse('redirect', args=[url_obj.short_code])
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, 302)  # Проверяем редирект
        self.assertEqual(response.url, self.test_url)

        # Проверяем, что счетчик увеличился
        url_obj.refresh_from_db()
        self.assertEqual(url_obj.click_count, 1)

    def test_get_stats(self):
        """Тест получения статистики"""
        url_obj = ShortenedURL.objects.create(original_url=self.test_url)
        stats_url = reverse('url_stats', args=[url_obj.short_code])
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['original_url'], self.test_url)

    def test_invalid_url_creation(self):
        """Тест создания ссылки с невалидным URL"""
        data = {'original_url': 'invalid-url'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RedirectViewTest(TestCase):
    def test_redirect_nonexistent_code(self):
        """Тест редиректа с несуществующим коротким кодом"""
        response = self.client.get('/api/v1/nonexistent/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
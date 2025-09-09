from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.response import Response
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer
import logging

class CreateShortURLView(generics.CreateAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer

class URLStatsView(generics.RetrieveAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'short_code'

def redirect_view(request, short_code):
    """Перенаправляет на оригинальный URL и увеличивает счетчик кликов"""
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    shortened_url.click_count += 1
    shortened_url.save()
    logging.info(f"Переход по короткой ссылке https://127.0.0.1:8000/api/v1/{short_code} с переходом на {shortened_url.original_url[:25]}...")
    return redirect(shortened_url.original_url)

from django.contrib import admin
from .models import ShortenedURL

@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ['original_url', 'short_code', 'click_count', 'created_at']
    readonly_fields = ['short_code', 'click_count']
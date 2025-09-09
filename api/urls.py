from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateShortURLView.as_view(), name='create_short_url'),
    path('stats/<str:short_code>/', views.URLStatsView.as_view(), name='url_stats'),
    path('<str:short_code>/', views.redirect_view, name='redirect'),
]
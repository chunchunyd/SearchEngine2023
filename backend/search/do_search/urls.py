"""
路由配置
"""
from django.urls import path, include
from .views import text_search, key_search


urlpatterns = [
    path('text_search/', text_search),
    path('key_search/', key_search)
]
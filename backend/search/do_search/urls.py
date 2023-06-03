"""
路由配置
"""
from django.urls import path, include
from .views import text_search, key_search, similar_search, test_similar


urlpatterns = [
    path('text_search/', text_search),
    path('key_search/', key_search),
    path('similar_search/', similar_search),
    path('test_similar/', test_similar),
]
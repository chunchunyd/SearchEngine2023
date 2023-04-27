"""
路由配置
"""
from django.urls import path, include
from .views import query_search


urlpatterns = [
    path('query_search/', query_search),
]
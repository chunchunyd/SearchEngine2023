"""
路由配置
"""
from django.urls import path
from .views import launch_spider, spider_progress

urlpatterns = [
    path('launch_spider/', launch_spider),
    path('spider_progress/', spider_progress),
]
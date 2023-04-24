"""
router for common app
"""
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IndexViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('indexes', IndexViewSet)

urlpatterns = [
    path('', include(router.urls))
]
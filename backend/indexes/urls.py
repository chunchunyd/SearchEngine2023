"""
路由配置
"""
from django.urls import path, include
from .views import build_index, test_search, build_term, build_user_dict, load_user_dict
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('term', TermViewSet)
# router.register('posting', PostingViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('build_index/', build_index),
    path('build_term/', build_term),
    path('test_search/', test_search),
    path('build_userdict/', build_user_dict),
    path('load_userdict/', load_user_dict),
]
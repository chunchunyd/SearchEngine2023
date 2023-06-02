"""
路由配置
"""
from django.urls import path
from .views import test_iter, test_doc2vec

urlpatterns = [
    path('test_iter/', test_iter),
    path('test_doc2vec/', test_doc2vec),
]
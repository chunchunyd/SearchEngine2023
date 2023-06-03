"""
路由配置
"""
from django.urls import path
from .views import test_iter, test_doc2vec, test_get_doc, train_model

urlpatterns = [
    path('test_iter/', test_iter),
    path('test_doc2vec/', test_doc2vec),
    path('test_get_doc/', test_get_doc),
    path('train_model/', train_model),
]

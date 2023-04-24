from rest_framework.serializers import ModelSerializer
from .models import Tag, Index


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IndexSerializer(ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'

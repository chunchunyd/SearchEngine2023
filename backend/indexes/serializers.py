from rest_framework.serializers import ModelSerializer
from .models import *


class TermSerializer(ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'


class PostingSerializer(ModelSerializer):
    class Meta:
        model = Posting
        fields = '__all__'

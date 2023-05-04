from rest_framework import serializers
from .models import *


class TermSerializer(serializers.Serializer):
    term = serializers.CharField(max_length=100)
    document_count = serializers.IntegerField()


class PostingSerializer(serializers.Serializer):
    term = serializers.CharField(max_length=100)
    doc_id = serializers.IntegerField()
    frequency = serializers.IntegerField()
    position = serializers.IntegerField()

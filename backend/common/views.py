"""
使用ModelViewSet来代替APIView
"""
from rest_framework.viewsets import ModelViewSet
from .models import Tag, Index
from .serializers import TagSerializer, IndexSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IndexViewSet(ModelViewSet):
    queryset = Index.objects.all()
    serializer_class = IndexSerializer


# 如果不使用ModelViewSet,则需要使用APIView：
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Tag, Index
# from .serializers import TagSerializer, IndexSerializer
#
#
# class TagView(APIView):
#     def get(self, request):
#         tags = Tag.objects.all()
#         serializer = TagSerializer(tags, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = TagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

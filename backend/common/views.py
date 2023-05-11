"""
使用ModelViewSet来代替APIView
"""
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from backend.settings import DEFAULT_PAGE_SIZE
from .models import *
from .serializers import *
from .filters import *


class CourtViewSet(ReadOnlyModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

    filter_backends = [DjangoFilterBackend]
    filterset_class = CourtFilterSet


class ProcuratorateViewSet(ReadOnlyModelViewSet):
    queryset = Procuratorate.objects.all()
    serializer_class = ProcuratorateSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProsecutionFilterSet


class PartyViewSet(ReadOnlyModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


class AgentViewSet(ReadOnlyModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


class LawReferenceViewSet(ReadOnlyModelViewSet):
    queryset = LawReference.objects.all()
    serializer_class = LawReferenceSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


class JudgeViewSet(ReadOnlyModelViewSet):
    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


class DocumentViewSet(ReadOnlyModelViewSet):
    queryset = LawDocument.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

    filter_backends = [DjangoFilterBackend]
    filterset_class = LawDocumentFilterSet


class JudgmentViewSet(ReadOnlyModelViewSet):
    queryset = Judgment.objects.all()
    serializer_class = JudgmentSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

    filter_backends = [DjangoFilterBackend]
    filterset_class = JudgmentFilterSet


class ProsecutionViewSet(ReadOnlyModelViewSet):
    queryset = Prosecution.objects.all()
    serializer_class = ProsecutionSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

    filter_backends = [DjangoFilterBackend]
    filterset_class = ProsecutionFilterSet


class DocAgentPartyViewSet(ReadOnlyModelViewSet):
    queryset = DocAgentParty.objects.all()
    serializer_class = DocAgentPartySerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE

# class TagViewSet(ModelViewSet):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#
#
# class IndexViewSet(ModelViewSet):
#     queryset = Index.objects.all()
#     serializer_class = IndexSerializer


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

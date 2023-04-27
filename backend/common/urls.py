"""
router for common app
"""
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()
router.register('court', CourtViewSet)
router.register('procuratorate', ProcuratorateViewSet)
router.register('party', PartyViewSet)
router.register('agent', AgentViewSet)
router.register('lawreference', LawReferenceViewSet)
router.register('judge', JudgeViewSet)
router.register('document', DocumentViewSet)
router.register('judgment', JudgmentViewSet)
router.register('prosecution', ProsecutionViewSet)
router.register('docagentparty', DocAgentPartyViewSet)

urlpatterns = [
    path('', include(router.urls))
]
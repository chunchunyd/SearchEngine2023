from rest_framework.serializers import ModelSerializer
from .models import *


class CourtSerializer(ModelSerializer):
    class Meta:
        model = Court
        fields = '__all__'


class ProcuratorateSerializer(ModelSerializer):
    class Meta:
        model = Procuratorate
        fields = '__all__'


class PartySerializer(ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'


class AgentSerializer(ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class LawReferenceSerializer(ModelSerializer):
    class Meta:
        model = LawReference
        fields = '__all__'


class JudgeSerializer(ModelSerializer):
    class Meta:
        model = Judge
        fields = '__all__'


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class JudgmentSerializer(ModelSerializer):
    class Meta:
        model = Judgment
        fields = '__all__'


class ProsecutionSerializer(ModelSerializer):
    class Meta:
        model = Prosecution
        fields = '__all__'

import pymongo
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

    # def get_short_text(self, obj, first_word):
    #     client = pymongo.MongoClient('mongodb://localhost:27017/')
    #     db = client['search_engine']
    #     Posting = db['posting']
    #     # 获取文档的倒排索引
    #     posting = list(Posting.find({'doc_id': obj.id, 'term': first_word}))
    #     if posting[0]['positions'][0] - 20 < 0:
    #         start = 0
    #     else:
    #         start = posting[0]['positions'][0] - 20
    #     if posting[0]['positions'][0] + 280 > len(obj.text):
    #         end = len(obj.text)
    #     else:
    #         end = posting[0]['positions'][0] + 280
    #     return obj.full_text[start:end]

    class Meta:
        model = LawDocument
        fields = '__all__'


class JudgmentSerializer(ModelSerializer):
    class Meta:
        model = Judgment
        fields = '__all__'


class ProsecutionSerializer(ModelSerializer):
    class Meta:
        model = Prosecution
        fields = '__all__'


class DocAgentPartySerializer(ModelSerializer):
    class Meta:
        model = DocAgentParty
        fields = '__all__'
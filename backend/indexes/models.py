from django.db import models
from common.models import LawDocument
from mongoengine import Document, StringField, IntField, ListField, FloatField


# class Term(Document):
#     """
#     存储索引词条
#     """
#     term = StringField(max_length=100)  # 词条
#     document_count = IntField()  # 出现该词条的文档数
#     idf = FloatField()  # 逆文档频率
#     meta = {
#         'collection': 'term',
#         'indexes': [
#             'term',
#         ]}
#
#
# class Posting(Document):
#     """
#     存储倒排索引
#     """
#     term = StringField(max_length=100)  # 词条
#     doc_id = IntField()  # 文档ID
#     # frequency = IntField()  # 词频
#     position = ListField()  # 位置
#     freq = IntField()  # 词频
#     meta = {
#         'collection': 'posting',
#         'indexes': [
#             'term',
#             'doc_id',
#             'freq'
#         ]}
#
#
# class Law_Document(Document):
#     """
#     存储文档
#     """
#     doc_id = IntField(primary_key=True)  # 文档ID
#     doc_len = IntField()  # 文档长度
#     meta = {
#         'collection': 'law_document',
#         'indexes': [
#             'doc_len'
#         ]}

# class Term(models.Model):
#     """
#     存储索引词条
#     """
#     term = models.CharField(max_length=100, verbose_name='词条')  # 词条
#     document_count = models.IntegerField(verbose_name='出现该词条的文档数')  # 出现该词条的文档数
#
#     class Meta:
#         verbose_name = '词条'
#         verbose_name_plural = verbose_name
#         indexes = [
#             models.Index(fields=['term']),
#         ]
#
#     def __str__(self):
#         return self.term
#
#
# class Posting(models.Model):
#     """
#     存储倒排索引
#     """
#     term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='词条')  # 词条
#     doc_id = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='文档ID')  # 文档ID
#     frequency = models.IntegerField(verbose_name='词频')  # 词频
#     position = models.IntegerField(verbose_name='位置')  # 位置
#
#     class Meta:
#         verbose_name = '倒排索引'
#         verbose_name_plural = verbose_name
#         indexes = [
#             models.Index(fields=['term']),
#             models.Index(fields=['doc_id']),
#             models.Index(fields=['term', 'doc_id']),
#         ]
#
#     def __str__(self):
#         return self.term.term

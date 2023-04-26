from django.db import models
from common.models import Document


# Create your models here.
# class Index(models.Model):
#     """
#     倒排索引
#     """
#     word = models.CharField(max_length=100, verbose_name='词条')  # 词条
#     doc_id = models.IntegerField(verbose_name='文档ID')  # 文档ID
#     frequency = models.IntegerField(verbose_name='词频')  # 词频
#     position = models.TextField(verbose_name='位置')  # 位置
#
#     class Meta:
#         verbose_name = '倒排索引'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.word

class Term(models.Model):
    """
    存储索引词条
    """
    term = models.CharField(max_length=100, verbose_name='词条')  # 词条
    document_count = models.IntegerField(verbose_name='出现该词条的文档数')  # 出现该词条的文档数

    class Meta:
        verbose_name = '词条'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['term']),
        ]

    def __str__(self):
        return self.term


class Posting(models.Model):
    """
    存储倒排索引
    """
    term = models.ForeignKey(Term, on_delete=models.CASCADE, verbose_name='词条')  # 词条
    doc_id = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name='文档ID')  # 文档ID
    frequency = models.IntegerField(verbose_name='词频')  # 词频
    position = models.IntegerField(verbose_name='位置')  # 位置

    class Meta:
        verbose_name = '倒排索引'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['term']),
            models.Index(fields=['doc_id']),
            models.Index(fields=['term', 'doc_id']),
        ]

    def __str__(self):
        return self.term.term

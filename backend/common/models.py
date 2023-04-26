"""
raw_data: 原始数据
"""
from django.db import models


# 设置max_length时注意汉字占三个字符
class Court(models.Model):
    """
    法院模型
    """
    name = models.CharField(max_length=100, verbose_name='法院名称')  # 法院标准名称
    code = models.CharField(max_length=10, verbose_name='法院层级码')  # 法院层级码
    level = models.CharField(max_length=10, verbose_name='法院级别')  # 法院级别(eg. 基层、中级、高级)
    province = models.CharField(max_length=30, verbose_name='省份')  # 行政区划——省份
    city = models.CharField(max_length=50, verbose_name='城市')  # 行政区划——城市

    class Meta:
        verbose_name = '法院'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Procuratorate(models.Model):
    """
    检察院模型
    """
    name = models.CharField(max_length=100, verbose_name='检察院名称')  # 检察院名称
    district_code = models.CharField(max_length=10, verbose_name='行政区划代码')  # 行政区划代码
    province = models.CharField(max_length=30, verbose_name='省份')  # 行政区划——省份
    city = models.CharField(max_length=50, verbose_name='城市')  # 行政区划——城市
    county = models.CharField(max_length=50, verbose_name='区县', null=True, blank=True)  # 行政区划——区县
    level = models.IntegerField(verbose_name='检察院级别')  # 检察院级别(eg. 4)

    class Meta:
        verbose_name = '检察院'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Party(models.Model):
    """
    当事人模型
    """
    name = models.CharField(max_length=100, verbose_name='当事人名称')  # 当事人名称
    name_is_fuzzy = models.BooleanField(verbose_name='当事人名称是否模糊')  # 当事人名称是否模糊(可能是化名)
    h_type = models.CharField(max_length=10, verbose_name='当事人类型')  # 当事人类型(eg. 个人、法人、其他)
    nationality = models.CharField(max_length=10, verbose_name='国籍', blank=True)  # 国籍
    nation = models.CharField(max_length=10, verbose_name='民族', blank=True)  # 民族
    gender = models.CharField(max_length=10, verbose_name='性别', blank=True)  # 性别
    birthday = models.DateField(verbose_name='出生日期', blank=True, null=True)  # 出生日期

    class Meta:
        verbose_name = '当事人'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class Agent(models.Model):
    """
    代理人模型
    """
    name = models.CharField(max_length=100, verbose_name='代理人名称')  # 代理人名称
    h_type = models.CharField(max_length=10, verbose_name='代理人类型')  # 代理人类型(eg. 个人、法人、其他)
    profession = models.CharField(max_length=30, verbose_name='代理人辩护人职业类型', blank=True)  # 职业(eg. 职业律师、非法务人员)
    a_type = models.CharField(max_length=20, verbose_name='辩护人或诉讼代理人类型', blank=True)  # 代理类型(eg. 律师、亲友)

    # 被代理人
    parties = models.ManyToManyField(Party, verbose_name='被代理人', db_index=True)  # 被代理人

    class Meta:
        verbose_name = '代理人'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name


class LawReference(models.Model):
    """
    法条引用模型
    """
    law_name = models.CharField(max_length=100, verbose_name="法律名称")  # 法律名称
    law_clause = models.CharField(max_length=30, verbose_name="条", null=True, blank=True)  # 条
    law_clause_item = models.CharField(max_length=30, verbose_name="款", null=True, blank=True)  # 款
    law_item = models.CharField(max_length=30, verbose_name="项", null=True, blank=True)  # 项

    class Meta:
        verbose_name = '法条引用'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['law_name']),
            models.Index(fields=['law_name', 'law_clause']),
            models.Index(fields=['law_name', 'law_clause', 'law_clause_item']),
            models.Index(fields=['law_name', 'law_clause', 'law_clause_item', 'law_item']),
        ]

    def __str__(self):
        return self.law_name


class Judge(models.Model):
    """
    法官模型
    """
    name = models.CharField(max_length=50, verbose_name='法官名称')  # 法官名称
    full_name = models.CharField(max_length=100, verbose_name='法官全称')  # 法官全称

    class Meta:
        verbose_name = '法官'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return self.name


class Document(models.Model):
    """
    文书基类
    """
    WSZZDW = (
        ('1', '法院'),
        ('2', '检察院'),
        ('3', '司法行政'),
    )

    # 文书基本信息
    address = models.CharField(max_length=100, verbose_name='地址')  # 地址
    agency = models.CharField(max_length=20, choices=WSZZDW, verbose_name='文书制作单位')  # 文书制作单位
    doc_name = models.CharField(max_length=30, verbose_name='文书名称', blank=True)  # 文书名称
    doc_type = models.CharField(max_length=30, verbose_name='文书种类', blank=True)  # 文书种类
    full_text = models.TextField(verbose_name='全文')  # 全文

    class Meta:
        verbose_name = '文书'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['address']),
            models.Index(fields=['agency']),
            models.Index(fields=['doc_name']),
            models.Index(fields=['doc_type']),
        ]

    def __str__(self):
        return self.doc_type


class Judgment(Document):
    """
    法院文书模型（裁判文书+决定书）
    """
    # 文书基本信息
    case_number = models.CharField(max_length=100, verbose_name='案号')  # 案号
    case_type = models.CharField(max_length=30, verbose_name='案件类别')  # 案件类别
    # 裁判日期
    judgment_date = models.DateField(verbose_name='裁判日期', blank=True, null=True)  # 裁判日期

    # 法院信息
    court = models.ForeignKey(Court, on_delete=models.CASCADE, verbose_name='法院')  # 法院

    # 当事人信息
    plaintiff = models.ManyToManyField(Party, related_name='plaintiff', verbose_name='原告', db_index=True)  # 原告
    defendant = models.ManyToManyField(Party, related_name='defendant', verbose_name='被告', db_index=True)  # 被告

    # 代理人信息
    agent = models.ManyToManyField(Agent, related_name='plaintiff_agent', verbose_name='代理人',
                                   blank=True, db_index=True)  # 代理人

    # 法条引用
    law_reference = models.ManyToManyField(LawReference, verbose_name='法条引用', db_index=True)  # 法条引用

    # 审判组织信息
    judge = models.ManyToManyField(Judge, verbose_name='法官', db_index=True)  # 法官

    class Meta:
        verbose_name = '判决书'
        verbose_name_plural = verbose_name
        indexes = [
            # 'case_number', 'case_type', 'judgment_date'
            models.Index(fields=['case_number']),
            models.Index(fields=['case_type']),
            models.Index(fields=['judgment_date']),
        ]

    def __str__(self):
        return self.doc_title


class Prosecution(Document):
    """
    检察院文书模型
    """
    # 文书基本信息
    case_number = models.CharField(max_length=100, verbose_name='案号')  # 案号
    case_type = models.CharField(max_length=30, verbose_name='案件类别')  # 案件类别

    # 诉至法院
    court = models.CharField(max_length=100, verbose_name='诉至法院')  # 诉至法院

    # (不)起诉日期
    p_date = models.DateField(verbose_name='(不)起诉日期', blank=True, null=True)  # (不)起诉日期

    # 检察院信息
    procuratorate = models.ForeignKey(Procuratorate, on_delete=models.CASCADE, verbose_name='检察院')  # 检察院

    # 被告人信息
    defendant = models.ManyToManyField(Party, related_name='prosecution_defendant', verbose_name='被告', db_index=True)  # 被告

    class Meta:
        verbose_name = '检察院文书'
        verbose_name_plural = verbose_name
        indexes = [
            # 'case_number', 'case_type', 'p_date'
            models.Index(fields=['case_number']),
            models.Index(fields=['case_type']),
            models.Index(fields=['p_date']),
        ]

    def __str__(self):
        return self.doc_title

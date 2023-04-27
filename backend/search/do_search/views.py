"""
联合查询: 通过关键词查询 + 通过倒排索引查询
"""
import json
import jieba
from django.http import JsonResponse
from common.models import *
from indexes.models import *
from indexes.views import search_by_index
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE


def search_by_keywords(words):
    """
    直接通过关键词查询，这里都是严格匹配
    """
    # 法院信息搜索
    courts = Court.objects.filter(name__in=words)
    # 检察院信息搜索
    procuratorates = Procuratorate.objects.filter(name__in=words)
    # 当事人信息搜索
    parties = Party.objects.filter(name__in=words)
    # 代理人信息搜索
    agents = Agent.objects.filter(name__in=words)
    # 审判人员信息搜索
    judges = Judge.objects.filter(name__in=words)

    return {
        'courts': courts,
        'procuratorates': procuratorates,
        'parties': parties,
        'agents': agents,
        'judges': judges
    }


def union_search(query):
    """
    联合查询，query为查询字符串
    """
    # 分词
    words = jieba.cut_for_search(query)
    # 去除停用词
    stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
        stop_words += f.read().splitlines()
    words = [word for word in words if word not in stop_words]

    # 关键词查询
    keywords_result = search_by_keywords(words)

    # 全文检索
    full_text_result = search_by_index(words)

    return {
        'keywords_result': keywords_result,
        'full_text_result': full_text_result
    }


def similar_search(query):
    """
    todo:相似查询，query为查询字符串
    """
    pass


def search(request):
    """
    搜索接口
    """
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
    # 联合查询
    result = union_search(query)
    # # 相似查询
    # similar_search(query)
    return JsonResponse({'code': 200,
                         'msg': 'ok',
                         'data': result})

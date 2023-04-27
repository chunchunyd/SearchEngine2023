import logging
from django.http import JsonResponse
from common.models import Document, Party, Agent, Judge
from indexes.models import Term, Posting
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE
import jieba
import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *


class TermViewSet(ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


class PostingViewSet(ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = DEFAULT_PAGE_SIZE


def build_inverted_index():
    """
    建立倒排索引
    """
    print('开始建立倒排索引')
    # 测试发现, jieba分词对人名支持很差，所以这里从数据库手动添加人名dict
    # 获取所有人名，构建人名dict
    parties = Party.objects.all()
    for party in parties:
        jieba.add_word(party.name)
    agents = Agent.objects.all()
    for agent in agents:
        jieba.add_word(agent.name)
    judges = Judge.objects.all()
    for judge in judges:
        jieba.add_word(judge.name)
    print('人名dict构建完成')

    # 获取停用词
    # 先获取符号词
    stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
    # stop_words.txt文件中，可以不断添加新的停用词
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
        stop_words += f.read().splitlines()
    print('停用词获取完成')

    # 获取所有文档
    print('开始遍历文档')
    documents = Document.objects.all()
    cnt = 0
    # 遍历文档
    for document in documents:
        cnt += 1
        print(f'\r正在处理第{cnt}/{len(documents)}个文档', end='')
        # 获取文档内容
        content = document.full_text
        # 用jieba分词
        words = jieba.cut_for_search(content)
        # 去除停用词
        words = [word for word in words if word not in stop_words]
        # 遍历分词结果
        visited_words = set()  # 用于记录已经访问过的词条
        for word in words:
            term = Term.objects.get_or_create(term=word, defaults={'document_count': 0})[0]
            # 如果本文档中第一次访问到该词条，则文档数+1
            if word not in visited_words:
                term.document_count += 1
                visited_words.add(word)
            term.save()
            # 建立倒排索引
            posting = Posting.objects.get_or_create(term=term,
                                                    doc_id=document,
                                                    defaults={'frequency': 0, 'position': 0})[0]
            posting.frequency += 1
            posting.position = content.find(word)
            posting.save()
    print('\n倒排索引建立完成')


def search_by_index(query):
    """
    根据query在倒排索引中搜索, 返回文档id集合
    这里的query是用户输入的搜索内容分词后的结果，以一个list的形式传入，具体操作在search APP中完成
    """
    # 获取query中的所有词条
    terms = Term.objects.filter(term__in=query)
    # 获取每个词条的倒排索引
    postings = Posting.objects.filter(term__in=terms)
    # 获取每个词条的倒排索引所对应的文档id和出现位置
    results = {}
    for posting in postings:
        if posting.doc_id.id not in results:
            results[posting.doc_id.id] = []
        results[posting.doc_id.id].append(posting.position)
    # 返回结果
    return results


def build_index(request):
    """
    建立倒排索引
    """
    build_inverted_index()
    return JsonResponse({'msg': '倒排索引建立完成'})


def test_search(request):
    """
    测试搜索功能
    """
    query = request.GET.get('query')
    query = [query]
    doc_ids = search_by_index(query)
    documents = Document.objects.filter(id__in=doc_ids)
    result = []
    for document in documents:
        result.append({
            'address': document.address,
        })

    # todo:把result缓存到redis中
    # redis.set('search_result', result)
    # redis.expire('search_result', 60)  # 设置过期时间为60s

    # 分页
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    total = len(result)
    result = result[(page - 1) * DEFAULT_PAGE_SIZE: page * DEFAULT_PAGE_SIZE]
    return JsonResponse({'msg': '搜索成功', 'result': result, 'total': total})

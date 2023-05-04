import logging
from django.http import JsonResponse
from django.db import transaction
from common.models import LawDocument, Party, Agent, Judge
from indexes.models import Term, Posting
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE
import jieba
import json
import time
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *


#
# class TermViewSet(ModelViewSet):
#     queryset = Term.objects.all()
#     serializer_class = TermSerializer
#     pagination_class = LimitOffsetPagination
#     pagination_class.default_limit = DEFAULT_PAGE_SIZE
#
#
# class PostingViewSet(ModelViewSet):
#     queryset = Posting.objects.all()
#     serializer_class = PostingSerializer
#     pagination_class = LimitOffsetPagination
#     pagination_class.default_limit = DEFAULT_PAGE_SIZE
#
# 实际上应该用drf-me的ModelViewSet，但是非常麻烦，所以不用viewset了


@transaction.atomic
def handle_document(document, stop_words):
    # 获取文档内容
    content = document.full_text
    # 用jieba分词
    words = jieba.tokenize(content, mode='search')
    # 去除停用词
    words = [word for word in words if word[0] not in stop_words]
    # 遍历分词结果
    visited_words = set()  # 用于记录已经访问过的词条
    for word in words:
        # 存入mongoDB

        # 词条不存在则创建
        term = Term.objects().filter(term=word[0]).first()
        if term is None:
            term = Term.objects.create(term=word[0], document_count=0)
        # 如果是第一次访问该词条, 则文档数+1
        if word not in visited_words:
            term.document_count += 1
            # 将词条加入已访问集合
            visited_words.add(word)
        # 保存词条
        term.save()

        # 建立倒排索引
        posting = Posting.objects().filter(term=word[0], doc_id=document.id).first()
        if posting is None:
            posting = Posting.objects.create(term=word[0], doc_id=document.id, position=[])
        # posting.frequency += 1
        posting.position.append(word[1])
        posting.save()


def build_inverted_index():
    """
    建立倒排索引
    """
    stop_watch = time.time()
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

    now = time.time()
    print(f'初始化用时{now - stop_watch:.2f}s')
    stop_watch = now

    # 获取所有文档
    print('开始遍历文档')
    documents = LawDocument.objects.all()
    start_doc_id = 1
    cnt = 0
    total_time = 0
    start_time = stop_watch
    # 遍历文档
    for document in documents:
        cnt += 1
        print(f'\r正在处理第{cnt}/{len(documents)}个文档', end=' ')

        # 如果文档id小于start_doc_id，说明已经处理过，跳过
        if document.id < start_doc_id:
            print(f'文档{cnt}已处理过')
            continue

        handle_document(document, stop_words)

        now = time.time()
        print(
            f'文档{cnt}用时{now - stop_watch:.2f}s, 总用时{now - start_time:.2f}s, 平均用时{(now - start_time) / cnt:.2f}s')
        stop_watch = now

    print('\n倒排索引建立完成')


def search_by_index(query):
    """
    根据query在倒排索引中搜索, 返回文档id集合
    这里的query是用户输入的搜索内容分词后的结果，以一个list的形式传入，具体操作在search APP中完成
    """
    # 获取query中的所有词条
    terms = Term.objects.filter(term__in=query)
    # 获取每个词条的倒排索引
    postings = Posting.objects.filter(term__in=query)
    # 获取每个词条的倒排索引所对应的文档id和出现位置

    sons = [pst.to_mongo() for pst in postings]
    # print(sons)
    # [SON([('_id', ObjectId('6453ce69c32402d481968f81')), ('term', '浙江'), ('doc_id', 1), ('position', [0, 1065])]),
    # SON([('_id', ObjectId('6453ce79c32402d48196a0bc')), ('term', '浙江'), ('doc_id', 8), ('position', [0, 98, 2108])])
    # ,...]

    results = {}
    for son in sons:
        posting = son.to_dict()
        # {'_id': ObjectId('6453ce69c32402d481968f81'), 'term': '浙江', 'doc_id': 1, 'position': [0, 1065]}
        # {'_id': ObjectId('6453ce79c32402d48196a0bc'), 'term': '浙江', 'doc_id': 8, 'position': [0, 98, 2108]}

        if posting['doc_id'] not in results:
            document = LawDocument.objects.filter(id=posting['doc_id']).first()
            results[posting['doc_id']] = {"address": document.address, "terms": {}}
        results[posting["doc_id"]]["terms"][posting["term"]] = posting["position"]
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
    query1 = request.GET.get('query1')
    query2 = request.GET.get('query2')
    query = [query1, query2]
    result = search_by_index(query)
    # result = []
    # for document in documents:
    #     result.append({
    #         'address': document.address,
    #     })

    # todo:把result缓存到redis中
    # redis.set('search_result', result)
    # redis.expire('search_result', 60)  # 设置过期时间为60s

    # 分页
    result = list(result.items())       # 为了分页，把dict转换成list
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    total = len(result)
    result = result[(page - 1) * DEFAULT_PAGE_SIZE: page * DEFAULT_PAGE_SIZE]
    return JsonResponse({'msg': '搜索成功', 'result': result, 'total': total})

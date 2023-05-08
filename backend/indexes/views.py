import logging
from django.http import JsonResponse
from django.db import transaction
from common.models import LawDocument, Party, Agent, Judge, Court, Procuratorate
from indexes.models import Term, Posting
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE, BASE_DIR
import jieba
import json
import time
import pymongo
import os
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *


@transaction.atomic
def handle_document(document, stop_words, posting):
    # 获取文档内容
    content = document.full_text
    # 用jieba分词
    words = jieba.tokenize(content, mode='search')
    # 去除停用词
    words = [word for word in words if word[0] not in stop_words]
    # # 遍历分词结果
    # visited_words = set()  # 用于记录已经访问过的词条

    # 预处理词条
    word_list = {}
    for word in words:
        if word[0] not in word_list:
            word_list[word[0]] = []
        word_list[word[0]].append(word[1])

    posting_list = []

    for word, pos in word_list.items():
        # 存入mongoDB
        posting_list.append({
            'term': word,
            'doc_id': document.id,
            'pos': pos
        })

    posting.insert_many(posting_list)


def build_inverted_index():
    """
    建立倒排索引
    """
    # 连接mongoDB
    client = pymongo.MongoClient('localhost', 27017)
    db = client['test_pymongo']
    posting = db['posting']
    # 设置posting的词条、index
    posting.create_index([('term', pymongo.ASCENDING)])
    posting.create_index([('doc_id', pymongo.ASCENDING)])

    stop_watch = time.time()
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

    build_setting = json.load(open(os.path.join(BASE_DIR, 'indexes', 'build_setting.json'), 'r', encoding='utf-8'))
    start_doc_id = build_setting['start_doc_id']
    # start_doc_id = 1

    cnt = 0
    start_time = stop_watch
    # 遍历文档, 建立Posting
    print('开始建立Posting')
    for document in documents:
        cnt += 1
        print(f'\r正在处理第{cnt}/{len(documents)}个文档', end=' ')

        # 如果文档id小于start_doc_id，说明已经处理过，跳过
        if document.id < start_doc_id:
            print(f'文档{cnt}已处理过')
            continue

        # 如果文档id等于start_doc_id，说明是上次中断的文档，需要删除posting中的相关记录
        if document.id == start_doc_id:
            print(f'文档{cnt}是上次中断的文档，需要删除posting中的相关记录')
            posting.delete_many({'doc_id': document.id})

        handle_document(document, stop_words, posting)
        build_setting['start_doc_id'] = cnt + 1
        json.dump(build_setting, open(os.path.join(BASE_DIR, 'indexes', 'build_setting.json'), 'w', encoding='utf-8'))

        now = time.time()
        print(
            f'文档{cnt}用时{now - stop_watch:.2f}s, 总用时{now - start_time:.2f}s, 平均用时{(now - start_time) / (cnt - start_doc_id + 1):.2f}s')
        stop_watch = now

    print('\n倒排索引建立完成')


def build_terms():
    """
    根据posting表建立terms表
    """
    # 连接mongoDB
    client = pymongo.MongoClient('localhost', 27017)
    db = client['search_engine']
    posting = db['posting']
    pipeline = [
        {
            '$group': {
                '_id': '$term',
                'document_count': {'$sum': 1}
            }
        }
    ]
    # 获取term的document_count
    results = posting.aggregate(pipeline)
    # 存入term表
    term = db['term']
    cnt = 0
    for result in results:
        cnt += 1
        print(f'\r正在处理第{cnt}个term', end=' ')
        term.insert_one({
            'term': result['_id'],
            'document_count': result['document_count']
        })


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
    return {
        'doc_count': len(results),
        'doc_list': results
    }


# 对外提供的接口
def build_index(request):
    """
    建立倒排索引
    """
    build_inverted_index()
    return JsonResponse({'msg': '倒排索引建立完成'})


def build_term(request):
    """
    建立词条
    """
    build_terms()
    return JsonResponse({'msg': '词条列表建立完成'})


def build_user_dict(request):
    """
    用户词典
    """
    user_dict = set()
    parties = Party.objects.all()
    for party in parties:
        user_dict.add(party.name)
    agents = Agent.objects.all()
    for agent in agents:
        user_dict.add(agent.name)
    judges = Judge.objects.all()
    for judge in judges:
        user_dict.add(judge.name)
    # 法院检察院名称也添加一下
    courts = Court.objects.all()
    for court in courts:
        user_dict.add(court.name)
    procuratorates = Procuratorate.objects.all()
    for procuratorate in procuratorates:
        user_dict.add(procuratorate.name)
    with open(os.path.join(BASE_DIR, 'resources', 'user_dict.txt'), 'w', encoding='utf-8') as f:
        for word in user_dict:
            f.write(word + '\n')
    return JsonResponse({'user_dict': user_dict})


def load_user_dict(request):
    """
    加载用户词典
    """
    jieba.load_userdict(os.path.join(BASE_DIR, 'resources', 'user_dict.txt'))
    return JsonResponse({'msg': '用户词典加载完成'})


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
    result = list(result.items())  # 为了分页，把dict转换成list
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    total = len(result)
    result = result[(page - 1) * DEFAULT_PAGE_SIZE: page * DEFAULT_PAGE_SIZE]
    return JsonResponse({'msg': '搜索成功', 'result': result, 'total': total})

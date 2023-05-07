import logging
from django.http import JsonResponse
from django.db import transaction
from common.models import LawDocument, Party, Agent, Judge
from indexes.models import Term, Posting
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE, BASE_DIR
import jieba
import json
import time
import os
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
        posting_list.append(Posting(term=word, doc_id=document.id, position=pos))

    Posting.objects.insert(posting_list, load_bulk=False)


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

    # build_setting = json.load(open(os.path.join(BASE_DIR,'indexes','build_setting.json'), 'r', encoding='utf-8'))
    # start_doc_id = build_setting['start_doc_id']
    start_doc_id = 1

    cnt = 0
    total_time = 0
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

        handle_document(document, stop_words)
        # build_setting['start_doc_id'] = cnt + 1
        # json.dump(build_setting, open(os.path.join(BASE_DIR,'indexes','build_setting.json'), 'w', encoding='utf-8'))

        now = time.time()
        print(
            f'文档{cnt}用时{now - stop_watch:.2f}s, 总用时{now - start_time:.2f}s, 平均用时{(now - start_time) / (cnt - start_doc_id + 1):.2f}s')
        stop_watch = now

    print('\n倒排索引建立完成')


def build_terms():
    """
    根据posting表建立terms表,
    TODO: 使用MongoDB的MapReduce来统计term出现次数 或 使用MongoDB的聚合管道来统计
    TODO: 对本文件做优化，取消掉ORM的部分，直接用pymongo操作mongoDB
    """
    cnt = 0
    # term_doc_cnt = {}
    # 遍历posting表
    for posting in Posting.objects.all():
        cnt += 1
        print(f'\r正在处理第{cnt}个posting', end=' ')
        # if posting.term not in term_doc_cnt:
        #     term_doc_cnt[posting.term] = 0
        # term_doc_cnt[posting.term] += 1

    # 存入terms表
    # term_list = []
    # for term, doc_cnt in term_doc_cnt.items():
    #     term_list.append(Term(term=term, document_count=doc_cnt))
    #
    # Term.objects.insert(term_list, load_bulk=False)
    # print(f'共{cnt}个posting')

    # 输出Posting表中的term数量
    # print(f'共{len(Posting.objects.all())}个posting')


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

# 优化前：
# 正在处理第268/19879个文档 获取词条用时5.50s, 保存词条用时4.23s, 获取倒排索引用时7.68s, 保存倒排索引用时5.08s
# 文档268用时24.18s, 总用时24.18s, 平均用时24.18s
# 正在处理第269/19879个文档 获取词条用时1.08s, 保存词条用时0.85s, 获取倒排索引用时1.73s, 保存倒排索引用时0.93s
# 文档269用时4.65s, 总用时28.83s, 平均用时14.41s
# 正在处理第270/19879个文档 获取词条用时1.15s, 保存词条用时0.90s, 获取倒排索引用时1.87s, 保存倒排索引用时1.03s
# 文档270用时5.01s, 总用时33.84s, 平均用时11.28s
# 正在处理第271/19879个文档 获取词条用时3.64s, 保存词条用时2.84s, 获取倒排索引用时5.24s, 保存倒排索引用时3.23s
# 文档271用时15.10s, 总用时48.94s, 平均用时12.23s
# 正在处理第272/19879个文档 获取词条用时2.69s, 保存词条用时2.13s, 获取倒排索引用时4.12s, 保存倒排索引用时2.58s
# 文档272用时11.64s, 总用时60.58s, 平均用时12.12s
# 正在处理第273/19879个文档 获取词条用时5.01s, 保存词条用时3.86s, 获取倒排索引用时7.25s, 保存倒排索引用时4.54s
# 文档273用时20.90s, 总用时81.47s, 平均用时13.58s
# 正在处理第274/19879个文档 获取词条用时6.77s, 保存词条用时5.27s, 获取倒排索引用时9.60s, 保存倒排索引用时6.33s
# 文档274用时28.28s, 总用时109.75s, 平均用时15.68s
# 正在处理第275/19879个文档 获取词条用时3.91s, 保存词条用时3.05s, 获取倒排索引用时5.82s, 保存倒排索引用时3.73s
# 文档275用时16.67s, 总用时126.42s, 平均用时15.80s
# 正在处理第276/19879个文档 获取词条用时0.42s, 保存词条用时0.34s, 获取倒排索引用时0.78s, 保存倒排索引用时0.37s
# 文档276用时1.93s, 总用时128.35s, 平均用时14.26s
# 正在处理第277/19879个文档 获取词条用时1.65s, 保存词条用时1.26s, 获取倒排索引用时2.63s, 保存倒排索引用时1.48s
# 文档277用时7.09s, 总用时135.44s, 平均用时13.54s

# 思路：
# 1. 先将words整理成一个字典，key是词条，value是词条的位置信息；然后遍历这个字典，而不是遍历原来的words
# 2. 这样的话，在插入term时，每个词条只需要查询一次，而不是出现一次查询一次；
#              在插入posting时，每个词条不需要查询，直接插入即可


# 优化后：
# 正在处理第334/19879个文档 获取词条用时0.55s, 保存词条用时0.43s, 获取倒排索引用时0.00s, 保存倒排索引用时0.39s
# 文档334用时1.50s, 总用时38.76s, 平均用时1.17s
# 正在处理第335/19879个文档 获取词条用时0.72s, 保存词条用时0.58s, 获取倒排索引用时0.00s, 保存倒排索引用时0.55s
# 文档335用时2.03s, 总用时40.79s, 平均用时1.20s
# 正在处理第336/19879个文档 获取词条用时0.42s, 保存词条用时0.33s, 获取倒排索引用时0.00s, 保存倒排索引用时0.26s
# 文档336用时1.10s, 总用时41.88s, 平均用时1.20s
# 正在处理第337/19879个文档 获取词条用时0.23s, 保存词条用时0.16s, 获取倒排索引用时0.00s, 保存倒排索引用时0.18s
# 文档337用时0.60s, 总用时42.48s, 平均用时1.18s
# 正在处理第338/19879个文档 获取词条用时0.83s, 保存词条用时0.65s, 获取倒排索引用时0.00s, 保存倒排索引用时0.62s
# 文档338用时2.40s, 总用时44.89s, 平均用时1.21s
# 正在处理第339/19879个文档 获取词条用时0.23s, 保存词条用时0.17s, 获取倒排索引用时0.00s, 保存倒排索引用时0.16s
# 文档339用时0.58s, 总用时45.47s, 平均用时1.20s
# 正在处理第340/19879个文档 获取词条用时0.56s, 保存词条用时0.45s, 获取倒排索引用时0.00s, 保存倒排索引用时0.38s
# 文档340用时1.51s, 总用时46.98s, 平均用时1.20s
# 正在处理第341/19879个文档 获取词条用时0.65s, 保存词条用时0.55s, 获取倒排索引用时0.00s, 保存倒排索引用时0.52s
# 文档341用时1.87s, 总用时48.85s, 平均用时1.22s
# 正在处理第342/19879个文档 获取词条用时0.52s, 保存词条用时0.41s, 获取倒排索引用时0.00s, 保存倒排索引用时0.36s
# 文档342用时1.39s, 总用时50.25s, 平均用时1.23s
# 正在处理第343/19879个文档 获取词条用时0.26s, 保存词条用时0.20s, 获取倒排索引用时0.00s, 保存倒排索引用时0.17s
# 文档343用时0.65s, 总用时50.90s, 平均用时1.21s
# 正在处理第344/19879个文档 获取词条用时0.55s, 保存词条用时0.40s, 获取倒排索引用时0.00s, 保存倒排索引用时0.40s
# 文档344用时1.44s, 总用时52.34s, 平均用时1.22s
# 正在处理第345/19879个文档 获取词条用时0.38s, 保存词条用时0.28s, 获取倒排索引用时0.00s, 保存倒排索引用时0.25s
# 文档345用时0.96s, 总用时53.30s, 平均用时1.21s


# 优化2：遍历字典时，将posting和new_term先保存在一个list，结束后再批量插入

# 正在处理第22/68382个文档 获取词条用时0.61s, 保存词条用时0.35s, 获取倒排索引用时0.00s, 保存倒排索引用时0.08s 文档22用时1.19s, 总用时22.65s, 平均用时1.03s
# 正在处理第23/68382个文档 获取词条用时0.84s, 保存词条用时0.46s, 获取倒排索引用时0.00s, 保存倒排索引用时0.11s 文档23用时1.58s, 总用时24.23s, 平均用时1.05s
# 正在处理第24/68382个文档 获取词条用时0.46s, 保存词条用时0.29s, 获取倒排索引用时0.00s, 保存倒排索引用时0.05s 文档24用时0.87s, 总用时25.10s, 平均用时1.05s
# 正在处理第25/68382个文档 获取词条用时0.66s, 保存词条用时0.41s, 获取倒排索引用时0.00s, 保存倒排索引用时0.08s 文档25用时1.28s, 总用时26.38s, 平均用时1.06s
# 正在处理第26/68382个文档 获取词条用时0.23s, 保存词条用时0.14s, 获取倒排索引用时0.00s, 保存倒排索引用时0.03s 文档26用时0.43s, 总用时26.81s, 平均用时1.03s
# 正在处理第27/68382个文档 获取词条用时0.37s, 保存词条用时0.26s, 获取倒排索引用时0.00s, 保存倒排索引用时0.04s 文档27用时0.72s, 总用时27.53s, 平均用时1.02s
# 正在处理第28/68382个文档 获取词条用时0.70s, 保存词条用时0.37s, 获取倒排索引用时0.00s, 保存倒排索引用时0.09s 文档28用时1.29s, 总用时28.82s, 平均用时1.03s
# 正在处理第29/68382个文档 获取词条用时0.21s, 保存词条用时0.14s, 获取倒排索引用时0.00s, 保存倒排索引用时0.02s 文档29用时0.40s, 总用时29.22s, 平均用时1.01s
# 正在处理第30/68382个文档 获取词条用时1.40s, 保存词条用时0.62s, 获取倒排索引用时0.00s, 保存倒排索引用时0.16s 文档30用时2.48s, 总用时31.69s, 平均用时1.06s
# 正在处理第31/68382个文档 获取词条用时0.39s, 保存词条用时0.25s, 获取倒排索引用时0.00s, 保存倒排索引用时0.05s 文档31用时0.74s, 总用时32.43s, 平均用时1.05s
# 正在处理第32/68382个文档 获取词条用时0.86s, 保存词条用时0.51s, 获取倒排索引用时0.00s, 保存倒排索引用时0.10s 文档32用时1.68s, 总用时34.11s, 平均用时1.07s
# 正在处理第33/68382个文档 获取词条用时0.26s, 保存词条用时0.18s, 获取倒排索引用时0.00s, 保存倒排索引用时0.03s 文档33用时0.49s, 总用时34.60s, 平均用时1.05s
# 正在处理第34/68382个文档 获取词条用时0.30s, 保存词条用时0.19s, 获取倒排索引用时0.00s, 保存倒排索引用时0.04s 文档34用时0.58s, 总用时35.18s, 平均用时1.03s
# 正在处理第35/68382个文档 获取词条用时0.22s, 保存词条用时0.12s, 获取倒排索引用时0.00s, 保存倒排索引用时0.02s 文档35用时0.39s, 总用时35.57s, 平均用时1.02s
# 正在处理第36/68382个文档 获取词条用时0.27s, 保存词条用时0.18s, 获取倒排索引用时0.00s, 保存倒排索引用时0.03s 文档36用时0.52s, 总用时36.09s, 平均用时1.00s
# 正在处理第37/68382个文档 获取词条用时0.75s, 保存词条用时0.44s, 获取倒排索引用时0.00s, 保存倒排索引用时0.10s 文档37用时1.41s, 总用时37.50s, 平均用时1.01s
# 正在处理第38/68382个文档 获取词条用时0.43s, 保存词条用时0.27s, 获取倒排索引用时0.00s, 保存倒排索引用时0.05s 文档38用时0.80s, 总用时38.31s, 平均用时1.01s


# 优化3：先不处理term, 只处理倒排索引posting。posting做完后，统一一次写入term

"""
联合查询: 通过关键词查询 + 通过倒排索引查询
"""
import json
import jieba
import time
import redis
import re
import pymongo
from django.http import JsonResponse
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE, BASE_DIR, MONGO_DB
from common.serializers import *
from analysis.views import bm25_sort


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
        'courts': CourtSerializer(courts, many=True).data,
        'procuratorates': ProcuratorateSerializer(procuratorates, many=True).data,
        'parties': PartySerializer(parties, many=True).data,
        'agents': AgentSerializer(agents, many=True).data,
        'judges': JudgeSerializer(judges, many=True).data
    }


def construct_page(page, page_size, doc_list, word_list):
    """
    构造分页结果
    """
    # print(f'word_list: {word_list}')
    # 计算总页数
    total_page = len(doc_list) // page_size + 1
    # 计算当前页的文档起始位置
    start = (page - 1) * page_size
    # 计算当前页的文档结束位置
    end = min(page * page_size, len(doc_list))
    # 构造当前页的文档id列表
    doc_list = doc_list[start:end]
    # 获取当前页的文档内容
    doc_list = LawDocument.objects.filter(id__in=doc_list)
    # 构建结果
    result = {}
    Posting = MONGO_DB['posting']
    # 获取当前页的文档的摘要
    for doc in doc_list:
        # 获取文档的倒排索引
        for word in word_list:
            posting = list(Posting.find({'doc_id': doc.id, 'term': word}))
            if posting:
                if posting[0]['position'][0] - 20 < 0:
                    start = 0
                else:
                    start = posting[0]['position'][0] - 20
                if posting[0]['position'][0] + 280 > posting[0]['doc_len']:
                    end = posting[0]['doc_len']
                else:
                    end = posting[0]['position'][0] + 280

                # 找到第一个以"号"字结尾的位置
                title_end_1 = re.search(r"号 ", doc.full_text).span()
                title_end_2 = re.search(r"案 ", doc.full_text).span()
                title_end = min(title_end_1[1], title_end_2[1])

                result[doc.id] = {
                    'id': doc.id,
                    'address': doc.address,
                    'title': doc.full_text[:title_end],
                    'short_text': doc.full_text[start:end],
                }
                break
    # 返回结果
    return {
        'total_page': total_page,
        'word_list': word_list,
        'doc_list': result
    }


def search_by_index(word_list):
    """
    根据query在倒排索引中搜索, 返回文档id集合
    这里的query是用户输入的搜索内容分词后的结果，以一个list的形式传入，具体操作在search APP中完成
    """
    # mongoDB连接
    Term = MONGO_DB['term']
    Posting = MONGO_DB['posting']

    # 获取query中的所有词条
    st_time = time.time()
    terms = Term.find({'term': {'$in': word_list}})
    # print(terms[0])
    print(f'获取词条用时{time.time() - st_time}s')

    # 获取每个词条的倒排索引
    st_time = time.time()
    postings = Posting.find({'term': {'$in': word_list}})
    # print(postings[0])
    # print(type(postings[0]['doc_id']))
    print(f'获取倒排索引用时{time.time() - st_time}s')

    results = set()

    # for pst in postings:
    #     if pst['doc_id'] not in results:
    #         doc = Law_Document.find_one({'doc_id': pst['doc_id']})
    #         results[pst['doc_id']] = {"address": doc['address'], "terms": {}}  # 这里的address是文档的地址
    #     results[pst["doc_id"]]["terms"][pst["term"]] = pst["position"]
    # print(f'序列化用时{time.time() - st_time}s')

    for pst in postings:
        results.add(pst['doc_id'])

    # 无排序
    # results = list(results)
    # BM25排序
    print(f'搜索结果数量{len(results)}, 开始排序')
    st_time = time.time()
    results = bm25_sort(list(results), word_list)
    print(f'BM25排序用时{time.time() - st_time}s')
    # 返回结果
    return results


def text_search(request):
    """
    全文搜索，query为查询字符串
    """
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
    page = int(request.GET.get('page', 1))  # 页码,默认为1
    Term = MONGO_DB['term']

    # 分词
    st_time = time.time()
    words = jieba.cut_for_search(query)
    # 去除停用词
    stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
        stop_words += f.read().splitlines()
    word_list = [word for word in words if word not in stop_words]
    print(f'分词用时:{time.time() - st_time}, 分词结果: {words}')

    # 筛选词条
    word_idfs = {}
    term_list = list(Term.find({'_id': {'$in': word_list}}))
    for term in term_list:
        word_idfs[term['_id']] = term['idf']
    print(f'全部查询词：{word_list}')
    print(f'全部词条：{[term["_id"] for term in term_list]}')
    # 按idfs降序排列, 删除idf<阈值的词条
    idf_threshold = 0
    word_list = sorted(word_list, key=lambda x: word_idfs[x], reverse=True)
    term_list = sorted(term_list, key=lambda x: word_idfs[x['_id']], reverse=True)
    word_list_for_sort = [word for word in word_list if word_idfs[word] > idf_threshold]
    word_list_for_sort = [term for term in term_list if term['idf'] > idf_threshold]
    print(f'参与排序的词条：{[term["_id"] for term in term_list]}')

    # 检查redis中是否有缓存
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    if redis_conn.exists(query):
        print('命中redis获取缓存')
        doc_list = json.loads(redis_conn.get(query))
    else:
        # 全文检索
        st_time = time.time()
        doc_list = search_by_index(word_list)
        print(f'全文检索用时:{time.time() - st_time}')
        # 存入redis缓存
        redis_conn.set(query, json.dumps(doc_list), ex=60 * 5)  # 5分钟过期

    # 分页构建结果返回
    st_time = time.time()
    result = construct_page(page, DEFAULT_PAGE_SIZE, doc_list, word_list)
    # print(full_text_result)

    return JsonResponse({
        'code': 200,
        'msg': 'ok',
        'result': result
    })


def key_search(request):
    """
    关键词搜索，query为查询字符串
    """
    query = request.GET.get('query')
    if not query:
        return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
    # 分词
    st_time = time.time()
    words = jieba.cut_for_search(query)
    # 去除停用词
    stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
    with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
        stop_words += f.read().splitlines()
    words = [word for word in words if word not in stop_words]

    print(f'分词用时:{time.time() - st_time}, 分词结果: {words}')

    # 关键词查询
    st_time = time.time()
    keywords_result = search_by_keywords(words)
    print(f'关键词查询用时:{time.time() - st_time}')
    # print(keywords_result)

    return JsonResponse({
        'code': 200,
        'msg': 'ok',
        'result': keywords_result,
    })


def similar_search(query):
    """
    todo:相似查询，query为查询字符串
    """
    pass


# def query_search(request):
#     """
#     搜索接口
#     """
#     query = request.GET.get('query')
#     if not query:
#         return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
#     # 联合查询
#     result = union_search(query)
#     # # 相似查询
#     # similar_search(query)
#     return JsonResponse({'code': 200,
#                          'msg': 'ok',
#                          'data': result})

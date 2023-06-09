"""
联合查询: 通过关键词查询 + 通过倒排索引查询
"""
import json
import os
import bs4
import jieba
import time
import redis
import re
import pymongo
from django.http import JsonResponse
from backend.settings import SIGN_WORDS_PATH, STOP_WORDS_PATH, DEFAULT_PAGE_SIZE, BASE_DIR, MONGO_DB, STATICFILES_DIRS, \
    USER_DICT_PATH
from common.models import *
from common.serializers import *
from analysis.views import bm25_sort
from crawlers.handlers import find_node

from search.query_parse.views import parse_query
from analysis.views import get_similar_docs


def search_by_keywords(words):
    """
    直接通过关键词查询，这里都是严格匹配
    """
    # 法院信息搜索
    courts = Court.objects.filter(name__in=words)
    # 检察院信息搜索
    procuratorates = Procuratorate.objects.filter(name__in=words)
    # # 当事人信息搜索
    # parties = Party.objects.filter(name__in=words)
    # # 代理人信息搜索
    # agents = Agent.objects.filter(name__in=words)
    # 审判人员信息搜索
    judges = list(JudgeSerializer(Judge.objects.filter(full_name__in=words), many=True).data)
    for judge in list(JudgeSerializer(Judge.objects.filter(name__in=words), many=True).data):
        if judge not in judges:
            judges.append(judge)

    return {
        'courts': CourtSerializer(courts, many=True).data,
        'procuratorates': ProcuratorateSerializer(procuratorates, many=True).data,
        # 'parties': PartySerializer(parties, many=True).data,
        # 'agents': AgentSerializer(agents, many=True).data,
        'judges': judges,
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
        result[doc.id] = {
            'id': doc.id,
            'address': doc.address,
        }

        # 找到第一个以"号"字结尾的位置
        title_end = re.search(r"号 ", doc.full_text)
        if title_end is not None:
            title_end = title_end.span()
        else:
            title_end = re.search(r"案 ", doc.full_text)
            if title_end is not None:
                title_end = title_end.span()
            else:
                title_end = (39, 40)
        result[doc.id]['title'] = doc.full_text[:title_end[1]]

        # 找到doc中第一个出现的词条，用于摘要
        start = 0
        end = 300
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
                break
        result[doc.id]['short_text'] = doc.full_text[start:end]

        # # 获取文档的类型，添加对应的信息
        # doc_type = doc.doc_type
        # if doc_type == '判决书' or doc_type == '裁定书' or doc_type == '调解书' or doc_type == '决定书':
        #     doc = Judgment.objects.get(id=doc.id)
        #     result[doc.id]['court_id'] = doc.court.id
        #     result[doc.id]['court_name'] = doc.court.name
        #     result[doc.id]['judges'] = []
        #     for judge in doc.judge.all():
        #         result[doc.id]['judges'].append({'judge_id': judge.id, 'judge_name': judge.name})
        #     result[doc.id]['law_refs'] = []
        #     for law in doc.law_reference.all():
        #         result[doc.id]['law_refs'].append({'law_id': law.id, 'law_detail': str(law)})
        # elif doc_type == '起诉书' or doc_type == '不起诉书':
        #     doc = Prosecution.objects.get(id=doc.id)
        #     result[doc.id]['procuratorate_id'] = doc.procuratorate.id
        #     result[doc.id]['procuratorate'] = doc.procuratorate.name
        #     result[doc.id]['to_court_id'] = doc.court.id
        #     result[doc.id]['to_court_name'] = doc.court.name

    # word_list按长度降序排列
    word_list.sort(key=lambda x: len(x), reverse=True)

    print(f'返回给前端的word_list: {word_list}')

    # 返回结果
    return {
        'total_page': total_page,
        'word_list': word_list,
        'doc_list': result
    }


def filter_result(doc_list, kwargs):
    """
    根据其他参数过滤结果
    """
    doc_list_filtered = set(doc_list)
    # 法院信息搜索
    if 'court_id' in kwargs and kwargs['court_id']:  # 如果有court_id参数且不为空
        print(f'court_id: {kwargs["court_id"][0]}')
        docs = Judgment.objects.filter(id__in=doc_list, court_id=kwargs['court_id'][0])
        docs = [doc.id for doc in docs]
        doc_list_filtered = doc_list_filtered.intersection(set(docs))
    if 'judge' in kwargs and kwargs['judge']:
        for judge_id in kwargs['judge']:
            print(f'judge_id: {judge_id}')
            docs = Judgment.objects.filter(id__in=doc_list, judge__id=judge_id)
            docs = [doc.id for doc in docs]
            doc_list_filtered = doc_list_filtered.intersection(set(docs))
    doc_list_filtered = sorted(list(doc_list_filtered), key=lambda x: doc_list.index(x))

    return doc_list_filtered


def text_search(request):
    """
    全文搜索，query为查询字符串
    """
    total_time = time.time()

    query = request.GET.get('query')
    if not query:
        return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
    page = int(request.GET.get('page', 1))  # 页码,默认为1
    # 把其他参数读入到kwargs中
    kwargs = {}
    for key, value in request.GET.items():
        if key != 'query' and key != 'page' and value:
            kwargs[key] = request.GET.getlist(key)
    print(f'query: {query}, page: {page}, kwargs: {kwargs}')

    # 检查redis中是否有缓存
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    if redis_conn.exists(query):
        print(f'redis获取缓存, 总用时:{time.time() - total_time}')
        doc_list, word_list, keywords_result = json.loads(redis_conn.get(query))
    else:
        print(f'redis无缓存, 总用时:{time.time() - total_time}')
        # 全文检索
        st_time = time.time()
        doc_ids, word_list, word_list_for_sort = parse_query(query)  # 返回: 文档id集合, 分词后的词条列表, 用于排序的词条列表
        print(f'全文检索用时:{time.time() - st_time}s')

        # 排序
        st_time = time.time()
        doc_list = bm25_sort(doc_ids, word_list_for_sort)
        print(f'排序用时:{time.time() - st_time}s')

        # 结构化信息
        user_word_list = []
        with open(USER_DICT_PATH, 'r', encoding='utf-8') as f:
            user_dict = json.load(f)
        for word in word_list:
            if word in user_dict:
                user_word_list.append(word)
        keywords_result = search_by_keywords(user_word_list)

        # 存入redis缓存
        redis_conn.set(query, json.dumps((doc_list, word_list, keywords_result)), ex=60 * 60 * 3)  # 3小时过期

    # 根据kwargs筛选搜索结果
    st_time = time.time()
    if len(kwargs) > 0:
        doc_list = filter_result(doc_list, kwargs)
    print(f'筛选用时:{time.time() - st_time}s')

    # 分页构建结果返回
    st_time = time.time()
    result = construct_page(page, DEFAULT_PAGE_SIZE, doc_list, word_list)
    print(f'构建返回页面用时:{time.time() - st_time}s')
    # print(full_text_result)
    print(f'总用时:{time.time() - total_time}s')

    return JsonResponse({
        'code': 200,
        'msg': 'ok',
        'result': result,
        'keywords_result': keywords_result
    })


# def key_search(request):
#     """
#     关键词搜索，query为查询字符串
#     """
#     query = request.GET.get('query')
#     if not query:
#         return JsonResponse({'code': 400, 'msg': 'query参数缺失'})
#     # 分词
#     st_time = time.time()
#     words = jieba.cut_for_search(query)
#     # 去除停用词
#     stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
#     with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
#         stop_words += f.read().splitlines()
#     words = [word for word in words if word not in stop_words]
#
#     print(f'分词用时:{time.time() - st_time}, 分词结果: {words}')
#
#     # 关键词查询
#     st_time = time.time()
#     keywords_result = search_by_keywords(words)
#     print(f'关键词查询用时:{time.time() - st_time}')
#     # print(keywords_result)
#
#     return JsonResponse({
#         'code': 200,
#         'msg': 'ok',
#         'result': keywords_result,
#     })


def similar_search(request):
    """
    上传一个xml文件，返回相似文档
    """
    st_time = time.time()
    stop_watch = st_time

    if request.method != 'POST':
        return JsonResponse({
            "status": "Error",
            "message": "请求方法错误"
        })
    xml_file = request.FILES.get('xml_file')
    if not xml_file:
        return JsonResponse({
            "status": "Error",
            "message": "上传的文件为空"
        })
    xml_file_name = xml_file.name
    xml_file_path = os.path.join(STATICFILES_DIRS[1], f'user_upload_{xml_file_name}_tmp')
    with open(xml_file_path, 'wb') as f:
        for chunk in xml_file.chunks():
            f.write(chunk)

    
    now = time.time()
    print(f'读文件{now - stop_watch:.2f}s')
    stop_watch = now

    try:
        # 解析xml文件, 获取全文
        with open(xml_file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            print(xml_file_path)
            if xml_file_path.endswith('.xml_tmp'):
                soup = bs4.BeautifulSoup(xml_content, features="xml")
                full_text = soup.find('QW').get('value')
                judges = soup.find_all('FGRYWZ')
                judge_list = [judge.get('value') for judge in judges]
            elif xml_file_path.endswith('.txt_tmp'):
                full_text = xml_content
        # 分词 + 去除停用词 + 筛选出user_dict中的词

        now = time.time()
        print(f'解析xml{now - stop_watch:.2f}s')
        stop_watch = now

        words = jieba.lcut(full_text)
        stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
        with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
            stop_words += f.read().splitlines()
        with open(USER_DICT_PATH, 'r', encoding='utf-8') as f:
            user_dict = json.load(f)
        word_list = []
        user_word_list = []

        now = time.time()
        print(f'分词{now - stop_watch:.2f}s')
        stop_watch = now

        for word in words:
            if word not in stop_words:
                word_list.append(word)
        user_word_list = word_list
        if len(judge_list) > 0:
            for judge in judge_list:
                user_word_list.append(judge)
        # print(f'user_word_list: {user_word_list}')
        # 关键词查询

        now = time.time()
        print(f'去停用词{now - stop_watch:.2f}s')
        stop_watch = now

        keywords_result = search_by_keywords(user_word_list)

        now = time.time()
        print(f'关键词查询{now - stop_watch:.2f}s')
        stop_watch = now

        # 对全文进行文本相似搜索
        similar_docs = get_similar_docs(word_list, 20)
        similar_result = construct_page(1, 30, similar_docs, [])
        # 删除文件
        os.remove(xml_file_path)

        return JsonResponse({
            "status": "Done",
            "result": {
                "keywords_result": keywords_result,
                "similar_result": similar_result,
            },
            "message": "上传成功",
        })
    except Exception as e:
        # 删除文件
        os.remove(xml_file_path)
        return JsonResponse({
            "status": "Error",
            "message": f"Invalid file: {str(e)}",
        })


def test_similar(request):
    user_dict = []
    with open(os.path.join(BASE_DIR, 'resources', 'user_dict.txt'), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            user_dict.append(line.strip())

    with open(os.path.join(BASE_DIR, 'resources', 'user_dict.json'), 'w', encoding='utf-8') as f:
        json.dump(user_dict, f, ensure_ascii=False)
    return JsonResponse("ok", safe=False)

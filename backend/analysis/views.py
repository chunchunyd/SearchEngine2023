import json
import os.path
from backend.settings import BASE_DIR, MONGO_DB

from django.http import JsonResponse
import pymongo
from math import log


# Create your views here.
# 为term预计算idf
def cal_idfs(request):
    """
    为term预计算idf
    """
    # 这部分用mongosh实现
    return JsonResponse({'status': 'success'})


# 计算BM25得分
def cal_bm25():
    # 使用BM25算法计算文档得分
    # 1.
    # 计算每个词条的idf值:
    # idf(t) = log((N - n(t) + 0.5) / (n(t) + 0.5))
    # 其中, N是文档总数, n(t)是包含词条t的文档数。
    # 2.
    # 计算每个词条在每个文档中的得分:
    # score(t, d) = idf(t) * freq(t, d) * (k1 + 1) / (freq(t, d) + k1 * (1 - b + b * len(d) / avgdl))
    # 其中, freq(t, d)是词条t在文档d中出现的次数, len(d)是文档d的长度, avgdl是所有文档的平均长度, k1和b是参数, 一般取k1 = 1.5, b = 0.75。
    # 3.
    # 计算每个文档的得分, 对各个词条在该文档中的分数求和:
    # score(d) = ∑ score(t, d)
    # 其中, t为出现在文档d中的各个词条。
    # 4.
    # 根据文档得分排序, 返回 top k 个结果。
    # 5.
    # 返回文档详细信息(地址、内容等)和高亮显示信息。
    # k1 = 1.5
    # b = 0.75
    # n_docs = 68582
    # avgdl = 4261
    # # 1. 计算每个词条的idf
    # st_time = time.time()
    # idfs = {}
    # for term in terms:
    #     print(term.term, term.document_count)
    #     idfs[term.term] = log((n_docs - term.document_count + 0.5) / (term.document_count + 0.5))
    # print(f'计算idf用时{time.time() - st_time}s')
    # # 2. 计算文档得分
    # st_time = time.time()
    # scores = {}
    # for pst in postings:
    #     if pst.doc_id not in scores:
    #         scores[pst.doc_id] = 0
    #     law_document = Law_Document.objects.filter(doc_id=pst.doc_id).first()
    #     scores[pst.doc_id] += \
    #         idfs[pst.term] * pst.freq * (k1 + 1) / (pst.freq + k1 * (1 - b + b * doc_len / avgdl))
    # print(f'计算文档得分用时{time.time() - st_time}s')
    # # 3. 返回前k个文档
    # st_time = time.time()
    # scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # print(f'排序用时{time.time() - st_time}s')
    # # 4. 返回文档的详细信息
    # # 5. 返回文档的高亮信息
    pass


def bm25_sort(doc_list, word_list):
    """
    对文档列表进行BM25排序
    """
    Posting = MONGO_DB['posting']
    Term = MONGO_DB['term']

    postings = list(Posting.find({'term': {'$in': word_list}, 'doc_id': {'$in': doc_list}}))

    k1 = 1.5
    b = 0.75
    avgdl = 4261  # 平均文档长度
    total_docs = 68382  # 文档总数

    doc_scores = {doc_id: 0 for doc_id in doc_list}  # 文档分数

    word_idfs = {}
    term_list = list(Term.find({'_id': {'$in': word_list}}))
    for term in term_list:
        word_idfs[term['_id']] = term['idf']

    print(f'全部查询词：{word_list}')
    print(f'全部词条：{[term["_id"] for term in term_list]}')

    # 按idfs降序排列, 删除idf<阈值的词条
    idf_threshold = 0
    # word_list = [word for word in word_list if word_idfs[word] > idf_threshold]
    term_list = [term for term in term_list if term['idf'] > idf_threshold]
    # word_list = sorted(word_list, key=lambda x: word_idfs[x], reverse=True)
    term_list = sorted(term_list, key=lambda x: word_idfs[x['_id']], reverse=True)
    print(f'参与排序的词条：{[term["_id"] for term in term_list]}')

    for term in term_list:
        idf = term['idf']
        for pst in postings:
            doc_scores[pst['doc_id']] += \
                idf * pst['freq'] * (k1 + 1) / (pst['freq'] + k1 * (1 - b + b * pst['doc_len'] / avgdl))

    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    json.dump(sorted_docs, open(os.path.join(BASE_DIR, 'resources', 'sorted_docs.json'), 'w'))
    return [doc_id for doc_id, score in sorted_docs]

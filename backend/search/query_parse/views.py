"""
预计用来支持搜索引擎常用的查询语法，如：AND, OR, NOT, NEAR, IN, ALL, ANY, EXACTLY, etc.
(严格模式)
"""
import json
import re
import time

import jieba
import redis

from backend.settings import MONGO_DB, SIGN_WORDS_PATH, STOP_WORDS_PATH


def split_into_tokens(query):
    """
    将查询语句分割成单词
    """
    # 提取所有括号
    brackets = re.findall(r'[\(\)]', query)
    if brackets.count('(') != brackets.count(')'):
        raise ValueError('括号不匹配')

    for bracket in brackets:
        query = query.replace(bracket, f' {bracket} ')

    tokens = query.split()
    return tokens


def infix_to_postfix(tokens):
    """
    中缀表达式转后缀表达式
    test: 'aa & (bb | cc & ee) - dd' -> ['aa', 'bb', 'cc', 'ee', '&', '|', '&', 'dd', '-']
    """
    stack = []  # 括号堆栈
    expr = []  # 后缀表达式
    # 先将中缀表达式转化为后缀表达式
    for token in tokens:
        if token == '(':
            stack.append('(')
        elif token == ')':
            while stack[-1] != '(':
                expr.append(stack.pop())
            stack.pop()
        elif token == '&':
            while stack and stack[-1] not in ['(', '|', '-']:
                expr.append(stack.pop())
            stack.append(token)
        elif token == '|':
            while stack and stack[-1] not in ['(', '-']:
                expr.append(stack.pop())
            stack.append(token)
        elif token == '-':
            while stack and stack[-1] != '(':
                expr.append(stack.pop())
            stack.append(token)
        else:
            expr.append(token)

    while stack:
        expr.append(stack.pop())

    return expr


def term_to_doc_ids(term_set):
    """
    根据词条获取文档id集合
    """
    print(f'查询词条：{term_set}')
    Posting = MONGO_DB['posting']
    redis_conn = redis.Redis(host='localhost', port=6379, db=1)
    doc_ids = set()
    for term in term_set:
        if redis_conn.exists(term):
            print(f'关键词{term}在缓存中', end=' ')
            doc_ids |= set(json.loads(redis_conn.get(term)))
        else:
            print(f'关键词{term}不在缓存中', end=' ')
            pipeline = [
                {'$match': {'term': term}},
                {'$group': {'_id': None, 'doc_ids': {'$addToSet': '$doc_id'}}},
            ]
            try:
                doc_id = next(Posting.aggregate(pipeline))['doc_ids']
            except:
                doc_id = []
            redis_conn.set(term, json.dumps(doc_id), ex=60 * 60 * 3)  # 3小时过期
            doc_ids |= set(doc_id)
    print('\n')
    return list(doc_ids), term_set  # 返回结果文档和包含的词条


def cal_doc_ids(expr):
    """
    根据后缀表达式计算文档id集合和包含的词条
    """
    stack = []
    for token in expr:
        if token == '&':
            right = stack.pop()
            left = stack.pop()
            stack.append((left[0] & right[0], left[1] | right[1]))
        elif token == '|':
            right = stack.pop()
            left = stack.pop()
            stack.append((left[0] | right[0], left[1] | right[1]))
        elif token == '-':
            right = stack.pop()
            left = stack.pop()
            stack.append((left[0] - right[0], left[1] - right[1]))
        else:
            stack.append(term_to_doc_ids({token}))

    return stack.pop()


def parse_query(query):
    """
    解析查询语句:
    & 表示并集，如：中国 & 人民
    | 表示交集，如：中国 | 人民
    - 表示排除，如：中国 - 人民
    """
    # 如果query以"EXACTLY"开头，则表示严格模式，只返回包含所有词条的文档
    st_time = time.time()
    if query.startswith('EXACTLY:'):
        query = query[8:]
        print(f'精确查询语句：{query}')
        tokens = split_into_tokens(query)
        expr = infix_to_postfix(tokens)
        doc_ids, word_list = cal_doc_ids(expr)
        doc_ids, word_list = list(doc_ids), list(word_list)
        word_list_for_sort = word_list
    else:
        print(f'普通查询语句：{query}')
        Term = MONGO_DB['term']
        # 去除停用词
        words = set(jieba.cut_for_search(query))    # todo：这里的分词方式可能需要调整，重复的词条是否需要保留？
        stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
        with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
            stop_words += f.read().splitlines()
        words = words - set(stop_words)
        print(f'分词结束，查询耗时：{time.time()-st_time}')
        doc_ids, word_list = term_to_doc_ids(words)
        print(f'检索结束，查询耗时：{time.time()-st_time}')
        doc_ids, word_list = list(doc_ids), list(word_list)
        word_list_for_sort = []
        word_idfs = {word: -99 for word in word_list}
        # 如果查询词条中有单个词条的idf值<0，则认为是无效词条，不参与排序
        for word in word_list:
            term = Term.find_one({'_id': word})
            if not term:
                continue
            word_idfs[word] = term['idf']
            if term['idf'] > 0:
                word_list_for_sort.append(word)
        word_list.sort(key=lambda x: word_idfs[x], reverse=True)
        word_list_for_sort.sort(key=lambda x: word_idfs[x], reverse=True)

    print(f'排序词条：{word_list_for_sort}')
    print(f'查询总耗时：{time.time() - st_time}')

    return doc_ids, word_list, word_list_for_sort

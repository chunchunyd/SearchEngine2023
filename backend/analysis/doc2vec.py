import gensim
import jieba
import json
import os
import time
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from common.models import LawDocument
from backend.settings import BASE_DIR, SIGN_WORDS_PATH, STOP_WORDS_PATH, MONGO_DB, D2V_MODEL


# 用于从sql获取文本并分词的迭代器
class MyDocs(object):
    def __init__(self, build=False, test=False):
        """
        初始化, build为True时从数据库中重新分词并保存, 否则从文件中读取
        """
        # 进度条
        self.cnt = 0
        self.start_time = time.time()
        self.stop_watch = self.start_time
        self.epoch = 0

        # 分词数据
        self.doc_words = []
        self.doc_ids = []
        self.documents_cnt = 0
        self.group_id = 0

        if build:
            # 停用词表
            stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
            # stop_words.txt文件中，可以不断添加新的停用词
            with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
                stop_words += f.read().splitlines()
            stop_words = stop_words

            # 数据库
            documents = LawDocument.objects.all()
            self.documents_cnt = len(documents)
            # 从数据库中获取文本并分词
            for document in documents:
                # 分词
                words = jieba.lcut(document.full_text)
                # 去除停用词
                words = [word for word in words if word not in stop_words]
                # 保存分词结果
                self.doc_words.append(words)
                self.doc_ids.append(str(document.id))
                # 进度条
                self.cnt += 1
                if self.cnt % 100 == 0:
                    now = time.time()
                    print(
                        f'正在处理第{self.cnt}/{self.documents_cnt}个文档, '
                        f'近100个用时{now - self.stop_watch:.2f}s, 总用时{now - self.start_time:.2f}s, '
                        f'平均用时{(now - self.start_time) / self.cnt:.4f}s', end='\r')
                    self.stop_watch = now
                if self.cnt % 5000 == 0 or self.cnt == self.documents_cnt:
                    # 保存分词结果
                    with open(os.path.join(BASE_DIR, 'resources', 'jieba_results',
                                           f'doc_words_{self.group_id}.json'), 'w', encoding='utf-8') as f:
                        json.dump(self.doc_words, f, ensure_ascii=False)
                    with open(os.path.join(BASE_DIR, 'resources', 'jieba_results',
                                           f'doc_ids_{self.group_id}.json'), 'w', encoding='utf-8') as f:
                        json.dump(self.doc_ids, f, ensure_ascii=False)
                    # 重置
                    self.group_id += 1
                    self.doc_words = []
                    self.doc_ids = []
            with open(os.path.join(BASE_DIR, 'resources', 'jieba_results', 'group_num.txt'), 'w',
                      encoding='utf-8') as f:
                f.write(str(self.group_id))
            print(f'分词完成, 用时{time.time() - self.start_time:.2f}s')
            # 初始化迭代器
            self.cnt = 0
            self.start_time = time.time()
            self.stop_watch = self.start_time
            self.epoch = 0
            self.group_id = 0

        # 从文件中读取分词结果, 先尝试全部读取, 若失败则分批读取
        with open(os.path.join(BASE_DIR, 'resources', 'jieba_results', 'group_num.txt'), 'r', encoding='utf-8') as f:
            group_num = int(f.read())
        if test:
            group_num = 1
        for i in range(group_num):
            with open(os.path.join(BASE_DIR, 'resources', 'jieba_results',
                                   f'doc_words_{i}.json'), 'r', encoding='utf-8') as f:
                self.doc_words += json.load(f)
            with open(os.path.join(BASE_DIR, 'resources', 'jieba_results',
                                   f'doc_ids_{i}.json'), 'r', encoding='utf-8') as f:
                self.doc_ids += json.load(f)
        self.documents_cnt = len(self.doc_ids)

    def __iter__(self):
        for i in range(self.documents_cnt):
            # 进度条
            self.cnt += 1
            if self.cnt % 100 == 0:
                now = time.time()
                print(
                    f'正在处理第{self.cnt}/{self.documents_cnt}个文档, '
                    f'近100个用时{now - self.stop_watch:.2f}s, 总用时{now - self.start_time:.2f}s, '
                    f'平均用时{(now - self.start_time) / self.cnt:.4f}s', end='\r')
                self.stop_watch = now

            # 迭代数
            if self.cnt == self.documents_cnt:
                self.epoch += 1
                self.cnt = 0
                print(f'\n第{self.epoch}轮迭代完成, 用时{time.time() - self.start_time:.2f}s')
                self.start_time = time.time()
                self.stop_watch = self.start_time

            # 返回结果
            yield TaggedDocument(self.doc_words[i], [self.doc_ids[i]])

    def set_epoch(self, epoch):
        self.epoch = epoch
        self.cnt = 0
        self.start_time = time.time()
        self.stop_watch = self.start_time


def train_doc2vec(test=False):
    """
    训练doc2vec模型
    """
    # 从sql中获取文本并分词
    print('正在获取文本并分词')
    docs = MyDocs(False, test=test)
    # 训练doc2vec模型
    print('正在初始化doc2vec模型')
    docs.set_epoch(0)
    model = Doc2Vec(docs, vector_size=300, window=5, min_count=1, workers=4, epochs=1)
    # 建立词汇表
    print('正在建立词汇表')
    docs.set_epoch(0)
    model.build_vocab(docs)
    # 训练
    print('正在训练doc2vec模型')
    docs.set_epoch(0)
    model.train(docs, total_examples=model.corpus_count, epochs=80)
    # 保存模型
    print('正在保存模型')
    model.save(os.path.join(BASE_DIR, 'resources', 'doc2vec_models', 'doc2vec.model'))
    # 保存词汇表
    print('正在保存词汇表')
    with open(os.path.join(BASE_DIR, 'resources', 'doc2vec_models', 'doc2vec.vocab'), 'w',
              encoding='utf-8') as f:
        for word in model.wv.index_to_key:
            f.write(word + '\n')
    # 保存词向量
    print('正在保存词向量')
    with open(os.path.join(BASE_DIR, 'resources', 'doc2vec_models', 'doc2vec.vector'), 'w',
              encoding='utf-8') as f:
        for word in model.wv.index_to_key:
            f.write(' '.join([str(num) for num in model.wv[word]]) + '\n')


def get_similar_docs_by_id(doc_id, topn=10):
    """
    获取相似文档
    """
    # 获取相似文档
    similar_docs = D2V_MODEL.docvecs.most_similar(doc_id, topn=topn)
    # 获取相似文档的id
    similar_docs_ids = [doc_id for doc_id, _ in similar_docs]
    return similar_docs_ids


def get_similar_docs_by_word_list(word_list, topn=10):
    """
    获取相似文档
    """
    import time
    st_time = time.time()
    stop_watch = st_time
    now = time.time()
    print(f'加载模型用时{now - stop_watch:.2f}s')
    stop_watch = now

    # 获取向量
    vector = D2V_MODEL.infer_vector(word_list)

    now = time.time()
    print(f'获取向量用时{now - stop_watch:.2f}s')
    stop_watch = now

    # 获取相似文档
    # similar_docs = D2V_MODEL.docvecs.most_similar(positive=word_list, topn=topn)
    similar_docs = D2V_MODEL.docvecs.most_similar([vector], topn=topn)

    now = time.time()
    print(f'获取相似文档用时{now - stop_watch:.2f}s')
    stop_watch = now

    # 获取相似文档的id
    similar_docs_ids = [doc_id for doc_id, _ in similar_docs]

    now = time.time()
    print(f'获取相似文档的id用时{now - stop_watch:.2f}s')
    stop_watch = now
    
    return similar_docs_ids

import gensim
import jieba
import json
import os
import time
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from common.models import LawDocument
from backend.settings import BASE_DIR, SIGN_WORDS_PATH, STOP_WORDS_PATH, MONGO_DB


# 用于从sql获取文本并分词的迭代器
class MyDocs(object):
    def __init__(self):
        # 停用词表
        stop_words = json.load(open(SIGN_WORDS_PATH, 'r', encoding='utf-8'))
        # stop_words.txt文件中，可以不断添加新的停用词
        with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
            stop_words += f.read().splitlines()
        self.stop_words = stop_words

        # 进度条
        self.cnt = 0
        self.start_time = time.time()
        self.stop_watch = self.start_time
        self.epoch = 0

        # 数据库
        self.documents = LawDocument.objects.all()
        self.documents_cnt = len(self.documents)

    def __iter__(self):
        for document in self.documents:
            # yield TaggedDocument(words=jieba.lcut(document.full_text), tags=[str(document.id)])
            # 分词
            words = jieba.lcut(document.full_text)
            # 去除停用词
            words = [word for word in words if word not in self.stop_words]

            # 进度条
            self.cnt += 1
            now = time.time()
            print(
                f'正在处理第{self.cnt}/{self.documents_cnt}个文档, '
                f'用时{now - self.stop_watch:.2f}s, 总用时{now - self.start_time:.2f}s, '
                f'平均用时{(now - self.start_time) / self.cnt:.2f}s', end='\r')
            self.stop_watch = now

            # 迭代数
            if self.cnt == self.documents_cnt:
                self.epoch += 1
                self.cnt = 0
                print(f'第{self.epoch}轮迭代完成, 用时{time.time() - self.start_time:.2f}s')
                self.start_time = time.time()
                self.stop_watch = self.start_time

            # 返回分词结果
            yield TaggedDocument(words, [str(document.id)])


def train_doc2vec():
    """
    训练doc2vec模型
    """
    # 从sql中获取文本并分词
    docs = MyDocs()
    # 训练doc2vec模型
    model = Doc2Vec(docs, vector_size=300, window=5, min_count=1, workers=4)
    # 建立词汇表
    print('正在建立词汇表')
    model.build_vocab(docs)
    # 训练
    print('正在训练doc2vec模型')
    model.train(docs, total_examples=model.corpus_count, epochs=5)
    # 保存模型
    print('正在保存模型')
    model.save(os.path.join(BASE_DIR, 'backend', 'analysis', 'doc2vec_models', 'doc2vec.model'))
    # 保存词汇表
    print('正在保存词汇表')
    with open(os.path.join(BASE_DIR, 'backend', 'analysis', 'doc2vec_models', 'doc2vec.vocab'), 'w',
              encoding='utf-8') as f:
        for word in model.wv.index2word:
            f.write(word + '\n')
    # 保存词向量
    print('正在保存词向量')
    with open(os.path.join(BASE_DIR, 'backend', 'analysis', 'doc2vec_models', 'doc2vec.vector'), 'w',
              encoding='utf-8') as f:
        for word in model.wv.index2word:
            f.write(' '.join([str(num) for num in model.wv[word]]) + '\n')

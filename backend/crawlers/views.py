import json
import os
import time
from django.http import JsonResponse
from common.models import *
from bs4 import BeautifulSoup
from backend.settings import BASE_DIR, STATICFILES_DIRS
from .handlers import handle_judgment, handle_prosecution, handle_document, find_node


# 爬虫逻辑(模拟，实际上是本地数据)
class XmlSpider:
    """
    爬虫逻辑(模拟，实际上是本地数据)
    """

    name = "xml_spider"  # 爬虫名称, 用于区分不同的爬虫

    def __init__(self):
        self.dir_path = ""
        self.xml_files = []
        self.total_count = 0
        self.current_count = 0

    def set_dir(self, dir_path):
        """
        设置数据文件夹
        """
        self.xml_files = os.listdir(dir_path)  # 相对于 STATICFILES_DIRS[0] 的路径

        # test
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'JCY', 'QSS.json'),
        #          'r', encoding='utf-8'))  # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'JCY', 'BQSS.json'),
        #          'r', encoding='utf-8'))  # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'SFXZ', 'ZYJWZXAL.json'),
        #          'r', encoding='utf-8'))    # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'PJS.json'),
        #          'r', encoding='utf-8'))  # 4000/40000 OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'TJS.json'),
        #          'r', encoding='utf-8'))  # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'CDS.json'),
        #          'r', encoding='utf-8'))  # 2000/20000 OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'TZS.json'),
        #          'r', encoding='utf-8'))  # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'JDS.json'),
        #          'r', encoding='utf-8'))  # OK
        # self.xml_files = json.load(
        #     open(os.path.join(BASE_DIR, 'scripts', 'classification', 'FY', 'QSZ.json'),
        #          'r', encoding='utf-8'))  # OK

        self.dir_path = dir_path
        self.total_count = len(self.xml_files)
        self.current_count = 0


    def parse(self, start_time):
        """
        解析xml文件
        """
        start_xml_id = 1
        for xml_file in self.xml_files:
            self.current_count += 1

            # 开始解析的xml_id
            if self.current_count < start_xml_id:
                continue

            if self.current_count % 1000 == 0:
                print(f', 总计用时：{time.time() - start_time}秒')
            print(f"\r当前进度：{self.current_count}/{self.total_count}", end='')
            xml_path = os.path.join(self.dir_path, xml_file)
            with open(xml_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
                soup = BeautifulSoup(xml_content, features="xml")
                # 文书种类
                doc_type = find_node(soup, 'WSZL').get('value')
                if doc_type == '判决书' or doc_type == '裁定书' or doc_type == '调解书' or doc_type == '决定书':
                    # 处理判决书
                    handle_judgment(soup, xml_file)
                elif doc_type == '起诉书' or doc_type == '不起诉书':
                    # 处理起诉书
                    handle_prosecution(soup, xml_file)
                elif doc_type == '':
                    # 坏网页
                    continue
                else:
                    # 处理其他文书
                    handle_document(soup, xml_file)


SPIDER = XmlSpider()


def launch_spider(request):
    """
    启动爬虫
    """
    start_time = time.time()
    SPIDER.set_dir(STATICFILES_DIRS[0])
    SPIDER.parse(start_time)
    end_time = time.time()
    print(f"总耗时：{end_time - start_time}秒")
    return JsonResponse({
        "status": "Done",
        "time": end_time - start_time
    })


def spider_progress(request):
    """
    获取爬虫进度
    """
    progress = {
        "total_count": SPIDER.total_count,
        "current_count": SPIDER.current_count,
        "file_name": SPIDER.relative_xml_paths[SPIDER.current_count - 1],
        "status": "Running"
    }
    return JsonResponse(progress)

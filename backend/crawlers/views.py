import os
from django.http import JsonResponse
from common.models import *
from bs4 import BeautifulSoup
from backend.settings import BASE_DIR
from .handlers import handle_judgment, handle_prosecution, handle_document, find_node


# 爬虫逻辑(模拟，实际上是本地数据)
class XmlSpider:
    """
    爬虫逻辑(模拟，实际上是本地数据)
    """

    name = "xml_spider"  # 爬虫名称, 用于区分不同的爬虫, 必须是唯一的

    def __init__(self):
        self.relative_xml_paths = []
        self.total_count = 0
        self.current_count = 0

    def set_dir(self, relative_dir):
        """
        设置数据文件夹
        """
        xml_files = os.listdir(relative_dir)
        self.relative_xml_paths = [os.path.join(relative_dir, xml_file) for xml_file in xml_files]
        self.total_count = len(self.relative_xml_paths)
        self.current_count = 0

    def parse(self):
        """
        解析xml文件
        """
        for relative_xml_path in self.relative_xml_paths:
            self.current_count += 1
            print(f"当前进度：{self.current_count}/{self.total_count}")
            xml_path = os.path.join(BASE_DIR, relative_xml_path)
            with open(xml_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
                soup = BeautifulSoup(xml_content, 'lxml')
                # 文书种类
                doc_type = find_node(soup, 'WSZL').get('value')
                if doc_type == '判决书' or doc_type == '裁定书' or doc_type == '调解书':
                    # 处理判决书
                    handle_judgment(soup)
                elif doc_type == '起诉书' or doc_type == '不起诉书':
                    # 处理起诉书
                    handle_prosecution(soup)
                elif doc_type == '':
                    # 坏网页
                    continue
                else:
                    # 处理其他文书
                    handle_document(soup)


SPIDER = XmlSpider()


def launch_spider(request):
    """
    启动爬虫
    """
    relative_dir = os.path.join(BASE_DIR, 'resources', 'static')
    SPIDER.set_dir(relative_dir)
    SPIDER.parse()


def spider_progress(request):
    """
    获取爬虫进度
    """
    progress = {
        "total_count": SPIDER.total_count,
        "current_count": SPIDER.current_count,
    }
    return JsonResponse(progress)

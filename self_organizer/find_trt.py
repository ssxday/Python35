# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:分三个步骤
1、page -> post
2、post -> download
3、download -> torrent暂时存放在文件中

"""
import requests
from html.parser import HTMLParser
from os.path import join
from bs4 import BeautifulSoup


class Config:
    """所需的常量及设置"""
    URL_ROOT = r'http://km.1024ky.trade/pw'
    KEY_WORDS = [
        'hardcore', 'blacked'
    ]


class TaskTeam:
    """通用队列类"""

    def __init__(self):
        self.tasks = []  # 没有上限

    def add_task(self, task):
        self.tasks.append(task)

    def take_task(self):
        if self.tasks:
            return self.tasks.pop(0)
        else:
            raise EOFError

    def __call__(self, *args, **kwargs):
        return self.tasks


class Page2PostParser(HTMLParser):
    def __init__(self):
        super(Page2PostParser, self).__init__()
        self.__tasks = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            query = dict(attrs)
            if query.get('href', '').startswith(r'htm_data'):
                self.__tasks.append(query.get('href'))  # 只负责添加

    def __call__(self, *args, **kwargs):
        return self.__tasks


class Page2Post(TaskTeam, Config):
    """本类的实例"""

    def __init__(self, start_page=5):
        super(Page2Post, self).__init__()
        self.start_page = start_page
        self.parser = Page2PostParser()
        self.list_post()

    def list_post(self):
        query_string = r'thread.php?fid=3&page={page}'.format(page=self.start_page)
        url = join(self.URL_ROOT, query_string)
        # print(url)
        page = requests.get(url)
        data = page.text
        self.parser.feed(data)  # 把当前页的所有帖子地址加入到task队列
        # 把task队列搬到当前对象的__task，已继承队列属性
        self.tasks.extend(self.parser())


class Post2download(TaskTeam, Config):
    """"""

    def __init__(self, query):
        """query从Page2Post的队列中取"""
        super(Post2download, self).__init__()
        text = self.pull_request(query)
        # 分析帖子text
        self.scan_post(text)

    def pull_request(self, query):
        """发起请求，得到帖子内容并返回内容"""
        url = join(self.URL_ROOT, query)
        print(url)
        page = requests.get(url)
        text = page.text
        return text

    def scan_post(self, data):
        """从post定位到download页面"""
        soup = BeautifulSoup(data, 'lxml')
        # 定位到主体div
        the_div = soup.find('div', attrs={'class': "tpc_content", 'id': "read_tpc"})
        for sub_str_elem in the_div.strings:
            # if 'hardcore' in str(sub_str_elem).lower():  # 要被替代
            if self.washing(sub_str_elem, *self.KEY_WORDS):
                for sibling in sub_str_elem.next_siblings:
                    if sibling.name == 'a' and sibling['href'] == sibling.string:
                        if sibling.string not in self.tasks:
                            print(sub_str_elem.__str__(), sibling.string)
                            self.add_task(str(sibling.string))
                        break

    @staticmethod
    def washing(sands, *golds):
        """
        从sands中检查gold是否存在,强制转换sands为字符串，不区分大小写。
        :param sands:expecting 字符串
        :param golds:目标
        :return:gold只要出现任何一个，返回True，否则返回False
        """
        for g in golds:
            if str(g).lower() in sands.lower():
                return True
        return False


pg = Page2Post()

'http://km.1024ky.trade/pw/htm_data/3/1701/527671.html'


class Downloader:
    def download(self):
        """进入download页面拿到目标地址然后下载资源到本地"""

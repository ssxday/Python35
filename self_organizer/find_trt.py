# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:按页号

"""
import requests
from html.parser import HTMLParser
from os.path import join
from bs4 import BeautifulSoup


class TaskTeam:
    """队列类"""

    def __init__(self):
        self.__tasks = []  # 没有上限

    def add_task(self, task):
        self.__tasks.append(task)

    def take_task(self):
        if self.__tasks:
            return self.__tasks.pop(0)
        else:
            raise EOFError

    def __call__(self, *args, **kwargs):
        return self.__tasks


class Page2PostParser(HTMLParser):
    def __init__(self):
        super(Page2PostParser, self).__init__()
        self.tasks = TaskTeam()  # 实例化一个task队列

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            query = dict(attrs)
            if query.get('href', '').startswith(r'htm_data'):
                self.tasks.add_task(query.get('href'))


class Post2torrentParser(HTMLParser):
    def __init__(self):
        super(Post2torrentParser, self).__init__()
        self.bullitin = TaskTeam()
    def handle_starttag(self, tag, attrs):
        pass


class Page:
    """"""
    URL_ROOT = r'http://km.1024ky.trade/pw'

    def __init__(self, start_page=5):
        self.start_page = start_page
        self.parser = Page2PostParser()
        self.targets = TaskTeam()

    def list_post(self):
        query_string = r'thread.php?fid=3&page={page}'.format(page=self.start_page)
        url = join(self.URL_ROOT, query_string)
        # print(url)
        page = requests.get(url)
        data = page.text
        self.parser.feed(data)  # 把当前页的所有帖子地址加入到task队列
        self.scan_post()
        self.download()

    def scan_post(self):
        """从post定位到download页面"""
        # for sub_str_elem in self.parser.tasks():
        #     print(sub_str_elem)
        if self.parser.tasks():
            url = join(self.URL_ROOT, self.parser.tasks.take_task())
        else:
            print('ALL DONE！')
            return
        print(url)
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data,'lxml')
        # 定位到主体div
        the_div = soup.find('div',attrs={'class':"tpc_content",'id':"read_tpc"})
        for sub_str_elem in the_div.strings:
            # print('@@',str(sub_str_elem))
            if 'hardcore' in str(sub_str_elem).lower():
                for sibling in sub_str_elem.next_siblings:
                    if sibling.name == 'a' and sibling['href'] == sibling.string:
                        if sibling.string not in self.targets():
                            print(sub_str_elem.__str__(), sibling.string)
                            self.targets.add_task(str(sibling.string))
                        break

    def download(self):
        """进入download页面拿到目标地址然后下载资源到本地"""
        if self.targets():
            pass

pg = Page()
pg.list_post()
print(pg.targets().__len__())

'http://km.1024ky.trade/pw/htm_data/3/1701/527671.html'
'第一个http://km.1024ky.trade/pw/htm_data/3/1701/515771.html'

class Downloader:
    pass




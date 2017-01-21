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


class Page2PostParser(HTMLParser):
    def __init__(self):
        super(Page2PostParser, self).__init__()
        self.count = 0
        self.__task = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            query = dict(attrs)
            # print(query.get('href'))
            if query.get('href', '').startswith(r'htm_data'):
                print(query.get('href'))
                self.count += 1

    def add_task(self, task):
        self.__task.append(task)

    def take_task(self):
        if self.__task:
            return self.__task.pop()
        else:
            raise EOFError

    def __call__(self, *args, **kwargs):
        return self.__task


class Post2torrentParser(HTMLParser):
    pass

url_root = r'http://km.1024ky.trade/pw'
start_page = 5
url = url_root + '/thread.php?fid=3&page={page}'.format(page=start_page)
print(url)
page = requests.get(url)
data = page.text

psr = Page2PostParser()
psr.feed(data)
for i in psr():
    print(i)

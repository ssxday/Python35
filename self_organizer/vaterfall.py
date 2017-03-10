# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:

"""
import requests
from random import choice
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from common_use import Headers, Jp


class Broke(Exception):
    def __init__(self, msg=''):
        self.msg = msg

    def __str__(self):
        return self.msg


def pull_request(page):
    url = urljoin(choice(Jp.HOSTS), r'page/{}'.format(page))
    resp = requests.get(url, headers=Headers.HEADERS)
    if resp:
        resp.encoding = 'utf-8'
        return resp.text
    else:
        raise Broke('没有response')


def scan(txt):
    """正常返回部件代码的生成器"""
    soup = BeautifulSoup(txt, 'lxml')
    waterfalls = soup.find_all('div', {'class': 'item'})
    if waterfalls:
        return (str(w) for w in waterfalls)
    else:
        raise Broke('未能分析出关键部件')


class Details:
    # __re_symbol = re.compile(r'^https?://www\.[a-z0-9]+\.com/([a-z0-9-]+)', re.I)

    def __init__(self, txt):
        self.__soup = BeautifulSoup(txt, 'lxml')
        self.__img_tag = self.__soup.find('img')
        self.__date_tag = self.__soup.find_all('date')
        self.__buttons = [btn.text for btn in self.__soup.find_all('button', {'disabled': 'disabled'})]

    @property
    def url(self):
        tag = self.__soup.find('a', {'class': 'movie-box'})
        return tag.get('href')

    @property
    def symbol(self):
        if self.__date_tag:
            s = self.__date_tag[0].text
            return s
        else:
            return 'Unknown'

    @property
    def thumbnail(self):
        if self.__img_tag:
            return self.__img_tag.get('src')
        else:
            return 'Unknown'

    @property
    def title(self):
        if self.__img_tag:
            return '{} {}'.format(self.symbol, self.__img_tag.get('title'))
        else:
            return 'Unknown'

    @property
    def date(self):
        if self.__date_tag:
            s = self.__date_tag[1].text
            return s
        else:
            return 'Unknown'

    def ishd(self):
        if self.__buttons:
            if '高清' in self.__buttons:
                return True
            else:
                return False
        return False

    def isrecent(self):
        if self.__buttons:
            if '新' in str(self.__buttons):
                return True
            else:
                return False
        return False

    def __str__(self):
        s = '<Details symbol={} title={} url={} thumbnail={} date={} HD={} recent={}>'
        return s.format(self.symbol, truncate(self.title, 20), self.url,
                        self.thumbnail, self.date,
                        self.ishd(), self.isrecent()
                        )


def truncate(txt='', max_length=30, abbreviation='...'):
    """截取过长字符串至指定长度，保留前部和尾部一部分，中间适当调整
    如果字符串本身不到指定长度，则不做处理
    """
    if max_length <= 5:
        return txt
    if len(txt) <= max_length:
        return txt
    else:
        cut_length = max_length // 3
        head = txt[:cut_length]
        tail = txt[-cut_length:]
        left_length_for_body = max_length - 2 * cut_length - len(abbreviation)
        body = txt[cut_length:cut_length + left_length_for_body]
        truncated = '{}{}{}{}'.format(head, body, abbreviation, tail)
        return truncated


######################################
def show(source):
    movie = Details(source)
    print(movie.url)
    print(movie.symbol)
    print(movie.thumbnail)
    print(movie.title)
    print(movie.date)
    print('HD', movie.ishd())
    print('Recent', movie.isrecent())


if __name__ == '__main__':
    code = pull_request('2')
    items = scan(code)
    for itm in items:
        show(itm)
        print('=' * 50)

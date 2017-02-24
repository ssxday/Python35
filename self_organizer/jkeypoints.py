# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:1.0
Description:提供一个识别码，返回其相关联的信息
    - 使用方法：
        info = describe(识别码[,to_json=False])
        默认返回字典形式的信息，当to_json为True时返回JSON
    该模块有4个类：
    SymbolSwitch对输入的识别码字符串进行分拣，为Describer提供requests的请求url
    Scan通过BeautifulSoup对response进行解析，提炼出所需信息
    Describer类的to_json参数默认为False，将不会把结果转化为JSON格式
    WeaknessError:自定义异常
"""
import requests
import re
import json
import math
from common_use import Jp
from common_use import Headers
from random import choice, random
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class SymbolSwitch:
    """目标分拣，给出的格式有
    ^[a-z]{1,5}-?\d{3,5}$    一般格式
    ^c\d{9}$                 F63格式
    ^n\d{5}$                 TH格式
    """
    re_letters = re.compile(r'^\d?[a-z]{1,5}', re.I)
    re_nums = re.compile(r'(\d{3,6})-?(\d{0,3})')

    def __init__(self, txt=''):
        letters = self.re_letters.search(txt)
        nums = self.re_nums.search(txt)
        self.symbol = txt  # 最终要的是它
        if letters and nums:
            letters = letters.group()
            # 下面详细处理letters和nums
            if letters.lower() == 'n':
                self.symbol = '{}{}'.format(letters, nums.group())
            elif letters.lower() == 'carib':
                self.symbol = '{}-{}'.format(nums.group(1), nums.group(2))
            elif letters.lower() == '1pond':
                self.symbol = '{}_{}'.format(nums.group(1), nums.group(2))
            else:
                self.symbol = '{}-{}'.format(letters.upper(), nums.group())
        else:
            raise WeaknessError('输入的内容无法转化为标准格式')


class WeaknessError(Exception):
    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt


class Scan:
    """"""

    def __init__(self, code):
        self.__soup = BeautifulSoup(code, 'lxml')
        self.info = dict()
        # 开始扫描
        self.__scan()

    def __scan(self):
        self.info.setdefault(5, self.__get_title())
        self.info.setdefault(7, self.__get_image())
        self.info.setdefault(11, self.__get_performer())
        self.info.setdefault(3, self.__get_publish_date())

    def __get_title(self):
        title_tag = self.__soup.find('h3')
        if title_tag:
            title = title_tag.text  # 标签内的字符串
            return title
        return 'Unknown'

    def __get_image(self):
        image_url_tag = self.__soup.find('a', {'class': 'bigImage'})
        if image_url_tag:
            image_url = image_url_tag.attrs.get('href')
            return image_url
        return 'Unknown'

    def __get_performer(self):
        star_name_divs = self.__soup.find_all('div', {'class': 'star-name'})
        if star_name_divs:
            star_names = [name.text for name in star_name_divs]
            return star_names
        return 'Unknown'

    def __get_publish_date(self):
        sands = self.__soup.find_all('span', {'class': 'header'})
        if sands:
            publish_tag = sands[1].next.next
            return str(publish_tag)
        return 'Unknown'


class Describer:
    def __init__(self, symbol, to_json=False):
        self.__host = choice(Jp.HOSTS)  # 随机选择一个base_url
        self.__req = SymbolSwitch(symbol).symbol  # 请求字符串
        self.__to_json = to_json
        self.__sess = requests.Session()  # 使用session
        self.__htm = self.__get_htm()  # 页面源代码
        # self.__get_mag_links()  # 获取并解析ajax内容

    def __get_htm(self):
        page_htm = self.__sess.get(urljoin(self.__host, self.__req), headers=Headers.HEADERS, timeout=20)  # 引入头信息设置
        if page_htm:
            page_htm.encoding = 'utf-8'
            sourcecode = page_htm.text
            print(page_htm.cookies)
            return sourcecode
        else:
            raise WeaknessError('Failed to open the page.')

    def __get_mag_links(self):
        """首先要取到ajax要发送的5个参数"""
        gid = re.search(r'var gid = (\d*?);', self.__htm).group(1)
        lang = 'zh'
        uc = re.search(r'var uc = (\d*?);', self.__htm).group(1)
        img = re.search(r"var img = '(.*?)';", self.__htm).group(1)
        floor = math.floor(random() * 1e3 + 1)

        ajax_url = self.__host + '/ajax/uncledatoolsbyajax.php?gid=%s&lang=%s&img=%s&uc=%s&floor=%s' % (
            gid, lang, img, uc, floor)
        print(ajax_url)
        # ajax的response
        ajax_result = self.__sess.get(ajax_url, headers=Headers.HEADERS)
        if ajax_result:
            ajax_result.encoding = 'utf-8'
            print(ajax_result.text)
            soup = BeautifulSoup(ajax_result.text, 'lxml')
            trs = soup.find_all('tr')  # 链接以tr标签为单元
            if trs:  # 返回了实质内容
                self.__magnet = [tr.td.a.get('href', 'Unknow') for tr in trs]  # 推导
            else:  # 没返回实质内容
                raise WeaknessError('AJAX Failed to fetch the magnet links')

    @property
    def infos(self):
        """"""
        details = {1: self.__req, }
        details.update(Scan(self.__htm).info)
        if self.__to_json:
            return json.dumps(details)
        return details

    def __del__(self):
        self.__sess.close()


relationship = {
    1: 'symbol', 5: 'title', 7: 'image',
    11: 'performers', 3: 'publish',
    13: 'magnet',
}


def describe(what, to_json=False):
    return Describer(what, to_json).infos


def desc_walk(begin, end, head='abp', to_json=False):
    for num in range(begin, end + 1):
        num_str = head + '{:0>3}'.format(num)
        desc = describe(num_str, to_json)
        print(desc)
        sleep(3)  # 循环太紧容易遭到服务器屏蔽


######################################################
if __name__ == '__main__':
    info = describe(input('输入识别码:'))
    for k, v in sorted(info.items()):
        print(relationship.get(k), ':', v)
######################################################

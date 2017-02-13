# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:1.0
Description:提供一个识别码，返回其相关联的信息
    该模块有4个类：
    SymbolSwitch对输入的识别码字符串进行分拣，为Describer提供requests的请求url
    Scan通过BeautifulSoup对response进行解析，提炼出所需信息
    Describer类的to_json参数默认为False，将不会把结果转化为JSON格式
    WeaknessError:自定义异常
"""
import requests
import re
import json
from common_use import Jp
from common_use import Headers
from random import choice
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class SymbolSwitch:
    """目标分拣，给出的格式有
    ^[a-z]{1,5}-?\d{3,5}$    一般格式
    ^c\d{9}$                 F63格式
    ^n\d{5}$                 TH格式
    """
    re_letters = re.compile(r'^\d?[a-z]{1,5}', re.I)
    re_nums = re.compile(r'\d{3,6}-?\d{0,3}$')

    def __init__(self, txt=''):
        letters = self.re_letters.search(txt)
        nums = self.re_nums.search(txt)
        self.symbol = txt  # 最终要的是它
        if letters and nums:
            letters = letters.group()
            nums = nums.group()
            # 下面详细处理letters和nums
            if letters.lower() == 'n':
                self.symbol = '{}{}'.format(letters, nums)
            elif letters.lower() == 'carib':
                self.symbol = '{}_{}'.format(nums[:6], nums[6:])
            elif letters.lower() == '1pond':
                self.symbol = '{}-{}'.format(nums[:6], nums[6:])
            else:
                self.symbol = '{}-{}'.format(letters.upper(), nums)
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
        self.info.setdefault(2, self.__get_title())
        self.info.setdefault(3, self.__get_image())
        self.info.setdefault(4, self.__get_performer())

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


class Describer:
    def __init__(self, symbol, to_json=False):
        host = choice(Jp.HOSTS)  # 随机选择一个base_url
        req = SymbolSwitch(symbol).symbol  # 请求字符串
        page = requests.get(urljoin(host, req), headers=Headers.HEADERS)  # 引入头信息设置
        page.encoding = 'utf-8'
        sourcecode = page.text
        infos = {1: req}
        infos.update(Scan(sourcecode).info)
        if to_json:
            self.info = json.dumps(infos)
        else:
            self.info = infos


relationship = {1: 'symbol', 2: 'title', 3: 'image', 4: 'performers'}
######################################################
if __name__ == '__main__':
    info = Describer(input('输入识别码:')).info
    for k, v in sorted(info.items()):
        print(relationship[k], ':', v)
######################################################

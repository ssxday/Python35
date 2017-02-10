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
from common_use import Constant
import os
import re


class Gothrough:
    re_mark = re.compile(r'[a-z]{2,5}-\d{3,5}', re.I)
    ACCEPT = ['.mp4', '.avi', '.rmvb', '.mkv', '.wmv']

    def __init__(self, name, dir_path):
        self.pool = dict()
        self.name = name
        self.engine(dir_path)

    def engine(self, root_path):
        contents = os.listdir(root_path)
        for f in [c for c in contents if not c.startswith('.') and not c.startswith('_')]:
            path = os.path.join(root_path, f)
            if os.path.isdir(path):
                self.engine(path)
            elif os.path.isfile(path):
                if os.path.splitext(f)[1] not in self.ACCEPT:
                    continue
                data = self.essence(f), [path]  # 数据格式
                self.add_data(data)  # 设计专门的添加方法

    def add_data(self, data=('', [])):
        key, lyst = data
        if key in self.pool:
            self.pool[key].extend(lyst)
        else:
            self.pool[key] = lyst

    @classmethod
    def essence(cls, txt):
        mark = cls.re_mark.search(txt)
        if mark:
            return mark.group()
        return txt

    def get(self, key):
        return self.pool.get(key)


class Compare:
    def __init__(self, compares):
        (one1, one2), (two1, two2) = compares.items()
        self.item1 = Gothrough(one1, one2)
        self.item2 = Gothrough(two1, two2)

    def common(self):
        cross = set(self.item1.pool.keys()) & set(self.item2.pool.keys())  # 交集
        if cross:
            for symbol in cross:
                one = self.item1.get(symbol)
                nameone = self.item1.name
                two = self.item2.get(symbol)
                nametwo = self.item2.name
                echo = '{symbol}:\n\t{name1}:{one}\n\t{name2}:{two}'.format(symbol=symbol, name1=nameone, one=one,
                                                                            name2=nametwo, two=two)
                print(echo)
        else:
            print('没有重复内容')


cmp_data = {
    'No.1': Constant.SIMU,
    'No.2': Constant.LAKESSD
}
cmpr = Compare(cmp_data)
cmpr.common()

# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:
- 既可查单个目录内部的重复，又可以查多个目录的两两组合中的重复
"""
from common_use import Constant
from itertools import combinations
import os
import re


class Gothrough:
    re_mark = re.compile(r'[a-z]{2,5}-\d{3,5}', re.I)
    ACCEPT = ['.mp4', '.avi', '.rmvb', '.mkv', '.wmv']

    def __init__(self, name, dir_path):
        self.pool = dict()
        self.name = 'No.{}'.format(name)  # 转换字符串
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

    def not_only_one(self):
        keys = [k for k, v in self.pool.items() if v.__len__() > 1]
        return {key: self.pool.get(key) for key in keys}

    @classmethod
    def essence(cls, txt):
        mark = cls.re_mark.search(txt)
        if mark:
            return mark.group()
        return txt

    def get(self, key):
        return self.pool.get(key)


class Compare:
    def __init__(self, *dir_to_check):
        assert 1 <= dir_to_check.__len__() <= 2
        self.__cmpool = []  # 初始化对比池
        for no in range(dir_to_check.__len__()):
            self.__cmpool.append(Gothrough(no, dir_to_check[no]))
        self.cbns = combinations(self.__cmpool, 2)  # 对比池的组合迭代器

    def inner_repeat(self):
        """单个对象内部的重复内容"""
        for k, v in self.__cmpool[0].not_only_one().items():
            print('{}:{}'.format(k, v))

    def couple_cross(self):
        """两两组合之中的重复内容"""
        # 遍历对比池中对象的组合
        for cbn in self.cbns:
            p, q = cbn
            cross = set(p.pool.keys()) & set(q.pool.keys())  # 交集
            if cross:
                for symbol in cross:
                    one = self.__cmpool[0].get(symbol)
                    nameone = self.__cmpool[0].name
                    two = self.__cmpool[1].get(symbol)
                    nametwo = self.__cmpool[1].name
                    echo = '{symbol}:\n\t{name1}:{one}\n\t{name2}:{two}'.format(symbol=symbol, name1=nameone, one=one,
                                                                                name2=nametwo, two=two)
                    print(echo)


cmpr = Compare(Constant.LAKESSD)
cmpr.inner_repeat()

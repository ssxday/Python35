# coding:utf-8
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:fnameReg2.py
Author:
Version:2.0
Description:本模块为批量规范化文件名而设计
该版本采取"一步一动"的模式，通过循环遍历查找指定标识的文件名，对不符合格式的文件名随即进行修改
本模块对listlib模块有依赖，所有的文件名标识都存放在listlib.lib中
- 2.0新特性：
    使用了任务队列，在正式规范化修改文件名之前，程序首先会把所有要执行的任务列出来
    在正式执行改名前，可以一览任务的详情和数目
    在确认后程序统一执行上述任务
"""
import re
import os
from listlib import lib


class TodoList:
    """"""
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args)
        return cls._only

    def __init__(self):
        self.__todo = []

    def add_todo(self, task):
        self.__todo.append(task)  # 没有上限

    def take_task(self):
        if not self.is_empty():
            task = self.__todo.pop(0)
            return task
        else:
            raise EOFError

    def is_empty(self):
        if self.__todo.__len__():
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        return self.__todo


class MyProcessor:
    def __init__(self):
        self.loop = 0
        self.todo = TodoList()

    def tour(self, pathname=r'/Users/AUG/Desktop/overall', flag=False):
        """
        """
        if not os.path.exists(pathname):
            raise FileNotFoundError(404, "the path doesn't exist", "use a real path to a directory.")
        elif not os.path.isdir(pathname):
            raise NotADirectoryError(4, "Your target should be a directory", 'use a real path to a directory.')

        for sign in lib:
            self.__engine(pathname, sign, flag)
        return self.loop

    def __engine(self, pathname='', sign='', flag=False):
        files = os.listdir(pathname)
        for f in files:
            if not (f.startswith('.') or f.startswith('_')):
                srcing = os.path.join(pathname, f)
                if os.path.isfile(srcing) and sign.lower() in f.lower():
                    dsting = os.path.join(pathname, self.__reg(f, sign))
                    if srcing == dsting:
                        continue
                    if os.path.exists(dsting):
                        dsting = os.path.splitext(dsting)[0] + ' (' + str(self.loop) + ')' \
                              + os.path.splitext(dsting)[1]
                    # 加入任务列表
                    self.todo.add_todo((srcing, dsting))
                    self.loop += 1
                elif os.path.isdir(srcing) and flag:
                    self.__engine(srcing, sign, flag)

        return self.loop

    @staticmethod
    def __reg(filename, symbol=''):
        """"""
        if symbol.lower() in filename.lower():
            pat_fan = '[a-z]*' + symbol + '[a-z]*'
            fanlist = re.findall(pat_fan, filename, re.I)
            if symbol.lower() in [i.lower() for i in fanlist]:
                fan = symbol.upper()
            else:
                return filename

            start = filename.lower().find(symbol.lower())
            half_str = filename[start + len(symbol):]
            prefix = os.path.splitext(half_str)[0]
            suffix = os.path.splitext(half_str)[1]
            try:
                hao = re.findall(r'\d{3,}', prefix)[0]
            except IndexError:
                return filename
            else:
                tail = prefix[prefix.find(hao) + len(hao):]
                return "%s-%s %s%s" % (fan, hao, tail.strip(), suffix) \
                    if tail.strip() != '' else "%s-%s%s" % (fan, hao, suffix)
        else:
            return filename

    def __del__(self):
        pass


processor = MyProcessor()
count = processor.tour(r'/users/aug/lakessd', flag=True)
for t in processor.todo():
    t = (os.path.split(tt)[1] for tt in t)
    src, dst = t
    print('{:<30} => {}'.format(src, dst))
print('共计%d项任务'.center(50, '*') % count)
confirm = input('确认以上任务吗？')
if confirm:
    while processor.todo():
        t = processor.todo.take_task()
        src, dst = t
        os.rename(src, dst)
        print('{}已更名为{}'.format(src, dst))

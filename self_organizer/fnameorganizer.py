# coding:utf-8
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:fnameorganizer.py
Description:

Author:
Version:2.0
"""
import re
import os


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

    def pichuli(self, pathname=r'/Users/AUG/Desktop/overall', flag=False):
        """
        """
        if not os.path.exists(pathname):
            return "路径不存在\nYour path doesn't exist."
        elif not os.path.isdir(pathname):
            return "目标必须是一个目录\nYour target should be a directory."

        from listlib import lib
        for sign in lib:
            self.__engine(pathname, sign, flag)
        return self.loop

    def __engine(self, pathname='', sign='abp', flag=False):
        files = os.listdir(pathname)
        for f in files:
            if not (f.startswith('.') or f.startswith('__')):
                src = os.path.join(pathname, f)
                if os.path.isfile(src) and sign.lower() in f.lower():
                    dst = os.path.join(pathname, self.__reg(f, sign))
                    if src == dst:
                        continue
                    if os.path.exists(dst):
                        dst = os.path.splitext(dst)[0] + ' (' + str(self.loop) + ')' \
                              + os.path.splitext(dst)[1]
                    # 加入任务列表
                    self.todo.add_todo((src, dst))
                    self.loop += 1
                elif os.path.isdir(src) and flag:
                    self.__engine(src, sign, flag)

        return self.loop

    def __reg(self, filename, symbol=''):
        """
        __私有方法
        对包含指定字符串标记zding的文件名filename进行整理
        在引擎engine中，已经对是否为文件进行了判断，这里只研究一个问题，把新文件名整理出来
        :param filename:
        :param symbol:
        :return: 重新整理过的字符串
        """
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
count = processor.pichuli(flag=True)
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

# coding:utf-8
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:fnameReg3.py
Author:
Version:3.0
Description:本模块为批量规范化文件名而设计
本版本通过一次遍历目录，实现对所有已知标识进行处理，效率提升至少100倍
- 3.0新特性：
任务列表更清晰
支持中途手动变更任务列表
"""
import re
import os
from common_use import Constant


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
        s, d = task
        if d in self.__todo.__repr__():
            d = '({})'.format(self.__todo.__len__()).join(os.path.splitext(d))
        self.__todo.append((s, d))  # 没有上限

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
    re_before_hao = re.compile(r'.*?[a-z]{2,5}(?=[- _]?\d{3,5}.*)', re.I)  # *?表示最短匹配
    re_fan = re.compile(r'[a-z]{2,5}$', re.I)
    re_fan_hao = re.compile(r'[a-z]{2,5}-?\d{3,5}', re.I)

    def __init__(self, root_dir):
        self.loop = 0
        self.root_dir = root_dir
        self.todo = TodoList()

    def start(self, flag=False):
        """flag:是否要遍历子目录
        """
        if not os.path.exists(self.root_dir):
            raise FileNotFoundError(404, "the path doesn't exist", "use a real path to a directory.")
        elif not os.path.isdir(self.root_dir):
            raise NotADirectoryError(4, "Your target should be a directory", 'use a real path to a directory.')
        self.__engine(self.root_dir, flag)
        return self.loop

    def __engine(self, pathname='', flag=False):
        files = os.listdir(pathname)
        for f in files:
            if not (f.startswith('.') or f.startswith('_')):
                srcing = os.path.join(pathname, f)
                if os.path.isfile(srcing):
                    reg_f = self.__reg(f)  # 预期的新文件名
                    dsting = os.path.join(pathname, reg_f)
                    if srcing == dsting:
                        continue
                    try:
                        # 断言：待使用的新文件名长度一定大于原文件名的长度
                        assert len(dsting) >= len(srcing)
                    except AssertionError:
                        # 有可能鉴别出错，需要人工处理的条件
                        print('原@{}\n期@{}'.format(srcing, dsting))
                        fan_hao = self.re_fan_hao.search(reg_f).group()  # 标的是reg_f，返回值必定存在，且必带连字符
                        # 把识别码前置
                        new_f = fan_hao + self.re_fan_hao.sub('', f)
                        dst_join = os.path.join(pathname, new_f)
                        # os.rename(srcing, dst_join)
                        print('后@{}\n'.format(dst_join))
                        continue  # 不同的处理逻辑，一定要continue
                    if os.path.exists(dsting):
                        if srcing.lower() != dsting.lower():
                            dsting = '({})'.format(self.loop).join(os.path.splitext(dsting))
                    # 加入任务列表
                    self.todo.add_todo((srcing, dsting))
                    self.loop += 1
                elif os.path.isdir(srcing) and flag:
                    self.__engine(srcing, flag)

    def __reg(self, filename=''):
        """"""
        before_hao = self.re_before_hao.search(filename)
        if before_hao:
            before_hao_string = before_hao.group()
            fan = self.re_fan.search(before_hao_string)
            if fan:
                fan_string = fan.group()  # 现在找到了关键的fan_string，跟lib对照
                if fan_string.lower() not in Constant.SYMBOLS:
                    return filename
                # 已经确定了fan，接下来要把hao连接上
                start_posi = filename.find(fan_string)
                if start_posi < 0:  # 没找到是不可能的，但是为了逻辑严谨
                    return filename
                hao_start_posi = start_posi + len(fan_string)
                hao_and_after = filename[hao_start_posi:]  # 有可能以空格下划线或横杠开头
                real_hao_posi = self.where_first_digit(hao_and_after)
                # 从第一个数字开始
                hao_and_after = hao_and_after[real_hao_posi:]
                return fan_string.upper() + '-' + hao_and_after
            else:
                return filename
        else:
            return filename

    @staticmethod
    def where_first_digit(txt):
        """取到字符串中第一个数字的索引"""
        i = 0
        for letter in txt:
            if letter.isdigit():
                return i
            i += 1

    def __del__(self):
        pass


def truncate(txt='', max_length=30, abbreviation='...'):
    """截取过长字符串至指定长度，保留前部和尾部一部分，中间适当调整
    如果字符串本身不到指定长度，则不做处理
    """
    if len(txt) <= max_length:
        return txt
    else:
        cut_length = max_length // 3
        head = txt[:cut_length]
        tail = txt[-cut_length:]
        left_length_for_body = max_length - 2 * cut_length - len(abbreviation)
        body = txt[cut_length:cut_length + left_length_for_body]
        truncated = head + body + abbreviation + tail
        return truncated


processor = MyProcessor(Constant.LAKESSD)
count = processor.start(flag=True)  # 默认False不遍历子目录
if count:
    for n, t in enumerate(processor.todo(), start=1):
        t = (os.path.split(tt)[1] for tt in t)
        src, dst = t
        print('{:<4} {:<35} => {}'.format(n, truncate(src), truncate(dst)))
    print('共计%d项任务'.center(50, '*') % count)
    confirm = input('确认以上任务吗？\n'
                    '\t取消任务 - 直接回车\n'
                    '\t需要剔除指定任务 - drop\n'
                    '\t执行任务 - 其他任意字母\n'
                    )
    if confirm:
        if confirm == 'drop':
            drop_which = input('需要单独剔除任务的编号(范围1~{},以空格间隔):'.format(processor.todo().__len__()))
            print()
            if drop_which:
                which_numbers = drop_which.split(' ')  # 列表
                fine_numbers = [int(n) for n in which_numbers if n.isdigit()]
                if max(fine_numbers) > processor.todo().__len__() or min(fine_numbers) < 1:
                    raise ValueError('输入的数字超出任务数量')
                for num in sorted(fine_numbers, reverse=True):  # 一定要从编号大的开始弹出
                    processor.todo().pop(num - 1)  # 因为显示是从1开始
            else:
                print('按原计划执行 - Mission proceed\n')
        while processor.todo():
            t = processor.todo.take_task()
            src, dst = t
            os.rename(src, dst)
            print('{} 已更名为 {}'.format(os.path.split(src)[1],
                                      os.path.split(dst)[1])
                  )
    else:
        print('\n任务已取消 - Mission Abort')
else:
    root_d = os.path.split(processor.root_dir)[1]
    print(' 太好了！目录{}中所有文件名都已标准化，无需处理 '.format(root_d).center(50, '*'))

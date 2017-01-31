# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:f63.py
Author:
Version:2.0
Description:本模块为批量规范化某些文件名而设计
- 2.0新特性：
只遍历一层目录
加入任务列表
任务最终执行前进行确认
"""
import re
import os
from common_use import Constant


class TaskTeam:
    def __init__(self):
        self.team = []

    def add_task(self, task):
        self.team.append(task)

    def take(self):
        if self.team:
            return self.team.pop(0)
        else:
            raise EOFError

    def __call__(self, *args, **kwargs):
        return self.team


class F63:
    loop = 0
    re_chuanhao = re.compile(r'\d{6}[ \-_]+\d{3}', re.S)
    re_riqi = re.compile(r'\D?(\d{6})\D?', re.S)
    re_xuhao = re.compile(r'\D+(\d{3})\D?', re.S)
    re_head_dict = {
        'c': re.compile(r'cari(?:bbean|bpr|b)?|cappv|加勒比PPV動畫|加勒比', re.I),
        'y': re.compile(r'1pon(?:do|d)?|一本道', re.I)
    }

    def __init__(self, root_dir, mark='c'):
        if not os.path.exists(root_dir):
            raise FileNotFoundError("路径不存在\nYour path doesn't exist.")
        elif not os.path.isdir(root_dir):
            raise NotADirectoryError("目标必须是一个目录\nYour target should be a directory.")
        elif not mark:
            raise ValueError("必须指定字符串标识\nA string should be designated here.")

        self.tasks = TaskTeam()
        self.root = root_dir
        self.mark = mark
        self.re_head = self.re_head_dict.get(mark)

        self.start()

    def start(self):
        """
        批处理引擎
        :return: 本次处理的次数
        """
        files = os.listdir(self.root)
        for f in files:
            if not (f.startswith('.') or f.startswith('_')):
                # --执行核心开始--
                src = os.path.join(self.root, f)
                dst = os.path.join(self.root, self.__reg(f))
                # 当目标路径已存在，且不是自己本身的时候
                # 添加数字标识，以免覆盖掉既有的最简形式
                if os.path.exists(dst) and src != dst:
                    # 下面把dst拆成文件名和后缀，中间插入数字序号以示区分
                    dst = os.path.splitext(dst)[0] + '(' + str(self.loop) + ')' \
                          + os.path.splitext(dst)[1]
                # 当要改成的名字就是它自己时（说明已经化为标准最简形式），跳过本轮循环，
                elif os.path.exists(dst) and src == dst:
                    continue
                # os.rename(src, dst)
                self.tasks.add_task((src, dst))
                # --执行核心结束--
                self.loop += 1
        return self.loop

    @staticmethod
    def __ridof(txt='', *sub_str):
        for s in sub_str:
            txt = txt.replace(s, '')
        return txt

    def __reg(self, txt=''):
        # 对各部分进行匹配，如果抓取失败则return最初的string
        try:
            symbol = self.re_head.findall(txt)[0]  # SYMBOL
            chuanhao = self.re_chuanhao.findall(txt)  # XXXXXX-XXX
            if len(chuanhao) == 1:
                xuhao = self.re_xuhao.findall(chuanhao[0])[0]
            else:
                return txt
            middle = self.re_riqi.findall(chuanhao[0])[0]  # XXXXXX
        except IndexError:
            return txt

        # 在处理完leftover前，不要改动head,middle,xuhao的格式！！！！！
        leftover = self.__ridof(txt, symbol, middle, xuhao, '-', '_', ' ', '@')
        if 'ppv' in symbol.lower():
            symbol = 'CAPPV'
        elif self.mark == 'c':
            symbol = 'Carib'
        elif self.mark == 'y':
            symbol = '1pond'
        else:
            symbol = symbol.title()
        return "{}-{}-{} {}".format(symbol, middle, xuhao, leftover)


###############################################################
receptionist = F63(r'/Volumes/ToshibaCanvio/lake/ru', 'c')
count = receptionist.start()
if count:
    for t in receptionist.tasks():
        print(t)
    print('共有{}个任务'.format(count).center(50, '*'))
    confirm = input('是否确认？')
    if confirm:
        while receptionist.tasks():
            srcing, dsting = receptionist.tasks.take()
            os.rename(srcing, dsting)
    else:
        print('\n已取消')
else:
    print('全部整理好了，无需再处理')

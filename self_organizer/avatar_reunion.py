# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:avatar_reunion.py
Author:
Version:2.1
Description:
    - 此版本删除上个版本中多余的可供学习参考使用的类或函数
    — 移植了Describer类实现网络资源获取
"""
import os
import re
import requests
import threading
from random import choice
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from common_use import Constant
from common_use import Jp
from common_use import Headers


# 单例装饰器
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class Scan:
    def __init__(self, code):
        self.__soup = BeautifulSoup(code, 'lxml')
        self.info = dict()
        # 开始扫描
        self.__scan()

    def __scan(self):
        self.info.setdefault('title', self.__get_title())
        self.info.setdefault('image', self.__get_image())

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


class Describer:
    def __init__(self, symbol):
        host = choice(Jp.HOSTS)  # 随机选择一个base_url
        page = requests.get(urljoin(host, symbol), headers=Headers.HEADERS)  # 引入头信息设置
        if page:
            page.encoding = 'utf-8'
            sourcecode = page.text
            self.info = Scan(sourcecode).info
        else:
            self.info = dict()


@singleton
class TodoList:
    """采用单线程时，你并不知道任务总量有多少
    因此首先把整体的任务列出来，再分别处理掉，同时可以掌握进度
    队列无上限，或设置一个很高的上限
    所有对象共用一张TodoList，因此本类采用单例模式
    """

    def __init__(self):
        self.__todo = []  # 初始化任务列表

    def add_task(self, task):
        self.__todo.append(task)

    def take_task(self):
        if not self.isempty():  # 还有任务可以领
            """do something"""
            task = self.__todo.pop(0)  # 弹出任务，并return这个任务
            return task
        else:  # 没有任务了
            raise TaskError('No Task Left.')

    def isempty(self):
        if any(self.__todo):
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        """可能启动多线程的点"""
        return self.__todo

    def __getitem__(self, item):
        return self.__todo[item]

    def __len__(self):
        return len(self.__todo)


class TaskError(Exception):
    def __init__(self, note):
        self.note = note

    def __str__(self):
        return self.note


class Fetch:
    """连接互联网，去拿图片回来"""

    def __init__(self, task=('', '')):
        self.keyword, self.savepath = task
        desc = Describer(self.keyword).info
        self.target = desc.get('image')  # 目标资源的URL
        self.title = self.truncate(desc.get('title'))  # 下到本地的文件名(不含扩展名)
        self.retrieve()

    def retrieve(self):  # 等同于recover()
        """使用requests.get()把目标url资源下载到指定位置的方法"""
        dst = self.savepath + os.sep + self.title + os.path.splitext(self.target)[1]
        telefile = requests.get(self.target, headers=Headers.HEADERS)
        with open(dst, 'wb') as localfile:
            localfile.write(telefile.content)  # 写入文件，完成！
        telefile.close()

    @staticmethod
    def truncate(txt='', max_length=50, abbreviation='...'):
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

    def __del__(self):
        """"""
        # print('%s任务完成' % self.keyword)


class Match:
    """"""
    VIDEO = ['.mp4', '.avi', '.rmvb', '.mkv', '.wmv']
    IMAGE = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']

    def __init__(self, path):
        self.img_pool = []
        self.todo = TodoList()  # 初始化多线程任务列表
        self.engine(path)  # 自动运行engine()

    def engine(self, pathname=r''):
        """engine()只遍历包含文件夹和视频文件名称的列表"""
        if not os.path.isdir(pathname):
            exit('路径不存在或路径并非是一个目录.')
            # return  # 将会得到一个空的指令集
        for file in self.__branch(pathname):
            filepath = os.path.join(pathname, file)
            if os.path.isfile(filepath):  # 这里的file已经只有视频的类型了
                self.pairing(filepath)
            elif os.path.isdir(filepath):
                self.engine(filepath)  # 递归

    def __branch(self, pathname):
        """分流，只留视频文件和本层文件夹，以供engine遍历"""
        vs = []
        dirs = []
        imgs = []
        files = os.listdir(pathname)
        for file in files:
            if self.exceptions(file):  # 封装了一个去掉例外的函数
                continue
            filepath = os.path.join(pathname, file)  # 前头拼接上路径
            # 是文件，且有内容，空文件不行。规避了写入失败却留下空文件影响下一轮的判断
            if os.path.isfile(filepath) and os.path.getsize(filepath):
                suffix = os.path.splitext(file)[1]  # 文件扩展名
                if suffix in self.VIDEO:
                    vs.append(file)
                elif suffix in self.IMAGE:
                    imgs.append(file)
            elif os.path.isdir(filepath):
                dirs.append(file)  # 只带了纯目录名，没有带路径
        # 分别对各支流进行处理
        dirs.sort()
        vs.sort()
        self.img_pool = [self.mark_out(i) for i in imgs]  # 把比对库剥离出标志
        # 注意：return的顺序(先文件后目录)要与engine()中遍历时对文件或目录的判断顺序一致
        # 否则img_pool发生错位
        return vs + dirs

    def pairing(self, filepath):
        """
        几经过滤，传进来的一定是视频后缀的文件路径
        1、判断是否存在与之对应的图片文件。如果没有，继续第2步
        2、用于执行联网Fetch任务的关键信息有：
            1、识别码
            2、原标的文件所在的路径，以便保存回原来的目录
        :param filepath:整段文件路径
        :return: None
        """
        pure_path = os.path.split(filepath)[0]  # 文件所在目录
        pure_name = os.path.split(filepath)[1]  # 文件名+扩展名
        # 由于mark_out()方法设计的原因，当文件名不具备标志时，会原样输出
        # 这种情况下不能带着文件路径一块传出去，因此多声明一个pure_name
        v_mark = self.mark_out(pure_name)  # 剥离出标的对象的标志
        if v_mark not in self.img_pool:  # 与比对库进行比对，说明不存在相应的文件
            # 过滤掉因mark_out()原样输出造成v_mark不符合符合标准格式的情况
            if not re.search(r'^[a-z]{2,}-\d{3,}', v_mark, re.I):
                return
            # 进入关键环节
            instructions = v_mark, pure_path  # 关键指令！！！
            self.todo.add_task(instructions)  # 添加任务指令 -> tuple
        else:  # 相对应的文件存在时
            pass

    @staticmethod
    def exceptions(filename):
        """以下任意一项为True，则返回True"""
        # filename以.或_开头
        if filename.startswith('.') or filename.startswith('_'):
            return True
        # filename里有rids出现
        rids = [
            'cari', '1pon', 'paco', 'mywife', 'luxu', 'dic',
            'gkd', 'hmpd', 'nacr'
        ]
        for r in rids:
            if r in filename.lower():
                return True
        return False

    @staticmethod
    def mark_out(text):
        """在text中剥离出标志"""
        ptn = r'^[a-z]{2,}-\d{3,}'  # 标志的正则
        try:
            mark = re.findall(ptn, text, re.I)[0]
            return mark
        except IndexError:
            return text  # 注意，如果找不到合格的标志，则返回原本的text


class Reunion:
    """多线程"""
    i = 0

    def __init__(self, root_dir):
        self.reunion = Match(root_dir)
        self.todo = self.reunion.todo()  # for easily use
        self.__pool_threads = []
        if self.todo:
            print('查看任务列表：')
            for t, d in self.todo:
                print('{:\t<8} =>\t{}'.format(t, d))
            print('任务个数共计:', self.todo.__len__())
            num_thread = input('需要开启几个线程？')
            if num_thread:
                if num_thread.isdigit():
                    self.load_thread(int(num_thread))  # 加载线程
                    print('下面依次处理各项任务'.center(50, '*'))
                    self.start()
                    # 等所有线程结束
                    print(' 主程序END '.center(50, '='))
                else:
                    raise TypeError('必须输入纯数字')
            else:
                print('Mission Abort.')
        else:
            print(' Hooh! Already United! '.center(50, '='))

    def load_thread(self, n=1):
        # 线程的数目以任务量多少和最大线程数中较小的为准
        for i in range(min(n, self.todo.__len__())):
            self.__pool_threads.append(threading.Thread(target=self.unit, args=()))

    def start(self):
        if self.__pool_threads:
            print('共开启线程{}个'.format(self.__pool_threads.__len__()))
            for thrd in self.__pool_threads:
                thrd.start()
            for thrd in self.__pool_threads:
                if thrd.is_alive():
                    thrd.join()

    def unit(self):
        while self.todo:
            self.i += 1
            task = self.reunion.todo.take_task()  # 取出一项任务
            print('{:0>3} 正在将{} 的资源下载到{}'.format(self.i, task[0], task[1]))
            Fetch(task)


#######################################
Reunion(Constant.SEAGATE)  #
#######################################

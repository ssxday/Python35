# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:avatar_reunion.py
Author:
Version:2.0
Description:
- 2.0版本实现了跨越式发展，在1.1版本的基础上，使用了多线程处理任务，使得执行效率大大提高
"""
import random
import os
import re
import http.client as hct
import urllib.request as uq
import requests
import html.parser
import threading
from common_use import Constant


# 单例装饰器
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class TodoList:
    """采用单线程时，你并不知道任务总量有多少
    因此首先把整体的任务列出来，再分别处理掉，同时可以掌握进度
    队列无上限，或设置一个很高的上限
    所有对象共用一张TodoList，因此本类采用单例模式
    """

    def __init__(self):
        self.__todo = []  # 初始化任务列表

    # 在Match.pairing()中调用
    def add_task(self, task):
        self.__todo.append(task)

    # 在Dispatch.start()中被调用
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


class MyHTMLParser(html.parser.HTMLParser):
    """解析网络数据的源代码，定位目标"""

    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.target = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            if ('class', 'bigImage') == attrs[0]:
                href, url = attrs[1]
                self.target = url  # 成功定位目标资源url
                # 警告警告警告：handle_系列函数只能设置找到了怎么办
                # 不能设置找不到怎么办，因为：
                # 找到了之后parser还可能重复调用本方法
                # 把原本处理好的数据丢弃，比如下面这个else，将把self.target擦掉
                # else:  # 并没有找到目标资源的url
                #     self.target = ''  # 这个值将在Fetch.pickup()被Fetch.target引用

    # 构造一个上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Fetch:
    """连接互联网，去拿图片回来，利用多线程"""
    user_agents = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    ]

    def __init__(self, task=('', '')):
        self.keyword, self.savepath = task
        self.HOST = Constant.AVATAR_HOST  # 用https包请求网络资源不需要加https协议前缀
        self.hcc = None  # 准备HTTPConnection
        self.parser = None  # 准备解析互联网上返回的源代码
        self.target = ''  # 目标资源的URL

        # self.fetch(self.keyword)  # 初始化调用fetch()
        self.fetch1(self.keyword)  # 二选一

    def fetch(self, keyword):  # 等同于fetch1
        """获取网络资源"""
        request = os.sep + keyword
        self.hcc = hct.HTTPSConnection(self.HOST, 443)  # 连接服务器对象(HTTPS协议)
        self.hcc.request('GET', request)  # 请求数据
        with self.hcc.getresponse() as resp:
            data = resp.rread().decode()
            self.pickup(data)  # 把取回来的数据交给pickup()处理
        self.hcc.close()

    def fetch1(self, keyword):  # 等同于fetch
        """使用requests包获取网络资源"""
        requesturl = r'https://' + self.HOST + os.sep + keyword
        r = requests.get(requesturl)
        data = r.content.decode()
        r.close()
        self.pickup(data)

    def pickup(self, data):
        """从带回来的数据data里找出所需资源的url"""
        with MyHTMLParser() as self.parser:  # 自定义的上下文管理器，HTMLParser自身并不是
            self.parser.feed(data)  # 自定义解析器开始工作
            self.target = self.parser.target  # 从解析器对象里拿到目标url
        # 因为互联网因素，这个值有可能取到一个空字符串，因此要做一个判断
        if self.target:
            # self.recover()  # 把远程资源下载到指定位置
            self.retrieve()  # 把远程资源下载到指定位置，二选一
        else:
            print('未能通过指令获取到{}的URL'.format(self.keyword))

    def recover(self):  # 等同于retrieve()
        """使用urllib.request.urlopen()把目标url资源下载到指定位置"""
        hdr = {  # 头信息
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        dst = self.savepath + os.sep + self.keyword + os.path.splitext(self.target)[1]
        req = uq.Request(self.target, headers=hdr)  # 设置详细的请求，重点是头信息
        with uq.urlopen(req) as telefile:
            with open(dst, 'wb') as localfile:
                localfile.write(telefile.rread())  # 写入文件，完成！

    def retrieve(self):  # 等同于recover()
        """使用requests.get()把目标url资源下载到指定位置的方法"""
        dst = self.savepath + os.sep + self.keyword + os.path.splitext(self.target)[1]
        telefile = requests.get(self.target)
        with open(dst, 'wb') as localfile:
            localfile.write(telefile.content)  # 写入文件，完成！
        telefile.close()

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
        """比对视频文件在图片池中有无对应，从而得出Todo任务，并添加到TodoList
        几经过滤，传进来的一定是视频后缀的文件路径
        1、判断是否存在与之对应的图片文件。如果没有，继续第2步
        2、实例化TodoList，提交用于执行联网Fetch任务的关键信息
            需要提供的执行信息有：
            1、标志
            2、原标的文件所在的目录，以便保存
        3、。。。
        :param filepath:整段文件路径
        :return:
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
            'cari', '1pon', 'paco', 'heyzo', 'mywife', 'luxu', 'dic',
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
Reunion(Constant.LAKESSD)  #
#######################################

# -*- coding:utf-8 -*-
import os
import re
import http.client as hct
import urllib.request as uq
import html.parser
import threading


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
        self.todo = []  # 初始化任务列表

    # 在Match.pairing()中调用
    def add_task(self, task):
        self.todo.append(task)

    # 在Dispatch.start()中被调用
    def take_task(self):
        if not self.isempty():  # 还有任务可以领
            """do something"""
            task = self.todo.pop(0)  # 弹出任务，并return这个任务
            return task
        else:  # 没有任务了
            raise TaskError('No Task Left.')

    def isempty(self):
        if any(self.todo):
            return False
        else:
            return True

    def __call__(self, *args, **kwargs):
        """可能启动多线程的点"""
        return self.todo

    def __getitem__(self, item):
        return self.todo[item]

    def __len__(self):
        return len(self.todo)


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

    def __init__(self, task=('', '')):
        self.keyword, self.savepath = task
        self.HOST = r'www.javbus3.com'  # 用https包请求网络资源不需要加https协议前缀
        self.hcc = None  # 准备HTTPConnection
        self.parser = None  # 准备解析互联网上返回的源代码
        self.target = ''  # 目标资源的URL

        self.fetch(self.keyword)  # 初始化调用fetch()

    def fetch(self, keyword):
        """获取网络资源"""
        # https://www.javbus3.com/PGD-907
        request = os.sep + keyword
        self.hcc = hct.HTTPSConnection(self.HOST, 443)  # 连接服务器对象(HTTPS协议)
        self.hcc.request('GET', request)  # 请求数据
        with self.hcc.getresponse() as resp:
            data = resp.read().decode()
            # print(data)
            self.pickup(data)  # 把取回来的数据交给pickup()处理
        self.hcc.close()
        # print('发出的请求是：', request)

    def pickup(self, data):
        """从带回来的数据data里找出所需资源的url"""
        with MyHTMLParser() as self.parser:  # 自定义的上下文管理器，HTMLParser自身并不是
            self.parser.feed(data)  # 自定义解析器开始工作
            self.target = self.parser.target  # 从解析器对象里拿到目标url
        # 因为互联网因素，这个值有可能取到一个空字符串，因此要做一个判断
        if self.target:
            self.recover()  # 把远程资源下载到指定位置
        else:
            print('未能通过指令获取到{}的URL'.format(self.keyword))

    def recover(self):
        """把目标url资源下载到指定位置"""
        hdr = {  # 头信息
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        dst = self.savepath + os.sep + self.keyword + os.path.splitext(self.target)[1]
        req = uq.Request(self.target, headers=hdr)  # 设置详细的请求，重点是头信息
        with uq.urlopen(req) as telefile:
            with open(dst, 'wb') as localfile:
                localfile.write(telefile.read())  # 写入文件，完成！


class Match:
    """"""
    VIDEO = ['.mp4', '.avi', '.rmvb', '.mkv', '.wmv']
    IMAGE = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']

    def __init__(self):
        self.img_pool = []
        self.todo = TodoList()  # 初始化多线程任务列表
        self.engine()  # 自动运行engine()

    def engine(self, pathname=r'/Users/AUG/Desktop/overall'):
        """engine()只遍历包含文件夹和视频文件名称的列表"""
        if not os.path.isdir(pathname):
            exit('路径不存在或路径并非是一个目录.')
            # return  # 得到一个空的指令集
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
            if os.path.isfile(filepath):
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
            # 需要去互联网上找资源
            # print('我要上网去找', v_mark)  # 实时查看
            # print('img_pool是：', self.img_pool)  # 实时查看
            # 进入关键环节
            instructions = v_mark, pure_path  # 关键指令！！！
            self.todo.add_task(instructions)  # 添加任务指令 -> tuple
        else:  # 相对应的文件存在时
            pass

    def exceptions(self, filename):
        """以下任意一项为True，则返回True"""
        # filename以.或_开头
        if filename.startswith('.') or filename.startswith('_'):
            return True
        # filename里有rids出现
        rids = ['cari', '1pon', 'paco', 'heyzo']
        for r in rids:
            if r in filename.lower():
                return True
        return False

    def mark_out(self, text):
        """在text中剥离出标志"""
        ptn = r'^[a-z]{2,}-\d{3,}'  # 标志的正则
        try:
            mark = re.findall(ptn, text, re.I)[0]
            return mark
        except IndexError:
            return text  # 注意，如果找不到合格的标志，则返回原本的text


class Dispatch:
    """"""
    def __init__(self, tasks=TodoList(), n=4):
        """
        #
        :param tasks: expecting a TodoList object
        :param n: 开启的线程数目
        """
        self.todo = tasks  # 把TodoList对象传进来
        self.lines = []  # 初始化线程管理器，n代表同时开n个线程
        i = 1
        while i <= n:
            self.lines.append(threading.Thread)
            i += 1
        # print('这是任务列表对象：', self.todo）
        self.start()  # 千里之行始于足下

    def start(self):
        """当线程集非空的时候，就一直循环
        需要一个机制，当一个线程完成时，判断TodoList是否还有任务
        不需要关心线程集满没满，因为结束的线程会空出自己的位置
        它只要判断还有没有TodoList，并重新调用自己接受新任务
        """
        while self.lines:  # 当还有线程位置的时候
            try:
                task = self.todo.take_task()  # 取到任务指令
                print('拿到一个任务', task)
                # 判断有没有空闲的线程，如果有，加入线程并启动，如果没有，就join()等

                print('完成这个任务', task)
            except TaskError:
                # 说明已经取不到task了 -> 删除已经关闭的线程，否则会一直重复进行最后一个task
                pass

            self.lines.pop()

        print('ALL TASKS COMPLETED.')

    def do(self, task):
        fetch = Fetch(task)
        pass


fc = Match()  # 结果就是最终生成TodoList
td = TodoList()  # TodoList是单例类，确保了各实例的元素完全一致
print('查看任务列表：', td())
print('测试dispatch'.center(50, '*'))
dp = Dispatch()
# print('aaa',dp.lines)
# print('aaa',dp.lines[1]())
# dp.do(('abp-123', '/Users/AUG/Desktop/overall'))  # 成功


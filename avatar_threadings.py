# -*- coding:utf-8 -*-
import os
import re
import http.client as hct
import urllib.request as uq
import html.parser
import threading


class Tasks:
    """"""


class MyHTMLParser(html.parser.HTMLParser):
    """解析网络数据的源代码，定位目标"""

    def __init__(self):
        super(MyHTMLParser, self).__init__()
        self.target = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            if ('class', 'bigImage') == attrs[0]:
                href, value = attrs[1]
                self.target = value

    # 构造一个上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Fetch:
    """连接互联网，去拿图片回来，利用多线程"""

    def __init__(self, mark, savepath):
        self.keyword = mark  # fanhao
        self.savepath = savepath  # 只是纯目录
        self.HOST = r'www.javbus3.com'  # 用https包请求网络资源不需要加https协议前缀
        self.hcc = None  # 准备HTTPConnection
        self.parser = None  # 准备解析互联网上返回的源代码
        self.target = ''  # 目标资源的URL

        self.fetch(mark)  # 初始化调用fetch()

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
        with MyHTMLParser() as self.parser:  # 自定义的上下文管理器，原来没有
            self.parser.feed(data)  # 自定义解析器开始工作
            self.target = self.parser.target  # 从解析器对象里拿到目标url
        self.recover()  # 把远程资源下载到指定位置

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


class Mate:
    """"""
    VIDEO = ['.mp4', '.avi', '.rmvb', '.mkv']
    IMAGE = ['.jpg', '.jpeg', '.gif', '.bmp', '.png']

    def __init__(self):
        self.img_pool = []
        self.fetch = None
        pass

    def engine(self, pathname=r'/Users/AUG/Desktop/overall'):
        """engine()只遍历包含文件夹和视频文件名称的列表"""
        for file in self.__branch(pathname):
            filepath = os.path.join(pathname, file)
            if os.path.isfile(filepath):  # 这里的file已经只有视频的类型了
                self.mating(filepath)
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

    def mating(self, filepath):
        """
        几经过滤，传进来的一定是视频后缀的文件路径
        1、判断是否存在与之对应的图片文件。如果没有，继续第2步
        2、实例化fetch对象去互联网上取相应的文件
            需要对fetch提供的信息有：
            1、标志
            2、原标的文件所在的目录，以便保存
        3、把取回来的文件保存到对应的目录
        :param filepath:整段文件路径
        :return:
        """
        pure_path = os.path.split(filepath)[0]  # 文件所在目录
        pure_name = os.path.split(filepath)[1]  # 文件名+扩展名
        # 由于mark_out()方法设计的原因，当文件名不具备标志时，会原样输出
        # 这种情况下不能带着文件路径一块传出去，因此多声明一个pure_name
        v_mark = self.mark_out(pure_name)  # 剥离出标的对象的标志
        if v_mark not in self.img_pool:  # 与比对库进行比对，说明不存在相应的文件
            # 且 v_mark符合标准格式时
            # if not re.search(r'^[a-z]{2,}-\d*', v_mark, re.I):
            #     return  # 可能会出错
            # 需要去互联网上找资源
            # print('我要上网去找', v_mark)  # 实时查看
            # print('img_pool是：', self.img_pool)  # 实时查看
            # 进入关键环节
            self.fetch = Fetch(v_mark, pure_path)  # 请求互联网数据的开关
        else:  # 相对应的文件存在时
            pass

    def exceptions(self, filename):
        """以下任意一项为True，则返回True"""
        # filename以.或_开头
        if filename.startswith('.') or filename.startswith('_'):
            return True
        # filename里有rids出现
        rids = ['Cari', '1pon', 'paco']
        for r in rids:
            if r in filename:
                return True
        return False

    def mark_out(self, text):
        """在text中剥离出标志"""
        ptn = r'^[a-z]{2,}-\d*'  # 标志的正则
        try:
            mark = re.findall(ptn, text, re.I)[0]
            return mark
        except IndexError:
            return text  # 注意，如果找不到合格的标志，则返回原本的text


fc = Mate()
fc.engine()


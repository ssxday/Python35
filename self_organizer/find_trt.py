# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:2.0
Description:分三个步骤
1、page -> post
2、post -> download 加入多线程
3、download -> torrent暂时存放在文件中(暂未开通)

"""
import requests
from html.parser import HTMLParser
from os.path import join
from bs4 import BeautifulSoup
from random import choice
import re
import xlwt
import threading
from time import sleep


class Config:
    """所需的常量及设置"""
    URL_ROOT = r'http://km.1024ky.trade/pw'
    KEY_WORDS = [
        'manon', 'anniversary'
    ]
    USER_AGENTS = [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 \
        Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0"
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    ]
    HEADERS = {
        'User-Agent': choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml,application/force-download/;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


class Condit:
    AND = ''
    OR = ''
    NOT = ''


class TaskTeam:
    """通用队列类"""

    def __init__(self):
        self.tasks = []  # 没有上限

    def add_task(self, task):
        self.tasks.append(task)

    def take_task(self):
        if self.tasks:
            return self.tasks.pop(0)
        else:
            raise EOFError

    def __call__(self, *args, **kwargs):
        return self.tasks


class Page2PostParser(HTMLParser):
    def __init__(self):
        super(Page2PostParser, self).__init__()
        self.__tasks = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and len(attrs) == 2:
            attrs_in_dict = dict(attrs)
            if attrs_in_dict.get('href', '').startswith(r'htm_data'):
                self.__tasks.append(attrs_in_dict.get('href'))  # 只负责添加

    def __call__(self, *args, **kwargs):
        results = self.__tasks.copy()  # 一定要导出一份copy再clear
        self.__tasks.clear()  # 应对Page2Post.scan_page()中的extend()不要重复添加
        return results


class Page2Post(TaskTeam, Config):
    """本类的实例"""

    def __init__(self, from_page=5, to_page=None):
        super(Page2Post, self).__init__()
        self.parser = Page2PostParser()
        self.engine(from_page, to_page)

    def engine(self, from_page, to_page):
        """"""
        if to_page is None or from_page == to_page:
            to_page = from_page
            step = 1
        else:
            if from_page > to_page:
                step = -1
            else:
                step = 1

        for page_no in range(from_page, to_page + step, step):
            try:
                pagecode = self.pull_request(page_no)
            except:
                print('{} @Page2Post:')
                sleep(2)  # 挂起2秒
                continue
            self.scan_page(pagecode)

    def pull_request(self, which_page):
        """"""
        query_string = r'thread.php?fid=3&page={page}'.format(page=which_page)
        url = join(self.URL_ROOT, query_string)
        # print(url)
        page = requests.get(url, headers=self.HEADERS)
        page.encoding = 'utf-8'
        source_code = page.text
        return source_code

    def scan_page(self, data):
        self.parser.feed(data)  # 把当前页的所有帖子地址加入到task队列
        # 把task队列搬到当前对象的__task，已继承队列属性
        self.tasks.extend(self.parser())


class Post2Download(TaskTeam, Config):
    """"""

    def __init__(self, query, showall=True):
        """query从Page2Post的队列中取"""
        super(Post2Download, self).__init__()
        # 是否每一步都要打印出来
        self.show_all = showall
        # 拼接帖子链接
        self.url = join(self.URL_ROOT, query)
        try:  # 获取帖子的源代码
            source_code = self.pull_request(self.url)
            # 扫描分析帖子源代码
            self.scan_post(source_code)
        except:
            print('{} @Post2Download')
            sleep(2)

    def pull_request(self, url):
        """发起请求，得到帖子内容并返回内容"""
        if self.show_all:
            print('正在处理帖子 {}'.format(url))
        page = requests.get(url, headers=self.HEADERS)
        page.encoding = 'utf-8'  # 设置编码
        text = page.text
        return text

    def scan_post(self, source_code):
        """从post定位到download页面"""
        soup = BeautifulSoup(source_code, 'lxml')
        # 定位到主体div
        the_div = soup.find('div', attrs={'class': "tpc_content", 'id': "read_tpc"})
        for sub_str_elem in the_div.strings:
            if self.washing(sub_str_elem, *self.KEY_WORDS):  # 选择的策略都在washing里
                for sibling in sub_str_elem.next_siblings:
                    if sibling.name == 'a' and sibling['href'] == sibling.string:
                        if sibling.string not in self.tasks:
                            landing_url = str(sibling.string)  # 下载着陆页的url
                            title = self.name_quot(str(sub_str_elem))  # 去掉不能出现在文件名的符号
                            # 控制打印显示
                            if not self.show_all:
                                print('当前处理帖子 {}'.format(self.url))
                                print(title, landing_url, '\n')
                            else:
                                print(title, landing_url)
                            self.add_task((title, landing_url))
                        break

    @staticmethod
    def name_quot(txt):
        """把不适合做文件名的符号用-替换掉
        """
        reg = re.compile(r'[｜|?？，、:*/\\]+')
        cleaned = reg.sub('-', txt)
        return cleaned

    @staticmethod
    def washing(sands, *golds):
        """
        从sands中检查gold是否存在,强制转换sands为字符串，不区分大小写。
        :param sands:expecting 字符串
        :param golds:目标
        :return:gold只要出现任何一个，返回True，否则返回False
        """
        for g in golds:
            if str(g).lower() in sands.lower():
                return True
        return False

    @staticmethod
    def conditions(sand=''):
        """washing的替换"""
        sand = sand.lower()
        if Condit.NOT in sand:
            return False
        else:
            for o in Condit.OR:
                if o in sand:
                    return True
                else:
                    return False
            return True


class Start:
    """协调者"""
    thrds = []  # 线程池

    def __init__(self, from_page=5, to_page=None, showall=False):
        self.to_xls_data = []  # 数据为items()格式
        # 实例化同时把指定页码的所有帖子链接全部存进自身队列
        self.page2post = Page2Post(from_page, to_page)
        num_to_thread = input('共有{}个帖子需要扫描,需要开启几个线程：'.format(self.page2post().__len__()))
        # 初始化多线程
        for i in range(int(num_to_thread)):
            self.thrds.append(threading.Thread(target=self.unit, args=(showall,)))
        self.do()

    def do(self):
        if self.thrds:
            for thd in self.thrds:
                thd.start()
            for thd in self.thrds:
                if thd.is_alive():
                    thd.join()

    def unit(self, showall):
        while self.page2post():
            query = self.page2post.take_task()
            try:
                # 完成一个帖子的检查后，要把收集到的数据通过调用自身的方法传递出来
                post2download = Post2Download(query, showall)  # 成功
            except:
                post2download = lambda x='': []
                continue  # 一定要保证循环能结束，因为任何一个线程不结束，程序都进行不下去
            self.to_xls_data.extend(post2download())

    @staticmethod
    def to_xls(data=list()):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        # 遍历to_xls_data
        for r in range(data.__len__()):  # 行
            for c in range(2):  # 列
                worksheet.write(r, c, data[r][c])
        workbook.save('/Users/aug/Desktop/essence.xls')

    def __del__(self):
        print('\n扫描完成！正在写入Excel文件...')
        self.to_xls(self.to_xls_data)
        print('Excel文件写入成功.')


###############################
Start(1, 5, showall=True)  #
###############################


# 以下为试验区
class Downloader(Config):
    def download(self):
        """进入download页面拿到目标地址然后下载资源到本地"""
        url = 'http://www2.j32048downhostup9s.info/freeone/down.php'
        data = {
            'type': 'torrent',
            'name': 'OJGSOWr',
            'id': 'OJGSOWr'
        }
        resp = requests.post(url, data=data, headers=self.HEADERS)
        print(1, resp.status_code)
        content = resp.content
        print(2, resp.status_code)
        with open('/users/aug/desktop/testhaha.torrent', 'wb') as f:
            f.write(content)

# d = Downloader()  # 并不成功
# d.download()

# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:find_trt.py
Version:3.0
Description:
-使用方法：
step1：set your rules by Conditions(v,o,a)
    v is a string containing words that should never appear in final result.
    o is a string containing some words, as long as which shows, the line will be chosen.
    a is a string containing words, all of which have to be in the line, so that the line will be chosen.
step2: start the scanner by Start(frompage,topage,showall)

-设计思路：
1、page -> post post可进行Redis缓存
2、post -> download 加入多线程
3、download -> torrent暂时存放在文件中(暂未开通)

- 3.0 重大更新：加入了Redis缓存

- 分词算法更新：优化了过滤数据的算法，支持多种与或非多种条件同时筛选
把英文单词与其他语言分开处理：英文单词以单词列表存在，而其他语言仍然以字符串存在
这样在匹配关键词时，相连的中英文混杂字符串清晰的被分开
"""
import re
import xlwt
import threading
import requests
import redis
from os.path import join
from bs4 import BeautifulSoup
from random import choice
from time import sleep
from common_use import RedisConf


# 单例装饰器
def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


class Config:
    """所需的常量及设置"""
    URL_ROOT = r'http://t3.9laik.click/pw'
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


@singleton
class Conditions:
    """设置过滤关键词的条件
    每一项条件以空格分开
    """
    __HISTORY_ = [
        'blacked', 'colette', 'heyzo', 'Kristen Lee', 'Eva Lovia', 'Moka Mora', 'Haley Reed',
        'Cadence Lux', 'Anya Olsen', 'Stella Cox', 'Lyra Law', 'sweet cat', 'Lucy Heart',
        'Tiffany Watson', 'Lana Rhoades', 'Marina Woods'
    ]

    def __init__(self, v='', o='', a=''):
        self.__veto = v  # veto
        self.__any = o  # any
        self.__all = a  # all

    @property
    def veto(self):
        if self.__veto:
            return self.__veto.strip().lower().split(' ')

    @veto.setter
    def veto(self, v):
        self.__veto = v

    @property
    def any(self):
        if self.__any:
            return self.__any.strip().lower().split(' ')

    @any.setter
    def any(self, o):
        self.__any = o

    @property
    def all(self):
        if self.__all:
            return self.__all.strip().lower().split(' ')

    @all.setter
    def all(self, a):
        self.__all = a

    def __str__(self):
        s = ''
        if self.__veto:
            s += '排除' + self.__veto
        if self.__any:
            s += '任意' + self.__any
        if self.__all:
            s += '同时满足' + self.__all
        return s

    def __call__(self):
        """调试用，调用实例看详情"""
        print('NOT', self.veto)
        print('OR ', self.any)
        print('AND', self.all)


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


class RCache:
    """Redis缓存"""

    def __init__(self, mark='', expire=1800):
        self.__mark = mark
        self.__expire = expire
        self.__redis = redis.StrictRedis(db=0, password=RedisConf.AUTH)

    def in_service(self):
        try:
            try:
                return self.__redis.ping()
            except Exception:
                raise SomethingWrong('Redis Not In Service')
        except SomethingWrong:
            return False

    def exists(self):
        return self.__redis.exists(self.__mark)

    def get(self):
        return [i.decode() for i in self.__redis.lrange(self.__mark, 0, len(self))]

    def add(self, *items):
        self.__redis.rpush(self.__mark, *items)
        self.__redis.expire(self.__mark, self.__expire)  # 缓存有效期

    def clear(self):
        """清除缓存"""
        self.__redis.delete(self.__mark)

    def __len__(self):
        return self.__redis.llen(self.__mark)


class SomethingWrong(Exception):
    def __init__(self, note='something wrong occurred'):
        self.note = note

    def __str__(self):
        return self.note


class Page2Post(TaskTeam, Config):
    """本类的实例"""

    def __init__(self, from_page=5, to_page=None):
        super(Page2Post, self).__init__()
        mark = '{}:{}'.format(from_page, to_page)
        self.__rcache = RCache(mark)
        if self.__rcache.in_service():
            # redis开启
            # 查找有无对应的mark数据
            if self.__rcache.exists():  # 有
                # 调用数据
                print('从Redis缓存中获取数据')
                self.tasks.extend(self.__rcache.get())
            else:  # 2、没有
                # 启动engine，同时往redis里添加数据
                print('缓存中没有相应数据，将启动engine')
                self.engine(from_page, to_page)
        else:  # redis服务没有开启
            print('Redis缓存服务器没有开启')
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
            except AssertionError:
                print('第{}页发生错误@Page2Post'.format(page_no))
                sleep(2)  # 挂起2秒
                continue
            self.scan_page(page_no, pagecode)

    def pull_request(self, which_page):
        """"""
        query_string = r'thread.php?fid=3&page={page}'.format(page=which_page)
        url = join(self.URL_ROOT, query_string)
        # print(url)
        page = requests.get(url, headers=self.HEADERS, )
        assert page
        page.encoding = 'utf-8'
        source_code = page.text
        return source_code

    def scan_page(self, page_no, data):
        # 把task队列搬到当前对象的__task，已继承队列属性
        soup = BeautifulSoup(data, 'lxml')
        post_tags = soup.find_all('a', {'title': '打开新窗口', 'target': '_blank'})
        if post_tags:
            post_suffixes = [tag.get('href', '') for tag in post_tags]
            self.tasks.extend(post_suffixes)
            if self.__rcache.in_service():
                # redis开着，顺便放进redis去缓存
                self.__rcache.add(*post_suffixes)
        else:
            raise SomethingWrong('第{}页没有符合条件的帖子@Page2Post'.format(page_no))


class Post2Download(TaskTeam, Config):
    """"""
    re_punc = re.compile(r'[- .?？！!;；:：,，。_/\\()\[\]【】\s\xa0]+')
    re_alphabet = re.compile(r"[a-z']+", re.I)  # 目标处理前已全部小写

    def __init__(self, query, showall=True):
        """query从Page2Post的队列中取"""
        super(Post2Download, self).__init__()
        self.__filter = Conditions()  # 实例化要筛选的关键字对象
        # 是否每一步都要打印出来
        self.show_all = showall
        # 拼接帖子链接
        self.url = join(self.URL_ROOT, query)
        try:  # 获取帖子的源代码
            source_code = self.pull_request(self.url)
            # 扫描分析帖子源代码
            self.scan_post(source_code)
        except AssertionError:
            print('{} @Post2Download'.format(self.url))
            sleep(2)

    def pull_request(self, url):
        """发起请求，得到帖子内容并返回内容"""
        if self.show_all:
            print('正在处理帖子 {}'.format(url))
        page = requests.get(url, headers=self.HEADERS)
        assert page
        page.encoding = 'utf-8'  # 设置编码
        text = page.text
        return text

    def scan_post(self, source_code):
        """从post定位到download页面"""
        soup = BeautifulSoup(source_code, 'lxml')
        # 定位到主体div
        the_div = soup.find('div', attrs={'class': "tpc_content", 'id': "read_tpc"})
        for sub_str_elem in the_div.strings:
            if self.washing(sub_str_elem):  # 选择的策略都在washing里
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

    def washing(self, sand=''):
        # sand在这里被分词，成为列表
        eng, other = self.segments(sand)
        # print(sands)
        # 首先过滤NOT
        if self.__filter.veto:  # 非None
            for n in self.__filter.veto:
                if n in eng or n in other:
                    # print(1)
                    return False
        # 其次过滤OR
        if self.__filter.any:
            for o in self.__filter.any:
                if o in eng or o in other:
                    # print(2)
                    return True
        # 最后过滤AND
        if self.__filter.all:
            for a in self.__filter.all:
                if not (a in eng or a in other):
                    # print(3)
                    return False
            # print(4)
            return True
        # 当没有设置任何条件时
        return False

    def segments(self, txt=''):
        """
        :return 英文以单词列表的形式，其他语言以字符串形式，构成元组([list], 'str')
        """
        txt = txt.lower()  # 全部小写
        eng = self.re_alphabet.findall(txt)  # 英文分词完成
        without_eng = self.re_alphabet.sub('', txt)  # 除了英文剩余的语言和标点
        leftover = self.re_punc.sub('', without_eng)  # 再去掉标点符号
        return eng, leftover


class Start:
    """协调者"""
    thrds = []  # 线程池

    def __init__(self, from_page=5, to_page=None, showall=False):
        self.to_xls_data = []  # 数据为items()格式
        # 实例化同时把指定页码的所有帖子链接全部存进自身队列
        self.page2post = Page2Post(from_page, to_page)
        if self.page2post():  # 对象内部的队列中有内容
            num_to_thread = input('共有{}个帖子需要扫描,需要开启几个线程：'.format(self.page2post().__len__()))
            # 初始化多线程
            for i in range(int(num_to_thread)):
                self.thrds.append(threading.Thread(target=self.unit, args=(showall,)))
            self.do()
            print('\n扫描完成！正在写入Excel文件...')
            self.to_xls(self.to_xls_data)
            print('Excel文件写入成功.')
        else:  # 对象内部的队列中没有内容
            print(' 未找到可以扫描的帖子，程序结束 '.center(50, '='))

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
            except ConnectionResetError:  # 可能漏洞
                print('something wrong happened @unit()')
                self.page2post.add_task(query)  # 把做错的任务再放回去
                sleep(2)
                continue  # 一定要保证循环能结束，因为任何一个线程不结束，程序都进行不下去
            self.to_xls_data.extend(post2download())
            sleep(1)

    @staticmethod
    def to_xls(data=list()):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        # 遍历to_xls_data
        for r in range(data.__len__()):  # 行
            for c in range(2):  # 列
                worksheet.write(r, c, data[r][c])
        workbook.save('/Users/aug/Desktop/essence-{}.xls'.format(str(Conditions())))

    def __del__(self):
        """"""


###########################################
if __name__ == '__main__':
    print(Conditions(o='blacked', a='kendra sunderland'))
    Start(1, 12, showall=False)
###########################################

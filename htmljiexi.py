# -*- coding:utf-8 -*-
import html.parser as hp
from urllib.request import urlopen
page = urlopen('http://localhost/code/inno.php').read().decode()
print(page)
help(hp.HTMLParser)
class MyHParser(hp.HTMLParser):  # 一定要继承HTMLParser
    # hp.HTMLParser.handle系列
    def handle_starttag(self,tag,attr):  # 重载的方法必须跟原方法参数对应
        if tag == 'form':
            print('我他妈的找到了！')

    def handle_data(self,data):
        pass

    def handle_endtag(self,tag):
        pass

    def handle_startendtag(self,tag,end):
        pass

    # 构造一个上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# p = MyHParser()
# print('HTMLParser实例：', p)
# chifan = p.feed(page)  # 事件驱动
# print('喂饱了',chifan)  # None，print毫无疑义
# p.close()  # 有开始就有结束，那么可以同时把MyHParser做成一个做一个上下文管理器

# 使用上下文管理器
with MyHParser() as p:  # 同上效果
    print('HTMLParser实例：', p)
    p.feed(page)
    print('吃饱了！')






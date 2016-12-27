# -*- coding:utf-8 -*-
from urllib.request import *  # urllib.request里的变量，函数和类直接用
# 通过用户名密码访问http资源
# help(FancyURLopener.open)
class MyOpener(FancyURLopener):
    def __init__(self,username=None,password=None):
        super(MyOpener, self).__init__()
        # 既可以通过构造方法设置用户名密码，
        # 也可以在实例化之后，open()之前，通过setAuth()设置
        self.setAuth(username,password)

    def get_user_passwd(self, host, realm, clear_cache=0):
        return self.username,self.password

    def setAuth(self,username,password):
        self.username = username
        self.password = password

myopener = MyOpener()
print('中间层开瓶器：', myopener)
# 自定义头信息,addheader方法给自己添加的 发送给服务器的 头信息，
# 而不是服务器返回来的HTTPResponse的头信息
# 在调用open()方法之前
print('自己添加头信息：√')
myopener.addheader('fucker','son of a bitch')
myopener.addheader('wearing','condom')
myopener.addheader('User-Agent','Mozilla hahahaha')
myopener.addheader('Accept', 'sound/basic')
# version属性 即User-Agent，发送方的属性
# 而HTTPResponse.header属性是收到人家发过来的信息的属性
print('version属性：',myopener.version)
# help(FancyURLopener)


page = myopener.open('http://localhost/code/inno.php')
print('用opener打开的资源：',page)
print(page.headers)

# 直接用urlopen() 对照组
zy = urlopen('http://localhost/code/inno.php')
print('直接用urlopen()打开的资源：',zy)




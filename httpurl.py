# -*- coding:utf-8 -*-
# urllib.request
print(' urllib.request模块 '.center(50, '*'))
import urllib.request

# 运用urlopen() -> 获取网页源代码
theurl = r'http://localhost/code/inno.php'  # 一定要指明http协议
page = urllib.request.urlopen(theurl)
print(page)  # 返回HTTPResponse对象
print(page.readlines())  # read() 返回字节串，需要decode()转换为字符串
# print(page.read().decode())

# geturl()方法：
print('HTTPResponse对象的geturl()方法:',page.geturl())
# url属性
print('HTTPResponse对象的url属性：',page.url)

# localhost() -> 返回本机做localhost的IP地址
lh = urllib.request.localhost()
print('localhost IP：', lh)  # string
# thishost() -> 返回路由器给本机分配的IP地址
thst = urllib.request.thishost()
print('路由器分配的IP地址数据：', thst)  # tuple

# urlretrieve() -> 把URL保存为本地文件@临时文件夹。
# 返回tuple(临时文件路径, http.client.HTTPMessage对象)
obj = urllib.request.urlretrieve(theurl,'/Users/AUG/Desktop/myretrievtemp.txt',)
print('urlretrieve:', obj)
# urlretrieve()的reporthook参数
# reporthook必须是可调用的，格式是设定好的，包含3个参数
# 反正系统在调用reporthook时就传着三个实参，怎么处理形参就是自己的事了
def reporthk(block_count,block_size,file_size):
    if file_size == -1:
        print('无法获取资源信息')
    else:
        print('已经获取到进度%d / %d'%(block_count*block_size,file_size))

print('使用reporthook：')
obj = urllib.request.urlretrieve(
    r'http://www.sina.com.cn',
    '/Users/AUG/Desktop/myretrievtemp.txt',
    reporthook=reporthk)
print('retrieve结束')

# urlcleanup() -> 把urlretrieve()生成的临时文件删除
# 只能删这一次生成的文件，因此需要跟urlretrieve()成对出现
# print('cleanup:', urllib.request.urlcleanup())  # 无返回值，None

# urllib.parse模块：用于解析URL
print(' urllib.parse模块：用于解析URL '.center(50, '*'))
import urllib.parse

myurl = 'ftp://www.localhost.net:8080/index.php?wd=upper&name=tom#cost'
# urlencode(query, doseq=False)
uquery = urllib.parse.urlencode({'wd': 'wocao', 'partner': '操', 'condom': '戴'})
print(uquery)  # 是一个字符串
# 当doseq=True时，键还是键，值可以是一个可以迭代的序列
uquery = urllib.parse.urlencode({'wd':('step1','step2','step3')},True)
print('doseq=True的情况：',uquery)

# urlsplit() -> tuple <scheme>://<netloc>/<path>?<query>#<fragment>
parts = urllib.parse.urlsplit(myurl)
print(parts)

# urlparse()
parts = urllib.parse.urlparse(myurl)
print(parts)

# urldefrag() -> 返回tuple(#前的url,#后的fragment)
du = urllib.parse.urldefrag(myurl)
print(du)

# urljoin(base, url)
joulr = urllib.parse.urljoin('http://www.baidu.com','so/s?wd=hello')
print('拼接URL',joulr)

# quote()和quote_plus() -> 返回被urlencode了的整个url字符串，
# 区别于urlencode()只是处理query键值对
uqt = urllib.parse.quote(myurl)
print('Original str:', myurl)
print('Quoted string:', uqt)

# splittag()
stg = urllib.parse.splitport('localhost:8080')
print(stg)

# urllib.robotparser模块
print(' urllib.robotparser：用于解析robot.txt '.center(50, '*'))
# import urllib.robotparser

# http.client模块
import http.client

# http.client.HTTPConnection类
print(' http.client模块.HTTPConnection类: '.center(50, '*'))

# 类要先实例化HTTPConnection类！！！
httpconn = http.client.HTTPConnection(r'www.baidu.com', 80)
# request()方法 -> 纯命令，向服务器发送request，程序会挂在这里等回应
httpconn.request('GET', '/s?wd=red')  # 纯命令，无返回，None
# getresponse()方法 -> 刚刚发出了request，本方法用来接收对方回应
resp = httpconn.getresponse()  # 收到的是一个HTTPResponse对象
print('远程的回应:', resp)  # resp就是一个HTTPResponse对象
# http.client.HTTPResponse类
print(' http.client模块.HTTPResponse类: '.center(50, '*'))
print('verson:%s\nstatus:%s\nreason:%s' %
      (resp.version, resp.status, resp.reason))
# help(resp)
# print(resp.read().decode())

# http.client.HTTPMessage类
print(' http.client.HTTPMessage对象 '.center(50,'*'))
# HTTPResponse对象的info()方法或headers属性即可得到一个HTTPMessage对象
msgobj = resp.headers  # response的头信息
print(type(msgobj))  # <class 'http.client.HTTPMessage'>
print('直接打印输出msgobj对象:\n',msgobj)
print('Message对象.items()方法:\n',msgobj.items())  # 类似字典的items()
# 纯dict操作：可更改头信息输出的格式
# for k,v in msgobj.items():
#     print('%s\t%s'%(k,v))

# 对部分头信息进行的封装
print('\n对部分头信息进行的封装:')
print('Content-Type:',msgobj.get_content_type())
print('Content-Subtype:',msgobj.get_content_subtype())
print('Content-Maintype:',msgobj.get_content_maintype())





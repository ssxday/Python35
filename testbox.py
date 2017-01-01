# -*- coding:utf-8 -*-
import http.client as hct
# help(hct.HTTPResponse)
httpconn = hct.HTTPConnection(r'www.baidu.com', 80)
# request()方法 -> 纯命令，向服务器发送request，程序会挂在这里等回应
httpconn.request('GET', '/s?wd=red')  # 纯命令，无返回，None
# getresponse()方法 -> 刚刚发出了request，本方法用来接收对方回应
with httpconn.getresponse() as resp:  # 收到的是一个HTTPResponse对象
    print('远程的回应:', resp.read())  # resp就是一个HTTPResponse对象

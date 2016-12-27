# -*- coding:utf-8 -*-
# 访问FTP服务器，完成文件的上传下载
host = 'localhost'
user = 'auggie Si'
pswd = '3721'
import ftplib  # 模块

help(ftplib.FTP.getresp)
# 实例化ftplib模块里的FTP类
ftpobj = ftplib.FTP()
print('实例化FTP类：', ftpobj)
# 连接ftp服务器
conn = ftpobj.connect(host)  # 实例化的时候没连接的话，可以在这里连接
print('连接ftp服务器：', conn)  # 返回 220 ::1 FTP server (tnftpd 20100324+GSSAPI) ready.
# 登录
lgn = ftpobj.login(user, pswd)  # user在Mac的ftp上不区分大小写
print('login:', lgn)  # 返回response： 230 User AUG logged in.
# getwelcome() 获取欢迎信息
welcome = ftpobj.getwelcome()
print('welcome:', welcome)  # 同connect()的返回信息相同！！！！
# ftp文件管理：
print()
# pwd() 返回当前目录是什么
print('当前目录：', ftpobj.pwd())  # 返回的是服务器中的绝对路径，而不是客户端路径
# cwd(pathname) 进入指定目录
cd = ftpobj.cwd('ftptest')
print('执行cwd():', cd)
# 再看一次当前目录变了
print('当前目录变成了：', ftpobj.pwd())
print()
# dir() 列出当前目录的内容
# catalog = ftpobj.dir()  # 直接执行dir，无返回
# print('列出当前目录:', catalog)  # None
# nlst()
filelist = ftpobj.nlst()
print('获取目录中的内容列表：', filelist)  # 目录为空会出错
# 创建目录mkd(pathname)，如果路径已存在，报错！
# mkdirectory = ftpobj.mkd('../fuckers')
# print('创建目录：',mkdirectory)  # 返回创建的路径 ../fuckers
# rename 重命名,同时有移动文件的功能！！！！！
# rn = ftpobj.rename('logo.jpg','./fighters/logo.jpg')
# print('执行重命名：',rn)  # 250 RNTO command successful.
# 删除文件,或空目录！！ delete(pathname)
# dl = ftpobj.delete('../fuckers')
# print('删除delete：',dl)
# 只能删除空目录 rmd(dirname)
# rd = ftpobj.rmd('../fuckers')
# print('删除rmd：',rd)  # 成功则返回：250 RMD command successful.

# size() 获取文件大小
# sz = ftpobj.size('seag.txt')  # 不知为何出错
# print('文件大小：', sz)





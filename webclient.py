# -*- coding:utf-8 -*-
import socket
# 设置要连接的远程服务器，跟web.py设置相同才行
HOST = 'localhost'
PORT = 12321
# 要发送的数据
data = 'i am about to huh'
# 建立socket实例
sk = socket.socket()
# 连接远程服务器
sk.connect((HOST, PORT))  # 有没有返回值？
# 向远程发送数据
sk.sendall(data.encode())  # 需要发送byte数据
# 接收远程发过来的数据
rv = sk.recv(1024)
# 处理接收的数据
print(rv.decode())
# 关闭socket连接
sk.close()



# -*- coding:utf-8 -*-
import socket

abouttosend = 'i am 客户端, and will fuck you tonight.'
# 因为UDP协议在客户端没有connect()的过程，所以这里设置的地址参数直接在收发时才使用
HOST = 'localhost'
PORT = 12345
# 创建socket
udp = socket.socket(type=socket.SOCK_DGRAM)
# 向远程服务器发送信息
sending = udp.sendto(abouttosend.encode(), (HOST, PORT))
print('sending:', sending)  # 返回值为已发送字节数
# 接收远程服务器消息
data, addr = udp.recvfrom(1024)
print('远程服务器发来：',data.decode())
print('远程服务器地址：',addr)
# 关闭连接



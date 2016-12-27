# -*- coding:utf-8 -*-
import socket
HOST = ''
PORT = 12345
# 建立socket实例，类型UDP
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定本机地址
udp.bind((HOST, PORT))
# 用来接收客户端数据
data, addr = udp.recvfrom(1024)  # addr是客户端地址
print('人家发来的信息是：',data.decode())
print('人家的地址是：',addr)
# 向客户端发送信息
udp.sendto(b'i am server, watch your back!',addr)  # 地址是从recvfrom弄下来的
# 关闭连接
udp.close()







# -*- coding:utf-8 -*-
# socket模块
import socket
HOST = ''  # 空表示本机
PORT = 12321
# 第一步，建立socket
sck = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)  # 都可以默认
# 第二步，绑定本机地址
sck.bind((HOST,PORT))
# 第三步，监听连接
lsn = sck.listen(1)  # 最大挂起连接为backlog
print('lsn:',lsn)  # 没有返回值，None
# 第四部，等待远程接入
conn, addr = sck.accept()  # 返回
print('conn:',conn)  # <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 12321), raddr=('127.0.0.1', 50260)>
print('addr:',addr)  # ('127.0.0.1', 50323)
# 第五步，接收或发送数据
while True:
    data = conn.recv(1024)  # buffsize必填
    if not data:
        break
    print('接收到的data是',data.decode())
    conn.send(b'your message has arrived.')
# 第六步，关闭连接
conn.close()









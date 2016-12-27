# -*- coding:utf-8 -*-
server = 'pop.163.com'
username = 'letsp2p@163.com'
password = 'star1186'
import poplib  # 这是个模块

# help(poplib.POP3.noop)
# 实例化POP3类
pp3 = poplib.POP3(server)  # host=pop3服务器
# 发送用户名
usr = pp3.user(username)  # 返回值是字节串，远程服务器的响应信息
print('usr:', usr)
# 发送密码
psd = pp3.pass_(password)  # 返回字节串，内容包括邮件数量和邮箱大小
# b'+OK 964 message(s) [161793713 byte(s)]' 需要decode()->String
print('psd:', psd)

# 获取邮件服务器欢迎信息（字节码）
# b'+OK Welcome to coremail Mail Pop3 Server (163coms[726cd87d72d896a1ac393507346040fas])'
wlcm = pp3.getwelcome()
print('wel:', wlcm)
# stat() -> 获取邮箱状态 返回tuple(邮件数量, 占用空间)
many, space = pp3.stat()
print('邮件有%d封，占用%d字节' % (many, space))
# 获取邮件大小的列表
listemails = pp3.list(3)
print(listemails)
# 获取指定的邮件内容 retr(which) -> 返回tuple(response,[line...],octet)
content = pp3.retr(10)
print('retr()方法：', content)
# 取到content索引为1的元素并解码
content_formed = [s.decode() for s in content[1]]
# for s in content_formed:
#     print(s)

# 或者，用top()方法获取指定邮件的前几行内容
preview = pp3.top(10, 1)
print('preview@ @：', preview)

# 删除dele()与取消删除rset()
dl = pp3.dele(3)
print('设置删除标签：', dl)  # 返回response: b'+OK core mail'
rdl = pp3.rset()
print('取消删除标签：', rdl)  # 返回response: b'+OK core mail'
# 保持同服务器的连接noop()
np = pp3.noop()
print('保持连接：', np)  # 返回response: b'+OK core mail'
# 设置调试级别（可用可不用）有啥用？
dbl = pp3.set_debuglevel(2)
print('设置debug级别：', dbl)  # 无返回值，None
# 单方面断开连接：close()
# 向服务器发送断开连接的指令quite()
pp3.quit()  # 断开连接
(b'+OK 33 198989', [b'1 9919', b'2 14872', b'3 2542', b'4 8986',
                    b'5 12272', b'6 2075', b'7 12139', b'8 12268',
                    b'9 1657', b'10 1686', b'11 1681', b'12 1684',
                    b'13 1666', b'14 1675', b'15 1666', b'16 1667',
                    b'17 1686', b'18 1661', b'19 1822', b'20 1829',
                    b'21 17206', b'22 4364', b'23 4367', b'24 5247',
                    b'25 5385', b'26 7604', b'27 7742', b'28 8033',
                    b'29 6591', b'30 4077', b'31 5386', b'32 13285',
                    b'33 14249'], 295)

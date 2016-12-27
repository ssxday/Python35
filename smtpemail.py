# -*- coding:utf-8 -*-
myserver = 'smtp.163.com'
username = 'letsp2p@163.com'
mypswd = 'star1186'
toaddr = '2905911570@qq.com'  # 收件人
data = 'Testing mail sent via Python.'  # 邮件内容
import smtplib
help(smtplib.SMTP.send)
# 实例化smtplib模块中的SMTP类
sp = smtplib.SMTP()  # 这里不指定host或port，也可以之后用SMTP.connect()方法
print('实例化SMTP:',sp)
# 连接smtp服务器,用connect()方法。其实，在SMTP实例化的时候已经被构造方法调用
cnct = sp.connect(myserver)
print('连接服务器：',cnct)  # 返回 tuple(220, b'163.com Anti-spam GT for Coremail System (163com[20141201])')
# 使用账号密码登录 loggin()方法
lgn = sp.login(username,mypswd)
print('login登录：',lgn)  # 返回 tuple(235, b'Authentication successful')
# 发送邮件
fasong = sp.sendmail(username,toaddr,data)
print('邮件发送：',fasong)






# 断开与服务器的连接
sp.quit()

# -*- coding:utf-8 -*-
import subprocess as sp

# help(sp)
# call()方法
# democall = sp.call(['python','hellow.py'])
# print('call()返回码：', democall)

# check_call()方法
democheckcall = sp.check_call(['python', 'hellow.py'])
print('check_all()返回码', democheckcall)

# getstatusoutput()
# gso = sp.getstatusoutput(['python','hellow.py'])
# print('getstatusoutput()返回：', gso)

# getoutput()
# got = sp.getoutput(['python','hellow.py'])
# print('getoutput():',got)

# Popen类
# 实例化
prcs = sp.Popen(['python', 'hellow.py'],
                stdin=sp.PIPE,  # sp.PIPE = -1
                stdout=sp.PIPE,
                stderr=sp.PIPE,
                universal_newlines=True,  # 输入和输出可以用字符串了
                shell=True
                )
# help(sp)
print('实例化Popen对象：', prcs)
# 属性pid
print('该进程对象的pid是：',prcs.pid)
# 属性returncode，返回码
print('返回码是：',prcs.returncode)  # None表示进程尚未退出
# 方法poll():检查进程是否结束
print('进程是否结束：', prcs.poll())
# 方法communicate()
cmn = prcs.communicate('我是中间输进去的。')
print('communicate()方法：',cmn)



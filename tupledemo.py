# -*- coding:utf-8 -*-
element = '氢氦锂铍硼'
t = [2,6],5,element  # 用逗号隔开的几个值，自动就是一个元组，甚至不用打上小括号
print(type(t))
print(t)

# 打包pack和解包unpack
tuple = (1,2,3,4,5,'abcde')  #元祖中的元素可以不同类型
x,y,z,m,n,p = tuple # 解包的个数要跟tuple相等
print(p[2:4])

# 变量交换
H = '氢'
He = '氦'

H,He = He,H # 等号右边的实质是一个元组，这是一个解包过程
print(H,He)


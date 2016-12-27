# -*- coding:utf-8 -*-
print(type(1 + 3j))

print(2 * 3 ** 3 % 2 + 1)  # 顺序：乘方，乘除，取模，最后加减

print(str(2 > 3) + 'haha')

foo_ = 1
print(2 ** 38)

print(True or False and True)

# calculate the sum from 1 to 100
s = 0
for i in range(1, 101):
    s = s + i
print(s)

s2 = 100 * (1 + 100) / 2
print(s2)

strs = 'this is 1 island.'
tuple1 = ('apple', 'orange', 'pear')
print(list(strs))
print(list(tuple1))

lst = ['hey', 2, 'fucker', 5]
print(str(lst))
s = 2.50100000
print(float(s))
print(int('44', base=9))

print(3 or 5)

# 输入数字，并计算它们的平均数
# scores = input('输入数字，以逗号隔开：').split(',')
# for i in range(len(scores)):
#     scores[i] = int(scores[i])

# scores = [int(i) for i in input('输入数字，以逗号隔开：').split(',')]  # 使用了列表的推导！！！！！！

# print('%.2f' % (sum(scores) / len(scores)))
# print(scores)

# if 可以写在单行用作三元运算, 对比上面for的用法！！！！
a = 3
a = -a if a <= 0 else a ** 2
print('a =', a)

# 进制的换算
n = 3
print('%d换算成二进制%s' % (n, bin(n)))
print('%d换算成八进制%s' % (n, oct(n)))
print('%d换算成十六进制%s' % (n, hex(n)))
# print('%d换算成二进制%b' % (n, bin(n)))

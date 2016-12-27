# filter()
x = 0
def zheng(x):
    if x > 0:
        return str(x) + "f"

flt = filter(zheng,range(-5,6))  #第一个参数function，只写函数名zheng，不加括号！！！！
print(flt)
print(list(flt))  #输出[-5, -4, -3, -2, -1, 1, 2, 3, 4, 5] 为什么少了0,因为filter会把false的元素过滤掉！

# filter()的一个小问题
flt = filter(None,range(-5,6))
print(list(flt))  #输出[-5, -4, -3, -2, -1, 1, 2, 3, 4, 5] 为什么少了0,因为filter会把false的元素过滤掉！
print(list(range(-5,6)))  #输出[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

# reduce()求数列前n项和，和阶乘！
def jia(x, y):
    return x+y


def jiecheng(x,y):
    return x*y

def pingfang(x,y):
    return x**2 + y**2

from functools import reduce  #reduce在pyth3.x中不能直接用了，得从functools调用

he = reduce(jia,range(1,101))
print("he =",he)


ji = reduce(jiecheng,range(1,4))
print("ji =",ji)


pingfang = reduce(pingfang,range(3))
print("pingfang =",pingfang)

print('sum =',sum(range(1,101)))  # sum()可以直接加

# map()
mp = map(jia, range(5),range(5,8))  #
print(list(mp))

# 总结 filter() reduce() map()
# filer() 会把序列的值一一套在指定函数上运算，并对结果进行布尔判断，留下能使函数为True的序列中的元素。
# reduce() 把序列的值一一对应的套在指定函数上运算，并连续用默认函数的算法进行处理。指定函数必须有两个参数否则出错
# map() 把序列中的元素的值依次套进指定函数中，再把运算结果依次放在list中输出。指定函数有多少个参数，就得给map()几个序列

print(isinstance('haha',float))

# 通过from...import...导入的函数可以直接调用，不需要用.调用
from math import *
print(sqrt(9))
print(tan(9))
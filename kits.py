# -*- coding:utf-8 -*-
"""
目录：

"""
# 判断质数
def isprime(n=3):
    if n <= 1:
        return False
    for i in range(2,n//2+1):
        if n % i ==0:
            return False
        else:
            continue
    return True


def isPrime(n):
    """
    判断一个正整数n是否是一个质数
    速度快！
    :param n:
    :return:
    """
    if n <= 1:
        return False
    i = 2
    while i*i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def lookforprime(start=2,end=100,flag=False):
    """
    列出从start到end(包含)范围内所有的质数，默认[2,100]
    :param start:起始默认2
    :param end:起始默认100
    :param flag:是否打印数据
    :return: 找到质数的个数
    """
    fltr = filter(isPrime,range(start,end+1))
    i = 0
    if not flag:
        for r in fltr:
            i += 1
    else:
        for r in fltr:
            print(r)
            i += 1
    return i


def photoshoped(img):
    """
    判断一张图片是否被ps修过
    需要PIL.ExifTags和PIL.Image模块支持
    :param img:PIL.Image.Image对象
    :return:a bool True or False
    """
    software = img._getexif()[305]
    if 'photoshop' in software.lower():
        return True
    else:
        return False

class Fibo:
    """
    生成斐波那契数列迭代器
    """
    def __init__(self, stop):
        self.stop = stop
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.stop:
            self.n += 1
            return self.__fb(self.n)
        else:
            raise StopIteration

    def __fb(self,n):
        if n <= 0:
            pass
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        elif n >= 3:
            return self.__fb(n-1)+self.__fb(n-2)

# 语句块执行计时器
import time
t1 = time.time()
# start = 100000000000000
# print(lookforprime(start,start+99,True),'results found.')
t2 = time.time()
print('Time Cost:%fseconds'%(t2-t1))




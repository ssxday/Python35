# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:

"""
# defaultdict  不存在的键就会新建并调用初始化函数作为默认值
print('default dict'.center(50, '*'))
from collections import defaultdict


# help(defaultdict)
class OBJ:
    def __init__(self):
        self.name = '我是属性name'

    def __call__(self, *args, **kwargs):
        return self.name + 'call'


obj = OBJ()
dc = defaultdict(obj)  # 括号里的对象必须要可调用
print(dc[4])

# Counter 实例化传进一个序列，返回一个字典，以序列元素为键，以元素出现次数为值
from collections import Counter

sentence = """hello, my name is name"""
words = sentence.split()
print(words)
# count = Counter(words)
count = Counter('thisisanisland')
print(count)
# Counter.elements()-> 返回迭代器itertools.chain
ctr_elements = count.elements()  # 迭代器(重复元素扎堆迭代！！但无关顺序)
print(ctr_elements)
# for e in ctr_elements:
#     print(e)

# Counter.most_common(n)
mc = count.most_common(2)  # 返回以出现次数降序排列的items()列表形式
print(mc)

# Counter.subtract(另一个能统计数量的对象)
count.subtract('notanisland')  # count的次数，减掉新对象对应元素的次数，无返回值
# 直接从原count上减掉
print(count)

# 可命名的元组
from collections import namedtuple

print('namedtuple'.center(50, '*'))

Demensions = namedtuple('Demensions', 'x y z')  # 返回一个类
print(Demensions)  # <class '__main__.Demensions'>
size = Demensions(12, 23, 8)
print('y尺寸为：', size.y)  # 23

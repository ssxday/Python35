# dictionary
dct = {'c': 'CoCo', 'p': 'peach', 'm': 'mango', 's': 'strawberry'}
print(dct)  # 字典是无所谓顺序的，每次print出来次序是不一样的

print(dct['c'])
print(dct.pop('b', '没有那个Key'))  # pop()有返回值，del()没有返回值

# dct.clear()
# print('cleared',dct)

print(dct.items())

del dct['p']  # 删除字典里的某元素
print(dct)
print('##############################################\n遍历字典')

dct = {'c': 'CoCo', 'p': 'peach', 'm': 'mango', 's': 'strawberry'}
# 遍历key
for i in dct:
    print(i)  # 将会把键给遍历出来，因此把i作为下标即可遍历值

# 遍历value
for j in dct:
    print(dct[j])

# 同时遍历键值对!!!!!!!
for k, v in dct.items():  # 元组拆包
    print('dct中的键值对：', k, ':', v)

print('##############################################\n字典的方法')

# 输出key组成的list
keys = dct.keys()
print(type(keys))  # 注意！Python3.x并不能纯粹输出key的列表，fuck

# 输出value组成的list
print(dct.values())
print(sorted(dct.values()))  # 用sorted()搞一下就会变成列表了

# items(),会把每对key和value组成一个tuple
print('items()方法：', dct.items())

# get()的用法
print(dct.get('m', "the key doesn't exist."))  # similar to jQuery

# 合并两个字典update(),原有重复的键名将被覆盖
D1 = {'hello'}
D2 = {'world'}
D1.update(D2)  # 仅仅对目标字典做运算，并不返回任何对象
print('D1 :', D1)
print('D2 :', D2)

# copy()与update()不同，是有返回值的，因此赋值时会抹掉D1
D1 = D2.copy()  # 浅拷贝，跟直接 D1 = D2是不同的
print(D1)
print(D2)

# 深拷贝与浅拷贝
A = {'fuck'}
B = {'you'}
B = A.copy()
B = {'mom'}
print('A = ', A)
print(B)

print('##############################################\n排序')

sd = sorted(dct)  # python3 只把键给排了
print("sd =", sd)
print(dct)

sv = sorted(dct.values())
print("sv = ", sv)

print('##############################################\n sys.module')
import sys

sm = sys.modules
print(type(sm.keys()))
for i in sm.keys():
    print(i)

print("os =", sm['os'])

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
count = Counter(words)
count = Counter('thisisanisland')
print(count)

# 字典的推导
a = {'a': 1, 'b': 2, 'c': 3}
b = {k: pow(v, 2) for k, v in a.items() if k > 'a'}  # 字典的推导要用到items()
print(b)






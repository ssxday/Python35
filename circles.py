# -*- coding:utf-8 -*-
# part1
# i = 0
# numb = input('输入几个数字，用逗号隔开:').split(',')
# print("numbers are:",numb)
#
# while i < len(numb):
#     print(numb[i])
#     i+=1
#

# part2
m = 0
for i in [1,2,3,4,5]:
    if m == i:
        continue
    m += i

# for与迭代函数
    # sorted 排序迭代()
    # enumerate 编号迭代() 返回[(元组),(元组),...]这样的结构
    # reversed 翻转迭代()
    # zip() 并行迭代
# enumerate()
for k,v in enumerate('dqrh'):  # 参见字典的键值对遍历
    print('第%d个字母是%s' % (k+1,v))

# sorted() 和 reversed()
for i in reversed(sorted([3,0,1,6])):
    print(i) # 从大到小排好

# 对字符串进行sorted()，会先变成列表再排序
print('对字符串进行sorted:',sorted('motherfucker'))
# zip() 遍历n个序列里相同编号的元素
lista = ['a','b','c']
listb = ['p','q','r']
listc = ['x','y']

for i,j,k in zip(lista,listb,listc):  #zip类似打包
    print(i,j,k)

for i in zip(lista,listb,listc):
    print(i)

a = 'hello'
b = 'mother'
c = 'fucker'

for i,j,k in zip(a,b,c):
    print(i,j,k)
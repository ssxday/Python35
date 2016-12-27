# list
lst = ['apple', 'banana', 'cherry', 'durian', 'elva', 'fig', 'grape']
lst.append('honey')
# lst.append(['hhhhhhhoney'])
# print('lllllllll  =',lst)
lst.remove('cherry')
lst.insert(2,'cherry')
p = lst.pop()  #默认-1


# print(lst)
# print(p)
# print(lst[1:-1]) #不包含后一个索引的值
# 遍历list
for i in lst:
    print(i)

print('##############################################')

print(lst)
fruit1 = lst[0:4]
fruit2 = lst[4:-1] # -1取不出来
print(fruit1+fruit2)
print(fruit1.extend(fruit2)) # 注意！extend是直接在fruit1上连接，不返回东西(None),但print里面的语句执行了
print(fruit1)

#list 的乘法
fruit3 = fruit2 * 2
print(fruit3)

print('##############################################')

# print(lst.index('honey'))  # honey此时还不在lst中，报错
print('honey' not in lst) # false

lst += ['honey']  #注意！这里是['honey']，不是'honey'
print(lst.index('honey'))

print('##############################################')
# lst.reverse().reverse()  #reverse()不返回对象，所以obj.reverse()不能再.reverse()
print(lst)
print(lst.reverse())  # 返回None，reverse直接排，不返回,但是reverse()已执行
print(lst)
# print(lst.sort())  # 返回None，sort直接排，不返回
sorted(lst) # sorted是有返回值的，不会在原list上改动
print(lst)

'''
lst.reverse()
print(lst)
lst.sort()
print(lst)
'''

# 列表支持加法运算
print([1,2]+[3,4])  # [1,2,3,4]

# 列表支持乘法运算
print([2,]*3)  # [2,2,2]


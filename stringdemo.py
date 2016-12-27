# %c    单个字符及其ASCII码
# %s    字符串
# %d    整形
# %u    无符号整形
# %o    无符号八进制数
# %x    无符号十六进制数
# %X    无符号十六进制数大写
# %f    浮点数
# %e    科学计数法浮点数
# %E    同上
# %g    根据值的大小决定是%f还是%e
# %G    同上
# %p    用十六进制数格式化变量地址#

import iterable # 自定义的文件，不加后缀py
print(iterable.ll)

# print('%d'%'a35dhtjksdd87dgf')  #错误
fmt = '%10s %.2f' % ('version', 2.2)  # 有括号可不是元组！！而是一一对应的"格式"，有字符串也有浮点
print(fmt)

# 对齐center,ljust,rjust
print(type(fmt.center(5)))  # str
print(fmt.center(50, '='))  # 50 stands for width
print(fmt.ljust(50, '='))
print(fmt.rjust(50, '='))

# 转义字符
# \'    '
# \"    "
# \\    \
# \a    系统响铃
# \n    换行
# \r    回车
# \b    退格
# \t    横行制表符Tab
# \v    纵向制表符
# \f    换页
# \o    八进制数
# \x    十六进制数
# |000  终止符，后面的字符全部忽略#
print('mother\tfucker')
print('mother\ffucker')
print('mother\rfucker')
print('mother\vfucker')
print('mother\000fucker')  # 终止符没用

# 字符串的连接
# 用+连接
str = 'mother' + 'fucker' + 'son' + 'of' + 'a' + 'bitch'
print(str)
# 用join()把列表的元素连起来
print('join()用法:',str.join("@@@"))
strs = ['mother', 'fucker', 'son', 'of', 'a', 'bitch']
print(' '.join(strs))  # 用空格连接，逆运算为split()
print('原列表没改：', strs)  # 原列表不变
strs = ' '.join(strs)  # 列表变字符串
print('原列表变成字符串了：', strs)

# 字符串不可变，要变的话就是创建一个新的字符串，这点同元组一样
# strs[5] = 'f'  # 报错！！

# 字符串的截取
print(str[2:10:3])  # 切片，从start起，每隔step取1个字符，直到end前一个字符为止

print(strs.split(' ', 3))  # 3 stands for maxsplit times
print(strs)  # strs并没有改变

# 字符串掐头去尾lstrip(),rstrip()
a = '3335554aaaaabc-789abc.avi'
print(a)
# 默认切空格
print(a.lstrip()) # 重点：按照chars的序列一个一个切，不怕重复，只要次序对都能全切掉


# 字符串的比较 （相等，不相等，包含关系）--> bool
print(str, '\n', strs)
print('以t开头吗?', strs.startswith('t', 2, len(str)))  # 必须以substring开头，在中间出现不行
print('以n结尾吗?', strs.endswith('n', 6))  # 切片为strs的结尾到strs[6]
print('以h结尾吗?', str.endswith('h', 1, 4))  # 以切片[1:4]（切片为oth）判断是否以h结尾，因此为True


# 字符串翻转
# 方法1
def fanzhuan(s):
    s = list(s)
    # print(s)
    s.reverse()
    s = ''.join(s)
    return s


print(fanzhuan('hellow'))


# 方法2 easiest!
def fanzhuan2(s):
    return s[::-1]  # 中间不能写0，不然没有正数第一个字符了


print("倒过来：".center(50, '='), fanzhuan2('motherfucker'))

# 字符串查找 find(),rfind() 找到了返回索引，找不到返回-1
print(str.rfind('q'))
print('q' in str)
print("bool(-1)", bool(-1))

# find与count
print('count:', str.count('f'))  # 返回子字符串的数量
print('find:', str.find('f'))  # 返回子字符串的位置

# 字符串替换 replace()
newstrs = strs.replace('mother', 'father')  # 如果找不到mother则返回原字符串
print(newstrs)

# 大小写转换upper(),lower(),swapcase()
strs = 'hey, motherFUCKer!'
print(strs)
print('swap', strs.swapcase())
print('lower', strs.lower())
print('upper', strs.upper())
print('strs原本的样子 ：',strs)

# 每个单词首字母大写，如果原来在中间有大写，也会变成小写，只留首字母大写
strs.title() # 并不直接在原字符串上改动
print('Titled :',strs.title())
# 字符串首字母大写，其他字母如果有大写，则变成小写，只留首字母大写
print('Capitalized :',strs.capitalize())

# encode() decode()字符串 <--> 字节串
encoded = '你好,motherfucker'.encode()
print('执行encode：',encoded)
print('执行decode:',encoded.decode())

for i in 'basket':
    print(i)

'''
# 日期与字符串的互相转换
# 字符串 --> 时间：二次转化，三个步骤
    #1、strptime()把字符串变成表示时间的元组
    #2、把表示时间的元组解包赋值给年、月、日等变量
    #3、表示年月日的变量传给datetime()
'''

tmstr = '19860831'
import time, datetime

tm = time.strptime(tmstr, "%Y%m%d")  # 第一步
print("时间元组：", tm)
y, m, d = tm[0:3]  # 第二步：解包，分配给年月日
# print(y,m,d)
time_obj = datetime.datetime(y, m, d)  # 第三步，datetime()返回时间类型
print(type(time_obj), time_obj)

# 时间 ——> 字符串：strftime()
# 上文已经import了

lctm = time.localtime()  # lctm的格式跟strptime()生成的时间元组格式相同
print("localtime:", lctm)

# hh = ':'.join(lctm)  # 不能用这种方法，因为即便转换成列表，里面的元素也是数字而非字符串，不能用:连接
# print("hehe=",hh)

tmstr = time.strftime('%Y-%m-%d %a %I:%M:%S', lctm)  # lctm不写的话，默认是本地时间！！！
print("时间转化为的字符串：", tmstr)

# 日期时间格式
# %Y    四位数年份
# %y    二位数年份
# %m    数字月份
# %b    英文简写月份
# %B    英文完整月份
# %d    日期数1~31
# %H    小时数24
# %I    小时数12
# %M    分钟数0~59
# %S    秒数
#
# %a    英文简写星期
# %A    英文完整星期
# %w    星期几的索引，0是星期天
# %W    本年的第几周
# %j    本年的第几天
# %x    当天日期，格式mm/dd/yy
# %X    当天时间，格式HH:MM:SS
who = 'wo'
where = '北京798'
what = '吃饭'
# 按顺序依次对应
print('%s要去%s的coffee%%shop%s' % (who, where, what))

print(dir(datetime))
t1 = datetime.datetime.now()
t2 = datetime.datetime.now()
sub = t2-t1
print(sub.seconds)

t1 = time.time()
print(type(t1))

print('*'*30)
help(time)
# ctime(seconds) 把秒数转换成表示 当地时间 的字符串
print(type(time.ctime()))

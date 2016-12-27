# help(list)
# 第一题:sort()和sorted()的用法
L = [2,5,3,8,10,1]
# print(sorted(L))

L.sort()
print(L)

# 若要降序排列
L.sort(reverse=True)
print(L)

# 第二题：(提示用切片，不知道怎么用，试过s[-1,0]不行)
def tailup(string):
    string = str(string)  #传进来的不管是不是字符串统统转换成字符串
    r = ""
    for i in range(len(string)-1,-1,-1):
        r += string[i]
    return r

# s = 1234567
s = "1234567"
# s = (1,2,3,4)
print(tailup(s))

# 第三题：求100以内的所有质数，输出时用逗号隔开
zhishu = ""
yushu = []
for beichushu in range(2,100):
    yushu.clear()
    for chushu in range(2,beichushu//2+1):
        yushu.append(beichushu % chushu)
    # print("yushu =",yushu)
    if 0 not in yushu:
        zhishu += str(beichushu)+","
print(zhishu)

# 第四题
d = {'a':1,'b':2,'c':3}
print('keys =',list(d.keys()))
print('values =',list(d.values()))

d['d'] = 4
print(d)

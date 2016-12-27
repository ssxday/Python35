# 正则的匹配
import re
s = "howARE7you finethank8YOU9你呢"
phone = '+86-13068719868'

print(s)
reg1 = r'^\d'  # r表示这段字符串不用转义！
reg2 = r'[^\d]'
reg3 = r'\d+'
print(re.findall(reg2,s,re.I))
print(re.findall(reg3,phone))
print(re.split(reg3,phone))  # 把匹配出来的字符串当做分隔符！

# re.match() re.search() re.findall()
reg4 = r'(www|http://www)\.[a-z0-9-]*\.(cn|com|net)'
rematch = re.match(reg4,'www.baidu.com')
print('re.match:',rematch.group())
research = re.search(reg4,'url:www.baidu.com')
print('re.search:',research.group())
refindall = re.findall(reg4,'www.yzology.cn/url=http://www.sina.com')
print('re.findall:',refindall)
print(re.findall(r'cari(bbean|b)','carib-010102-122.caribbean.mp4'))

# 正则替换sub()和subn()
print('正则替换sub()和subn()'.center(30,'*'))
s = 'hello, there! how are you doing?'
ss = re.subn(r'there|you','motherfucker',s)
print(s)  # 并没有改变原字符串
print(ss)  #subn()比sub()多输出替换次数，放在元组里

# 正则表达式预编译compile(),返回pattern对象，pattern对象类似于re对象使用
print('正则表达式对象'.center(30,'*'))
reg2 = r'cari(b|bbean)'
s = 'carib-010102-122.caribbean.mp4'
ptn = re.compile(reg2,re.I)
print('编译正则：',ptn)
print('pattern:',ptn.pattern)
print(ptn.findall(s))

# 分组
print('分组'.center(30,'*'))
# reg5 = r'(?P<Area>\d{3,4})-?(?P<no>\d{7,8})'
reg5 = r'(\d{3,4})-?(\d{7,8})'
# reg5 = r'(\d{3,4})(-?)'
s = '075561881937'
ptn = re.compile(reg5,re.I)
landline = ptn.search(s)
print(landline.groupdict())
# print(landline.group(1))
# findall对分组的处理
landline = ptn.findall(s)
print(landline)
print((255))

# # exercise
# # s = input("请任意输入：")
# s = 'ab2b3n5n2n67mm4n2'
# snum = re.findall(r"\d+",s)
# print(''.join(snum))  # 把数字挑出来组合成新的字符串
#
# s_quchong = list(set(list(s)))  #用set()去重！！！！！
# dicts = {}
# print(s_quchong)
# for letter in s_quchong:
#     dicts[letter] = s.count(letter)  # 记住count()的用法！！
#
# print(dicts)
# print('字母"n"出现的次数为',dicts['n'])





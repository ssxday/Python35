# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageChops

# open()函数（不在类中，不叫方法）
cliff = Image.open('cliff.jpg')
tu95 = Image.open('tu95.jpeg')
macgif = Image.open('mac.gif')
tw = Image.open('taiwan.jpeg')
monkey = Image.open('monkey.png')
print('open()函数返回对象：', macgif)

for i in filter(lambda x: not x.startswith('_'),dir(ImageChops)):
    print(i)

# add() 图片相加
adds = ImageChops.add(tu95,cliff)
print('图片相加：',adds)
# adds.show()

# subtract() 图片相减
jian = ImageChops.subtract(cliff,tu95)
print('图片相减：',jian)
# jian.show()

# dark() 留下对应像素较小的值
dk = ImageChops.darker(cliff,tu95)
print('留下暗部：',dk)
# dk.show()

# lighter() 留下对应像素较大值
lt = ImageChops.lighter(cliff,tu95)
print('留下亮部：', lt)
# lt.show('lighter')

# multiply() 正片叠底
mtpl = ImageChops.multiply(cliff,tu95)
print('正片叠底：',mtpl)
# mtpl.show('multi')

# screen() 屏幕效果
scr = ImageChops.screen(cliff,tu95)
print('同时投屏：',scr)
# scr.show('screen')

# invert() 相反--底片效果
dipian = ImageChops.invert(tu95)
print('相反底片效果：',dipian)
# dipian.show()

# difference() 比较
diff = ImageChops.difference(cliff,tu95)
print('比较：',diff)
# diff.show()

# constant() 灰度填充
cstt = ImageChops.constant(tu95,255)
print('灰度填充：',cstt)
# cstt.show()

# offse() 偏移
ofst = ImageChops.offset(tu95,100)
print('偏移offset：',ofst)
# ofst.show()

# add_modulo() - add two images without clipping the result
help(ImageChops.add_modulo)
result = ImageChops.add_modulo(cliff,tu95)
print('add_modulo:',result)
# result.show()




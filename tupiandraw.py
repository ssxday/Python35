# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw
cvs = Image.new('RGB', (800, 600),'white')
tu95 = Image.open('tu95.jpeg')
print('画布：', cvs)
# cvs.show()

tu95draw = ImageDraw.ImageDraw(tu95)
print('imagedraw:', tu95draw)
cvsdraw = ImageDraw.Draw(cvs)
print('-----draw:', tu95draw)

help(ImageDraw.ImageDraw.text)
# 画直线，折线 - line()
cvsdraw.line((200,200,500,500,450,300),fill='#ccc',width=5)
cvsdraw.line((400,0,400,600),fill='#ccc',width=2)
cvsdraw.line((50,50,700,50),fill='#ccc',width=2)

# 画矩形 rectangle()
cvsdraw.rectangle((300,400,600,500),outline='red')

# 画弧线 arc()
cvsdraw.arc((300,400,600,500),45,135,'red')

# 画(椭)圆的弦 chord()
# cvsdraw.chord((300,400,600,500),45,135,'yellow')

# 画扇形
cvsdraw.pieslice((100,100,500,300),0,45,'yellow')

# 画多边形
cvsdraw.polygon((100,100,300,250,400,500,450,300,600,500),outline='gray')

# 绘制字符串
cvsdraw.text((400,50),'helloworld','blue')


cvs.show()




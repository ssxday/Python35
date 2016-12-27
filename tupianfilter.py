# -*- coding:utf-8 -*-
from PIL import Image,ImageFilter
# help(ImageFilter.UnsharpMask)

tu95 = Image.open('tu95.jpeg')#.resize((400,300))
print(tu95)

# 调用Image对象的filter()方法使用滤镜
# 模糊滤镜ImageFilter.BLUR
blur = tu95.filter(ImageFilter.BLUR)
# blur.show()

# 高斯模糊ImageFilter.GaussianBlur
gsblur = tu95.filter(ImageFilter.GaussianBlur(8))
# gsblur.show()

# 查找边缘FIND_EDGES
fe = tu95.filter(ImageFilter.FIND_EDGES)
# fe.show()

# 边缘增强 EDGE_ENHANCE
ee = tu95.filter(ImageFilter.EDGE_ENHANCE)
# ee.show()

# 锐化 SHARPEN
sp = tu95.filter(ImageFilter.SHARPEN)
# sp.show()

# DETAIL
dtl = tu95.filter(ImageFilter.DETAIL)
# dtl.show()

# CONTOUR
ctr = tu95.filter(ImageFilter.CONTOUR)
# ctr.show()

# EMBOSS 浮雕
emb = tu95.filter(ImageFilter.EMBOSS)
# emb.show()

# SMOOTH
smth = tu95.filter(ImageFilter.SMOOTH)
# smth.show()

# ImageFilter.MinFilter() 最小值滤波
minf = tu95.filter(ImageFilter.MinFilter(5))
# minf.show()

# ImageFilter.MedianFilter() 中值滤波
midf = tu95.filter(ImageFilter.MedianFilter(5))
# midf.show()

# ImageFilter.MaxFilter() 最小值滤波
mixf = tu95.filter(ImageFilter.MaxFilter(5))
# mixf.show()

# ImageFilter.UnsharpMask() USM锐化
usm = tu95.filter(ImageFilter.UnsharpMask(5))
# usm.show()



# -*- coding:utf-8 -*-
# Pillow库
# Image模块
import PIL.Image as PLIG

# help(PLIG.blend)
# open()函数（不在类中，不叫方法）
cliff = PLIG.open('cliff.jpg')
tu95 = PLIG.open('tu95.jpeg')
macgif = PLIG.open('mac.gif')
tw = PLIG.open('taiwan.jpeg')
monkey = PLIG.open('monkey.png')
print('open()函数返回对象：', macgif)

# new(mode, size, color=0) 函数
# 新建一个图片
createimg = PLIG.new('RGBA', (800, 600))
print('new()新建图像：', createimg)

# blend(img1,img2,alpha)函数
bld = PLIG.blend(cliff, tu95, 0.5)
print('blend():', bld)
# bld.show()  # 打开混合的图片

# composite()
cps = PLIG.composite(tu95, cliff, createimg)
print('composite():', cps)


# cps.show()


# eval(img,func) 对图像的每个像素使用func计算
def func(n):
    return n // 2  # 整除


evalimg = PLIG.eval(tu95, func)
print('eval():', evalimg)
# evalimg.show()
# tu95.show()

# merge() 将多个通道合成一副图像
# help(PLIG.merge)
# mg = PLIG.merge()

# Pillow.Image.Image类
print('Pillow.Image.Image类：')
# format属性,mode属性,size属性
w, h = tw.size
print(r'图片taiwan.jpeg的format格式是%s，图像模式为%s，尺寸为%d✖%d' %
      ((tw.format, tw.mode,) + tw.size))  # 这样也行

# PIL.Image.Image.convert(mode,matrix)方法，
# 支持L，RGB，CMYK之间的转换
# 把tu95转换成L模式（黑白）
tu95L = tu95.convert('L')
print('RGB转化成L', tu95L)
# tu95L.show()
# 把tw转换成RGB
twRGB = tw.convert('RGB')
print('L转化成RGB', twRGB)
# twRGB.show()

# 调整图像尺寸resize()
tu95rsz = tu95.resize((400, 200))
print('调整尺寸后返回copy：',tu95rsz)  # 可以不等比例缩放
# tu95rsz.show()

# transform(size, method)



# PIL.Image.Image.save(fp,format)
# -> 把Image对象保存成文件
def desktop(filename=''):
    return r'/Users/AUG/Desktop/' + filename.lstrip('/')

# baocun = tu95L.save(desktop('tu95heibai.jpg'))
# print('save()返回:', baocun)  # 返回None

# PIL.Image.transpose(method)
tmacgif = macgif.transpose(PLIG.FLIP_LEFT_RIGHT)  # 左右镜像
print('左右镜像处理后返回对象：', tmacgif)
# tmacgif.show()
rtmac = macgif.transpose(PLIG.ROTATE_90)  # 角度逆时针为正
# rtmac.show()

# rotate(角度)
rt = macgif.rotate(45, expand=1)
# rt.show()

# PIL.Image.Image.paste(img,box,msk)
# 怎样正好把小图放在大图x方向的中心：
poix = (tu95L.size[0] - macgif.size[0]) // 2
poiy = 50  # 同样逻辑
tu95L.paste(macgif, (poix, poiy))
# tu95L.save(desktop('macpasted.jpg'))

# crop(box区域) -> 返回剪下来的那块区域
crp = tu95.crop((250,250,450,450))
print('被crop()剪下来的那块',crp)
# crp.show()

# getbands() 返回图像的通道列表
print('tu95L的通道列表：', tu95L.getbands())
print('cliff的通道列表：', cliff.getbands())

# getextrema() 返回图像最大最小像素点值，跟图像模式有关
print('getextrema()：',macgif.getextrema())

# getpixel(xy)  返回坐标(x,y)处的像素颜色值，不同mode有不同的表示方法
x,y = 300,400
print('像素值(RGB)：',tu95.getpixel((x,y)))
print('像素值(P)：',macgif.getpixel((100,50)))

# 返回所有像素的像素值
data = monkey.getdata()  # 返回所有像素的像素值的序列
print('图片一共有%d个像素' % len(data))  # 数量=图片长×宽
# print(tu95.getpixel((1,1)))

# 像素数量直方图histogram()
zhifangtu = tw.histogram()
print(len(zhifangtu))
# print('直方图：',zhifangtu)

# point() 跟eval()差不多
pointjmg = tu95.point(func)  # 传入func函数
print(pointjmg)
# pointjmg.show()

# split()
cliffbands = cliff.split()
print('split()后返回:', cliffbands)

# thumbnail()
# help(PLIG.Image)
cliff_thumbnail = cliff.copy()  # 因为直接处理源图，所以先做个copy
cliff_thumbnail.thumbnail((200,90))
print('还没thumbnail:',cliff)
print('thumbnail:',cliff_thumbnail)
# cliff_thumbnail.show()

for k,v in tu95.info.items():
    print('%s:\t%s'%(k,v))
# print(tu95.info['exif'])

exifs = tu95._getexif()
# print(exifs.keys())
import PIL.ExifTags
# help(exif)
lookups = PIL.ExifTags.TAGS
# print(lookups)
print('查看exif信息：')
for k,v in exifs.items():
    k = lookups[k]
    print('%s:\t%s' % (k, v))



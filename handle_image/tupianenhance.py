# -*- coding:utf-8 -*-
from PIL import Image, ImageEnhance

tu95 = Image.open('tu95.jpeg').resize((640, 480))
cliff = Image.open('cliff.jpg')
print('tu95:', tu95)
# tu95.show()

h = ImageEnhance.Color(tu95)
print('degenerate:', h.degenerate)
print('返回image:', h.image)
print('返回intermediate_mode:', h.intermediate_mode)


# 封装一个函数，来对比测试所有的增强效果
def framed(imgobj, enh, level=1.0, flag=False):
    # 设置对比画框
    frame = Image.new(imgobj.mode, (imgobj.size[0] * 2, imgobj.size[1]))
    # 把原图粘贴到画框左侧
    frame.paste(imgobj, (0, 0))
    # 设置选择器
    opt = {
        'color': ImageEnhance.Color,
        'contr': ImageEnhance.Contrast,
        'brt': ImageEnhance.Brightness,
        'shp': ImageEnhance.Sharpness
    }
    # 执行增强器
    enhanced = opt[enh](imgobj).enhance(level)
    # 把增强后的结果放到画框右侧
    frame.paste(enhanced, (frame.size[0] // 2, 0))
    # 输出画框
    if flag:
        frame.show()
    return enhanced


# 色彩平衡调整器类Color
# ihcolor = ImageEnhance.Color(tu95)
framed(tu95, 'color', -5)

# 对比度调整器类Contrast
# contr = ImageEnhance.Contrast(tu95)
framed(tu95, 'contr', 0.5)

# 亮度调节类Brightness
# bri = ImageEnhance.Brightness(tu95)
framed(tu95, 'brt', 0.6)

# 清晰度调节类Sharpness
# shp = ImageEnhance.Sharpness(tu95)
framed(tu95, 'shp', -2)

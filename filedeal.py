f = open('dreamtour.txt', 'r+')
print(f.fileno())
# lines = f.readlines()  # 每一行内容的list列表
# print(lines)

line = f.read(1)  # 读取n个字符，返回字符串,不填代表全部读取！！！！
print(line)

line = f.read(2)  # 同时光标指针向后移动n个单位
print(line)

print(f.mode)  # file属性之一，显示文件的打开方式

print(f.encoding)  # UTF-8

print(f.name)  # dreamtour.txt

print(f.closed)  # 判断文件是否关闭，True or False

print(f.tell())  # 显示文件指针的位置,为什么是12呢？

print(f.read(6))

print(f.readline(3))  # readline(n)的n指的是取line的前n个字符！！！！！

print(f.__next__())  # 返回自指针起的一行的内容，并将指针移动到下一行

print(f.__next__())

print(f.readline())  # 显示效果同f.__next__()

f.seek(0, 2)  # 移动指针，移至相对结尾（2），偏移（0）的地方。

# f.write('\r李白是唐代伟大的诗人')

f.close()
print('CLOSED?', f.closed)

# how to delete file ---- Module os and os.path are required
# remove() is in Module os
df = open('hello.txt', 'a+')  # 创建一个实验用的文件
data = ['卧槽原来不换行!\r\n','还他妈的加换行符\n']
# df.writelines(data)  # 这里临时关掉了

# 删除文件的套路如下：
import os

if os.path.exists('tkinter.py'):  # 先判断文件是否存在
    os.remove('tkinter.py')
# 获得当前程序运行的路径(绝对路径)
print('os.getcwd:',os.getcwd())

# 创建目录
# os.mkdir('overall')  # 目标必须事先不存在，才能创建
# 删除目录
# os.rmdir('overall')  # 目标目录必须非空才能删除

# help(os.wait)

# os.stat(path) 查看文件的的各项状态，类似右键属性
st = os.stat('cliff.jpg')
print(st)  # 返回os.stat_result对象，可用数字索引或对象属性值访问
print('文件权限模式：',st.st_mode)
print('最后一次访问时间的时间戳',st.st_atime)

# 查看目录中文件列表 listdir()
li = os.listdir('.')  # 默认当前目录。没有后缀的是文件夹！
print('目录结构：', li)

# os.walk()
print('os.walk()'.center(30,'*'))
walk = os.walk('overall')  # 返回的是一个可以迭代的生成器对象<generator object walk>
print(type(walk))
# list(walk)
print(type(walk))
# print(walk)
for wk in walk:
    print(wk)

print('os.walk()结束'.center(30,'*'))

print('行分隔符%s，目录分隔符%s'%(os.linesep,os.sep))
# 重命名
if 'chaoxie.txt' in os.listdir():
    os.rename('chaoxie.txt', 'zhuanzheng.txt')

# os.path
# os.path.isabs()
p = os.path.isabs('/desktop/haha.php')
print('这是一个绝对路径吗？',p)

# os.path.abspath()
print(os.path.abspath('overall/img.py'))

# os.path.join()
print(os.path.join('desktop/overall/img.py','haha.py','wocao/diu.php'))

# 分割文件名和扩展名os.path.splitext()
nameAndExtension = os.path.splitext('aa.bb.cc.torr')
print('返回文件名和扩展名的元组：', nameAndExtension)  # 是一个元组
print('文件名是：', nameAndExtension[0], '\n扩展名是：', nameAndExtension[1])  # 只分割最后一个点

# 分割路径和文件名os.path.split()
pathAndFilename = os.path.split('./overall/laketwo/aBp_123.avi.torrent')
print(pathAndFilename)
i, j = pathAndFilename
print('路径是%s\n文件名是%s' % (i, j))

# 批量修改文件名程序,为避免对后面的脚本造成干扰，本节注释掉,详见goup-rename.py
# files = os.listdir('.')
# for filename in files:
#     # pos = filename.find('.')
#     if filename.endswith('.txt'):
#         newname = filename.replace('.txt','.haha')
#         os.rename(filename,newname)

# glob模块用于匹配路径，返回路径下的文件列表list
import glob

print(glob.glob('./overall/*.py'))  # 只返回匹配到的文件列表，没有文件夹

# 文件的复制粘贴（移动、复制）
# file类没有提供直接复制的方法
# 可用file1.write(file2.read())的方式替代
# Module shutil提供了相关的文件、目录的管理接口
import shutil

shutil.copyfile('dreamtour.txt', 'chaoxie.txt')  # 目标文件不存在的话，会创建。存在的话，覆盖内容。

# shutil.move('src','dst')  # 把src移动到dst，可以顺便改名

# 文件的比较difflib
import difflib

f1 = open('src.txt', 'r')
f2 = open('dst.txt', 'r')
# print(src)
src = f1.read()
dst = f2.read()
print(lambda x: x == '')
compare = difflib.SequenceMatcher(lambda x: x == '', src, dst)
for tag, i1, i2, j1, j2 in compare.get_opcodes():
    # 注意下面正则格式的对应！！！
    print(r"%s src[%d:%d]=%s dst[%d:%d]=%s" % \
          (tag, i1, i2, src[i1:i2], j1, j2, dst[j1:j2]))

# fileinput模块
print('fileinput模块'.center(50,'*'))
import fileinput
filelines = fileinput.input(('gl.py','notes.py'))  # 可迭代的行对象
print(filelines)
# help(fileinput.fileno)
for line in filelines:
    print(line)
filelines.close()

# fileinput自带上下文管理器，可用with语句，就无需close()了
print('Using context-manager:')
with fileinput.input(['gl.py','notes.py']) as lines:
    for line in lines:
        print('总第%d行'%lines.lineno(),
              '文件%s中的第%d行:'%(lines.filename(),lines.filelineno()),
              line)

# 文件和流
f = open('hello.txt','w')
import sys
# 标准输出
saved = sys.stdout  # 把console对象保存起来
print(saved)
sys.stdout = f
# print(sys.stdout)
# print(f)
print('改变了输出的设备到这个文件，而不在console了')
print(f.name)
sys.stdout = sys
sys.stdout = saved  # 流输出设备改回到了原来的console
print('我又在系统控制台console显示了！')
f.close()

# 标准输入
# 同read()



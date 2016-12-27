# 批量修改文件后缀程序
def mrename(src = 'haha',dst = 'txt',srcdir = '.'):
    src = '.' + src
    dst = '.' + dst

    warning = input('警告！你确定要把后缀为'''+ src +'的文件修改为' + dst + '的后缀吗？(Y/N)：')
    if warning not in ['y','Y']:
        exit('还好你放弃了')

    import os
    files = os.listdir(srcdir)
    for filename in files:
        if filename.endswith(src):
            newname = filename.replace(src,dst)
            os.rename(filename,newname)



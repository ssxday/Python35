# -*- coding:utf-8 -*-
# 遍历目录文件及子文件夹
def gothr(path = './overall'):
    import os
    l = os.listdir(path)
    decration = ''

    for ford in l:
        decration = '-'
        if os.path.isdir(path + os.sep + ford):
            print(decration,ford)
            gothr(path + '/' + ford)
        elif os.path.isfile(path + os.sep + ford):
            print(decration,ford)

    # return l

# gothr()










def goover(pth = './overall'):
    import os
    l = os.walk(pth)
    for root, dirname, filename in l:
        print('\nroot:',root)
        print('dir:', dirname)
        print('file:',filename)


    # print(l)

# goover()









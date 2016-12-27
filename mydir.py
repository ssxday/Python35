# -*- coding:utf-8 -*-
import os, time


class MyDir:
    def __init__(self, pathname='./overall'):
        # 初始化...
        self.__root = pathname  # 指定路径名称
        self.__logfile = pathname[pathname.rfind(os.sep) + 1:] + '.txt'  # 日志文件名称
        self.data = time.ctime() + '\n'  # 要写入日志的内容的第一行并换行
        self.num_file = 0  # 文件计数器

        try:
            self.__engine(pathname)
        except:
            # 引擎engine出错
            self.data += '程序出错，可能是指定的路径的问题\nSomething wrong occured, ' \
                         'check on your pathname, perhaps.'
        # 将遍历到的内容写入
        self.__mywrite()

    def __mysorted(self, pathname):
        """
        列出指定路径(pathname)下的文件夹和文件
        并按照先文件夹后文件的顺序排列好
        :param pathname: 指定目录路径
        :return: 指定pathname下的目录与文件列表,指定路径出错返回False
        """
        try:
            sth_in_dir = os.listdir(pathname)
        except NotADirectoryError:
            return False
        except FileNotFoundError:
            return False
        dirs = []
        files = []
        for f in sth_in_dir:
            # 去掉.和_开头的元素
            # 同时过滤掉.db文件和logfile本身(如果它也在的话)
            if not (f.startswith('.') or f.startswith('_') or
                        f.endswith('.db') or f == self.__logfile):
                # 除了以上情况外，如果是文件的话，放入files序列
                if os.path.isfile(pathname + os.sep + f):
                    files.append(f)
                # 如果是目录的话，放入dirs序列
                elif os.path.isdir(pathname + os.sep + f):
                    dirs.append(f)
                else:
                    pass
        sth_in_dir = sorted(dirs) + sorted(files)
        return sth_in_dir

    def __engine(self, pathname):
        # 在循环前确定本轮循环的目录在哪个level上
        level = self.__level(pathname)
        for f in self.__mysorted(pathname):
            if os.path.isfile(pathname + os.sep + f):
                self.data += '|\t' * level + f + '\r\n'
                self.num_file += 1  # 计数器+1
            elif os.path.isdir(pathname + os.sep + f):
                self.data += '|\t' * level + '<%s>' % f + '\r\n'
                self.__engine(pathname + os.sep + f)
            else:
                pass
        return self.data

    def __level(self, pathname):
        """
        判断pathname相对self.__root的层级level
        :param pathname:
        :return: level -> int。当pathname和self.__root无关时返回False
        """
        # 去掉可能在路径结尾出现的分隔符，以避免错误的计算level层级
        pathname = pathname.rstrip(os.sep)
        if pathname.startswith(self.__root):
            difference = pathname[len(self.__root):]
            level = difference.count(os.sep)
            return level
        else:
            return False

    def __mywrite(self):
        f = open('/users/AUG/desktop' + os.sep + self.__logfile, 'w')
        f.write(self.data)
        f.close()

    def __del__(self):
        print('Have done.')
        pass


# module time is already loaded at first.
target = r'/Volumes/Seagate/Tencent/Dat/gext/pre'
# target = r'/Users/AUG/我的坚果云/tr'
# target = r'/Users/AUG/Desktop/tr'
# target = r'./overall'
# target = r'http://localhost'
# target = r'/Library/WebServer/Documents'
t1 = time.time()
my = MyDir(target)
print(my.data)
print('共有文件%s个' % my.num_file)
t2 = time.time()
sub = t2 - t1
print('用时%f秒' % sub)

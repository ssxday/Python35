# -*- coding:utf-8 -*-
"""
Manual:
请先实例化，
processor = MyProcessor()
~ 如果只想对单个标识进行整理，调用引擎engine()如下：
processor.engine(string <待整理的目录路径>, string <指定标识>, flag<是否操作子目录>)
~ 如果要指定多个标识，请把标识字符串放入文件listlib.py中的lib列表，在本程序下调用pichuli()如下：
processor.pichuli(string <待整理的目录路径>, flag<是否操作子目录>)
~ OK, easy as always!
"""
import re
import os


class MyProcessor:
    """
    本类功能
    1、通过引擎循环遍历目录中的文件和文件夹，对符合制定要求的文件名进行修改
    """

    loop = 0  # 核心部件执行的次数

    def pichuli(self, pathname='./overall', flag=False):
        """
        本方法通过map启动引擎，调用外部列表作为关键参数，
        从而实现了对指定目标的指定文件名进行整理
        :param pathname: 引擎需要的路径参数
        :param flag: 功能见engine()引擎
        :return: 修改次数的总和
        """
        import listlib  # 自定义的模块
        mp = map(self.engine, self.listchef(pathname, len(listlib.lib)), \
                 listlib.lib, self.listchef(flag, len(listlib.lib)))
        return sum(list(mp))

    def engine(self, pathname='./overall', zding='abp', flag=False):
        """
        批处理引擎
        需求：
        2、去掉hao与tail之间可能出现的标点符号
        :param pathname: 要处理的目录路径
        :param zding: 指定的字符串标识，大前提不能为空
        :param flag:默认False，只对当前目录进行处理。该值为True时，同时对子目录进行处理
        :return: 本次处理的次数
        """
        # 安全开关，参数的基本判断
        if not os.path.exists(pathname):
            return "路径不存在\nYour path doesn't exist."
        elif not os.path.isdir(pathname):
            return "目标必须是一个目录\nYour target should be a directory."
        elif len(zding) == 0:
            return "必须指定字符串标识\nA string should be designated here."

        files = os.listdir(pathname)
        for f in files:
            if not (f.startswith('.') or f.startswith('__')):
                if os.path.isfile(pathname + os.sep + f) \
                        and zding.lower() in f.lower():  # 判断f是文件,还得符合制定字符串在文件名中
                    # --执行核心开始--
                    src = pathname + os.sep + f
                    dst = pathname + os.sep + self.__zhiding(f, zding)
                    # 当目标路径已存在，
                    # 且不是自己本身的时候，
                    # 添加数字标识，以免覆盖掉既有的最简形式
                    if os.path.exists(dst) and src != dst:
                        # 下面把dst拆成文件名和后缀，中间插入数字序号以示区分
                        dst = os.path.splitext(dst)[0] + '(' + str(self.loop) + ')' \
                              + os.path.splitext(dst)[1]
                    # 当要改成的名字就是它自己时（说明已经化为标准最简形式），跳过本轮循环，
                    # 不执行改名，
                    # 节省运算资源
                    elif os.path.exists(dst) and src == dst:
                        continue
                    os.rename(src, dst)
                    # --执行核心结束--
                    self.loop += 1
                elif os.path.isdir(pathname + os.sep + f) and flag:
                    self.engine(pathname + os.sep + f, zding, flag)
                else:
                    pass

        return self.loop

    def __zhiding(self, filename, zding='abp'):
        """
        __私有方法
        对包含指定字符串标记zding的文件名filename进行整理
        在引擎engine中，已经对是否为文件进行了判断，这里只研究一个问题，把新文件名整理出来
        :param filename:
        :param zding:
        :return: 重新整理过的字符串
        """
        # 判断filename里有没有指定的字符串
        # 在engine中已经有判断过，为了保持其逻辑完整性
        # 和单独工作的能力，此处再独立判断一次
        # 首先判断最基本的包含关系
        if zding.lower() in filename.lower():
            # 对多重包含关系进行选择，并最终决定是选择还是跳过
            pat_fan = '[a-z]*' + zding + '[a-z]*'  # 凑正则
            fanlist = re.findall(pat_fan, filename, re.I)
            if zding.lower() in [i.lower() for i in fanlist]:  # 漏洞是如果后面偶然出现了完全匹配，无比避免的绕过本if
                # 确定zding已是最简，没有更大的字符串对其进行包含，就是zding
                fan = zding.upper()
            else:
                # 说明filename中还有包含zding的字符串
                return filename

            # 确定指定的字符串存在，找其后面的数字
            start = filename.lower().find(zding.lower())
            half_str = filename[start + len(zding):]  # fan之后的，带有扩展名的字符串
            # hao当然是在fan之后的prefix里找
            prefix = os.path.splitext(half_str)[0]  # prefix是half_str的文件名部分
            # 注意！被splitext()切出来的扩展名是带.的!!!!!
            suffix = os.path.splitext(half_str)[1]  # suffix是half_str的扩展名部分
            # 从half_str里找后面的第一组数字
            try:
                hao = re.findall(r'\d{3,}', prefix)[0]
            except IndexError:
                return filename
            else:  # half_str中找到了3位及以上的数字
                # 截取数字后的字符串尾巴
                tail = prefix[prefix.find(hao) + len(hao):]
                return "%s-%s %s%s" % (fan, hao, tail.strip(), suffix) \
                    if tail.strip() != '' else "%s-%s%s" % (fan, hao, suffix)
        else:
            return filename

    def listchef(self, element, n):
        """
        这是一个用于生成重复元素列表的函数
        列表中将会有n个element
        :param element:指定填充何种数据
        :param n: 指定元素个数
        :return: 生成的重复元素列表
        """
        return [element, ] * n

    def shift(self, pathname='./overall', flaw=':', flag=False):
        """
        批处理引擎
        :param pathname: 要处理的目录路径
        :param flaw: 指定的字符串标识，大前提不能为空
        :param flag:默认False，只对当前目录进行处理。该值为True时，同时对子目录进行处理
        :return: 本次处理的次数
        """
        # 安全开关，参数的基本判断
        if not os.path.exists(pathname):
            return "路径不存在\nYour path doesn't exist."
        elif not os.path.isdir(pathname):
            return "目标必须是一个目录\nYour target should be a directory."
        elif len(flaw) == 0:
            return "必须指定字符串标识\nA string should be designated here."

        files = os.listdir(pathname)
        for f in files:
            if not (f.startswith('.') or f.startswith('__')):
                if os.path.isfile(pathname + os.sep + f) \
                        and flaw.lower() in f.lower():
                    # --执行核心开始--
                    src = pathname + os.sep + f
                    dst = pathname + os.sep + f.replace(flaw, ' - ')  # 只有这里同engine不一样
                    if os.path.exists(dst) and src != dst:
                        dst = os.path.splitext(dst)[0] + '(' + str(self.loop) + ')' \
                              + os.path.splitext(dst)[1]
                    elif os.path.exists(dst) and src == dst:
                        continue
                    os.rename(src, dst)
                    # --执行核心结束--
                    self.loop += 1
                elif os.path.isdir(pathname + os.sep + f) and flag:
                    self.shift(pathname + os.sep + f, flaw, flag)
                else:
                    pass

        return self.loop

    def __del__(self):
        # print('I will be back!')
        pass


processor = MyProcessor()
# print(processor.pichuli('./overall',True))

if input('Proceed?(y for yes else for nothing):') == 'y':
    import time

    t1 = time.time()
    # 要计时的脚本start
    print(processor.pichuli(r'/Volumes/Seagate/Tencent/Dat/gext/pre/LakeEast', True))
    # print(processor.engine('./overall','dv',True))
    # print(processor.shift('./overall',':',True))
    # 要计时的脚本end
    t2 = time.time()
    sub = t2 - t1
    print('Time Cost:%f seconds' % sub)

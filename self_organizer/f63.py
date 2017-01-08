# -*- coding:utf-8 -*-
import re, os


class F63:
    loop = 0

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
                if True:  # os.path.isfile(pathname + os.sep + f):  # 判断f是文件,还得符合制定字符串在文件名中
                    # --执行核心开始--
                    src = pathname + os.sep + f
                    dst = pathname + os.sep + self.jiexi(f, zding)
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
                # elif os.path.isdir(pathname + os.sep + f) and flag:
                #     self.engine(pathname + os.sep + f, zding, flag)
                # else:
                #     pass

        return self.loop

    def __ridof(self, string='', *substr):
        for s in substr:
            string = string.replace(s, '')
        return string

    def jiexi(self, string='', zding=''):
        if True:  # zding.lower() in string.lower():
            # 确定各部分的正则匹配
            if zding.lower() in ['cari', 'carib']:
                ptn_head = r'cari(?:bbean|bpr|b)?|cappv|加勒比PPV動畫|加勒比'
            elif zding.lower() in ['1pon', '1pond', '1pondo']:
                ptn_head = r'1pon(?:do|d)?|一本道'
            else:
                return string
            ptn_chuanhao = r'\d{6}[ \-_]+\d{3}'
            ptn_riqi = r'\D?(\d{6})\D?'
            ptn_xuhao = r'\D+(\d{3})\D?'
            # 对各部分进行匹配，如果抓取失败则return最初的string
            try:
                head = re.findall(ptn_head, string, re.I)[0]
                chuanhao = re.findall(ptn_chuanhao, string, re.S)
                if len(chuanhao) == 1:
                    xuhao = re.findall(ptn_xuhao, chuanhao[0])[0]
                else:
                    return string
                middle = re.findall(ptn_riqi, chuanhao[0], re.S)[0]
            except IndexError:
                return string

            # 在处理完leftover前，不要改动head,middle,xuhao的格式！！！！！
            leftover = self.__ridof(string, head, middle, xuhao, '-', '_', ' ', '@')
            if head.lower() in ['cari', 'carib', 'caribbean', '加勒比']:
                head = 'Carib'
            elif head.lower() in ['cappv', '加勒比ppv動畫']:
                head = 'CAPPV'
            elif head.lower() in ['1pon', '1pond', '1pondo', '一本道']:
                head = '1pond'
            else:
                head = head.title()
            return "%s-%s-%s %s" % (head, middle, xuhao, leftover)
        else:
            return string


agent = F63()

# 单独调试jiexi()
# print(agent.jiexi(c7,'cari'))

if input('Proceed?(y for yes else for nothing):') == 'y':
    import time

    t1 = time.time()
    # 要计时的脚本start
    # print(processor.pichuli('./overall',True))
    # print(agent.engine(r'/Users/AUG/我的坚果云/tr', 'cari', True))
    print(agent.engine(r'/Volumes/Seagate/Tencent/Dat/gext/pre/LakeEast/Carib', 'cari', False))
    # print(processor.shift('./overall',':',True))
    # 要计时的脚本end
    t2 = time.time()
    sub = t2 - t1
    print('Time Cost:%f seconds' % sub)

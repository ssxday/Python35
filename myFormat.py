# -*- coding:utf-8 -*-
'''
本程序用来批量修改文件名，并进行目录操作
'''
import re,os


class automatic:

    ptn_fan = re.compile(r'[a-z]+',re.I)
    ptn_hao = re.compile(r'\d+')

    def arrange(self, filename):
        '''
        功能是解析重构文件名
        1、避开exception，把以字母开头的，番号不带-的字符串中间插入-
        2、番号全部大写
        :param filename:
        :param fan:
        :param hao:
        :return: 改好的字符串
        '''
        # exceptions = ['1pon','s2m','t28','cari','sm3d']
        # # print(all(list(map(lambda x:filename.count(x),exceptions))))
        # if any(map(lambda x:filename.lower().count(x),exceptions)):  # exception中，只要有一个配上了，就原样输出。
        #     return filename

        # try:  # 如果文件名中没有捕捉到数字，列表就会为空，用索引取值时将发生错误
        #     fan = re.findall(pattern_fan,filename,re.I)[0]
        #     hao = re.findall(pattern_hao,filename,re.I)[0]
        # except IndexError:
        #     return filename

        fan = self.ptn_fan.findall(filename)[0]
        hao = self.ptn_hao.findall(filename)[0]
        posi = filename.find(hao)
        des = filename[posi+len(hao):]
        # print(posi)
        return '%s-%s%s'%(fan.upper(),hao,des)

    loop = 0

    def pichuli(self,pathname='./overall',flag=False):
        """

        :param pathname:待处理的目录路径
        :param flag: 默认False，不对子目录进行操作。flag=True时，连同子目录一起操作
        :return: 修改文件名的次数
        """
        files = os.listdir(pathname)
        exceptions = ['.py','1pon', 's2m', 't28', 'cari', 'sm3d']
        for f in files:  # f 代表filename
            if any(map(lambda x: f.lower().count(x), exceptions)):  # exception中，只要有一个配上了，就原样输出。
                continue

            # try:  # 如果文件名中没有捕捉到数字，列表就会为空，用索引取值时将发生错误
            #     m = self.ptn_fan.findall(f)[0]
            #     n = self.ptn_hao.findall(f)[0]
            # except IndexError:
            #     continue

            if not f.startswith('.') and not f.startswith('__'):
                # print(os.path.isfile(pathname + '/' + f))
                if os.path.isfile(pathname+'/'+f):  # 判断是否是文件
                    try:  # 如果文件名中没有捕捉到数字，列表就会为空，用索引取值时将发生错误
                        fan = self.ptn_fan.findall(f)[0]
                        hao = self.ptn_hao.findall(f)[0]
                    except IndexError:
                        continue
                    dst = pathname+'/' + self.arrange(f)
                    src = pathname+'/'+f
                    os.rename(src,dst)
                    self.loop += 1
                elif os.path.isdir(pathname+'/'+f) and flag:
                    self.pichuli(pathname+'/'+f)
        return self.loop


prcsor = automatic()

print(prcsor.pichuli('./overall'))


# filenamelist = [
#     'sky065紅たる.torrent',
#     'SM3DBD-04 本リ[左寬].mp4',
#     '1pondo-090112_419-HD上ぐMgu「時巨.avi',
#     'heY_0917-张三.mkv',
#     'SMbD-162) S Model 162 厚中~谷音.avi',
#     '东京热n0076-n0080.torrent',
#     'aBp_318-hD.24sui好'
# ]
#

# fname = 'prnt'
# a = fname[4:]
# print(a=='')
# b = 'qianmian' if a!='' else 'houmian'
# print(b)

# a = os.path.splitext('aBp_314.aaa')
# print(a)





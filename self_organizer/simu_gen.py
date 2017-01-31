# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:simu_gen.py
Author:
Version:
Description:
本程序可以以某个目录的结构为蓝本，在指定位置重新创建一套具有相同目录结构的文件夹
其中的文件以少许字节填充，并不具备母本的功能
"""
import os
from common_use import Constant


class SimuGen:
    FILLING = b"""p!$vx)o(&@|2sk#1t83>9dhn?*%^0wgfe;45gcm:"u7r/aq'<lzbi6y"""
    DST = r'/Users/AUG/Desktop/'

    def __init__(self, root_dir):
        self.src_root = root_dir
        p, name = os.path.split(root_dir)
        self.dst_root = os.path.join(self.DST, name)
        if os.path.exists(self.dst_root):
            raise FileExistsError('目标已存在，请另外新建。')
        else:
            os.mkdir(self.dst_root)
        self.engine(root_dir)

    def engine(self, src_root):
        files = os.listdir(src_root)
        for file in files:
            if not file.startswith('.') and not file.startswith('_'):
                srcpath = os.path.join(src_root, file)
                dstpath = srcpath.replace(self.src_root, self.dst_root)
                if os.path.isdir(srcpath):
                    os.mkdir(dstpath)
                    self.engine(srcpath)
                elif os.path.isfile(srcpath):
                    with open(dstpath, 'wb') as simu_f:
                        simu_f.write(self.FILLING)


if __name__ == '__main__':
    sg = SimuGen(Constant.THEONE)

# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:

"""
import re
import os

pathname = '/Volumes/Seagate/Tencent/Dat/gext/pre/LakeEast/1pondo'
names = os.listdir(pathname)
ptnobj = re.compile(r'^1pondo', re.I)
for name in names:
    namepath = os.path.join(pathname, name)
    if not name.startswith('.'):
        # 正式开始判断
        nameafter = ptnobj.sub('1pond', name, 1)
        if nameafter != name:
            # 如果与标准格式不同
            print('{src}\n{dst}\n'.format(src=name, dst=nameafter))
            # os.rename(namepath, os.path.join(pathname, nameafter))

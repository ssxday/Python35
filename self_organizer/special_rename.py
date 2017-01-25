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

pathname = '/users/aug/lakessd'
names = os.listdir(pathname)
ptnobj = re.compile(r'[\W]?blacked[^0-9a-z]+', re.I)
for name in names:
    namepath = os.path.join(pathname, name)
    if os.path.isfile(namepath) and not name.startswith('.'):
        # 正式开始判断
        nameafter = ptnobj.sub('BLACKED - ', name, 1)
        if nameafter != name:
            # 如果与标准格式不同
            print('{src} 改成 {dst}'.format(src=name, dst=nameafter))
            # os.rename(namepath, os.path.join(pathname, nameafter))

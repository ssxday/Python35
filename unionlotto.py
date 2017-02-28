# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:双色球

"""
from collections import namedtuple

Lotto = namedtuple('UnionLotto', 'A B C D E F G')
l1 = Lotto(10, 12, 15, 24, 29, 31, 6)
print(l1)
for i in l1:
    print(i)


class UnionLotto:
    """"""



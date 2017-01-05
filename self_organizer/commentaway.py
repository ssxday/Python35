# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:commentaway.py
Description:本程序将自动处理掉Python代码中的注释

Author:
Version:1.0
"""
import os
comment_sign = r'#'
src = r'/Users/AUG/Desktop/fnameReg.py'
dst = '-cc'.join(os.path.splitext(src))


def whereisalone(line='', sign='#'):
    """找不被quot包裹的的sign的位置"""
    # 找sign左侧的quot个数
    posi = -1
    for s in line:
        posi += 1
        if s == sign:  # 依次碰到#
            count_q = line[:posi].count("'")
            count_dq = line[:posi].count('"')
            if count_q % 2 == 0 and count_dq == 0:
                return posi
    # 找不到落单的sign
    raise EOFError


def newline(line=''):
    """围绕着#展开
    1、确定有没有#，没有井号的原样输出
    2、出现了#：
        #是否出现在去掉空白的开头位置
        #没有出现在开头位置
    """
    if r'#' not in line:
        # 没有#则原样输出
        return line
    else:
        # 出现了#，则找第一个左侧quot个数是偶数(包括0)的#的位置
        try:
            comment_start_posi = whereisalone(line)
        except EOFError:
            return line
        return line[:comment_start_posi].rstrip()+os.linesep if line[:comment_start_posi].strip() != '' else ''


with open(src) as srcfile:
    with open(dst, 'w') as dstfile:
        for line in srcfile.readlines():
            dstfile.write(newline(line))







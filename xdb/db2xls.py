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
import xlwt
from xdb.dborm import Candidate

rows = Candidate.readrow()


def to_xls():
    rnum = 0
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    # 遍历to_xls_data
    while rows:
        try:
            row = rows.__next__()  # 取出一个行对象
        except StopIteration:
            break
        for col in range(7):
            worksheet.write(rnum, col, row.get(col))
        rnum += 1
    workbook.save('/Users/aug/Desktop/essence-{}.xls')

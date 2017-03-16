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
import xlrd  # 文档 http://xlrd.readthedocs.io/en/latest/

# 读取xls文件,formatting_info默认为False，将无法识别合并单元格
xfile = xlrd.open_workbook(r'/users/aug/desktop/11.xls', formatting_info=True)
print(xfile)  # <xlrd.book.Book object at 0x1007a1f28>

# 选择工作表(sheet)
# 列出工作表列表
print('所有的sheets', xfile.sheets())  # 返回所有工作表对象的列表
print('所有sheets的名称', xfile.sheet_names())  # 返回所有工作表对象的列表
# 通过索引选择sheet
sheet1 = xfile.sheet_by_index(0)
print('选择了工作表：', sheet1)
print(sheet1.name)  # 本sheet对象的名称
print(sheet1.ncols)  # 列数
print(sheet1.nrows)  # 行数，数据数量
# 获取行
print(sheet1.row(6))  # 返回行号对应的cell对象列表
print(sheet1.row_values(6))
rows = sheet1.get_rows()  # 以行为单位的生成器
print('行生成器:',rows)
print(rows.__next__())

# 获取单元格
cell61 = sheet1.cell(6, 1)
print(cell61)  # ctype:value
# 单元格ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
print('ctype:', cell61.ctype)
# 查出哪些地方是合并的单元格
mergedcells = sheet1.merged_cells
print('合并的单元格：', mergedcells)
ar = sheet1.row_types(0)
print(list(ar))
print(all(ar))
print(sheet1.row(0))
# help(ar)

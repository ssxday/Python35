# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:
将excel文件内容导入数据库
"""
import xlrd
from sqlalchemy import create_engine, String, Integer, Column


# from sqlalchemy.orm

# 选择xls文件并读取到一个对象里去
class XRead:
    def __init__(self, file, sheet_no=1, skip1st=True):
        xfile = xlrd.open_workbook(file, formatting_info=True)
        self.__sheet = xfile.sheet_by_index(sheet_no - 1)
        self.__skip = skip1st  # 是否跳过假设的表头(第一满行)

    @property
    def table_title(self):
        """提取出合并单元格做表头"""
        merged = self.__sheet.merged_cells
        if merged:  # 存在合并的单元格
            for row, rowrange, col, colrange in merged:
                if col == 0 and colrange == self.__sheet.ncols:
                    # 第一个横跨合并整个表的单元格，应该就是表头
                    return self.__sheet.cell_value(row, col)
        return self.__sheet.name

    def first_solid_row(self):
        """找第一行满列的行索引"""
        for row_no in range(self.__sheet.nrows):
            types = [self.__filter(i) for i in self.__sheet.row_types(row_no)]
            if all(types):
                return row_no
        return 0

    def rread(self):
        """"""
        rows = self.__sheet.get_rows()
        start = self.first_solid_row()  # 第一个满行的索引号
        if self.__skip:  # 跳过第一满行
            start += 1
        else:  # 不跳过第一满行
            pass
        while start > 0:
            # 跳过
            rows.__next__()
            start -= 1
        for row in rows:
            yield [unit.value for unit in row]

    @staticmethod
    def __filter(i):
        if i == 6:  # 6是合并单元格的blank类型
            return 0
        return i


xls = XRead('/users/aug/desktop/11.xls')
print(xls.table_title)
print('从第{}行索引开始'.format(xls.first_solid_row()))
rs = xls.rread()
# fir = rs.__next__()
# print(fir)
# for f in fir:
#     print(f.value)
# for r in rs:
#     gai = [i.value for i in r]
#     print(gai)
print(rs.__next__())
for r in rs:
    print(r)

"sis578 18718175437"

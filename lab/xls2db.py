# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:xls2db.py
Author:
Version:
Description:
- 将excel文件内容导入数据库
- 本模块与dborm模块紧密依赖
- 在处理xlsx文件时，formatting_info须设为False，否则报错
- 使用方法：
    1、构造dborm.py中的数据库模型
    2、构造本模块中的RowData对象
    3、conveyor(filepath, sheet_no, skip1st)
"""
import xlrd
from lab.dborm import Candidate


# 选择xls文件并读取到一个对象里去
class XRead:
    def __init__(self, file, sheet_no=1, skip1st=True, formatting_info=True):
        xfile = xlrd.open_workbook(file, formatting_info)
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

    def __first_solid_row_index(self):
        """找第一行满列的行索引"""
        for row_no in range(self.__sheet.nrows):
            types = [self.__filter(i) for i in self.__sheet.row_types(row_no)]
            if all(types):
                return row_no
        return 0

    def rread(self):
        """"""
        rows = self.__sheet.get_rows()
        start = self.__first_solid_row_index()  # 第一个满行的索引号
        if self.__skip:  # 跳过第一满行
            start += 1
        else:  # 不跳过第一满行
            pass
        while start > 0:
            # 跳过
            rows.__next__()
            start -= 1
        for row in rows:
            yield list(RowData(row))

    @staticmethod
    def __filter(i):
        if i == 6:  # 6是合并单元格的blank类型
            return 0
        return i


class RowData:
    """构造成一个迭代器，使得对象实例可以被list()一步转化为列表
    对于不同的xls表格，需要预先定义不同的行数据
    """
    Branch = {'应届毕业生': 1, '在职人才': 2, '归国留学人员': 3}
    Degree = {'本科': 1, '硕士研究生': 2, '博士研究生': 3}
    Stage = {'租房补贴首发': 0}

    def __init__(self, lyst):
        self.__l = [unit.value for unit in lyst]
        self.__l[4] = self.Branch.get(self.__l[4])
        self.__l[5] = self.Degree.get(self.__l[5])
        self.__l[6] = self.Stage.get(self.__l[6])

    def __iter__(self):
        return self

    def __next__(self):
        if self.__l:
            return self.__l.pop(0)
        else:
            raise StopIteration


def conveyor(filepath, sheet_no=1, skip1st=True):
    xls = XRead(filepath, sheet_no, skip1st)
    # print(xls.table_title)
    # print('从第{}行索引开始'.format(xls.first_solid_row_index()))
    rs = xls.rread()
    for r in rs:
        Candidate(*r).insert()


if __name__ == '__main__':
    """"""
    conveyor('/users/aug/desktop/11.xls', 2)

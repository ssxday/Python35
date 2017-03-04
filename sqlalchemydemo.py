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
from common_use import Constant
# 先得创建一个引擎
from sqlalchemy import create_engine
# 查询也需要用到模型
from sqlalchemy.ext.declarative import declarative_base
# 构造模型就得用行，列，数据类型什么的
from sqlalchemy import Column, Integer, String
# 要查询就得用会话事务
from sqlalchemy.orm import sessionmaker

import sqlalchemy

print(sqlalchemy.__version__)

# 创建引擎
drive = r'sqlite:///' + Constant.SQLITE + '/wordworld.db'
engine = create_engine(drive, echo=False)
# print(type(engine))
print(engine.table_names())  # 返回所有表名的列表，如果确定库里面有表，则正好验证是否连接成功
# 创建orm模型
DBase = declarative_base(engine)


class Word(DBase):
    __tablename__ = 'freshword'
    wid = Column(Integer, primary_key=True, autoincrement=True)
    attr = Column(Integer)
    chn = Column(String, nullable=False)
    eng = Column(String, nullable=False)
    date = Column(String, nullable=False)  # 现加的
    source = Column(String)

    def __repr__(self):
        return """<Word {}:{}:{}>""".format(self.wid, self.chn, self.eng)


class Attr(DBase):
    __tablename__ = 'attr'
    mark = Column(Integer, primary_key=True)
    attr = Column(String)

    def __repr__(self):
        return """<Attr {} = {}>""".format(self.mark, self.attr)


# 通过模型创建表
# Word.metadata.create_all(engine)

# 创建会话事物
Sess = sessionmaker(bind=engine)
shiwu = Sess()
# 查询
print(' retrieve查询 '.center(50, '*'))
# 查询对象
soso = shiwu.query(Word, Attr)
"""
query()要查的参数可以是多个，可以是一个表，也可以是某个表的某一列
如果是多个(其实一个也算多个)，返回的对象(每行)是个可以用键名访问的元组
结果是每个查询对象的行的全部组合，数量=arg1*arg2
"""
for 代表组合中的Word, 代表组合中的Attr in soso:
    print(代表组合中的Word.chn, '##', 代表组合中的Attr.attr)
print('结果共计个数', soso.count())

# 过滤结果
print('过滤结果'.center(30, '='))
ft = soso.filter_by(attr=2)  # 指的是第一个查询对象Word的attr
print('#', ft.all())
# 用filter()过滤
qu = shiwu.query(Word)  # 重新开始一个查询
# filter()的各种条件表达：
# 大于(等于)
ft = qu.filter(Word.attr >= 1)
print('@', ft.all())
# like()
ft = qu.filter(Word.eng.like('app%'))
print('LIKE', ft.all())
# in_(例子列表)
ft = qu.filter(Word.eng.in_(['apple', 'kevin']))
print('IN', ft.scalar())
print('IN', ft.one() is ft.scalar())
print('IN', ft.all())
# NOT IN ~~~~
ft = qu.filter(~Word.eng.in_(['apple', 'apply']))
print('NOT IN', ft.all())
# is null -> is_(None)
ft = qu.filter(Word.date.is_(None))  # None stands for NULL
print('date为空的行', ft.all())  # 这些行的date列是空的
# is not null -> isnot(None)
ft = qu.filter(Word.date.isnot(None))
print('date非空的行', ft.all())  # 这些行的date列是非空的
# 逻辑and -> 3种表达：
# 1、另外引入操作符 from sqlalchemy import and_
# filter(and_(条件1,条件2))
# 2、用逗号罗列filter(条件1,条件2)条件 ==> 罗列多个条件其逻辑是AND
# 3、多次连接filter(条件1).filter(条件2)
ft = qu.filter(Word.date.isnot(None), Word.attr == 2)
print('同时满足date非空，还是动词', ft.all())
# 逻辑或 -> 引入新的操作符or_
from sqlalchemy import or_

ft = qu.filter(or_(Word.date.isnot(None), Word.attr == 2))
print('满足date非空，或者是动词', ft.all())

# 添加数据行
print(' add增加 '.center(50, '*'))


# 封装一个函数
def add_word(eng, chn, attr=0, date=None, source=None):
    word = Word(attr=attr, chn=chn, eng=eng, date=date, source=source)
    shiwu.add(word)
    shiwu.commit()


# add_word('front', '前线', 1)

# 删除数据
print(' delete删除 '.center(50, '*'))


# 先查询出结果，再调用删除方法
# 封装一个函数
def delem(where=70):
    s = Sess()  # 再生产一个会话
    to_del = s.query(Word).filter(Word.wid > where).delete()
    print('要删除{}个数据'.format(to_del))  # 返回准备删除的行数
    s.commit()  # 最后必须commit()


delem()

print(' update修改 '.center(50, '*'))


# 先查询，再修改
def update(which, where, what):
    """把which表的wid等于where那一行的数据的date列的值改成what"""
    s = Sess()
    to_up = s.query(which).filter(which.wid == where).update({'date': what})
    print('要修改%d行' % to_up)  # 将被改动的地方有几行
    s.commit()


update(Word, 4, None)

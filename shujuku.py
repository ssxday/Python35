# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:
一些ORM框架举例
SQLObject
Storm
Django's ORM
Peewee
Pony ORM
SQLAlchemy
1、工作单元
2、会话session单元
3、擅长处理多数据库

创建SQLalchemy应用
1、创建连接
2、
"""
from common_use import Constant
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

conn_str = r'sqlite:///'+Constant.SQLITE+'/jike.db'
engine = create_engine(conn_str, echo=True)

Base = declarative_base()  # 返回一个基类


class User(Base):
    __tablename__ = 'users'
    idd = Column(Integer, primary_key=True)
    name = Column(String(10))
    pswd = Column(String(28))

    def __repr__(self):
        return "<{}(id='{}' name='{}' password='{}')>".format(
            __name__, self.idd, self.name, self.pswd)

# 执行创建数据库表
User.metadata.create_all(engine)

# SQL事务
# 创建会话session
from sqlalchemy.orm import sessionmaker  # 类,工厂函数,但是不知道绑哪个引擎
Sess = sessionmaker(bind=engine)  # 绑定连接引擎,还是一个类
print(type(Sess))  # <class 'sqlalchemy.orm.session.sessionmaker'>

session = Sess()  # 事务都在一个Sess实例里
print('变量名session打印：',session)  # <sqlalchemy.orm.session.Session object>

# 持久化一个实例对象，增：
# ed_user = User(2, 'ed', 'edpassword')  # 错误写法！！
# ed_user = User(idd=2, name='ed', pswd='edpassword')
# ed_user = User(idd=1, name='edison', pswd='edisonspassword')  # 数据表的行
zhangsan = User(name='张三', pswd='sanord')  # 数据表的行
lisi = User(name='lisi', pswd='lisiiiiining')  # 数据表的行
# print(ed_user)
# session.add(ed_user)
# session.add_all([
#     zhangsan,lisi,
# ])

# 删
# 改
# 查
# 最终落脚到all()或者first()才有结果集列表
the_user = session.query(User).filter(User.name=='lisi').all()
print('@@',the_user)
print('类型是：',type(the_user))
print(the_user[0].pswd)

session.commit()

# 使用SQLAlchemy Core层创建表
from sqlalchemy import MetaData,Table,ForeignKey
metadt = MetaData()
students = Table('studentable',metadt,
                 Column('id',Integer,primary_key=True),
                 Column('name',String(18)),
                 Column('sex',String(4)))
hometowm = Table('laojia',metadt,
                 Column('id',Integer,primary_key=True),
                 Column('place',String(20)),
                 Column('student_id',None,ForeignKey('studentable.id'))  # 一定要写表的名称而不是对象的变量名
                 )

metadt.create_all(engine)


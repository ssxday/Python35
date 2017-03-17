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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, String, Integer, Column, ForeignKey
from sqlalchemy.orm import sessionmaker

drive = r'sqlite:///' + Constant.SQLITE + '/candidates.db'
engine = create_engine(drive)
Base = declarative_base(engine)
Sess = sessionmaker(engine)


class OpMth:
    def insert(self):
        s = Sess()
        try:
            s.add(self)
            s.commit()
            return self.__dict__.__len__()
        except Exception as e:
            s.rollback()
            return e


# 构造ORM
class Candidate(Base, OpMth):
    __tablename__ = 'candidates'
    cid = Column(Integer, primary_key=True)
    name = Column(String)
    idnum = Column(String)
    age = Column(String)
    branch = Column(String)
    degree = Column(String)
    stage = Column(String)

    def __init__(self, cid, name, idnum, age, branch, degree, stage):
        self.cid = cid
        self.name = name
        self.idnum = idnum
        self.age = age
        self.branch = branch
        self.degree = degree
        self.stage = stage

    def __repr__(self):
        desc = '<Candidate {}{}{}>'.format(self.cid, self.name, self.age)
        return desc


class Degree(Base, OpMth):
    __tablename__ = '学历'
    did = Column(Integer, ForeignKey(Candidate.degree), primary_key=True)
    desc = Column(String)

    def __init__(self, did, desc):
        self.did = did
        self.desc = desc


class Branch(Base, OpMth):
    __tablename__ = '类别'
    bid = Column(Integer, ForeignKey(Candidate.branch), primary_key=True)
    desc = Column(String)

    def __init__(self, bid, desc):
        self.bid = bid
        self.desc = desc


class Stage(Base, OpMth):
    __tablename__ = '发放期数'
    sid = Column(Integer, ForeignKey(Candidate.stage), primary_key=True)
    desc = Column(String)

    def __init__(self, sid, desc):
        self.sid = sid
        self.desc = desc


if __name__ == '__main__':
    """"""
    Candidate.metadata.create_all(engine)

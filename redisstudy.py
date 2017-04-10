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
import redis
from common_use import RedisConf
rs = redis.StrictRedis(password=RedisConf.AUTH)
# keys命令
print(rs.keys())
# string类型
# ap = rs.append('us',['zhangsan','lisi','wangwu'])
# print(ap)
# get = rs.get('us')
# print(get.decode())
# print(type(get.decode()))
# list类型
lp = rs.lpush('digi',*[1,2,3,4,5])
print(lp)
g = rs.lrange('ll',0,-1)
print(g)
print(type(g[0]))
help(rs.expire)


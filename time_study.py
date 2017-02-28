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
import datetime
import time
import calendar

# datatime.date类
print('datatime.date类'.center(50, '*'))
chunjie = datetime.date(2017, 1, 27)
print(chunjie)
print(type(chunjie.ctime()))

# today()
td = datetime.date.today()
print(td)

# ctime()
ctime_str = chunjie.ctime()
print(ctime_str)  # <string> Fri Jan 27 00:00:00 2017

# isoformat()
print(chunjie.isoformat())

# isocalendar()
cld = chunjie.isocalendar()  # Return a 3-tuple (ISO year, week number, weekday)
print(cld)
print(type(cld))

# weekday
weekday = chunjie.weekday()
print(weekday)  # monday==0, sunday==6 这个weekday和isocalendar的weekday标准不同

# datatime.time类
print('datatime.time类'.center(50, '*'))

dinner = datetime.time(18, 31, 17, 200000)  # 微秒，不是毫秒
print('吃饭时间', dinner)
print(type(dinner))  # <class 'datetime.time'>

# isoformat()
iso = dinner.isoformat()
print('iso', iso)

print('datatime.datetime类'.center(50, '*'))
# now(cls)
now = datetime.datetime.now()
print('此时此刻', now)

launch = datetime.datetime(2017, 12, 17, 9, 27, 41, 370000)
print(launch)  # datetime-obj 2017-12-17 09:27:41.370000

# isoformat() 中间的T把日期和时间分开
print(launch.isoformat())  # 字符串 '2017-12-17T09:27:41.370000'

# date()
dt = now.date()
print(dt)
print(type(dt))

# combine()
nianyefan = datetime.datetime.combine(chunjie, dinner)  # 把一个date对象和一个time对象拼成一个datetime对象
print('年夜饭什么时候吃', nianyefan)

print('datatime.timedelta类'.center(50, '*'))
interval = datetime.timedelta(minutes=40)
after_interval = now + interval
print(after_interval)  # 40分钟以后的时间

print('time模块'.center(50, '='))
# time.time() -> 返回当前时间的Unix纪元值
epoc = time.time()  # float
print(epoc)

# localtime(纪元值) -> 返回当前的struct_time
structtimeobj = time.localtime()
print('当地地时间', structtimeobj)
# gmtime()
print('格林尼治时间', time.gmtime())

# struct_time对象
y = structtimeobj
print(y.tm_year)

print('calendar模块'.center(50, '='))

h = calendar.calendar(2017)
print(h)
print(type(h))

m = calendar.month(2017, 2)
print(m)


def 是闰年吗(year):
    return calendar.isleap(year)


y = int(input('输入年份：'))
print('{}年{}是闰年'.format(y, ('不', '')[是闰年吗(y)]))

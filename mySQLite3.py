# -*- coding:utf-8 -*-
import sqlite3
# 连接数据库
conn = sqlite3.connect(r'/Users/AUG/Documents/sqlite3lib/enterprise.db')
help(sqlite3.connect)
print(conn)  # <sqlite3.Connection object at 0x101187c70>

# 创建cursor对象来管理指令
curs = conn.cursor()
print(curs)  # <sqlite3.Cursor object at 0x1012bfb20>

# ce = curs.execute(
#     """CREATE TABLE zoo
#     (critter VARCHAR(20) PRIMARY KEY,
#     count INT,
#     damages FLOAT)"""
# )
# print(ce)  # <sqlite3.Cursor object at 0x1023bfb20>

# sql_in = """INSERT INTO zoo(critter,count,damages) VALUES(?,?,?)"""
# curs.execute(sql_in,('duck',5,0.0))
# curs.execute(sql_in,('bear',2,1000.0))
curs.execute('INSERT INTO zoo VALUES("duck",5,0.0)')

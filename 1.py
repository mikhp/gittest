#!/usr/bin/python3

import pymysql

# 打开数据库连接

db = pymysql.connect(
    host='localhost',
    port=3306,
    db='hpdb',
    user='root',
    passwd='',
    charset='utf8'
)

# 使用 cursor() 方法创建一个游标对象 cursor66
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")

cursor.execute("select * from T_user where username='胡平';")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print(data)

# 关闭数据库连接
db.close()

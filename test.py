# coding=utf-8
import requests
import json
from PIL import *
import pymssql
import MySQLdb
payload = {'key1': u'卧槽', 'key2': u'你好'}
r = requests.get("http://httpbin.org/get", data=payload)
x = r.headers
print x


# conn = MySQLdb.connect(host='192.168.6.238', user='root', passwd='123456')
# cur = conn.cursor()
# sql = "SHOW TABLES FROM yangqing"
# cur.execute(sql)
# info = cur.fetchall()
# for i in info:
#     print i[0]
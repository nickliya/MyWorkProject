#!/usr/bin/python
# coding=utf-8
# creat by 15025463191
import pymssql
import random
import socket

conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
cur = conn.cursor()
IM = 'yv4Z0Vhe1gxf4377'
a = "SELECT mac FROM [sirui].[dbo].[Terminal] where IMEI=\'" + IM + "\';"
print a
cur.execute(a)
info = cur.fetchall()
mac = str(info)[4:-4]
cur.close()
conn.close()

print mac

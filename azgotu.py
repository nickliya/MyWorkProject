#!/usr/bin/python
#coding=utf-8
#creat by 15025463191
import socket
import re
import time
IMEI = input('请输入IMEI号：')

print('测试开始，请根据提示完成后输入1敲回车')
time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.6.154',2103))

s.send('(1*7c|a3|106,201|101,'+str(IMEI)+'|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')

input('请刷新手机，填写车辆信息来到第一步:')

s.send('(1*74|7|30f,14,333e,331a,GSM850_EGSM_DCS_PCS_MODE|)(1*33|7|30C,1,1,1,D,1|)')

input('请刷新手机来到第二步:')

s.send('(1*12|7|301,2,1111)(1*88|7|316,1,1,4B0,4F0|)')

input('请刷新手机来到第三步:')

s.send('(1*12|7|301,1,1111)')

input('请刷新手机来到第四步:')

s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')

input('请点击测试启动:')

data = s.recv(1024)
time.sleep(2)

r = r'\(\*..\|7\|\d\d\d,\w*?,1\|\)'

datainfo = re.findall(r,data)
str_data = str(datainfo[0])
a = str_data[0]+'1'+str_data[1:5]+'8'+str_data[6:]
s.send(a)
print(a)
b = a[0:6]+'7|4'+a[9:12]+'1,1|)'
s.send(b)
print(b)

input('请点击下一步来到第五步:')

s.send('(1*ed|7|30d,11,3,15,9,40,0,E,10663.88260,N,2971.82700,0,88,a,2,2,-1,b3|)')

input('经纬度已更新，请点击校验:')
print('后面的自己完成吧!bye!')

s.close()
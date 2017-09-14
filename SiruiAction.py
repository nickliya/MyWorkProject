#!/usr/bin/python
#coding=utf-8
#creat by 15025463191 2017/4/18
import socket
import re
import time
IMEI = input('请输入IMEI号：')

print('测试开始，请根据提示完成后输入1敲回车')
time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('192.168.6.52',2103))

s.send('(1*7c|a3|106,201|101,'+str(IMEI)+'|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
s.send('(1*7c|a3|106,201|101,864244022064553|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
print('device is online')
time.sleep(1)
s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')

kzl = 0
while kzl!= 2:
data = ''
input('请点击你要测试的功能:')
time.sleep(2)
data = s.recv(1024)
r = r'\(\*..\|7\|\d\d\w,\w*?,1\|\)'
datainfo = re.findall(r,data)
str_data = str(datainfo[0])
print('recv:'+str_data)
a = str_data[0]+'1'+str_data[1:5]+'8'+str_data[6:]
s.send(a)
print('send:'+a)
b = a[0:6]+'7|4'+a[9:12]+'1,1|)'
s.send(b)
print(b)

    kzl = input('继续测试功能输入1，结束测试待机输入2:')
    if not kzl:
        break
else:print('待机保持')


###########待机控制############
import threading
dj_wait = 0
a = '1'
def dj():
    global dj_wait
    while dj_wait != 2:
        s.send('()')
        time.sleep(2)
        dj_wait = int(a)
    else:print('byebye!')

def xc():
    global a
    a = raw_input('number 2 for quit:')
    time.sleep(3)

threads = []
t1 = threading.Thread(target=dj)
threads.append(t1)
t2 = threading.Thread(target=xc)
threads.append(t2)

for t in threads:
    t.setDaemon(True)
    t.start()

t.join()

s.close()
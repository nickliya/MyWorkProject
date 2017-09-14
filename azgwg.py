#!/usr/bin/python
#coding=utf-8
#creat by 15025463191
import socket
import time
import datetime
import sys
IMEI = input('请输入IMEI号：')

print('测试开始，请根据提示完成后输入1敲回车')
time.sleep(1)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((sys.argv[1],int(sys.argv[2])))
s.connect(('192.168.6.154',2107))


s.send('+RESP:GTGEO,110204,'+str(IMEI)+',GL500,3,1,0,25.1,100,2,0.1,0,5.7,121.390839,31.164621,20170412032650,0460,0000,1877,0873,,,,20161116080000,00A7$')

input('请刷新手机，填写车辆信息来到第一步:')

now_stamp = time.time()
local_time = datetime.datetime.fromtimestamp(now_stamp)
def local2utc(local_st):
    #本地时间转UTC时间（-8:00）
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st
# 本地转utc
utc_tran = local2utc(local_time)
nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
sbsj = int(nowtime)-500  #上报时间
print(sbsj)
s.send('+RESP:GTGEO,110204,'+str(IMEI)+',GL500,3,1,0,25.1,100,2,0.1,0,5.7,121.390839,31.164621,'+str(sbsj)+',0460,0000,1877,0873,,,,20161116080000,00A7$')
s.send('+RESP:GTCSQ,020102,'+str(IMEI)+',,8,0,20100214093254,11F0$')
s.send('+RESP:GTALL,110204,'+str(IMEI)+',GL500,BSI,cmnet,,,,,,,SRI,3,,1,192.168.8.154,8080,192.0.0.0,0,18019992863,5,1,0,,,,GBC,+8618883286632,GL500,000F,5,2,10111110111110,1508,24,3,1,7,20,1,3,0,3,+20+20,2,,,TMA,+0800,0,,,,,NMD,F,2,4,10,5,,,,WLT,2,1805169615,18019992863,18356001361,18883286632,,,,,,,,,,,GEO,0,2,117.200895,31.833078,50,5,,,,,,,,,1,1,117.200895,31.833078,50,5,,,,,,,,,2,1,117.200895,31.833078,50,5,,,,,,,,,3,1,117.200895,31.833078,50,5,,,,,,,,,4,1,117.200895,31.833078,50,5,,,,,,,,,PIN,1,1234,,,,,,20000101000105,47A1$')
input('上报时间，GSM信号，设备位置已更新，请刷新:')

print('后面的自己完成吧!bye!')
s.close()
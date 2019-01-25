# coding=utf-8

from socket import *
import socket
import time
import datetime


def BSJhextime():
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)

    def local2utc(local_st):
        time_struct = time.mktime(local_st.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st

    data = local2utc(local_time).strftime("%Y %m %d %H %M %S")
    str1 = ''
    str2 = ''
    data = data[2:]
    while data:
        str1 = data[0:2]
        if len(hex(int(str1))[2:4]) == 1:
            head = "0" + hex(int(str1))[2:4]
        else:
            head = hex(int(str1))[2:4]
        str2 += head + " "
        data = data[3:]
    return str2


def sendgps(imei):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('xx.xx.x.xx', 2103))

        loginmsg = "(1*7c|a3|106,201|101," + imei + "|102,460079241205511|104,otu.ost,05010000|105,a1,18|622,a1c2|)"

        s.send(loginmsg.encode())
        s.recv(2048)

        gps = '(1*7f|7|331,' + BSJhextime().replace(" ", "") + ',1,e,12124.24386,n,3110.28946,3,4a,7,1111,2220000,22000,000000,000,20,4,77a38,,11c,597,0,0,,,,|)'
        s.send(gps.encode())
        s.recv(2048)

        s.shutdown(2)
        s.close()

        return True
    except Exception as msg:
        return False



print(gps)

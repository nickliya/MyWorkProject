#!/usr/bin/env python
# coding=utf-8
# author:401219180

import socket
import threading
import time
import re
import datetime
from concurrent.futures import ThreadPoolExecutor

stopsingle = None


def logprint(threadname, msg):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    nowtime = local_time.strftime("%H:%M:%S.%f")

    print(threadname, nowtime, msg)


def sendmsgfun(s, waitime, a):
    time.sleep(waitime / 1000)
    s.send(a.encode())
    logprint(threading.current_thread().name, 'send:' + a)
    b = a[0:6] + '8|5' + a[9:12] + '|)'
    s.send(b.encode())
    logprint(threading.current_thread().name, 'send:' + b)


def runSocket(executor, imei, waitime):
    logprint(threading.current_thread().name, "启动")

    # 创建socket连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("cqfuzik.ticp.net", 2103))
    except Exception as msg:
        time.sleep(1)
        errorinfo = Exception, ":", msg
        print(errorinfo)
        return False

    # 登录
    loginMsg = '(1*7c|a3|106,201|101,' + imei + '|102,460079241205511|104,otu.ost,01022300|105,a1,18|622,a1c2|)'
    s.send(loginMsg.encode())

    global stopsingle
    stopsingle = 0

    # 控制循环
    while 1:
        tcpreceive = s.recv(1024).decode()
        xinfo = re.findall(r'\|(\w\w\w),', tcpreceive)  # 检测是否为控制协议
        if "511" in xinfo or "512" in xinfo or "513" in xinfo or '514' in xinfo or '515' in xinfo or '516' in xinfo \
                or '517' in xinfo or '518' in xinfo or '519' in xinfo or '51A' in xinfo or '51B' in xinfo \
                or '51C' in xinfo:
            protocol_dic = {
                "511": "上锁", "512": "解锁", "513": "寻车", "514": "静音", "515": "点火",
                "516": "熄火", "517": "关门窗", "518": "开门窗", "519": "关天窗", "51A": "开天窗",
                "51B": "通油", "51C": "断油",
            }
            r = r'\(\*..\|7\|\d\d\w,\w*?,\w*?\|\)'
            datainfo = re.findall(r, tcpreceive)
            str_data = str(datainfo[0])
            print(threading.current_thread().name, 'recv:' + protocol_dic[str_data[7:10]] + str_data)
            a = str_data[0] + '1' + str_data[1:7] + '4' + str_data[8:11] + '1,1|)'
            executor.submit(sendmsgfun, s, waitime, a)
        elif tcpreceive == "":
            stopsingle = 1
            s.shutdown(2)
            s.close()
        else:
            pass
        if stopsingle == 1:
            break


if __name__ == '__main__':
    start_time = time.time()
    executor = ThreadPoolExecutor(50)
    print('这是主线程：', threading.current_thread().name)
    thread_list = []

    file1=open("C:\\Users\\fuzhi\\Desktop\\plateNum.txt","r")
    data = file1.readlines()
    for datainfo in data:
        datalist = datainfo.split(",")
        imei = datalist[1]

        t = threading.Thread(target=runSocket, args=(executor, imei, 0), name="[线程"+imei+"]")
        thread_list.append(t)

    for t in thread_list:
        t.setDaemon(True)
        t.start()

    for t in thread_list:
        t.join()

    print('主线程结束', threading.current_thread().name)
    print('一共用时', time.time() - start_time)

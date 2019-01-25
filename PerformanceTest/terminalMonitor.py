#!/usr/bin/env python
# coding=utf-8
# author:401219180

import socket
import threading
import time
import re
import datetime
import logging
from concurrent.futures import ThreadPoolExecutor

stopsingle = None
socketlist = []


def myloger(logname):
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    formater = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    fhandler = logging.FileHandler(logname, "w")
    fhandler.setLevel(logging.DEBUG)
    fhandler.setFormatter(formater)

    shandler = logging.StreamHandler()
    shandler.setLevel(logging.DEBUG)
    shandler.setFormatter(formater)

    logger.addHandler(fhandler)
    logger.addHandler(shandler)
    return logger


def logprint(threadname, imei, msg):
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    nowtime = local_time.strftime("%H:%M:%S.%f")

    print threadname, nowtime, imei, msg


def sendmsgfun(s, waitime, a, imei):
    global sendloger
    if waitime == 9999:
        return False
    time.sleep(float(waitime) / float(1000))
    s.send(a.encode())
    sendloger.debug((threading.current_thread().name, imei, 'send:' + a,))
    b = a[0:6] + '8|5' + a[9:12] + '|)'
    s.send(b.encode())
    sendloger.debug(threading.current_thread().name + " " + imei + ' send:' + b + " 已等待" + str(float(waitime) / float(1000)) + "秒")


def runSocket(executor, imei, waitime):
    global recvloger, sendloger, socketlist
    logprint(threading.current_thread().name, imei, "启动")

    # 创建socket连接
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketlist.append(s)
    try:
        s.connect(("192.168.6.204", 2103))  # 凹凸预发布
        # s.connect(("192.168.6.211", 2103))  # 联动云
    except Exception as msg:
        time.sleep(1)
        errorinfo = Exception, ":", msg
        print(errorinfo)
        return False

    # 登录
    loginMsg = '(1*7c|a3|106,201|101,' + imei + '|102,460079241205511|104,otu.ost,01022300|105,a1,18|622,a1c2|)'
    s.send(loginMsg.encode())
    time.sleep(0.5)
    quanxian = '(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100,000,000,000|)'
    s.send(quanxian.encode())

    global stopsingle
    stopsingle = 0

    returnmsg = 0
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
            # print(threading.current_thread().name, 'recv:' + protocol_dic[str_data[7:10]] + str_data)
            recvloger.debug('recv:' + protocol_dic[str_data[7:10]] + str_data)
            # a = str_data[0] + '1' + str_data[1:7] + '4' + str_data[8:11] + '1,1|)'

            a = str_data[0] + '1' + str_data[1:7] + '4' + str_data[8:11] + hex(returnmsg)[2:] + ',1|)'
            returnmsg += 1

            if waitime != 0:
                executor.submit(sendmsgfun, s, waitime, a, imei)
            else:
                s.send(a)
                sendloger.debug((threading.current_thread().name, imei, 'send:' + a))
                b = a[0:6] + '8|5' + a[9:12] + '|)'
                s.send(b)
                sendloger.debug((threading.current_thread().name, imei, 'send:' + b))
        elif tcpreceive == "":
            stopsingle = 1
            s.shutdown(2)
            s.close()
            recvloger.info("远程中断了连接")
        else:
            pass
        if stopsingle == 1:
            break


if __name__ == '__main__':
    start_time = time.time()
    sendloger = myloger("send.log")
    recvloger = myloger("recv.log")
    threadPoolMain = ThreadPoolExecutor(3000)  # 创建主线程池
    threadPoolWait = ThreadPoolExecutor(3000)  # 创建异步等待的线程池
    print '这是主线程：', threading.current_thread().name
    thread_list = []

    # file1 = open("C:\\Users\\fuzhi\\Desktop\\aotuTerminal.txt", "r")
    # data = file1.readlines()
    # for i in range(1000):
    #     datainfo = data[i]
    #     datalist = datainfo.split(",")
    #     imei = datalist[1]
    #     t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 0)
    #     if i < 200:
    #         t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 1000)
    #     elif i < 400:
    #         t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 1500)
    #     elif i < 600:
    #         t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 2000)
    #     elif i < 800:
    #         t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 2500)
    #     elif i < 1000:
    #         t = threadPoolMain.submit(runSocket, threadPoolWait, imei, 9999)
    #     else:
    #         print "ok"
    #         pass

    t = threadPoolMain.submit(runSocket, threadPoolWait, "868729039450676", 0)

    time.sleep(3)
    inputstr = None
    while inputstr != "quit":
        inputstr = raw_input()

    for s in socketlist:
        s.shutdown(2)
        s.close()
    print("已结束所有线程")

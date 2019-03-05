# coding=utf-8
# create by 401219180 2018/02/10

from Resource.pubfun import *

from PyQt5 import QtCore
from PyQt5.QtCore import *
import binascii
import re
import struct
import xlrd


class WorkerSignals(QObject):
    """工作信号"""
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)
    animate_signal = QtCore.pyqtSignal(str)


class TcpThread(QtCore.QThread):
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)
    animate_signal = QtCore.pyqtSignal(str)
    wait_signal = QtCore.pyqtSignal(tuple)

    def __init__(self, socketcp, onBtn, heartcheck, senBtn, bindBtn, wg315Btn, entrywait):
        super().__init__()
        self.s = socketcp
        self.yqtool = Bianlifunction()
        self.onBtn = onBtn
        self.heartcheck = heartcheck
        self.sendBtn = senBtn
        self.bindBtn = bindBtn
        self.wg315Btn = wg315Btn
        self.entrywait = entrywait

    def run(self):
        """线程"""
        global stopsingle
        stopsingle = 0
        while 1:
            tcpreceive = self.s.recv(1024).decode()
            xinfo = re.findall(r'\|(\w\w\w),', tcpreceive)  # 检测是否为控制协议

            # 适配控制协议,如果存在下列编号则自动回复
            if "511" in xinfo or "512" in xinfo or "513" in xinfo or '514' in xinfo or '515' in xinfo or '516' in xinfo \
                    or '517' in xinfo or '518' in xinfo or '519' in xinfo or '51a' in xinfo or '51b' in xinfo \
                    or '51c' in xinfo or '51e' in xinfo or '51f' in xinfo:
                self.recv_signal.emit(tcpreceive)
                protocol_dic = {
                    "511": "上锁", "512": "解锁", "513": "寻车", "514": "静音", "515": "点火",
                    "516": "熄火", "517": "关门窗", "518": "开门窗", "519": "关天窗", "51a": "开天窗",
                    "51b": "通油", "51c": "断油", "51e": "授权", "51f": "夺权",
                }
                r = r'\(\*..\|7\|\d\d\w,\w*?,\w*?\|\)'
                datainfo = re.findall(r, tcpreceive)
                str_data = str(datainfo[0])
                print('recv:' + protocol_dic[str_data[7:10]] + str_data)
                a = str_data[0] + '1' + str_data[1:7] + '4' + str_data[8:11] + '2,1|)'
                waitime = self.entrywait.text()
                if waitime == "0":
                    self.s.send(a.encode())
                    self.send_signal.emit(a)

                    b = a[0:6] + '8|5' + a[9:12] + '|)'
                    self.s.send(b.encode())
                    self.send_signal.emit(b)
                else:
                    self.wait_signal.emit((self.s, a, waitime))
            # 适配蓝牙设置协议,如果存在下面编码则自动回复
            elif "281" in xinfo or "282" in xinfo or "26d" in xinfo:
                self.recv_signal.emit(tcpreceive)
                str_data2 = tcpreceive[:5] + "4" + tcpreceive[6:]
                str_data = str_data2[:1] + "1" + str_data2[1:]
                print('recv:' + str_data)
                self.s.send(str_data.encode())
                self.send_signal.emit(str_data)
            # 适配设备配置，如果存在下面编码则自动回复
            elif "217" in xinfo or "20a" in xinfo or "26a" in xinfo or "26b" in xinfo:
                self.recv_signal.emit(tcpreceive)
                str_data = tcpreceive
                # print('recv:' + protocol_dic[str_data[7:10]] + str_data)
                a = str_data[0] + '1' + str_data[1:5] + "4" + str_data[6:11] + '1,1|)'
                self.s.send(a.encode())
                self.send_signal.emit(a)
            elif "26e" in xinfo or "230" in xinfo:
                self.recv_signal.emit(tcpreceive)
                str_data = tcpreceive
                # print('recv:' + protocol_dic[str_data[7:10]] + str_data)
                a = str_data[0] + '1' + str_data[1:5] + "4" + str_data[6:]
                self.s.send(a.encode())
                self.send_signal.emit(a)
            # 如果回复消息未空,则判定为断线离线
            elif tcpreceive == "":
                stopsingle = 1
                self.s.shutdown(2)
                self.s.close()
                self.onBtn.setText("连接")
                self.animate_signal.emit("1")
                self.heartcheck.setChecked(False)
                self.heartcheck.setVisible(False)
                self.sendBtn.setDisabled(True)
                self.bindBtn.setDisabled(True)
                self.wg315Btn.setDisabled(True)
            else:
                self.recv_signal.emit(tcpreceive)
            if stopsingle == 1:
                break


class BSJTcpThread(QtCore.QThread):
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)
    animate_signal = QtCore.pyqtSignal(str)

    def __init__(self, socketcp, onBtn, heartcheck, senBtn):
        super().__init__()
        self.s = socketcp
        self.yqtool = Bianlifunction()
        self.onBtn = onBtn
        self.heartcheck = heartcheck
        self.sendBtn = senBtn

    def run(self):
        """线程"""
        global stopsingle
        stopsingle = 0
        while 1:
            btcpreceive = self.s.recv(1024)
            tcpreceive1 = str(binascii.b2a_hex(btcpreceive), encoding="utf-8")

            tcpreceive = ""
            i = 0
            while i < len(tcpreceive1) - 1:  # 十六进制数据处理,两个字节隔开
                if i == len(tcpreceive1) - 2:
                    tcpreceive += tcpreceive1[i:i + 2]
                    i += 2
                else:
                    tcpreceive += tcpreceive1[i:i + 2] + " "
                    i += 2

            if "52 45 4c 41 59 2c 31 23" in tcpreceive:
                print("收到断油指令")
                self.recv_signal.emit(tcpreceive)
            elif "52 45 4c 41 59 2c 30 23" in tcpreceive:
                print("收到通油指令")
                self.recv_signal.emit(tcpreceive)
            elif tcpreceive == "":
                stopsingle = 1
                self.s.shutdown(2)
                self.s.close()
                self.onBtn.setText("连接")
                self.animate_signal.emit("1")
                self.heartcheck.setChecked(False)
                self.heartcheck.setVisible(False)
                self.sendBtn.setDisabled(True)
            else:
                self.recv_signal.emit(tcpreceive)
            if stopsingle == 1:
                break


class WaiteandsendThread(QtCore.QRunnable):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.signals = WorkerSignals()

    def run(self):
        """线程"""
        try:
            print("等待" + self.message[2] + "毫秒发送")
            time.sleep(int(self.message[2]) / 1000)
            # self.sleep(int(self.message[2]) / 1000)
            print("已等待" + self.message[2] + "毫秒，开始发送")
            a = self.message[1]
            b = a[0:6] + '8|5' + a[9:12] + '|)'
            s = self.message[0]

            s.send(a.encode())
            # self.send_signal.emit(a)
            self.signals.recv_signal.emit(a)
            s.send(b.encode())
            self.signals.send_signal.emit(b)

        except Exception as msg:
            errorinfo = Exception, ":", msg
            print(errorinfo)


class GpsUploadThread(QtCore.QRunnable):
    def __init__(self, data, tcp):
        super().__init__()
        self.message = data
        self.s = tcp
        self.signals = WorkerSignals()
        self.yqtool = Bianlifunction()

    def hextosjc(self, datetime):
        """十六进制时间转时间戳"""

        # dt = "2016-05-05 20:28:54"
        dt = "20" + str(int(datetime[0:2], 16)).zfill(2) + "-" + str(int(datetime[2:4], 16)).zfill(2) + "-" + str(
            int(datetime[4:6], 16)).zfill(2) + " " + str(int(
            datetime[6:8], 16)).zfill(2) + ":" + str(int(datetime[8:10], 16)).zfill(2) + ":" + str(
            int(datetime[10:12], 16)).zfill(2)

        # 转换成时间数组
        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return timestamp

    def run(self):
        """线程"""
        try:
            # waitetime = self.message[0].split(",")[1]
            waitetime = self.message[0].split(",")[1]
            for i in self.message:
                datalist = i.split(",")
                # sleeptime = float(int(datalist[1]) - int(waitetime)) / 1000
                sleeptime = float(self.hextosjc(datalist[1]) - self.hextosjc(waitetime))
                time.sleep(sleeptime)
                time331 = self.yqtool.BSJhextime().replace(" ", "")
                # a = "(1*e4|7|331," + time331 + ",1,E," + str(float(datalist[3]) * 100) + ",N," + str(
                #     float(datalist[2]) * 100) + ",0,0,9,2200,2222222,22222,222222,222,22,1,7454,0,212,505,1,1,1,0,0|)"
                i = i[:-1]
                a = "(1" + i[:10] + time331 + i[22:] + ")"
                self.s.send(a.encode())
                self.signals.send_signal.emit(a)
                # time.sleep(5)
                waitetime = datalist[1]

        except Exception as msg:
            errorinfo = Exception, ":", msg
            print(errorinfo)


class DataThread(QtCore.QRunnable):
    """数据上传进程"""
    def __init__(self, dataUrl, tcp, gpsUploadBtn):
        super().__init__()
        self.dataUrl = dataUrl
        self.s = tcp
        self.signals = WorkerSignals()
        self.yqtool = Bianlifunction()
        self.oldtTimeStamp = 0
        self.gpsUploadBtn = gpsUploadBtn

    def decode30d(self, data):
        r = r'\|30d,(.*?),E,'
        msg = re.findall(r, data)
        msg = data.replace(msg[0], self.yqtool.hextime())
        return msg

    def decode331(self, data):
        r = r'\|331,(.*?),\d,.,'
        msg = re.findall(r, data)
        if msg[0] == "":
            print('decode331 failed')
        elif 'FFFFF' in msg[0]:
            return data
        else:
            pass
        time331 = self.yqtool.BSJhextime().replace(" ", "")
        msg = data.replace(msg[0], time331)
        return msg

    def run(self):
        """线程"""
        try:
            self.gpsUploadBtn.setDisabled(True)
            readbook = xlrd.open_workbook(self.dataUrl)
            sheet = readbook.sheet_by_index(0)
            row = 0
            rowcount = sheet.nrows
            print('共有' + str(rowcount) + '行数据')
            for i in range(rowcount):
                rowinfo = sheet.row_values(row)
                sendMsg = rowinfo[1]
                if sendMsg == 'null' or sendMsg == '':
                    row += 1
                    continue
                else:
                    sendMsg = "(1" + sendMsg + ")"
                timeStamp = rowinfo[0]
                timeStamp = int(timeStamp)
                if len(str(timeStamp)) > 10:
                    timeStamp = str(timeStamp)[:-3]

                if self.oldtTimeStamp == 0:
                    waiteTime = 0
                else:
                    waiteTime = int(timeStamp) - self.oldtTimeStamp

                time.sleep(waiteTime)
                if "|30d" in sendMsg:
                    sendMsg = self.decode30d(sendMsg)
                elif "|331" in sendMsg:
                    sendMsg = self.decode331(sendMsg)
                else:
                    pass

                self.s.send(sendMsg.encode())
                self.signals.send_signal.emit(sendMsg)
                print('发送第' + str(row+1) + '行数据')
                self.oldtTimeStamp = int(timeStamp)
                row += 1
        except Exception as msg:
            errorinfo = Exception, ":", msg
            print(errorinfo)
            print("遇到错误发送终止")
            self.gpsUploadBtn.setDisabled(False)
            return False

        print('全部数据发送完成')
        self.gpsUploadBtn.setDisabled(False)


class DataThreadBSJ(QtCore.QRunnable):
    """数据上传进程"""

    def __init__(self, dataUrl, tcp, gpsUploadBtn):
        super().__init__()
        self.dataUrl = dataUrl
        self.s = tcp
        self.signals = WorkerSignals()
        self.yqtool = Bianlifunction()
        self.oldtTimeStamp = 0
        self.gpsUploadBtn = gpsUploadBtn

    def dataSwitch(self, data):
        str1 = ''
        str2 = b''
        while data:
            str1 = data[0:2]
            s = int(str1, 16)
            str2 += struct.pack('B', s)
            data = data[3:]
        return str2

    def run(self):
        """线程"""
        try:
            self.gpsUploadBtn.setDisabled(True)
            readbook = xlrd.open_workbook(self.dataUrl)
            sheet = readbook.sheet_by_index(0)
            row = 0
            rowcount = sheet.nrows
            print('共有' + str(rowcount) + '行数据')
            for i in range(rowcount):
                rowinfo = sheet.row_values(row)
                sendMsg = rowinfo[1]
                if sendMsg == 'null' or sendMsg == '':
                    row += 1
                    continue

                timeStamp = rowinfo[0]
                timeStamp = int(timeStamp)
                if len(str(timeStamp)) > 10:
                    timeStamp = str(timeStamp)[:-3]

                if self.oldtTimeStamp == 0:
                    waiteTime = 0
                else:
                    waiteTime = int(timeStamp) - self.oldtTimeStamp

                time.sleep(waiteTime)

                self.s.send(self.dataSwitch(sendMsg))
                self.signals.send_signal.emit(sendMsg)
                print('发送第' + str(row + 1) + '行数据')
                self.oldtTimeStamp = int(timeStamp)
                row += 1
        except Exception as msg:
            errorinfo = Exception, ":", msg
            print(errorinfo)
            print("遇到错误发送终止")
            self.gpsUploadBtn.setDisabled(False)
            return False

        print('全部数据发送完成')
        self.gpsUploadBtn.setDisabled(False)
# coding=utf-8
# create by 401219180 2018/02/10

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from socket import *
import socket
import re
import qrcode
import base64
import pymssql
import os
import time
import datetime
import cgitb
import sys
import struct
import binascii
import configparser

cgitb.enable(format='text')  # 解决pyqt5异常只要进入事件循环,程序就崩溃,而没有任何提示

isexisted = os.path.exists('D:\Tcptemp')
if not isexisted:
    os.makedirs('D:\Tcptemp')
else:
    pass

stopsingle = None
waitmsg = None


class Bianlifunction:
    """个人便利方法集合"""

    @staticmethod
    def timeNow():
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        return local_time.strftime("%H:%M:%S.%f")

    @staticmethod
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

    @staticmethod
    def hextime():
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)

        def local2utc(local_st):
            time_struct = time.mktime(local_st.timetuple())
            utc_st = datetime.datetime.utcfromtimestamp(time_struct)
            return utc_st

        utc_tran = local2utc(local_time)
        # nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
        year = utc_tran.strftime('%Y')
        month = utc_tran.strftime('%m')
        day = utc_tran.strftime('%d')
        hour = utc_tran.strftime('%H')
        minute = utc_tran.strftime('%M')
        newminute = int(minute) - 3
        second = utc_tran.strftime('%S')

        if newminute < 0:
            newminute = newminute + 60
            hour = int(hour) - 1
            if hour < 0:
                hour = hour + 24
                day = int(day) - 1
        else:
            pass

        Y = '%x' % int(year[-2:])
        m = '%x' % int(month)
        d = '%x' % int(day)
        H = '%x' % int(hour)
        M = '%x' % newminute
        Sec = '%x' % int(second)
        strhextime = str(Y) + ',' + str(m) + ',' + str(d) + ',' + str(H) + ',' + str(M) + ',' + str(Sec)
        return strhextime


class CRCUtil:
    """思锐CRC解密算法"""

    def __init__(self):
        self.cycleCodes = ['G', 'H', 'I', 'J', '&', '<', '2', '8', 'd', '#', 'N', 'i', 'X', 's', '=', '5', 'R', '0',
                           '$', 'e', '4', 'Q', '%', '[', 'j', 'p', ']', 'c', '1', '3', '7', '9', 'A', '6', 'n', 'z',
                           'B', ';', 'h', 'r', ':', 'a', '_', 'O', '{', 'D', 'E', 'm', 'W', 'Y', 'k', '}', 'x', 'Z',
                           'P', 'u', ',', 'F', 'M', 'g', 'C', 'K', 'f', 't', '+', '>', 'L', 'S', 'T', 'U', 'V', 'q',
                           '|', 'w', 'l', 'y', 'b', 'o', 'v', '.']
        self.cycleIndex = []
        self.OTUMsgEncryptor()

    def OTUMsgEncryptor(self):
        for i in range(128):
            self.cycleIndex.append(-1)
        index = 0
        for i in range(len(self.cycleCodes)):
            self.cycleIndex[ord(self.cycleCodes[index])] = index
            index += 1

    def asiccCrcDecode(self, context, offset):
        index = 0
        plaintext = ""
        for i in range(len(context)):
            value = ord(context[index])
            if self.cycleIndex[value] >= 0:
                nextIndex = (self.cycleIndex[value] - index - offset) % len(self.cycleCodes)
                nextIndex = (len(self.cycleCodes) + nextIndex) % len(self.cycleCodes)
                plaintext += self.cycleCodes[nextIndex]
            index += 1
        print(plaintext)
        return plaintext


class Sqlfunticon:
    """sql方法"""

    @staticmethod
    def getinfo(sql):
        """sqlserver"""
        conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
        cur = conn.cursor()
        cur.execute(sql)
        info = cur.fetchall()
        cur.close()
        conn.close()
        return info


class TcpBackgroudView(QGraphicsView):
    """自定义界面2d
    当前未采用"""

    def __init__(self):
        super().__init__()
        self._set_color(QColor(105, 105, 105))
        self.iniAnimation()

    def _set_color(self, col):
        self.palette = QPalette()
        self.palette.setColor(self.backgroundRole(), col)
        # self.palette.setBrush(self.backgroundRole(), col)
        self.setPalette(self.palette)

    color = pyqtProperty(QColor, fset=_set_color)


class TcpBackgroudScene(QGraphicsScene):
    """自定义场景"""

    def __init__(self, widget):
        super(TcpBackgroudScene, self).__init__(widget)
        self.setBackgroundBrush(QColor(105, 105, 105))

        self.onlineAnimation()
        self.offlineAnimation()

    def _set_color(self, col):
        self.setBackgroundBrush(col)

    def onlineAnimation(self):
        """上线动画"""
        self.onlineCol = QPropertyAnimation(self, b'color')
        self.onlineCol.setDuration(1000)
        self.onlineCol.setStartValue(QColor(105, 105, 105))
        # self.onlineCol.setKeyValueAt(0.1, QColor(255, 255, 240))
        self.onlineCol.setEndValue(QColor(47, 79, 79))

    def offlineAnimation(self):
        """离线动画"""
        self.offlineCol = QPropertyAnimation(self, b'color')
        self.offlineCol.setDuration(1000)
        self.offlineCol.setStartValue(QColor(47, 79, 79))
        # self.offlineCol.setKeyValueAt(0.1, QColor(255, 255, 240))
        self.offlineCol.setEndValue(QColor(105, 105, 105))

    def threadAnimate(self, message):
        """多线程离线动画信号"""
        if message == "1":
            self.offlineCol.start()

    color = pyqtProperty(QColor, fset=_set_color)


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()
        self.iniGrid()
        self.initmenu()
        self.inittoolBar()
        self.deleteWigt = []
        self.yqtool = Bianlifunction()

    def showEvent(self, *args, **kwargs):
        # isexisted = os.path.exists('D:\Tcptemp')
        # if not isexisted:
        #     os.makedirs('D:\Tcptemp')
        # else:
        #     pass
        # data = open('D:\Tcptemp\mainData.txt', "a+")
        # historyinfo = data.read()  # 读取缓存文件data
        # historyinfolist = historyinfo.split(",")
        pass

    def closeEvent(self, *args, **kwargs):
        pass  # userinfo = self.entryUser.text()  # passwdinfo = self.entryPasswd.text()  # urlinfo = self.entryUrl.text()  # csuserinfo = self.entryCustomerUser.text()  # cspasswdinfo = self.entryCustomerPasswd.text()  # tcpinfo = self.entryTcp.text()  # databaseinfo = self.entryDatabases.text()  # historydata = open('D:\Tcptemp\mainData.txt', "w")  # 生成缓存文件data  # historydata.write(userinfo + "," + passwdinfo + "," + urlinfo + "," + csuserinfo +  #                   "," + cspasswdinfo + "," + tcpinfo + "," + databaseinfo)  # IMEI保存到缓存文件data  # historydata.close()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def inittoolBar(self):
        toolbarAction = QAction(u'思锐OTU', self)
        toolbarAction.setStatusTip(u'老思锐平台项目')
        toolbarAction.triggered.connect(self.otuSplice)

        toolbarAction2 = QAction(u'金融BSJ', self)
        toolbarAction2.setStatusTip(u'新金融项目BSJ设备模拟')
        toolbarAction2.triggered.connect(self.bsjSplice)

        toolbar = self.addToolBar("toolbar")
        toolbar.addAction(toolbarAction)
        toolbar.addAction(toolbarAction2)

    def initmenu(self):
        menuAction = QAction(QtGui.QIcon(u'思锐.png'), u'思锐', self)
        menuAction.setStatusTip('Exit application')
        # menuAction.triggered.connect(qApp.quit)

        menuAction2 = QAction(QtGui.QIcon(u'咪智汇.png'), u'咪智汇', self)
        menuAction2.setStatusTip('Exit application')
        # menuAction2.triggered.connect(qApp.quit)

        menuAction3 = QAction(QtGui.QIcon(u'皮皮车.png'), u'皮皮车', self)
        menuAction3.setStatusTip('Exit application')
        # menuAction3.triggered.connect(qApp.quit)

        menuAction4 = QAction(QtGui.QIcon(u'共享车快进.png'), u'共享车快进', self)
        menuAction4.setStatusTip('Exit application')
        # menuAction4.triggered.connect(qApp.quit)

        menuAction5 = QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        menuAction5.setShortcut(u'Ctrl+Q')
        menuAction5.setStatusTip('Exit application')
        menuAction5.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(menuAction)
        fileMenu.addAction(menuAction2)
        fileMenu.addAction(menuAction3)
        fileMenu.addAction(menuAction4)
        fileMenu.addAction(menuAction5)

    def initUI(self):
        self.resize(1300, 680)
        self.center()
        self.setWindowTitle(u'桴之科测试工具 Version:2018.11.26')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.statusBar()
        self.setWindowIcon(QtGui.QIcon('ui/icon.ico'))
        # self.setWindowOpacity(0.9)

    def iniGrid(self):
        # 主窗体
        self.mainwidget = QGraphicsView()
        self.scene = TcpBackgroudScene(self.mainwidget)  # 创建场景
        self.mainwidget.setScene(self.scene)  # 添加场景

        self.mainwidget.setFont(QtGui.QFont("75 10pt Microsoft YaHei"))
        self.maingrid = QGridLayout()
        self.mainwidget.setLayout(self.maingrid)
        # self.mainwidget.setObjectName("mainwidget")
        self.setCentralWidget(self.mainwidget)
        self.maingrid.setRowStretch(0, 0)


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
                    "51b": "通油", "51c": "断油", "51e": "通油", "51f": "断油",
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

            if tcpreceive == "":
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


class OtuMonitor(MainWidget):
    def __init__(self):
        super(OtuMonitor, self).__init__()
        self.sqlserver = Sqlfunticon()
        self.num = 0
        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(500)

    def otuSplice(self):
        for i in self.deleteWigt:
            i.deleteLater()
        self.OtuMonitor_UI()
        self.OtuMonitor_grid()
        try:
            self.s.shutdown(2)
            global stopsingle
            stopsingle = 1
            self.scene.offlineCol.start()
        except AttributeError:
            pass
        self.deleteWigt = [self.leftwidget, self.middlewiget]

    def OtuMonitor_UI(self):
        # styleqss = open("otu.qss", "r", encoding='UTF-8')
        # styleinfo = styleqss.read()
        styleinfo = 'QLabel{font:75 10pt "Microsoft YaHei";color:floralwhite;}QPushButton{font:75 10pt "Microsoft YaHei";background-color:#FFFFFF;border:1px solid #8f8f91;border-radius:9px;min-width:50px;min-height:24px}QPushButton::hover{background-color:#FF6A6A;}QRadioButton{font:75 10pt "Microsoft YaHei";color:floralwhite;}QRadioButton::indicator{width:10px;height:10px;border-radius:5px;}QRadioButton::indicator:checked{background-color:#FFA07A;border:1px solid black;}QRadioButton::indicator:unchecked{background-color:white;border:1px solid black;}QCheckBox{font:75 10pt "Microsoft YaHei";color:floralwhite;background-color:rgba(255,255,255,0);}QTextEdit{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}QTextBrowser{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}'
        self.mainwidget.setStyleSheet(styleinfo)
        # styleqss.close()

        """左侧窗口"""
        self.labelPort = QLabel("端口", self)
        self.labelPort.setMaximumWidth(50)
        self.labelIP = QLabel("IP", self)
        self.labelIP.setMaximumWidth(20)
        self.labelHardver = QLabel("硬件版本", self)

        self.labelOtuIMEI = QLabel(u"主机IMEI", self)
        self.labelwait = QLabel(u"等待时间", self)
        # self.waitimer = QTimer()
        # global waitmsg
        # self.waitimer.timeout.connect(lambda: self.waitimerfun(waitmsg))
        self.labelBTIMEI = QLabel("蓝牙IMEI", self)
        self.labelInput = QLabel("自定义输入界面", self)
        self.labelSendHistory = QLabel("发送历史", self)
        self.labelRecive = QLabel("接收历史", self)

        self.entryPort = QLineEdit()
        self.entryPort.setMaximumWidth(50)
        self.entryIP = QLineEdit()
        self.entryOtuIMEI = QLineEdit()
        self.entrywait = QLineEdit()
        self.entrywait.setText('0')
        self.entryBTIMEI = QLineEdit()
        self.entryHardver = QLineEdit()
        self.entrywaiguadev = QLineEdit()
        self.entrywaiguadev.setPlaceholderText("产品型号")

        data = open('D:\\Tcptemp\\data.txt', "a+")
        data.seek(0)  # 移动指针到头部
        historyinfo = data.read()  # 读取缓存文件data
        historyinfolist = historyinfo.split(",")
        data.close()

        try:
            self.entryOtuIMEI.insert(historyinfolist[0])
            self.entryPort.insert(historyinfolist[2])
            self.entryIP.insert(historyinfolist[1])
            self.entryHardver.insert(historyinfolist[3])
        except IndexError as msg:
            print(msg)

        # if len(historyinfolist) == 3:
        #     self.entryPort.insert(historyinfolist[2])
        # if len(historyinfolist) == 2 or len(historyinfolist) == 3:
        #     self.entryIP.insert(historyinfolist[1])

        self.defalBtn = QPushButton(u"默认")
        self.onBtn = QPushButton(u"连接")
        self.bindBtn = QPushButton(u"绑定")
        self.bindBtn.setDisabled(True)
        self.sendBtn = QPushButton(u"发送")
        self.sendBtn.setDisabled(True)
        self.clearBtn = QPushButton(u"清空")
        self.clearBtn2 = QPushButton(u"清空")
        self.clearBtn3 = QPushButton(u"清空")
        self.wg315Btn = QPushButton(u"315")
        self.wg315Btn.setDisabled(True)
        self.loginBtn = QPushButton(u"登录")
        self.searchAddrBtn = QPushButton(u"寻址")

        self.seleOtu = QRadioButton(u"otu")
        self.seleAudi = QRadioButton(u"audi")
        self.seleBuick = QRadioButton(u"buick")
        self.seleOtu.setChecked(True)

        self.heartcheck = QCheckBox("心跳挂机(保持连接请打钩√）")
        self.heartcheck.setVisible(False)

        self.textInput = QTextEdit()
        self.textInput.setAlignment(QtCore.Qt.AlignLeft)
        self.textSend = QTextBrowser()
        # self.textSend.setReadOnly(False) # 设置不可编辑
        self.textRecv = QTextBrowser()

        """中间窗口"""

        # self.btnnamelist = ["能力", "设防", "引擎", "门锁", "速度", "温度", "GSM", "星数"]
        self.protocol = {
            "能力": "(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100|)",
            "引擎": "(1*12|7|302,1)",
            "门锁": "(1*33|7|305,2,2222|)",
            "电压": "(1*88|7|316,1,1,4B0,4F0|)",
            "温度": "(1*33|7|30B,1,E0|)",
            "GSM": "(1*74|7|30f,14,333e,331a,GSM850_EGSM_DCS_PCS_MODE|)",
            "星数": "(1*33|7|30C,1,1,1,D,1|)",
            "设防": "(1*a7|7|308,1,1|)",
            "速度": "(1*88|7|31a,1,1,50|)",
            "车窗": "(1*88|7|317,1,11111|)",
            "车门": "(1*33|7|304,1,11111|)",
            "OBD": "(1*fa|7|30e,1,2,1,3333,1,0,2|)",
            "ON挡": "(1*12|7|301,2)",
            "余油614": "(1*ea|5|614,3,7#b312,1,32,32#|)",
            "余电614": "(1*ea|5|614,3,7#b313,1,32,32#|)",
            "余电31F": "(1*88|7|31F,1,32,0,0|)",
            "余油30A": "(1*88|7|30A,1,22|)",
            "里程614": "(1*ea|5|614,3,7#b311,9C4#|)",
            "里程313": "(1*10|7|313,1,10,1,552.0.0.0f39202a00,|)",
            "里程320": "(1*10|7|320,1,9C4|)",
            "里程614新": "(1*c1|5|614,3,7#b318,9C4#|)",
            "设防333": "(1*c1|7|333,1|)",

        }

        self.Btn1 = QPushButton(u"能力")
        self.Btn1.setStatusTip("100为开，(10c，关锁，开锁，寻车，静音，点火，熄火，关门窗，开门窗，关天窗，开天窗，通油，停车断油，强制断油，最后三个字段未知)")
        self.Btn2 = QPushButton(u"设防")
        self.Btn3 = QPushButton(u"引擎")
        self.Btn3.setStatusTip("1开2关(302，引擎状态)")
        self.Btn4 = QPushButton(u"门锁")
        self.Btn4.setStatusTip("1上锁2开锁(305，门锁状态，左前门，左后门，后前门，右后门)")
        self.Btn5 = QPushButton(u"速度")
        self.Btn5.setStatusTip("1有效2无效(31A，行驶状态，行驶时速有效状态，行驶时速)")
        self.Btn6 = QPushButton(u"温度")
        self.Btn6.setStatusTip("1有效2无效(30B，温度有效状态，具体温度)")
        self.Btn7 = QPushButton(u"GSM")
        self.Btn7.setStatusTip("(30F，信号质量CSQ，基站Loc，基站cell，基站频段)")
        self.Btn8 = QPushButton(u"星数")
        self.Btn8.setStatusTip("(30C，供电状态，定位状态，天线状态，卫星数量，稳定状态)")
        self.Btn9 = QPushButton(u"位置")
        self.Btn9.setStatusTip("1有效2无效(30d，年，月，日，时，分，秒，经，经度，纬，纬度，速度，方向，星数，状态on，状态引擎，时速，GPS坐标)")
        self.Btn10 = QPushButton(u"电压")
        self.Btn10.setStatusTip("1有效2无效(316，电瓶连接状态，主机电压有效状态，平均电压，当前电压，低压状态，漏电状态)")
        self.Btn11 = QPushButton(u"车窗")
        self.Btn11.setStatusTip("1关窗2开窗(317，车窗状态，左前窗，右前窗，左后窗，右后窗，天窗)")
        self.Btn12 = QPushButton(u"车门")
        # self.Btn12.setStatusTip("1上锁2开锁(305，门锁状态，左前门，做后面，后前门，右后门)")
        self.Btn13 = QPushButton(u"OBD")
        self.Btn13.setStatusTip("(30e，诊断连接状态，严重故障状态，严重故障数量，故障码列表，诊断类型1CAN2KIN，诊断类型附加字段，诊断发现其他设备接入冲突)")
        self.Btn14 = QPushButton(u"ON挡")
        self.Btn14.setStatusTip("1开2关")

        self.Btn15 = QPushButton(u"余油614")
        self.Btn16 = QPushButton(u"余电614")
        self.Btn17 = QPushButton(u"余油30A")
        self.Btn18 = QPushButton(u"余电31F")
        self.Btn19 = QPushButton(u"里程614")
        self.Btn20 = QPushButton(u"里程313")
        self.Btn21 = QPushButton(u"里程614新")
        self.Btn22 = QPushButton(u"里程320")
        self.Btn23 = QPushButton(u"单程421")
        self.Btn24 = QPushButton(u"设防333")

        # 331定制box
        self.aotubox = QGroupBox("331协议定制,√为开,门锁相反")
        self.aotuboxGrid = QGridLayout()
        self.aotubox.setLayout(self.aotuboxGrid)
        self.aotucheckbox1 = QCheckBox("ACC")
        self.aotucheckbox2 = QCheckBox("总门边")
        self.aotucheckbox3 = QCheckBox("左前门")
        self.aotucheckbox4 = QCheckBox("右前门")
        self.aotucheckbox5 = QCheckBox("左后门")
        self.aotucheckbox6 = QCheckBox("右后门")
        self.aotucheckbox7 = QCheckBox("后备箱")
        self.aotucheckbox8 = QCheckBox("前盖")
        self.aotucheckbox9 = QCheckBox("总门锁")
        self.aotucheckbox10 = QCheckBox("左前锁")
        self.aotucheckbox11 = QCheckBox("右前锁")
        self.aotucheckbox12 = QCheckBox("左后锁")
        self.aotucheckbox13 = QCheckBox("右后锁")
        self.aotucheckbox14 = QCheckBox("总门窗")
        self.aotucheckbox15 = QCheckBox("左前窗")
        self.aotucheckbox16 = QCheckBox("右前窗")
        self.aotucheckbox17 = QCheckBox("左后窗")
        self.aotucheckbox18 = QCheckBox("右后窗")
        self.aotucheckbox19 = QCheckBox("天窗")
        self.aotucheckbox20 = QCheckBox("总灯")
        self.aotucheckbox21 = QCheckBox("大灯")
        self.aotucheckbox22 = QCheckBox("小灯")
        self.aotucheckbox23 = QCheckBox("设防/撤防")
        self.aotucheckbox24 = QCheckBox("告警")
        self.aotualarmdataCreatebtn = QPushButton(u"生成")
        self.aotualarmdataCreatebtn.clicked.connect(self.aotudatacreate)
        self.label331ExcessOil = QLabel("余油")
        self.label331ExcessVoltage = QLabel("余电")
        self.label331EnduranceMileage = QLabel("续航里程")
        self.label331AccumulatedMileage = QLabel("累积里程")
        self.label331BatteryVoltage = QLabel("电瓶电压")

        self.label331ExcessOil_input = QLineEdit()
        self.label331ExcessVoltage_input = QLineEdit()
        self.label331EnduranceMileage_input = QLineEdit()
        self.label331AccumulatedMileage_input = QLineEdit()
        self.label331BatteryVoltage_input = QLineEdit()

        self.label331ExcessOil_input.setText("50")
        self.label331ExcessVoltage_input.setText("70")
        self.label331EnduranceMileage_input.setText("90")
        self.label331AccumulatedMileage_input.setText("23456")
        self.label331BatteryVoltage_input.setText("1125")

        self.btnlist = [self.Btn4, self.Btn5, self.Btn6, self.Btn7, self.Btn8,
                        self.Btn9, self.Btn10, self.Btn11, self.Btn12, self.Btn13, self.Btn14, self.Btn15, self.Btn16,
                        self.Btn17, self.Btn18, self.Btn19, self.Btn20, self.Btn21, self.Btn22]

        self.onBtn.clicked.connect(self.go_online)
        self.defalBtn.clicked.connect(self.siruisetDefalut)
        self.sendBtn.clicked.connect(self.sendTcpmsg)
        self.clearBtn.clicked.connect(lambda: self.clearinfo(1))
        self.clearBtn2.clicked.connect(lambda: self.clearinfo(2))
        self.clearBtn3.clicked.connect(lambda: self.clearinfo(3))

        self.bindBtn.clicked.connect(self.bindBt)
        self.wg315Btn.clicked.connect(self.waiguadev)
        self.loginBtn.clicked.connect(self.otulogindataCreate)
        self.searchAddrBtn.clicked.connect(self.searchAddr)

        self.heartcheck.stateChanged.connect(self.sendHeart)
        self.otutimer = QTimer(self)  # 初始化一个定时器
        self.otutimer.timeout.connect(self.otudisabledHeartcheck)  # 计时结束调用disabledHeartcheck()方法

        self.Btn1.clicked.connect(lambda: self.btnclickevent(self.Btn1))
        self.Btn2.clicked.connect(lambda: self.btnclickevent(self.Btn2))
        self.Btn3.clicked.connect(lambda: self.btnclickevent(self.Btn3))
        self.Btn4.clicked.connect(lambda: self.btnclickevent(self.Btn4))
        self.Btn5.clicked.connect(lambda: self.btnclickevent(self.Btn5))
        self.Btn6.clicked.connect(lambda: self.btnclickevent(self.Btn6))
        self.Btn7.clicked.connect(lambda: self.btnclickevent(self.Btn7))
        self.Btn8.clicked.connect(lambda: self.btnclickevent(self.Btn8))
        # self.Btn9.clicked.connect(lambda: self.btnclickevent(self.Btn9))
        self.Btn10.clicked.connect(lambda: self.btnclickevent(self.Btn10))
        self.Btn11.clicked.connect(lambda: self.btnclickevent(self.Btn11))
        self.Btn12.clicked.connect(lambda: self.btnclickevent(self.Btn12))
        self.Btn13.clicked.connect(lambda: self.btnclickevent(self.Btn13))
        self.Btn14.clicked.connect(lambda: self.btnclickevent(self.Btn14))
        self.Btn15.clicked.connect(lambda: self.btnclickevent(self.Btn15))
        self.Btn16.clicked.connect(lambda: self.btnclickevent(self.Btn16))
        self.Btn17.clicked.connect(lambda: self.btnclickevent(self.Btn17))
        self.Btn18.clicked.connect(lambda: self.btnclickevent(self.Btn18))
        self.Btn19.clicked.connect(lambda: self.btnclickevent(self.Btn19))
        self.Btn20.clicked.connect(lambda: self.btnclickevent(self.Btn20))
        self.Btn21.clicked.connect(lambda: self.btnclickevent(self.Btn21))
        self.Btn22.clicked.connect(lambda: self.btnclickevent(self.Btn22))
        self.Btn24.clicked.connect(lambda: self.btnclickevent(self.Btn24))
        self.Btn23.clicked.connect(self.dancheng)
        self.Btn9.clicked.connect(self.sendEN)

        self.labelmsg = QLabel("转换内容")
        self.labelmsg.setAlignment(QtCore.Qt.AlignCenter)

        self.entrymsg = QLineEdit()
        self.entrymsg.setMinimumWidth(160)
        self.btnCreatqrcode = QPushButton("生成普通二维码")
        self.btnCreatqrcode.setStatusTip("请检查空格，空格也会作为内容一部分转成二维码")

        self.btnCreatqrcode2 = QPushButton("生成展车二维码")
        self.btnCreatqrcode2.setStatusTip("请检查空格，空格也会作为内容一部分转成二维码")

        self.btnCreatqrcode3 = QPushButton("清除二维码")
        self.btnCreatqrcode.clicked.connect(lambda: self.createQRcode(1))
        self.btnCreatqrcode2.clicked.connect(lambda: self.createQRcode(2))

        self.labelqrode = QLabel("")
        self.labelqrode.setObjectName("qrlabel")

        self.gpsUpload = QPushButton(u"附件GPS上报")
        self.gpsUpload.setStatusTip("附件放至D:\Tcptemp")
        self.gpsUpload.clicked.connect(self.gpsUploadfun)

        # 协议解密
        self.protocolDecodeBtn = QPushButton(u"协议解密")
        self.protocolDecodeEntry = QLineEdit()
        self.protocolDecodeBtn.clicked.connect(self.protocolDecode)

    def OtuMonitor_grid(self):
        self.maingrid.setColumnStretch(0, 6)
        self.maingrid.setColumnStretch(1, 2)
        self.maingrid.setColumnStretch(2, 2)

        # 左边窗体
        self.leftwidget = QWidget()
        self.leftgrid = QGridLayout()
        self.leftwidget.setLayout(self.leftgrid)
        self.maingrid.addWidget(self.leftwidget, 0, 0)
        # self.leftgrid.setColumnStretch(0, 4)
        self.leftgrid.setRowStretch(4, 1)
        self.leftgrid.setRowStretch(6, 2)
        self.leftgrid.setRowStretch(8, 2)

        self.leftgrid.addWidget(self.labelPort, 0, 0)
        self.leftgrid.addWidget(self.entryPort, 0, 1)
        self.leftgrid.addWidget(self.labelIP, 0, 2)
        self.leftgrid.addWidget(self.entryIP, 0, 3)
        self.leftgrid.addWidget(self.labelHardver, 0, 4)
        self.leftgrid.addWidget(self.entryHardver, 0, 5)
        self.leftgrid.addWidget(self.seleOtu, 0, 6)
        self.leftgrid.addWidget(self.seleAudi, 0, 7)
        self.leftgrid.addWidget(self.seleBuick, 0, 8)
        self.leftgrid.addWidget(self.defalBtn, 0, 9)

        self.leftgrid.addWidget(self.labelOtuIMEI, 1, 0)
        self.leftgrid.addWidget(self.entryOtuIMEI, 1, 1, 1, 3)
        self.leftgrid.addWidget(self.labelwait, 1, 4)
        self.leftgrid.addWidget(self.entrywait, 1, 5, 1, 1)
        self.leftgrid.addWidget(self.onBtn, 1, 7)
        self.leftgrid.addWidget(self.searchAddrBtn, 1, 8)
        self.leftgrid.addWidget(self.loginBtn, 1, 9)

        self.leftgrid.addWidget(self.labelBTIMEI, 2, 0)
        self.leftgrid.addWidget(self.entryBTIMEI, 2, 1, 1, 3)
        self.leftgrid.addWidget(self.bindBtn, 2, 4)
        self.leftgrid.addWidget(self.entrywaiguadev, 2, 5, 1, 4)
        self.leftgrid.addWidget(self.wg315Btn, 2, 9)

        self.leftgrid.addWidget(self.labelInput, 3, 0, 1, 2)
        self.leftgrid.addWidget(self.heartcheck, 3, 2, 1, 3, QtCore.Qt.AlignCenter)
        self.leftgrid.addWidget(self.clearBtn, 3, 8)
        self.leftgrid.addWidget(self.sendBtn, 3, 9)
        self.leftgrid.addWidget(self.textInput, 4, 0, 1, 10)
        self.leftgrid.addWidget(self.labelSendHistory, 5, 0, 1, 7)
        self.leftgrid.addWidget(self.clearBtn2, 5, 9)
        self.leftgrid.addWidget(self.textSend, 6, 0, 1, 10)
        self.leftgrid.addWidget(self.labelRecive, 7, 0, 1, 4)
        self.leftgrid.addWidget(self.clearBtn3, 7, 9)
        self.leftgrid.addWidget(self.textRecv, 8, 0, 1, 10)
        self.leftgrid.addWidget(self.gpsUpload, 3, 6, 1, 2)
        # self.leftgrid.addWidget(self.aotubox, 9, 0, 1, 10)

        # 中间窗体
        self.middlewiget = QWidget()
        self.middlegrid = QGridLayout()
        self.middlewiget.setLayout(self.middlegrid)
        self.maingrid.addWidget(self.middlewiget, 0, 1)

        self.middlegrid.addWidget(self.Btn1, 0, 0)
        self.middlegrid.addWidget(self.Btn2, 0, 1)
        self.middlegrid.addWidget(self.Btn3, 0, 2)
        self.middlegrid.addWidget(self.Btn4, 0, 3)
        self.middlegrid.addWidget(self.Btn5, 0, 4)
        self.middlegrid.addWidget(self.Btn6, 0, 5)
        self.middlegrid.addWidget(self.Btn7, 2, 0)
        self.middlegrid.addWidget(self.Btn8, 2, 1)
        self.middlegrid.addWidget(self.Btn9, 2, 2)
        self.middlegrid.addWidget(self.Btn10, 2, 3)
        self.middlegrid.addWidget(self.Btn11, 2, 4)
        self.middlegrid.addWidget(self.Btn12, 2, 5)
        self.middlegrid.addWidget(self.Btn13, 3, 0)
        self.middlegrid.addWidget(self.Btn14, 3, 1)
        self.middlegrid.addWidget(self.Btn15, 3, 2)
        self.middlegrid.addWidget(self.Btn16, 3, 3)
        self.middlegrid.addWidget(self.Btn17, 3, 4)
        self.middlegrid.addWidget(self.Btn18, 3, 5)
        self.middlegrid.addWidget(self.Btn19, 4, 0)
        self.middlegrid.addWidget(self.Btn20, 4, 1)
        self.middlegrid.addWidget(self.Btn21, 4, 2)
        self.middlegrid.addWidget(self.Btn22, 4, 3)
        self.middlegrid.addWidget(self.Btn23, 4, 4)
        self.middlegrid.addWidget(self.Btn24, 4, 5)

        self.middlegrid.addWidget(self.aotubox, 5, 0, 1, 6)

        # 右边窗体
        self.rightwidget = QWidget()
        self.rightgrid = QGridLayout()
        self.rightwidget.setLayout(self.rightgrid)
        self.maingrid.addWidget(self.rightwidget, 0, 2)

        self.rightgrid.addWidget(self.labelmsg, 0, 0)
        self.rightgrid.addWidget(self.entrymsg, 0, 1)
        self.rightgrid.addWidget(self.btnCreatqrcode, 1, 0, 1, 2, QtCore.Qt.AlignLeft)
        self.rightgrid.addWidget(self.btnCreatqrcode2, 1, 0, 1, 2, QtCore.Qt.AlignRight)
        self.rightgrid.addWidget(self.labelqrode, 2, 0, 1, 2, QtCore.Qt.AlignCenter)
        self.rightgrid.addWidget(self.protocolDecodeBtn, 3, 0)
        self.rightgrid.addWidget(self.protocolDecodeEntry, 3, 1)

        self.aotuboxGrid.addWidget(self.aotucheckbox1, 0, 0)
        self.aotuboxGrid.addWidget(self.aotucheckbox2, 1, 0)
        self.aotuboxGrid.addWidget(self.aotucheckbox3, 1, 1)
        self.aotuboxGrid.addWidget(self.aotucheckbox4, 1, 2)
        self.aotuboxGrid.addWidget(self.aotucheckbox5, 1, 3)
        self.aotuboxGrid.addWidget(self.aotucheckbox6, 1, 4)
        self.aotuboxGrid.addWidget(self.aotucheckbox7, 0, 1)
        self.aotuboxGrid.addWidget(self.aotucheckbox8, 0, 2)
        self.aotuboxGrid.addWidget(self.aotucheckbox9, 2, 0)
        self.aotuboxGrid.addWidget(self.aotucheckbox10, 2, 1)
        self.aotuboxGrid.addWidget(self.aotucheckbox11, 2, 2)
        self.aotuboxGrid.addWidget(self.aotucheckbox12, 2, 3)
        self.aotuboxGrid.addWidget(self.aotucheckbox13, 2, 4)
        self.aotuboxGrid.addWidget(self.aotucheckbox14, 3, 0)
        self.aotuboxGrid.addWidget(self.aotucheckbox15, 3, 1)
        self.aotuboxGrid.addWidget(self.aotucheckbox16, 3, 2)
        self.aotuboxGrid.addWidget(self.aotucheckbox17, 3, 3)
        self.aotuboxGrid.addWidget(self.aotucheckbox18, 3, 4)
        self.aotuboxGrid.addWidget(self.aotucheckbox19, 0, 3)
        self.aotuboxGrid.addWidget(self.aotucheckbox20, 4, 0)
        self.aotuboxGrid.addWidget(self.aotucheckbox21, 4, 1)
        self.aotuboxGrid.addWidget(self.aotucheckbox22, 4, 2)
        self.aotuboxGrid.addWidget(self.aotucheckbox23, 4, 3)
        self.aotuboxGrid.addWidget(self.aotucheckbox24, 4, 4)
        self.aotuboxGrid.addWidget(self.aotualarmdataCreatebtn, 0, 4)
        self.aotuboxGrid.addWidget(self.label331ExcessOil, 5, 0)
        self.aotuboxGrid.addWidget(self.label331ExcessOil_input, 5, 1)
        self.aotuboxGrid.addWidget(self.label331ExcessVoltage, 5, 2)
        self.aotuboxGrid.addWidget(self.label331ExcessVoltage_input, 5, 3)
        self.aotuboxGrid.addWidget(self.label331AccumulatedMileage, 6, 0)
        self.aotuboxGrid.addWidget(self.label331AccumulatedMileage_input, 6, 1)
        self.aotuboxGrid.addWidget(self.label331EnduranceMileage, 6, 2)
        self.aotuboxGrid.addWidget(self.label331EnduranceMileage_input, 6, 3)
        self.aotuboxGrid.addWidget(self.label331BatteryVoltage, 7, 0)
        self.aotuboxGrid.addWidget(self.label331BatteryVoltage_input, 7, 1)

    def siruisetDefalut(self):
        """默认按钮"""
        self.entryPort.setText("2103")
        self.entryIP.setText("192.168.6.52")
        self.entryHardver.setText("02062300")

    def clearinfo(self, clearindex):
        """清 空"""
        if clearindex == 1:
            self.textInput.clear()
        elif clearindex == 2:
            self.textSend.clear()
        elif clearindex == 3:
            self.textRecv.clear()
        else:
            pass

    def sendTcpmsg(self):
        """发 送"""
        msg = self.textInput.toPlainText()
        self.s.send(msg.encode())
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.timeNow() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(msg)
        self.textInput.clear()

    def sendEN(self):
        """发送位置
        当前在光电园
        """
        timeinfo = '(1*b2|7|30d,' + self.yqtool.hextime() + ',E,10629.7228,N,2937.1144,0,10,c,1,1,-1,79|)'
        self.textInput.insertPlainText(timeinfo)

    # def send331(self):
    #     """发送位置
    #     当前在光电园
    #     """
    #     time331 = self.yqtool.BSJhextime().replace(" ", "")
    #     datainfo = "(1*e4|7|331," + time331 + ",1,E,10629.7228,N,2937.1144,0,0,9,2200,2222222,22222,000000,110,22,1,7454,0,212,505|)"
    #     self.textInput.insertPlainText(datainfo)

    def bindBt(self):
        """蓝牙绑定"""
        Bt_IMEI = self.entryBTIMEI.text()
        sql = "SELECT mac FROM [sirui].[dbo].[Terminal] WHERE IMEI=\'" + Bt_IMEI + "\';"
        info = self.sqlserver.getinfo(sql)
        mac = str(info)[3:-4]

        msg = '(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac' + str(mac) + '_300,|)'
        self.s.send(msg.encode())
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.timeNow() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(msg)

    def waiguadev(self):
        """315外挂设备"""
        wgdev = self.entrywaiguadev.text()
        msg = ' (1*2c|2|315,3_' + str(wgdev) + '_0548.release.1_b4_a1_rf444.0.0212_300,|)'
        self.textInput.insertPlainText(msg)

    def fillsendmsg(self, message):
        """填充发送历史"""
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.timeNow() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(message)

    def fillrecvmsg(self, message):
        """填充接收历史"""
        self.textRecv.setTextColor(QColor("#FF3030"))
        self.textRecv.append(self.yqtool.timeNow() + " ")
        self.textRecv.setTextColor(QColor("#FFFFFF"))
        self.textRecv.insertPlainText(message)

    def waitandsend(self, message):
        """等待信号，启动等待发送定时器"""
        self.tcpth2 = WaiteandsendThread(message)
        self.tcpth2.signals.recv_signal.connect(self.fillrecvmsg)
        self.tcpth2.signals.send_signal.connect(self.fillsendmsg)

        self.threadpool.start(self.tcpth2)

    def otulogindataCreate(self):
        """等待信号，启动等待发送定时器"""
        otu_IMEI = self.entryOtuIMEI.text()
        hardver = self.entryHardver.text()
        r_blank = r'\d*\d'
        IMEI_NUM = re.findall(r_blank, otu_IMEI)
        if not IMEI_NUM:
            self.textRecv.append("未输入IEMI")
            return False

        if self.seleOtu.isChecked():
            loginType = "ost"
        elif self.seleAudi.isChecked():
            loginType = "audi"
        else:
            loginType = "buick"

        loginMsg = '(1*7c|a3|106,201|101,' + str(
            IMEI_NUM[0]) + '|102,460079241205511|104,otu.' + loginType + ',' + str(
            hardver) + '|105,a1,18|622,a1c2|)'
        self.textInput.setText(loginMsg)

    def searchAddr(self):
        """等待信号，启动等待发送定时器"""
        otu_IMEI = self.entryOtuIMEI.text()
        hardver = self.entryHardver.text()
        r_blank = r'\d*\d'
        IMEI_NUM = re.findall(r_blank, otu_IMEI)
        if not IMEI_NUM:
            self.textRecv.append("未输入IEMI")
            return False

        if self.seleOtu.isChecked():
            loginType = "ost"
        elif self.seleAudi.isChecked():
            loginType = "audi"
        else:
            loginType = "buick"

        loginMsg = '(1*7c|a1|106,201|101,' + str(
            IMEI_NUM[0]) + '|102,460079241205511|104,otu.' + loginType + ',' + str(
            hardver) + '|105,a1,18|112,1|622,a1c2|)'
        self.textInput.setText(loginMsg)

    def go_online(self):
        """上线"""
        if self.onBtn.text() == "连接":
            otu_IMEI = self.entryOtuIMEI.text()
            hardver = self.entryHardver.text()
            tcpadress = self.entryIP.text()
            tcpport = self.entryPort.text()

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.s.connect((tcpadress, int(tcpport)))
            except Exception as msg:
                errorinfo = Exception, ":", msg
                appendinfo = errorinfo[2].strerror
                self.textRecv.append(appendinfo)
                return False

            self.scene.onlineCol.start()  # 上线动画

            # loginMsg = '(1*7c|a3|106,201|101,' + str(
            #     IMEI_NUM[0]) + '|102,460079241205511|104,otu.' + loginType + ',' + str(
            #     hardver) + '|105,a1,18|622,a1c2|)'
            #
            # self.s.send(loginMsg.encode())  # 商用去掉103
            # self.textSend.setTextColor(QColor("#FF3030"))
            # self.textSend.append(self.yqtool.timeNow() + " ")
            # self.textSend.setTextColor(QColor("#FFFFFF"))
            # self.textSend.insertPlainText(loginMsg)

            historydata = open('D:\Tcptemp\data.txt', "w")  # 生成缓存文件data
            historydata.write(otu_IMEI + "," + tcpadress + "," + tcpport + "," + hardver)  # IMEI保存到缓存文件data
            historydata.close()

            self.tcpth = TcpThread(self.s, self.onBtn, self.heartcheck, self.sendBtn, self.bindBtn, self.wg315Btn,
                                   self.entrywait)
            self.tcpth.recv_signal.connect(self.fillrecvmsg)
            self.tcpth.send_signal.connect(self.fillsendmsg)
            self.tcpth.animate_signal.connect(self.scene.threadAnimate)
            self.tcpth.wait_signal.connect(self.waitandsend)
            self.tcpth.start()

            self.onBtn.setText("断开")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)
            self.bindBtn.setDisabled(False)
            self.wg315Btn.setDisabled(False)

        elif self.onBtn.text() == "断开":
            self.scene.offlineCol.start()
            global stopsingle
            stopsingle = 1
            self.s.shutdown(2)
        else:
            pass

    def dancheng(self):
        u"""单程"""
        self.num += 1
        hexnum = "%x" % self.num
        msg = "(1*b4|7|421," + hexnum + ",ab0,59d8,0,0,8,2|)"
        self.textInput.append(msg)

    def otudisabledHeartcheck(self):
        self.s.send('()'.encode())
        self.fillsendmsg("()")

    def sendHeart(self):
        if self.heartcheck.isChecked():
            self.s.send('()'.encode())
            self.fillsendmsg("()")
            self.otutimer.start(30000)
        else:
            self.otutimer.stop()

    def btnclickevent(self, btn):
        info = self.protocol[btn.text()]
        # print(info)
        self.textInput.insertPlainText(info)

    def createQRcode(self, singalindex):
        """生成二维码"""
        singal = singalindex
        if singal == 2:
            Bt_IMEI = self.entrymsg.text()
            sql = "SELECT ClientType FROM [sirui].[dbo].[Terminal]WHERE IMEI=\'" + Bt_IMEI + "\';"
            info = self.sqlserver.getinfo(sql)
            clientType = str(info)[2:-3]
            if clientType == '16':
                sql = "SELECT randomID FROM [sirui].[dbo].[Bluetooth] WHERE mac=\'" + Bt_IMEI + "\';"
                info = self.sqlserver.getinfo(sql)
                randomID = str(info)[3:-4]
                # randomID = 'ccafd8'
                c = Bt_IMEI + '_' + randomID + '_0_copyright@sirui ChungKing'
            else:
                c = Bt_IMEI + '_' + Bt_IMEI[-6:] + Bt_IMEI[-2:] + '_0_copyright@sirui ChungKing'
            print(c)
            c_info = base64.b64encode(c.encode())
            imgdata = 'exhibition_' + c_info.decode()
            print(imgdata)
        else:
            imgdata = self.entrymsg.text()

        qr = qrcode.QRCode(
            version=5,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
            box_size=5,  # 每个格子的像素大小
            border=1,  # 边框的格子宽度大小
        )
        qr.add_data(imgdata)
        qr.make(fit=True)
        img = qr.make_image()
        img.save('D:\Tcptemp\qrcode.png')

        self.labelqrode.setPixmap(QtGui.QPixmap("D:\Tcptemp\qrcode.png"))

    def aotudatacreate(self):
        def checkindex(checkbox):
            if checkbox.isChecked():
                return "1"
            else:
                return "2"

        check1 = checkindex(self.aotucheckbox1)
        check2 = checkindex(self.aotucheckbox2)
        check3 = checkindex(self.aotucheckbox3)
        check4 = checkindex(self.aotucheckbox4)
        check5 = checkindex(self.aotucheckbox5)
        check6 = checkindex(self.aotucheckbox6)
        check7 = checkindex(self.aotucheckbox7)
        check8 = checkindex(self.aotucheckbox8)
        check9 = checkindex(self.aotucheckbox9)
        check10 = checkindex(self.aotucheckbox10)
        check11 = checkindex(self.aotucheckbox11)
        check12 = checkindex(self.aotucheckbox12)
        check13 = checkindex(self.aotucheckbox13)
        check14 = checkindex(self.aotucheckbox14)
        check15 = checkindex(self.aotucheckbox15)
        check16 = checkindex(self.aotucheckbox16)
        check17 = checkindex(self.aotucheckbox17)
        check18 = checkindex(self.aotucheckbox18)
        check19 = checkindex(self.aotucheckbox19)
        check20 = checkindex(self.aotucheckbox20)
        check21 = checkindex(self.aotucheckbox21)
        check22 = checkindex(self.aotucheckbox22)
        check23 = checkindex(self.aotucheckbox23)
        check24 = checkindex(self.aotucheckbox24)

        onStatus = str(check1)
        doorStatus = str(check2) + str(check3) + str(check4) + str(check5) + str(check6) + str(check7) + str(check8)
        doorLockStatus = str(check9) + str(check10) + str(check11) + str(check12) + str(check13)
        doorWindowStatus = str(check14) + str(check15) + str(check16) + str(check17) + str(check18) + str(check19)
        lightStatus = str(check20) + str(check21) + str(check22)
        shefangStatus = str(check23) + str(check24)
        time331 = self.yqtool.BSJhextime().replace(" ", "")

        AccumulatedMileage = hex(int(self.label331AccumulatedMileage_input.text()))[2:]  # "累积里程"
        BatteryVoltage = hex(int(self.label331BatteryVoltage_input.text()))[2:]  # 电瓶电压
        EnduranceMileage = hex(int(self.label331EnduranceMileage_input.text()))[2:]  # 续航里程
        ExcessVoltage = hex(int(self.label331ExcessVoltage_input.text()))[2:]  # 余电
        ExcessOil = hex(int(self.label331ExcessOil_input.text()))[2:]  # 余油

        datainfo = "(1*e4|7|331," + time331 + ",1,E,10629.7228,N,2937.1144,0,0,9," + onStatus + "200," + doorStatus + "," + doorLockStatus + "," + doorWindowStatus + "," + lightStatus + "," + shefangStatus + ",1," + AccumulatedMileage + "," + EnduranceMileage + "," + ExcessOil + "," + BatteryVoltage + ",1,1,1," + ExcessVoltage + ",0|)"
        self.textInput.insertPlainText(datainfo)

    def gpsUploadfun(self):
        file1 = open("D:\\Tcptemp\\gpslocation", "r")
        data = file1.readlines()
        file1.close()

        self.tcpth3 = GpsUploadThread(data, self.s)
        self.tcpth3.signals.recv_signal.connect(self.fillrecvmsg)
        self.tcpth3.signals.send_signal.connect(self.fillsendmsg)
        #
        self.threadpool.start(self.tcpth3)

    def protocolDecode(self):
        """协议解密"""
        msg = self.protocolDecodeEntry.text()
        context = msg[5:-1]
        offset = int(msg[2:4], 16)
        data = CRCUtil().asiccCrcDecode(context, offset)
        plaintext = msg[:5] + data + ")"
        self.protocolDecodeEntry.clear()
        self.protocolDecodeEntry.setText(plaintext)


class BSJMonitor(MainWidget):
    def __init__(self):
        super(BSJMonitor, self).__init__()
        self.sqlserver = Sqlfunticon()
        self.num = 0

    def bsjSplice(self):
        for i in self.deleteWigt:
            i.deleteLater()
        self.BSJMonitor_UI()
        self.BSJMonitor_grid()
        try:
            self.s.shutdown(2)
            global stopsingle
            stopsingle = 1
            self.scene.offlineCol.start()
        except AttributeError:
            pass
        self.deleteWigt = [self.leftwidget, self.middlewiget]

    def BSJMonitor_UI(self):
        # styleqss = open("otu.qss", "r", encoding='UTF-8')
        # styleinfo = styleqss.read()
        styleinfo = 'QLabel{font:75 10pt "Microsoft YaHei";color:floralwhite;}QPushButton{font:75 10pt "Microsoft YaHei";background-color:#FFFFFF;border:1px solid #8f8f91;border-radius:9px;min-width:50px;min-height:24px}QPushButton::hover{background-color:#FF6A6A;}QRadioButton{font:75 10pt "Microsoft YaHei";color:floralwhite;}QRadioButton::indicator{width:10px;height:10px;border-radius:5px;}QRadioButton::indicator:checked{background-color:#FFA07A;border:1px solid black;}QRadioButton::indicator:unchecked{background-color:white;border:1px solid black;}QCheckBox{font:75 10pt "Microsoft YaHei";color:floralwhite;background-color:rgba(255,255,255,0);}QTextEdit{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}QTextBrowser{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}'
        self.mainwidget.setStyleSheet(styleinfo)
        # styleqss.close()

        """左侧窗口"""
        # 登录box
        self.loginbox = QGroupBox("登录信息包")
        self.loginboxGrid = QGridLayout()
        self.loginbox.setLayout(self.loginboxGrid)
        self.labelOtuIMEI = QLabel(u"主机IMEI", self)
        self.entryOtuIMEI = QLineEdit()
        self.onBtn = QPushButton(u"连接")
        self.logindataCreatebtn = QPushButton(u"生成")

        # gpsbox
        self.gpsbox = QGroupBox("定位数据包")
        self.gpsboxGrid = QGridLayout()
        self.gpsbox.setLayout(self.gpsboxGrid)
        self.labelsatelliteCount = QLabel(u"星数", self)
        self.entrysatelliteCount = QLineEdit()
        self.entrysatelliteCount.setMaximumWidth(50)
        self.entrysatelliteCount.insert("13")
        self.labelLng = QLabel(u"经度", self)
        self.entryLng = QLineEdit()
        self.entryLng.insert("106.49557015756179")
        self.labelLat = QLabel(u"纬度", self)
        self.entryLat = QLineEdit()
        self.entryLat.insert("29.61881556261095")
        self.labelSpeed = QLabel(u"速度", self)
        self.entrySpeed = QLineEdit()
        self.entrySpeed.setMaximumWidth(50)
        self.entrySpeed.insert("60")
        self.labelCourse = QLabel(u"航向", self)
        self.entryCourse = QLineEdit()
        self.entryCourse.insert("123")
        self.entryCourse.setMaximumWidth(50)
        self.gpsdataCreatebtn = QPushButton(u"生成")

        # 告警box
        self.alarmbox = QGroupBox("告警包")
        self.alarmboxGrid = QGridLayout()
        self.alarmbox.setLayout(self.alarmboxGrid)
        self.checkbox1 = QCheckBox("震动")
        self.checkbox2 = QCheckBox("碰撞")
        self.checkbox3 = QCheckBox("急加速")
        self.checkbox4 = QCheckBox("急减速")
        self.checkbox5 = QCheckBox("急转弯")
        self.checkbox6 = QCheckBox("超速")
        self.checkbox7 = QCheckBox("主电源")
        self.checkbox8 = QCheckBox("加速度传感器")
        self.alarmdataCreatebtn = QPushButton(u"生成")

        # 心跳box
        self.heartbeatbox = QGroupBox("扩展字段")
        self.heartbeatboxGrid = QGridLayout()
        self.heartbeatbox.setLayout(self.heartbeatboxGrid)
        self.labelGSM = QLabel(u"GSM信号强度", self)
        self.entryGSM = QLineEdit()
        self.entryGSM.insert("31")
        self.labelMileage = QLabel(u"里程", self)
        self.entryMileage = QLineEdit()
        self.entryMileage.insert("1000")
        # self.sele1 = QRadioButton(u"无信号")
        # self.sele2 = QRadioButton(u"极弱")
        # self.sele3 = QRadioButton(u"较弱")
        # self.sele4 = QRadioButton(u"良好")
        # self.sele5 = QRadioButton(u"强")
        # self.sele5.setChecked(True)

        self.labelvoltage = QLabel(u"电压", self)
        self.entryvoltage = QLineEdit()
        self.entryvoltage.insert("1200")
        self.labelAcceleration = QLabel(u"加速度最大差值", self)
        self.entryAcceleration = QLineEdit()
        self.entryAcceleration.insert("484")

        # self.heartbeatdataCreatebtn = QPushButton(u"生成")

        self.labelPort = QLabel("端口2", self)
        self.labelPort.setMaximumWidth(50)
        self.labelIP = QLabel("IP", self)
        self.labelIP.setMaximumWidth(20)

        self.labelOtuIMEI = QLabel(u"主机IMEI", self)
        self.labelBTIMEI = QLabel("蓝牙IMEI", self)
        self.labelInput = QLabel("自定义输入界面", self)
        self.labelSendHistory = QLabel("发送历史", self)
        self.labelRecive = QLabel("接收历史", self)

        self.entryPort = QLineEdit()
        self.entryPort.setMaximumWidth(50)
        self.entryIP = QLineEdit()

        self.entryBTIMEI = QLineEdit()

        try:
            conf = configparser.ConfigParser()
            conf.read('D:\\Tcptemp\\bsjdata.ini')  # 文件路径
            port = conf.get("setting", "port")  # 获取指定section 的option值
            bsjip = conf.get("setting", "ip")  # 获取section1 的sex值
            imei = conf.get("setting", "imei")
            self.entryPort.insert(port)
            self.entryIP.insert(bsjip)
            self.entryOtuIMEI.insert(imei)
        except (AttributeError, configparser.NoOptionError, configparser.NoSectionError) as msg:
            print(msg)
            # pass

        self.defalBtn = QPushButton(u"默认")
        self.sendBtn = QPushButton(u"发送")
        self.sendBtn.setDisabled(True)
        self.clearBtn = QPushButton(u"清空")
        self.clearBtn2 = QPushButton(u"清空")
        self.clearBtn3 = QPushButton(u"清空")

        self.heartcheck = QCheckBox("心跳挂机(保持连接请打钩√）")
        self.heartcheck.setVisible(False)

        self.textInput = QTextEdit()
        self.textInput.setAlignment(QtCore.Qt.AlignLeft)
        self.textSend = QTextBrowser()
        # self.textSend.setReadOnly(False) # 设置不可编辑
        self.textRecv = QTextBrowser()

        self.logindataCreatebtn.clicked.connect(self.logindatacreate)
        self.gpsdataCreatebtn.clicked.connect(self.gpsdatacreate)
        self.alarmdataCreatebtn.clicked.connect(self.alarmdatacreate)
        # self.heartbeatdataCreatebtn.clicked.connect(self.heartbeatdatacreate)

        """中间窗口"""
        self.onBtn.clicked.connect(self.connectTcp)
        self.defalBtn.clicked.connect(self.bsjsetDefalut)
        self.sendBtn.clicked.connect(self.sendTcpmsghex)
        self.clearBtn.clicked.connect(lambda: self.clearinfo(1))
        self.clearBtn2.clicked.connect(lambda: self.clearinfo(2))
        self.clearBtn3.clicked.connect(lambda: self.clearinfo(3))

        self.heartcheck.stateChanged.connect(self.sendHeartBSJ)
        self.bsjtimer = QTimer(self)  # 初始化一个定时器
        self.bsjtimer.timeout.connect(self.bsjdisabledHeartcheck)  # 计时结束调用disabledHeartcheck()方法

        self.labelmsg = QLabel("转换内容")
        self.labelmsg.setAlignment(QtCore.Qt.AlignCenter)
        self.entrymsg = QLineEdit()
        self.btnCreatqrcode = QPushButton("生成普通二维码")
        self.btnCreatqrcode.setStatusTip("请检查空格，空格也会作为内容一部分转成二维码")

        self.btnCreatqrcode2 = QPushButton("生成展车二维码")
        self.btnCreatqrcode2.setStatusTip("请检查空格，空格也会作为内容一部分转成二维码")

        self.btnCreatqrcode3 = QPushButton("清除二维码")
        self.btnCreatqrcode.clicked.connect(lambda: self.createQRcode(1))
        self.btnCreatqrcode2.clicked.connect(lambda: self.createQRcode(2))

        self.labelqrode = QLabel("")
        self.labelqrode.setObjectName("qrlabel")

    def BSJMonitor_grid(self):
        self.maingrid.setColumnStretch(0, 7)
        self.maingrid.setColumnStretch(1, 2)
        # 左边窗体
        self.leftwidget = QWidget()
        self.leftgrid = QGridLayout()
        self.leftwidget.setLayout(self.leftgrid)
        self.maingrid.addWidget(self.leftwidget, 0, 0)

        self.leftgrid.setRowStretch(6, 1)
        self.leftgrid.setRowStretch(8, 2)
        self.leftgrid.setRowStretch(10, 2)

        self.leftgrid.addWidget(self.labelPort, 0, 0)
        self.leftgrid.addWidget(self.entryPort, 0, 1)
        self.leftgrid.addWidget(self.labelIP, 0, 2)
        self.leftgrid.addWidget(self.entryIP, 0, 3)
        self.leftgrid.addWidget(self.defalBtn, 0, 4)
        self.leftgrid.addWidget(self.onBtn, 0, 5)

        self.leftgrid.addWidget(self.loginbox, 1, 0, 1, 6)
        self.loginboxGrid.addWidget(self.labelOtuIMEI, 0, 0)
        self.loginboxGrid.addWidget(self.entryOtuIMEI, 0, 1)
        self.loginboxGrid.addWidget(self.logindataCreatebtn, 0, 2)

        self.leftgrid.addWidget(self.gpsbox, 2, 0, 1, 6)
        self.gpsboxGrid.addWidget(self.labelsatelliteCount, 0, 0)
        self.gpsboxGrid.addWidget(self.entrysatelliteCount, 0, 1)
        self.gpsboxGrid.addWidget(self.labelLat, 0, 2)
        self.gpsboxGrid.addWidget(self.entryLat, 0, 3)
        self.gpsboxGrid.addWidget(self.labelLng, 0, 4)
        self.gpsboxGrid.addWidget(self.entryLng, 0, 5)
        self.gpsboxGrid.addWidget(self.labelSpeed, 0, 6)
        self.gpsboxGrid.addWidget(self.entrySpeed, 0, 7)
        self.gpsboxGrid.addWidget(self.labelCourse, 0, 8)
        self.gpsboxGrid.addWidget(self.entryCourse, 0, 9)
        self.gpsboxGrid.addWidget(self.gpsdataCreatebtn, 0, 10)

        self.leftgrid.addWidget(self.heartbeatbox, 4, 0, 1, 6)
        # self.heartbeatboxGrid.addWidget(self.sele1, 0, 1)
        # self.heartbeatboxGrid.addWidget(self.sele2, 0, 2)
        # self.heartbeatboxGrid.addWidget(self.sele3, 0, 3)
        # self.heartbeatboxGrid.addWidget(self.sele4, 0, 4)
        # self.heartbeatboxGrid.addWidget(self.sele5, 0, 5)
        self.heartbeatboxGrid.addWidget(self.labelMileage, 0, 0)
        self.heartbeatboxGrid.addWidget(self.entryMileage, 0, 1)
        self.heartbeatboxGrid.addWidget(self.labelAcceleration, 0, 2)
        self.heartbeatboxGrid.addWidget(self.entryAcceleration, 0, 3)
        self.heartbeatboxGrid.addWidget(self.labelvoltage, 0, 4)
        self.heartbeatboxGrid.addWidget(self.entryvoltage, 0, 5)
        self.heartbeatboxGrid.addWidget(self.labelGSM, 0, 6)
        self.heartbeatboxGrid.addWidget(self.entryGSM, 0, 7)

        # self.heartbeatboxGrid.addWidget(self.heartbeatdataCreatebtn, 0, 8)

        self.leftgrid.addWidget(self.labelInput, 5, 0, 1, 2)
        self.leftgrid.addWidget(self.heartcheck, 5, 3, QtCore.Qt.AlignCenter)
        self.leftgrid.addWidget(self.clearBtn, 5, 4)
        self.leftgrid.addWidget(self.sendBtn, 5, 5)
        self.leftgrid.addWidget(self.textInput, 6, 0, 1, 6)

        self.leftgrid.addWidget(self.labelSendHistory, 7, 0, 1, 6)
        self.leftgrid.addWidget(self.clearBtn2, 7, 5)
        self.leftgrid.addWidget(self.textSend, 8, 0, 1, 6)

        self.leftgrid.addWidget(self.labelRecive, 9, 0, 1, 6)
        self.leftgrid.addWidget(self.clearBtn3, 9, 5)
        self.leftgrid.addWidget(self.textRecv, 10, 0, 1, 6)

        # 中间窗体
        self.middlewiget = QWidget()
        self.middlegrid = QGridLayout()
        self.middlewiget.setLayout(self.middlegrid)
        self.maingrid.addWidget(self.middlewiget, 0, 1)

        self.middlegrid.addWidget(self.alarmbox, 0, 0, 1, 3)
        self.alarmboxGrid.addWidget(self.checkbox1, 0, 0)
        self.alarmboxGrid.addWidget(self.checkbox2, 0, 1)
        self.alarmboxGrid.addWidget(self.checkbox3, 0, 2)
        self.alarmboxGrid.addWidget(self.checkbox4, 1, 0)
        self.alarmboxGrid.addWidget(self.checkbox5, 1, 1)
        self.alarmboxGrid.addWidget(self.checkbox6, 1, 2)
        self.alarmboxGrid.addWidget(self.checkbox7, 2, 0)
        self.alarmboxGrid.addWidget(self.checkbox8, 2, 1)
        self.alarmboxGrid.addWidget(self.alarmdataCreatebtn, 2, 2)

        self.middlegrid.addWidget(self.labelmsg, 3, 0)
        self.middlegrid.addWidget(self.entrymsg, 3, 1, 1, 2)
        self.middlegrid.addWidget(self.btnCreatqrcode, 4, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.middlegrid.addWidget(self.btnCreatqrcode2, 4, 0, 1, 3, QtCore.Qt.AlignRight)
        self.middlegrid.addWidget(self.labelqrode, 5, 0, 1, 3, QtCore.Qt.AlignCenter)

    def bsjsetDefalut(self):
        """默认按钮"""
        self.entryPort.setText("2111")
        self.entryIP.setText("192.168.6.52")

    def getExtendedField(self):
        mileage = ('%x' % (int(self.entryMileage.text()))).zfill(8)
        mileage = mileage[0:2] + " " + mileage[2:4] + " " + mileage[4:6] + " " + mileage[-2:]
        acceleration = ('%x' % (int(self.entryAcceleration.text()))).zfill(8)
        acceleration = acceleration[0:2] + " " + acceleration[2:4] + " " + acceleration[4:6] + " " + acceleration[-2:]
        voltage = ('%x' % (int(self.entryvoltage.text()))).zfill(4)
        voltage = voltage[0:2] + " " + voltage[-2:]
        gsm = ('%x' % (int(self.entryGSM.text()))).zfill(2)
        extendedField = "eb 23 05 01 " + mileage + " 03 02 01 1c 05 03 " + acceleration + " 03 04 " + voltage + " 02 05 " + gsm + " 03 06 ff fc 07 07 00 b4 80 b4 03 48"
        return extendedField

    def getgpsinfo(self):
        satelliteCount = ('%x' % int(self.entrysatelliteCount.text())).zfill(1)
        lat = self.entryLat.text()
        hexlat = ('%x' % (int(float(lat) * 60 * 30000))).zfill(8)
        hexlat = hexlat[0:2] + " " + hexlat[2:4] + " " + hexlat[4:6] + " " + hexlat[-2:]
        lng = self.entryLng.text()
        hexlng = ('%x' % (int(float(lng) * 60 * 30000))).zfill(8)
        hexlng = hexlng[0:2] + " " + hexlng[2:4] + " " + hexlng[4:6] + " " + hexlng[-2:]
        speed = ('%x' % int(self.entrySpeed.text())).zfill(2)
        course1 = ('%x' % int('000101' + bin(int(self.entryCourse.text()))[2:].zfill(10)[:2], 2)).zfill(2)
        course2 = ('%x' % int((bin(int(self.entryCourse.text()))[2:].zfill(10)[-8:]), 2)).zfill(2)
        course = course1 + " " + course2

        gpsinfo = "c" + satelliteCount + " " + hexlat + " " + hexlng + " " + speed + " " + course
        return gpsinfo

    def logindatacreate(self):
        imei = self.entryOtuIMEI.text()
        imei2 = imei.zfill(16)
        xindex = -16
        imeiphone = ""
        for i in range(8):
            if xindex + 2 == 0:
                imeiphone += imei2[xindex:]
            else:
                imeiphone += imei2[xindex:xindex + 2] + " "
            xindex += 2
        data = "78 78 11 01 " + imeiphone + " 02 00 03 20 00 01 8C DD 0D 0A"
        self.textInput.insertPlainText(data)

        conf = configparser.ConfigParser()
        conf.read('D:\\Tcptemp\\bsjdata.ini')
        try:
            conf.set("setting", "imei", imei)
        except configparser.NoSectionError:
            conf.add_section("setting")
            conf.set("setting", "imei", imei)
        with open('D:\\Tcptemp\\bsjdata.ini', 'w') as configfile:
            conf.write(configfile)
            configfile.close()

    def gpsdatacreate(self):
        gpsinfo = self.getgpsinfo()
        extendedField = self.getExtendedField()

        data = "78 78 47 22 " + self.yqtool.BSJhextime() + gpsinfo + " 01 cc 00 28 7d 00 1f b8 01 01 00 " + extendedField + " 00 03 80 81 0d 0a"
        self.textInput.insertPlainText(data)

    def alarmdatacreate(self):
        def checkindex(checkbox):
            if checkbox.isChecked():
                return "0"
            else:
                return "1"

        check1 = checkindex(self.checkbox1)
        check2 = checkindex(self.checkbox2)
        check3 = checkindex(self.checkbox3)
        check4 = checkindex(self.checkbox4)
        check5 = checkindex(self.checkbox5)
        check6 = checkindex(self.checkbox6)
        check7 = checkindex(self.checkbox7)
        check8 = checkindex(self.checkbox8)

        alarm = "0b111111111111111111111111" + check8 + check7 + check6 + check5 + check4 + check3 + check2 + check1
        alarmdatahex = '%x' % int(alarm, 2)
        alarmdata = alarmdatahex[0:2] + " " + alarmdatahex[2:4] + " " + alarmdatahex[4:6] + " " + alarmdatahex[-2:]

        gpsinfo = self.getgpsinfo()
        extendedField = self.getExtendedField()

        data = "78 78 49 26 " + self.yqtool.BSJhextime() + gpsinfo + " 08 01 CC 00 26 2C 00 0E BA " + alarmdata + " " + extendedField + " 00 cb 31 52 0d 0a"
        self.textInput.insertPlainText(data)

    def heartbeatdatacreate(self):
        voltage = ('%x' % (int(self.entryvoltage.text()))).zfill(4)
        voltage = voltage[0:2] + " " + voltage[-2:]
        datahex = ("%x" % (int(self.entryGSM.text()))).zfill(2)
        extendedField = "eb 23 03 04 " + voltage + " 02 05 " + datahex + " 03 06 ff fc"
        data = "78 78 12 13 " + extendedField + " 00 6a 02 da 0d 0a"
        self.textInput.insertPlainText(data)

    def clearinfo(self, clearindex):
        """清 空"""
        if clearindex == 1:
            self.textInput.clear()
        elif clearindex == 2:
            self.textSend.clear()
        elif clearindex == 3:
            self.textRecv.clear()
        else:
            pass

    def dataSwitch(self, data):
        str1 = ''
        str2 = b''
        while data:
            str1 = data[0:2]
            s = int(str1, 16)
            str2 += struct.pack('B', s)
            data = data[3:]
        return str2

    def sendTcpmsghex(self):
        """发 送"""
        msg = self.textInput.toPlainText()
        self.s.send(self.dataSwitch(msg))
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.timeNow() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(msg)
        self.textInput.clear()

    def fillsendmsg(self, message):
        """填充发送历史"""
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.timeNow() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(message)

    def fillrecvmsg(self, message):
        """填充接收历史"""
        self.textRecv.setTextColor(QColor("#FF3030"))
        self.textRecv.append(self.yqtool.timeNow() + " ")
        self.textRecv.setTextColor(QColor("#FFFFFF"))
        self.textRecv.insertPlainText(message)

    def connectTcp(self):
        """上线"""
        if self.onBtn.text() == "连接":
            tcpadress = self.entryIP.text()
            tcpport = self.entryPort.text()

            r_blank = r'\d*\d'

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.s.connect((tcpadress, int(tcpport)))
            except Exception as msg:
                errorinfo = Exception, ":", msg
                appendinfo = errorinfo[2].strerror
                self.textRecv.append(appendinfo)
                return False

            self.scene.onlineCol.start()  # 上线动画

            # 缓存
            conf = configparser.ConfigParser()
            conf.read('D:\\Tcptemp\\bsjdata.ini')
            try:
                conf.set("setting", "ip", tcpadress)
                conf.set("setting", "port", tcpport)
            except configparser.NoSectionError:
                conf.add_section("setting")
                conf.set("setting", "ip", tcpadress)
                conf.set("setting", "port", tcpport)
            with open('D:\\Tcptemp\\bsjdata.ini', 'w') as configfile:
                conf.write(configfile)
                configfile.close()

            self.tcpth = BSJTcpThread(self.s, self.onBtn, self.heartcheck, self.sendBtn)
            self.tcpth.recv_signal.connect(self.fillrecvmsg)
            self.tcpth.send_signal.connect(self.fillsendmsg)
            self.tcpth.animate_signal.connect(self.scene.threadAnimate)
            self.tcpth.start()

            self.onBtn.setText("断开")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)

        elif self.onBtn.text() == "断开":
            self.scene.offlineCol.start()
            global stopsingle
            stopsingle = 1
            self.s.shutdown(2)
        else:
            pass

    def bsjdisabledHeartcheck(self):
        self.s.send(self.dataSwitch('78 78 12 13 eb 0b 04 04 04 f6 02 05 17 03 06 ff fb 00 6a 02 da 0d 0a'))
        self.fillsendmsg("78 78 12 13 eb 0b 04 04 04 f6 02 05 17 03 06 ff fb 00 6a 02 da 0d 0a")

    def sendHeartBSJ(self):
        if self.heartcheck.isChecked():
            voltage = ('%x' % (int(self.entryvoltage.text()))).zfill(4)
            voltage = voltage[0:2] + " " + voltage[-2:]
            datahex = ("%x" % (int(self.entryGSM.text()))).zfill(2)
            extendedField = "eb 23 03 04 " + voltage + " 02 05 " + datahex + " 03 06 ff fc"
            data = "78 78 12 13 " + extendedField + " 00 6a 02 da 0d 0a"

            self.s.send(self.dataSwitch(data))
            self.fillsendmsg(data)
            self.bsjtimer.start(30000)
        else:
            self.bsjtimer.stop()

    def btnclickevent(self, btn):
        info = self.protocol[btn.text()]
        # print(info)
        self.textInput.insertPlainText(info)

    def createQRcode(self, singalindex):
        """生成二维码"""
        singal = singalindex
        if singal == 2:
            Bt_IMEI = self.entrymsg.text()
            sql = "SELECT ClientType FROM [sirui].[dbo].[Terminal]WHERE IMEI=\'" + Bt_IMEI + "\';"
            info = self.sqlserver.getinfo(sql)
            clientType = str(info)[2:-3]
            if clientType == '16':
                sql = "SELECT randomID FROM [sirui].[dbo].[Bluetooth] WHERE mac=\'" + Bt_IMEI + "\';"
                info = self.sqlserver.getinfo(sql)
                randomID = str(info)[3:-4]
                # randomID = 'ccafd8'
                c = Bt_IMEI + '_' + randomID + '_0_copyright@sirui ChungKing'
            else:
                c = Bt_IMEI + '_' + Bt_IMEI[-6:] + Bt_IMEI[-2:] + '_0_copyright@sirui ChungKing'
            print(c)
            c_info = base64.b64encode(c.encode())
            imgdata = 'exhibition_' + c_info.decode()
            print(imgdata)
        else:
            imgdata = self.entrymsg.text()

        qr = qrcode.QRCode(
            version=5,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
            error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
            box_size=5,  # 每个格子的像素大小
            border=1,  # 边框的格子宽度大小
        )
        qr.add_data(imgdata)
        qr.make(fit=True)
        img = qr.make_image()
        img.save('D:\Tcptemp\qrcode.png')

        self.labelqrode.setPixmap(QtGui.QPixmap("D:\Tcptemp\qrcode.png"))


class StartLoop(OtuMonitor, BSJMonitor):
    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    ex = StartLoop()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

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


class Bianlifunction:
    """个人便利方法集合"""

    @staticmethod
    def timeNow():
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        return local_time.strftime("%H:%M:%S")

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
        self.resize(1100, 680)
        self.center()
        self.setWindowTitle(u'桴之科测试工具 Version:2018.05.23')
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


class TcpThread(QtCore.QThread):
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)
    animate_signal = QtCore.pyqtSignal(str)

    def __init__(self, socketcp, onBtn, heartcheck, senBtn, bindBtn, wg315Btn):
        super().__init__()
        self.s = socketcp
        self.yqtool = Bianlifunction()
        self.onBtn = onBtn
        self.heartcheck = heartcheck
        self.sendBtn = senBtn
        self.bindBtn = bindBtn
        self.wg315Btn = wg315Btn

    def run(self):
        """线程"""
        global stopsingle
        stopsingle = 0
        while 1:
            tcpreceive = self.s.recv(1024).decode()
            xinfo = re.findall(r'\|(\w\w\w),', tcpreceive)  # 检测是否为控制协议
            if "511" in xinfo or "512" in xinfo or "513" in xinfo or '514' in xinfo or '515' in xinfo or '516' in xinfo \
                    or '517' in xinfo or '518' in xinfo or '519' in xinfo or '51A' in xinfo or '51B' in xinfo \
                    or '51C' in xinfo:
                self.recv_signal.emit(tcpreceive)
                # self.textRecv.append(self.yqtool.timeNow() + " " + tcpreceive)
                # self.textRecv.update()
                protocol_dic = {
                    "511": "上锁", "512": "解锁", "513": "寻车", "514": "静音", "515": "点火",
                    "516": "熄火", "517": "关门窗", "518": "开门窗", "519": "关天窗", "51A": "开天窗",
                    "51B": "通油", "51C": "断油",
                }
                r = r'\(\*..\|7\|\d\d\w,\w*?,\w*?\|\)'
                datainfo = re.findall(r, tcpreceive)
                str_data = str(datainfo[0])
                print('recv:' + protocol_dic[str_data[7:10]] + str_data)
                a = str_data[0] + '1' + str_data[1:5] + '8' + str_data[6:]
                self.s.send(a.encode())
                self.send_signal.emit(a)

                b = a[0:6] + '7|4' + a[9:12] + '1,1|)'
                self.s.send(b.encode())
                self.send_signal.emit(b)
            elif tcpreceive == "":
                stopsingle = 1
                self.s.shutdown(2)
                self.s.close()
                self.onBtn.setText("上线")
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


class OtuMonitor(MainWidget):
    def __init__(self):
        super(OtuMonitor, self).__init__()
        self.sqlserver = Sqlfunticon()
        self.num = 0

    def otuSplice(self):
        for i in self.deleteWigt:
            i.deleteLater()
        self.OtuMonitor_UI()
        self.OtuMonitor_grid()
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
        self.labelBTIMEI = QLabel("蓝牙IMEI", self)
        self.labelInput = QLabel("自定义输入界面", self)
        self.labelSendHistory = QLabel("发送历史", self)
        self.labelRecive = QLabel("接收历史", self)

        self.entryPort = QLineEdit()
        self.entryPort.setMaximumWidth(50)
        self.entryIP = QLineEdit()
        self.entryOtuIMEI = QLineEdit()
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
        self.onBtn = QPushButton(u"上线")
        self.bindBtn = QPushButton(u"绑定")
        self.bindBtn.setDisabled(True)
        self.sendBtn = QPushButton(u"发送")
        self.sendBtn.setDisabled(True)
        self.clearBtn = QPushButton(u"清空")
        self.clearBtn2 = QPushButton(u"清空")
        self.clearBtn3 = QPushButton(u"清空")
        self.wg315Btn = QPushButton(u"315")
        self.wg315Btn.setDisabled(True)

        self.seleOtu = QRadioButton(u"otu")
        self.seleAudi = QRadioButton(u"audi")
        self.seleBuick = QRadioButton(u"buick")
        self.seleOtu.setChecked(True)

        self.heartcheck = QCheckBox("心跳挂机(保持连接请打钩√）")
        self.heartcheck.setVisible(False)

        self.textInput = QTextEdit()
        self.textSend = QTextBrowser()
        # self.textSend.setReadOnly(False) # 设置不可编辑
        self.textRecv = QTextBrowser()

        """中间窗口"""

        # self.btnnamelist = ["能力", "设防", "引擎", "门锁", "速度", "温度", "GSM", "星数"]
        self.protocol = {
            "能力": "(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100,000,000,000|)",
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
            "ACC": "(1*12|7|301,2,1111)",
            "余油614": "(1*ea|5|614,3,7#b312,1,32,32#|)",
            "余电614": "(1*ea|5|614,3,7#b313,1,32,32#|)",
            "余电31F": "(1*88|7|31F,1,32,0,0|)",
            "余油30A": "(1*88|7|30A,1,22|)",
            "里程614": "(1*ea|5|614,3,7#b311,9C4#|)",
            "里程313": "(1*10|7|313,1,10,1,552.0.0.0f39202a00,|)",
            "里程320": "(1*10|7|320,1,9C4|)",
            "里程614新": "(1*c1|5|614,3,7#b318,9C4#|)",
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
        self.Btn14 = QPushButton(u"ACC")

        self.Btn15 = QPushButton(u"余油614")
        self.Btn16 = QPushButton(u"余电614")
        self.Btn17 = QPushButton(u"余油30A")
        self.Btn18 = QPushButton(u"余电31F")
        self.Btn19 = QPushButton(u"里程614")
        self.Btn20 = QPushButton(u"里程313")
        self.Btn21 = QPushButton(u"里程614新")
        self.Btn22 = QPushButton(u"里程320")
        self.Btn23 = QPushButton(u"单程421")

        # stylesheet = "QPushButton{border-image: url('qrcode.png');}"
        # self.Btn22.setStyleSheet(stylesheet)

        self.btnlist = [self.Btn4, self.Btn5, self.Btn6, self.Btn7, self.Btn8,
                        self.Btn9, self.Btn10, self.Btn11, self.Btn12, self.Btn13, self.Btn14, self.Btn15, self.Btn16,
                        self.Btn17, self.Btn18, self.Btn19, self.Btn20, self.Btn21, self.Btn22]

        self.onBtn.clicked.connect(self.go_online)
        self.defalBtn.clicked.connect(self.siruisetDefalut)
        self.sendBtn.clicked.connect(self.sendTcpmsg)
        self.clearBtn.clicked.connect(lambda: self.clearinfo(1))
        self.clearBtn2.clicked.connect(lambda: self.clearinfo(2))
        self.clearBtn3.clicked.connect(lambda: self.clearinfo(3))
        self.Btn9.clicked.connect(self.sendEN)
        self.bindBtn.clicked.connect(self.bindBt)
        self.wg315Btn.clicked.connect(self.waiguadev)

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
        self.Btn23.clicked.connect(self.dancheng)
        # for i in self.btnlist:
        #     i.clicked.connect(lambda: self.btnclickevent(i))

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

    def OtuMonitor_grid(self):
        self.maingrid.setColumnStretch(0, 7)
        self.maingrid.setColumnStretch(1, 2)
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
        self.leftgrid.addWidget(self.entryOtuIMEI, 1, 1, 1, 8)
        self.leftgrid.addWidget(self.onBtn, 1, 9)

        self.leftgrid.addWidget(self.labelBTIMEI, 2, 0)
        self.leftgrid.addWidget(self.entryBTIMEI, 2, 1, 1, 3)
        self.leftgrid.addWidget(self.bindBtn, 2, 4)
        self.leftgrid.addWidget(self.entrywaiguadev, 2, 5, 1, 4)
        self.leftgrid.addWidget(self.wg315Btn, 2, 9)

        self.leftgrid.addWidget(self.labelInput, 3, 0, 1, 2)
        self.leftgrid.addWidget(self.heartcheck, 3, 3, QtCore.Qt.AlignCenter)
        self.leftgrid.addWidget(self.clearBtn, 3, 8)
        self.leftgrid.addWidget(self.sendBtn, 3, 9)
        self.leftgrid.addWidget(self.textInput, 4, 0, 1, 10)
        self.leftgrid.addWidget(self.labelSendHistory, 5, 0, 1, 7)
        self.leftgrid.addWidget(self.clearBtn2, 5, 9)
        self.leftgrid.addWidget(self.textSend, 6, 0, 1, 10)
        self.leftgrid.addWidget(self.labelRecive, 7, 0, 1, 4)
        self.leftgrid.addWidget(self.clearBtn3, 7, 9)
        self.leftgrid.addWidget(self.textRecv, 8, 0, 1, 10)

        # 中间窗体
        self.middlewiget = QWidget()
        self.middlegrid = QGridLayout()
        self.middlewiget.setLayout(self.middlegrid)
        self.maingrid.addWidget(self.middlewiget, 0, 1)

        self.middlegrid.addWidget(self.Btn1, 0, 0)
        self.middlegrid.addWidget(self.Btn2, 0, 1)
        self.middlegrid.addWidget(self.Btn3, 0, 2)
        self.middlegrid.addWidget(self.Btn4, 1, 0)
        self.middlegrid.addWidget(self.Btn5, 1, 1)
        self.middlegrid.addWidget(self.Btn6, 1, 2)
        self.middlegrid.addWidget(self.Btn7, 2, 0)
        self.middlegrid.addWidget(self.Btn8, 2, 1)
        self.middlegrid.addWidget(self.Btn9, 2, 2)
        self.middlegrid.addWidget(self.Btn10, 3, 0)
        self.middlegrid.addWidget(self.Btn11, 3, 1)
        self.middlegrid.addWidget(self.Btn12, 3, 2)
        self.middlegrid.addWidget(self.Btn13, 4, 0)
        self.middlegrid.addWidget(self.Btn14, 4, 1)
        self.middlegrid.addWidget(self.Btn15, 4, 2)
        self.middlegrid.addWidget(self.Btn16, 5, 0)
        self.middlegrid.addWidget(self.Btn17, 5, 1)
        self.middlegrid.addWidget(self.Btn18, 5, 2)
        self.middlegrid.addWidget(self.Btn19, 6, 0)
        self.middlegrid.addWidget(self.Btn20, 6, 1)
        self.middlegrid.addWidget(self.Btn21, 6, 2)
        self.middlegrid.addWidget(self.Btn22, 7, 0)
        self.middlegrid.addWidget(self.Btn23, 7, 1)

        self.middlegrid.addWidget(self.labelmsg, 11, 0)
        self.middlegrid.addWidget(self.entrymsg, 11, 1, 1, 2)
        self.middlegrid.addWidget(self.btnCreatqrcode, 12, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.middlegrid.addWidget(self.btnCreatqrcode2, 12, 0, 1, 3, QtCore.Qt.AlignRight)
        self.middlegrid.addWidget(self.labelqrode, 13, 0, 1, 3, QtCore.Qt.AlignCenter)

        # self.middlegrid.addWidget(self.btnCreatqrcode3, 12, 2)

    def siruisetDefalut(self):
        """默认按钮"""
        self.entryPort.setText("2103")
        self.entryIP.setText("192.168.6.52")
        self.entryHardver.setText("01022300")

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

    def bindBt(self):
        """蓝牙绑定"""
        Bt_IMEI = self.entryBTIMEI.text()
        sql = "SELECT mac FROM [sirui].[dbo].[Terminal] WHERE IMEI=\'" + Bt_IMEI + "\';"
        info = self.sqlserver.getinfo(sql)
        mac = str(info)[3:-4]

        msg = '(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac' + str(mac) + '_300,|)'
        self.s.send(msg.encode())
        self.textSend.append(self.yqtool.timeNow() + " " + msg)

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

    def go_online(self):
        """上线"""
        if self.onBtn.text() == "上线":
            otu_IMEI = self.entryOtuIMEI.text()
            tcpadress = self.entryIP.text()
            tcpport = self.entryPort.text()
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

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.s.connect((tcpadress, int(tcpport)))
            except Exception as msg:
                errorinfo = Exception, ":", msg
                appendinfo = errorinfo[2].strerror
                self.textRecv.append(appendinfo)
                return False

            self.scene.onlineCol.start()  # 上线动画

            # s.send('(1*7c|a3|106,201|101,' + str(
            #     IMEI_NUM[0]) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
            loginMsg = '(1*7c|a3|106,201|101,' + str(
                IMEI_NUM[0]) + '|102,460079241205511|104,otu.' + loginType + ',' + str(
                hardver) + '|105,a1,18|622,a1c2|)'

            self.s.send(loginMsg.encode())  # 商用去掉103
            self.textSend.setTextColor(QColor("#FF3030"))
            self.textSend.append(self.yqtool.timeNow() + " ")
            self.textSend.setTextColor(QColor("#FFFFFF"))
            self.textSend.insertPlainText(loginMsg)

            historydata = open('D:\Tcptemp\data.txt', "w")  # 生成缓存文件data
            historydata.write(otu_IMEI + "," + tcpadress + "," + tcpport + "," + hardver)  # IMEI保存到缓存文件data
            historydata.close()

            self.tcpth = TcpThread(self.s, self.onBtn, self.heartcheck, self.sendBtn, self.bindBtn, self.wg315Btn)
            self.tcpth.recv_signal.connect(self.fillrecvmsg)
            self.tcpth.send_signal.connect(self.fillsendmsg)
            self.tcpth.animate_signal.connect(self.scene.threadAnimate)
            self.tcpth.start()

            self.onBtn.setText("离线")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)
            self.bindBtn.setDisabled(False)
            self.wg315Btn.setDisabled(False)

        elif self.onBtn.text() == "离线":
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
        self.labelLat = QLabel(u"经度", self)
        self.entryLat = QLineEdit()
        self.entryLat.insert("106.49557015756179")
        self.labelLng = QLabel(u"纬度", self)
        self.entryLng = QLineEdit()
        self.entryLng.insert("29.61881556261095")
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
        self.labelvoltage = QLabel(u"电压", self)
        self.entryvoltage = QLineEdit()
        self.entryvoltage.insert("1200")
        self.labelAcceleration = QLabel(u"加速度\n最大差值", self)
        self.entryAcceleration = QLineEdit()
        self.entryAcceleration.insert("484")

        # 心跳box
        self.heartbeatbox = QGroupBox("心跳包")
        self.heartbeatboxGrid = QGridLayout()
        self.heartbeatbox.setLayout(self.heartbeatboxGrid)
        self.labelGSM = QLabel(u"GSM信号强度", self)
        self.sele1 = QRadioButton(u"无信号")
        self.sele2 = QRadioButton(u"极弱")
        self.sele3 = QRadioButton(u"较弱")
        self.sele4 = QRadioButton(u"良好")
        self.sele5 = QRadioButton(u"强")
        self.sele5.setChecked(True)
        self.heartbeatdataCreatebtn = QPushButton(u"生成")

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
        self.textSend = QTextBrowser()
        # self.textSend.setReadOnly(False) # 设置不可编辑
        self.textRecv = QTextBrowser()

        self.logindataCreatebtn.clicked.connect(self.logindatacreate)
        self.gpsdataCreatebtn.clicked.connect(self.gpsdatacreate)
        self.alarmdataCreatebtn.clicked.connect(self.alarmdatacreate)
        self.heartbeatdataCreatebtn.clicked.connect(self.heartbeatdatacreate)

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
        self.heartbeatboxGrid.addWidget(self.labelGSM, 0, 0)
        self.heartbeatboxGrid.addWidget(self.sele1, 0, 1)
        self.heartbeatboxGrid.addWidget(self.sele2, 0, 2)
        self.heartbeatboxGrid.addWidget(self.sele3, 0, 3)
        self.heartbeatboxGrid.addWidget(self.sele4, 0, 4)
        self.heartbeatboxGrid.addWidget(self.sele5, 0, 5)
        self.heartbeatboxGrid.addWidget(self.heartbeatdataCreatebtn, 0, 6)

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
        self.alarmboxGrid.addWidget(self.labelvoltage, 3, 0)
        self.alarmboxGrid.addWidget(self.entryvoltage, 3, 1)
        self.alarmboxGrid.addWidget(self.labelAcceleration, 4, 0)
        self.alarmboxGrid.addWidget(self.entryAcceleration, 4, 1)
        self.alarmboxGrid.addWidget(self.alarmdataCreatebtn, 4, 2)

        self.middlegrid.addWidget(self.labelmsg, 3, 0)
        self.middlegrid.addWidget(self.entrymsg, 3, 1, 1, 2)
        self.middlegrid.addWidget(self.btnCreatqrcode, 4, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.middlegrid.addWidget(self.btnCreatqrcode2, 4, 0, 1, 3, QtCore.Qt.AlignRight)
        self.middlegrid.addWidget(self.labelqrode, 5, 0, 1, 3, QtCore.Qt.AlignCenter)

    def bsjsetDefalut(self):
        """默认按钮"""
        self.entryPort.setText("2111")
        self.entryIP.setText("192.168.6.52")

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

        data = "78 78 22 22 " + self.yqtool.BSJhextime() + "c" + satelliteCount + " " + hexlng + " " + hexlat + " " + speed + " " + course + " 01 cc 00 28 7d 00 1f b8 01 01 00 00 03 80 81 0d 0a"
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

        voltage = self.entryvoltage.text()
        voltagedatahex = ('%x' % int(voltage)).zfill(4)
        voltagedata = voltagedatahex[0:2] + " " + voltagedatahex[-2:]

        acceleration = self.entryAcceleration.text()
        accelerationdatahex = ('%x' % int(acceleration)).zfill(8)
        accelerationdata = accelerationdatahex[0:2] + " " + accelerationdatahex[2:4] + " " + accelerationdatahex[
                                                                                             4:6] + " " + accelerationdatahex[
                                                                                                          -2:]

        data = "78 78 41 26 10 0B 0A 09 05 31 C5 02 6D DE C0 0C 3B FE E6 00 15 54 08 01 CC 00 26 2C 00 0E BA " + alarmdata + " EB 1B 05 01 00 00 00 AE 03 02 00 EB 05 03 " + accelerationdata + " 03 04 " + voltagedata + " 02 05 0E 03 06 FF FC 00 93 68 6F 0D 0A"
        self.textInput.insertPlainText(data)

    def heartbeatdatacreate(self):
        datahex = "not select"
        if self.sele1.isChecked():
            datahex = "00"
        elif self.sele2.isChecked():
            datahex = "01"
        elif self.sele3.isChecked():
            datahex = "02"
        elif self.sele4.isChecked():
            datahex = "03"
        elif self.sele5.isChecked():
            datahex = "04"
        else:
            pass

        data = "78 78 12 13 eb 0b " + datahex + " 04 04 f6 02 05 17 03 06 ff fb 00 6a 02 da 0d 0a"
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

            self.onBtn.setText("离线")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)

        elif self.onBtn.text() == "离线":
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
            self.s.send(self.dataSwitch('78 78 12 13 eb 0b 04 04 04 f6 02 05 17 03 06 ff fb 00 6a 02 da 0d 0a'))
            self.fillsendmsg("78 78 12 13 eb 0b 04 04 04 f6 02 05 17 03 06 ff fb 00 6a 02 da 0d 0a")
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

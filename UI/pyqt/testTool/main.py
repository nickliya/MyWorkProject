# coding=utf-8
# create by 401219180 2018/02/10

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
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


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.initUI()
        self.iniGrid()
        self.initmenu()
        # self.inittoolBar()
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
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle(u'桴之科测试工具')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.statusBar()
        self.setWindowIcon(QtGui.QIcon('ui/icon.ico'))
        # self.setWindowOpacity(0.9)

    def iniGrid(self):
        # 主窗体
        self.mainwidget = QWidget()
        self.mainwidget.setFont(QtGui.QFont("75 10pt Microsoft YaHei"))
        self.maingrid = QGridLayout()
        self.mainwidget.setLayout(self.maingrid)
        self.mainwidget.setObjectName("mainwidget")
        self.setCentralWidget(self.mainwidget)
        self.maingrid.setRowStretch(0, 0)


class TcpThread(QtCore.QThread):
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)

    def __init__(self, socketcp, onBtn, heartcheck, senBtn, bindBtn):
        super().__init__()
        self.s = socketcp
        self.yqtool = Bianlifunction()
        self.onBtn = onBtn
        self.heartcheck = heartcheck
        self.sendBtn = senBtn
        self.bindBtn = bindBtn

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
                self.heartcheck.setChecked(False)
                self.heartcheck.setVisible(False)
                self.sendBtn.setDisabled(True)
                self.bindBtn.setDisabled(True)
            else:
                self.recv_signal.emit(tcpreceive)
            if stopsingle == 1:
                break


class HeartThread(QtCore.QThread):
    recv_signal = QtCore.pyqtSignal(str)
    send_signal = QtCore.pyqtSignal(str)

    def __init__(self, socketcp, heartcheck):
        super().__init__()
        self.s = socketcp
        self.heartcheck = heartcheck

    def run(self):
        """心跳线程"""
        while self.heartcheck.isChecked():
            self.s.send('()'.encode())
            self.send_signal.emit("()")
            # self.textSend.append(self.yqtool.timeNow() + " ()")
            time.sleep(30)
            if not self.heartcheck.isChecked():
                print("停止")
                break


class OtuMonitor(MainWidget):
    def __init__(self):
        super(OtuMonitor, self).__init__()
        self.zu()
        self.sqlserver = Sqlfunticon()

    # def inittoolBar(self):
    #     toolbarAction = QAction(u'保单系统', self)
    #     toolbarAction.setStatusTip(u'生成保单系统的测试项')
    #     # toolbarAction.triggered.connect(self.zu)
    #
    #     toolbar = self.addToolBar("toolbar")
    #     toolbar.addAction(toolbarAction)

    def zu(self):
        self.OtuMonitor_UI()
        self.OtuMonitor_grid()

    def OtuMonitor_UI(self):
        # styleqss = open("otu.qss", "r", encoding='UTF-8')
        # styleinfo = styleqss.read()
        styleinfo = 'QMainWindow{}QWidget#mainwidget{background-color:#2F4F4F;}QLabel{font:75 10pt "Microsoft YaHei";color:floralwhite;}QPushButton{font:75 10pt "Microsoft YaHei";background-color:#FFFFFF;border:1px solid #8f8f91;border-radius:9px;min-width:50px;min-height:24px}QPushButton::hover{background-color:#FF6A6A;}QRadioButton{font:75 10pt "Microsoft YaHei";color:floralwhite;}QRadioButton::indicator{width:10px;height:10px;border-radius:5px;}QRadioButton::indicator:checked{background-color:#FFA07A;border:1px solid black;}QRadioButton::indicator:unchecked{background-color:white;border:1px solid black;}QCheckBox{font:75 10pt "Microsoft YaHei";color:floralwhite;background-color:#2F4F4F;}QTextEdit{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}QTextBrowser{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}'
        self.mainwidget.setStyleSheet(styleinfo)
        # styleqss.close()

        """左侧窗口"""
        self.labelPort = QLabel("端口", self)
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
        self.entryOtuIMEI = QLineEdit()
        self.entryBTIMEI = QLineEdit()

        data = open('D:\Tcptemp\data.txt', "r")
        historyinfo = data.read()  # 读取缓存文件data
        historyinfolist = historyinfo.split(",")

        self.entryOtuIMEI.insert(historyinfolist[0])
        data.close()
        if len(historyinfolist) == 3:
            self.entryPort.insert(historyinfolist[2])
        if len(historyinfolist) == 2 or len(historyinfolist) == 3:
            self.entryIP.insert(historyinfolist[1])

        self.defalBtn = QPushButton(u"默认")
        self.onBtn = QPushButton(u"上线")
        self.bindBtn = QPushButton(u"绑定")
        self.bindBtn.setDisabled(True)
        self.sendBtn = QPushButton(u"发送")
        self.sendBtn.setDisabled(True)
        self.clearBtn = QPushButton(u"清空")
        self.clearBtn2 = QPushButton(u"清空")
        self.clearBtn3 = QPushButton(u"清空")

        self.seleOtu = QRadioButton(u"otu")
        self.seleOtu.setFont(QtGui.QFont("dsa"))
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

        # stylesheet = "QPushButton{border-image: url('qrcode.png');}"
        # self.Btn22.setStyleSheet(stylesheet)

        self.btnlist = [self.Btn4, self.Btn5, self.Btn6, self.Btn7, self.Btn8,
                        self.Btn9, self.Btn10, self.Btn11, self.Btn12, self.Btn13, self.Btn14, self.Btn15, self.Btn16,
                        self.Btn17, self.Btn18, self.Btn19, self.Btn20, self.Btn21, self.Btn22]

        self.onBtn.clicked.connect(self.go_online)
        self.defalBtn.clicked.connect(self.setDefalut)
        self.sendBtn.clicked.connect(self.sendTcpmsg)
        self.clearBtn.clicked.connect(lambda: self.clearinfo(1))
        self.clearBtn2.clicked.connect(lambda: self.clearinfo(2))
        self.clearBtn3.clicked.connect(lambda: self.clearinfo(3))
        self.Btn9.clicked.connect(self.sendEN)
        self.bindBtn.clicked.connect(self.bindBt)
        self.heartcheck.stateChanged.connect(self.sendHeart)

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
        self.maingrid.setColumnStretch(0, 4)
        self.maingrid.setColumnStretch(1, 1)

        # 左边窗体
        self.lefwidget = QWidget()
        self.leftgrid = QGridLayout()
        self.lefwidget.setLayout(self.leftgrid)
        self.maingrid.addWidget(self.lefwidget, 0, 0)
        # self.leftgrid.setColumnStretch(0, 4)
        self.leftgrid.setRowStretch(4, 1)
        self.leftgrid.setRowStretch(6, 2)
        self.leftgrid.setRowStretch(8, 2)

        self.leftgrid.addWidget(self.labelPort, 0, 0)
        self.leftgrid.addWidget(self.entryPort, 0, 1)
        self.leftgrid.addWidget(self.labelIP, 0, 2)
        self.leftgrid.addWidget(self.entryIP, 0, 3)
        self.leftgrid.addWidget(self.seleOtu, 0, 4)
        self.leftgrid.addWidget(self.seleAudi, 0, 5)
        self.leftgrid.addWidget(self.seleBuick, 0, 6)
        self.leftgrid.addWidget(self.defalBtn, 0, 7)

        self.leftgrid.addWidget(self.labelOtuIMEI, 1, 0)
        self.leftgrid.addWidget(self.entryOtuIMEI, 1, 1, 1, 6)
        self.leftgrid.addWidget(self.onBtn, 1, 7)

        self.leftgrid.addWidget(self.labelBTIMEI, 2, 0)
        self.leftgrid.addWidget(self.entryBTIMEI, 2, 1, 1, 6)
        self.leftgrid.addWidget(self.bindBtn, 2, 7)
        self.leftgrid.addWidget(self.labelInput, 3, 0, 1, 2)
        self.leftgrid.addWidget(self.heartcheck, 3, 3, QtCore.Qt.AlignCenter)
        self.leftgrid.addWidget(self.clearBtn, 3, 6)
        self.leftgrid.addWidget(self.sendBtn, 3, 7)
        self.leftgrid.addWidget(self.textInput, 4, 0, 1, 8)
        self.leftgrid.addWidget(self.labelSendHistory, 5, 0, 1, 5)
        self.leftgrid.addWidget(self.clearBtn2, 5, 7)
        self.leftgrid.addWidget(self.textSend, 6, 0, 1, 8)
        self.leftgrid.addWidget(self.labelRecive, 7, 0, 1, 2)
        self.leftgrid.addWidget(self.clearBtn3, 7, 7)
        self.leftgrid.addWidget(self.textRecv, 8, 0, 1, 8)

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

        self.middlegrid.addWidget(self.labelmsg, 11, 0)
        self.middlegrid.addWidget(self.entrymsg, 11, 1, 1, 2)
        self.middlegrid.addWidget(self.btnCreatqrcode, 12, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.middlegrid.addWidget(self.btnCreatqrcode2, 12, 0, 1, 3, QtCore.Qt.AlignRight)
        self.middlegrid.addWidget(self.btnCreatqrcode2, 12, 0, 1, 3, QtCore.Qt.AlignRight)
        self.middlegrid.addWidget(self.labelqrode, 13, 0, 1, 3, QtCore.Qt.AlignCenter)

        # self.middlegrid.addWidget(self.btnCreatqrcode3, 12, 2)

    def setDefalut(self):
        self.entryPort.setText("2103")
        self.entryIP.setText("192.168.6.52")

    def clearinfo(self, clearindex):
        if clearindex == 1:
            self.textInput.clear()
        elif clearindex == 2:
            self.textSend.clear()
        elif clearindex == 3:
            self.textRecv.clear()
        else:
            pass

    def sendTcpmsg(self):
        msg = self.textInput.toPlainText()
        self.s.send(msg.encode())
        self.textSend.append(self.yqtool.timeNow() + " " + msg)
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
        mac = str(info)[4:-4]

        msg = '(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac' + str(mac) + '_300,|)'
        self.s.send(msg.encode())
        self.textSend.append(self.yqtool.timeNow() + " " + msg)

    def fillsendmsg(self, message):
        self.textSend.append(self.yqtool.timeNow() + " " + message)

    def fillrecvmsg(self, message):
        self.textRecv.append(self.yqtool.timeNow() + " " + message)

    def go_online(self):
        """上线"""
        if self.onBtn.text() == "上线":
            otu_IMEI = self.entryOtuIMEI.text()
            tcpadress = self.entryIP.text()
            tcpport = self.entryPort.text()
            r_blank = r'\d*\d'
            IMEI_NUM = re.findall(r_blank, otu_IMEI)
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
            # s.send('(1*7c|a3|106,201|101,' + str(
            #     IMEI_NUM[0]) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
            loginMsg = '(1*7c|a3|106,201|101,' + str(
                IMEI_NUM[0]) + '|102,460079241205511|104,otu.' + loginType + ',01022300|105,a1,18|622,a1c2|)'

            self.s.send(loginMsg.encode())  # 商用去掉103
            self.textSend.append(self.yqtool.timeNow() + " " + loginMsg)

            historydata = open('D:\Tcptemp\data.txt', "w")  # 生成缓存文件data
            historydata.write(otu_IMEI + "," + tcpadress + "," + tcpport)  # IMEI保存到缓存文件data
            historydata.close()

            self.tcpth = TcpThread(self.s, self.onBtn, self.heartcheck, self.sendBtn, self.bindBtn)
            self.tcpth.recv_signal.connect(self.fillrecvmsg)
            self.tcpth.send_signal.connect(self.fillsendmsg)
            self.tcpth.start()

            self.onBtn.setText("离线")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)
            self.bindBtn.setDisabled(False)
            # frame2_c1['state'] = NORMAL

        elif self.onBtn.text() == "离线":
            global stopsingle
            stopsingle = 1
            self.s.shutdown(2)
        else:
            pass

    def sendHeart(self):
        if self.heartcheck.isChecked():
            self.heartth = HeartThread(self.s, self.heartcheck)
            self.heartth.send_signal.connect(self.fillsendmsg)
            self.heartth.start()

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
                randomID = str(info)[4:-4]
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


class StartLoop(OtuMonitor):
    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    ex = StartLoop()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

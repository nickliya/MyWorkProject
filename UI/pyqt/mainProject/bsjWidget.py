# coding=utf-8
# create by 401219180 2018/02/10
from threadManager import *
from Animation import *

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from socket import *

import qrcode
import base64
import socket
import configparser


class BSJMonitor(QWidget):
    def __init__(self):
        super(BSJMonitor, self).__init__()
        self.sqlserver = Sqlfunticon()
        self.yqtool = Bianlifunction()
        self.num = 0
        self.BSJMonitor_UI()
        self.BSJMonitor_grid()
        self.threadpool = QThreadPool.globalInstance()
        self.threadpool.setMaxThreadCount(500)

    def BSJMonitor_UI(self):
        styleqss = open("./qss/bsjStyle.qss", "r", encoding='UTF-8')
        styleinfo = styleqss.read()
        # styleinfo = 'QLabel{font:75 10pt "Microsoft YaHei";color:floralwhite;}QPushButton{font:75 10pt "Microsoft YaHei";background-color:#FFFFFF;border:1px solid #8f8f91;border-radius:9px;min-width:50px;min-height:24px}QPushButton::hover{background-color:#FF6A6A;}QRadioButton{font:75 10pt "Microsoft YaHei";color:floralwhite;}QRadioButton::indicator{width:10px;height:10px;border-radius:5px;}QRadioButton::indicator:checked{background-color:#FFA07A;border:1px solid black;}QRadioButton::indicator:unchecked{background-color:white;border:1px solid black;}QCheckBox{font:75 10pt "Microsoft YaHei";color:floralwhite;background-color:rgba(255,255,255,0);}QTextEdit{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}QTextBrowser{color:floralwhite;font:75 10pt "Microsoft YaHei";background-color:rgba(255,25,25,0);border-color:#FFEBCD;border-width:1px;border-style:solid;}'
        self.setStyleSheet(styleinfo)
        styleqss.close()

        """左侧窗口"""
        # 登录box
        self.loginbox = QGroupBox("登录信息包")
        self.loginboxGrid = QGridLayout()
        self.loginbox.setLayout(self.loginboxGrid)
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

        self.labelPort = QLabel("端口", self)
        self.labelPort.setMaximumWidth(50)
        self.labelIP = QLabel("IP", self)
        self.labelIP.setMaximumWidth(20)

        self.labelOtuIMEI = QLabel(u"主机IMEI", self)
        self.labelInput = QLabel("自定义输入界面", self)
        self.labelSendHistory = QLabel("发送历史", self)
        self.labelRecive = QLabel("接收历史", self)

        self.entryPort = QLineEdit()
        self.entryPort.setMaximumWidth(50)
        self.entryIP = QLineEdit()

        self.entryBTIMEI = QLineEdit()

        try:
            conf = configparser.ConfigParser()
            conf.read('./Tcptemp/bsjdata.ini')  # 文件路径
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

        self.gpsUploadBtn = QPushButton(u"附件GPS上报")
        self.gpsUploadBtn.setStatusTip("附件放至./Tcptemp/dataUpLoad.xlsx")
        self.gpsUploadBtn.clicked.connect(self.gpsUploadfunBSJ)

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
        # bsj窗体
        self.bsjGrid = QGridLayout()
        self.setLayout(self.bsjGrid)

        self.bsjGrid.setColumnStretch(0, 7)
        self.bsjGrid.setColumnStretch(1, 2)
        # 左边窗体
        self.leftwidget = QWidget()
        self.leftgrid = QGridLayout()
        self.leftwidget.setLayout(self.leftgrid)
        self.bsjGrid.addWidget(self.leftwidget, 0, 0)

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
        self.leftgrid.addWidget(self.gpsUploadBtn, 5, 3, QtCore.Qt.AlignRight)
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
        self.bsjGrid.addWidget(self.middlewiget, 0, 1)

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
        conf.read('./Tcptemp/bsjdata.ini')
        try:
            conf.set("setting", "imei", imei)
        except configparser.NoSectionError:
            conf.add_section("setting")
            conf.set("setting", "imei", imei)
        with open('./Tcptemp/bsjdata.ini', 'w') as configfile:
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
        self.textSend.append(self.yqtool.time_sfm() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(msg)
        self.textInput.clear()

    def fillsendmsg(self, message):
        """填充发送历史"""
        self.textSend.setTextColor(QColor("#FF3030"))
        self.textSend.append(self.yqtool.time_sfm() + " ")
        self.textSend.setTextColor(QColor("#FFFFFF"))
        self.textSend.insertPlainText(message)

    def fillrecvmsg(self, message):
        """填充接收历史"""
        self.textRecv.setTextColor(QColor("#FF3030"))
        self.textRecv.append(self.yqtool.time_sfm() + " ")
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

            # self.scene.onlineCol.start()  # 上线动画

            # 缓存
            conf = configparser.ConfigParser()
            conf.read('./Tcptemp/bsjdata.ini')
            try:
                conf.set("setting", "ip", tcpadress)
                conf.set("setting", "port", tcpport)
            except configparser.NoSectionError:
                conf.add_section("setting")
                conf.set("setting", "ip", tcpadress)
                conf.set("setting", "port", tcpport)
            with open('./Tcptemp/bsjdata.ini', 'w') as configfile:
                conf.write(configfile)
                configfile.close()

            self.tcpth = BSJTcpThread(self.s, self.onBtn, self.heartcheck, self.sendBtn)
            self.tcpth.recv_signal.connect(self.fillrecvmsg)
            self.tcpth.send_signal.connect(self.fillsendmsg)
            # self.tcpth.animate_signal.connect(self.scene.threadAnimate)
            self.tcpth.start()

            self.onBtn.setText("断开")
            self.heartcheck.setVisible(True)
            self.sendBtn.setDisabled(False)

        elif self.onBtn.text() == "断开":
            # self.scene.offlineCol.start()
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
        img.save('./Tcptemp/qrcode.png')

        self.labelqrode.setPixmap(QtGui.QPixmap("./Tcptemp/qrcode.png"))

    def gpsUploadfunBSJ(self):
        dataUrl = './Tcptemp/dataUpLoad.xlsx'

        self.tcpth3 = DataThreadBSJ(dataUrl, self.s, self.gpsUploadBtn)
        self.tcpth3.signals.recv_signal.connect(self.fillrecvmsg)
        self.tcpth3.signals.send_signal.connect(self.fillsendmsg)
        #
        self.threadpool.start(self.tcpth3)
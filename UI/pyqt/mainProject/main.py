# /usr/bin/python
# coding=utf-8
# create by 401219180 2017/12/4

from SharedVehicle.flow import *
import sys
from PyQt4 import QtGui, QtCore
import os


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.iniGrid()
        self.initmenu()

    def showEvent(self, *args, **kwargs):
        isexisted = os.path.exists('D:\Tcptemp')
        if not isexisted:
            os.makedirs('D:\Tcptemp')
        else:
            pass
        data = open('D:\Tcptemp\mainData.txt', "a+")
        historyinfo = data.read()  # 读取缓存文件data
        historyinfolist = historyinfo.split(",")
        self.entryUser.insert(historyinfolist[0])
        self.entryPasswd.insert(historyinfolist[1])
        self.entryUrl.insert(historyinfolist[2])
        self.entryCustomerUser.insert(historyinfolist[3])
        self.entryCustomerPasswd.insert(historyinfolist[4])
        self.entryTcp.insert(historyinfolist[5])
        self.entryDatabases.insert(historyinfolist[6])

    def closeEvent(self, *args, **kwargs):
        userinfo = self.entryUser.text()
        passwdinfo = self.entryPasswd.text()
        urlinfo = self.entryUrl.text()
        csuserinfo = self.entryCustomerUser.text()
        cspasswdinfo = self.entryCustomerPasswd.text()
        tcpinfo = self.entryTcp.text()
        databaseinfo = self.entryDatabases.text()
        historydata = open('D:\Tcptemp\mainData.txt', "w")  # 生成缓存文件data
        historydata.write(userinfo + "," + passwdinfo + "," + urlinfo + "," + csuserinfo +
                          "," + cspasswdinfo + "," + tcpinfo + "," + databaseinfo)  # IMEI保存到缓存文件data
        historydata.close()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initmenu(self):
        menuAction = QtGui.QAction(QtGui.QIcon(u'思锐.png'), u'思锐', self)
        menuAction.setStatusTip('Exit application')
        # menuAction.triggered.connect(QtGui.qApp.quit)

        menuAction2 = QtGui.QAction(QtGui.QIcon(u'咪智汇.png'), u'咪智汇', self)
        menuAction2.setStatusTip('Exit application')
        # menuAction2.triggered.connect(QtGui.qApp.quit)

        menuAction3 = QtGui.QAction(QtGui.QIcon(u'皮皮车.png'), u'皮皮车', self)
        menuAction3.setStatusTip('Exit application')
        # menuAction3.triggered.connect(QtGui.qApp.quit)

        menuAction4 = QtGui.QAction(QtGui.QIcon(u'共享车快进.png'), u'共享车快进', self)
        menuAction4.setStatusTip('Exit application')
        # menuAction4.triggered.connect(QtGui.qApp.quit)

        menuAction5 = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        menuAction5.setShortcut(u'Ctrl+Q')
        menuAction5.setStatusTip('Exit application')
        menuAction5.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(menuAction)
        fileMenu.addAction(menuAction2)
        fileMenu.addAction(menuAction3)
        fileMenu.addAction(menuAction4)
        fileMenu.addAction(menuAction5)

    def inittoolBar(self):
        toolbarAction = QtGui.QAction(u'保单系统', self)
        toolbarAction.setStatusTip(u'生成保单系统的测试项')
        toolbarAction.triggered.connect(self.bdxtUI)

        toolbar = self.addToolBar("toolbar")
        toolbar.addAction(toolbarAction)

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle(u'桴之科测试工具')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.statusBar()

        styleqss = open("qss/style.qss", "r")
        styleinfo = styleqss.read()
        self.setStyleSheet(styleinfo)
        styleqss.close()

        # self.setWindowOpacity(0.9)

        self.labelUser = QtGui.QLabel("user", self)
        self.labelPasswd = QtGui.QLabel("passwd", self)
        self.labelUrl = QtGui.QLabel(u"域名", self)
        self.labelCustomerUser = QtGui.QLabel("customerUser", self)
        self.labelCustomerPasswd = QtGui.QLabel("customerPasswd", self)
        self.labelTcp = QtGui.QLabel("tcp", self)
        self.labelDatabases = QtGui.QLabel("postgresql", self)
        self.entryUser = QtGui.QLineEdit()
        self.entryPasswd = QtGui.QLineEdit()
        self.entryUrl = QtGui.QLineEdit()
        self.entryCustomerUser = QtGui.QLineEdit()
        self.entryCustomerPasswd = QtGui.QLineEdit()
        self.entryTcp = QtGui.QLineEdit()
        self.entryDatabases = QtGui.QLineEdit()

        self.startestbtn = QtGui.QPushButton(u"开始测试")
        self.startestbtn.clicked.connect(self.startTest)
        # self.startestbtn.setStyleSheet("border:none")

    def iniGrid(self):
        # 主窗体
        mainwidget = QtGui.QWidget()
        self.maingrid = QtGui.QGridLayout()
        mainwidget.setLayout(self.maingrid)
        mainwidget.setObjectName("mainwidget")
        self.setCentralWidget(mainwidget)
        self.maingrid.setRowStretch(0, 0)
        self.maingrid.setRowStretch(1, 1)

        # 顶部窗体
        self.topwiget = QtGui.QWidget()
        self.topgrid = QtGui.QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.maingrid.addWidget(self.topwiget, 0, 0)

        self.topgrid.addWidget(self.labelUser, 0, 0)
        self.topgrid.addWidget(self.entryUser, 0, 1)
        self.topgrid.addWidget(self.labelPasswd, 0, 2)
        self.topgrid.addWidget(self.entryPasswd, 0, 3)
        self.topgrid.addWidget(self.labelUrl, 1, 0)
        self.topgrid.addWidget(self.entryUrl, 1, 1)
        self.topgrid.addWidget(self.labelCustomerUser, 1, 2)
        self.topgrid.addWidget(self.entryCustomerUser, 1, 3)
        self.topgrid.addWidget(self.labelCustomerPasswd, 2, 0)
        self.topgrid.addWidget(self.entryCustomerPasswd, 2, 1)
        self.topgrid.addWidget(self.labelTcp, 2, 2)
        self.topgrid.addWidget(self.entryTcp, 2, 3)
        self.topgrid.addWidget(self.labelDatabases, 3, 0)
        self.topgrid.addWidget(self.entryDatabases, 3, 1)
        self.topgrid.addWidget(self.startestbtn, 3, 2)

        # 中间窗体
        self.bodywiget = QtGui.QWidget()
        self.bodygrid = QtGui.QGridLayout()
        self.bodywiget.setLayout(self.bodygrid)
        self.maingrid.addWidget(self.bodywiget, 1, 0)

        self.feecheckwiget()

    def feecheckwiget(self):
        self.radioBtn = QtGui.QRadioButton(u"小时计费")
        self.radioBtn2 = QtGui.QRadioButton(u"分钟计费")
        self.radioBtn3 = QtGui.QRadioButton(u"里程计费")
        self.radioBtn4 = QtGui.QRadioButton(u"分钟里程计费")
        self.bodygrid.addWidget(self.radioBtn, 1, 0)
        self.bodygrid.addWidget(self.radioBtn2, 2, 0)
        self.bodygrid.addWidget(self.radioBtn3, 3, 0)
        self.bodygrid.addWidget(self.radioBtn4, 4, 0)

        self.labelVimID = QtGui.QLabel("vmid", self)
        self.lableVehicleID = QtGui.QLabel("vehicleid", self)
        self.entryVimID = QtGui.QLineEdit()
        self.entryVehicleID = QtGui.QLineEdit()
        self.bodygrid.addWidget(self.labelVimID, 0, 0)
        self.bodygrid.addWidget(self.entryVimID, 0, 1)
        self.bodygrid.addWidget(self.lableVehicleID, 0, 2)
        self.bodygrid.addWidget(self.entryVehicleID, 0, 3)

    def startTest(self):
        cus = App()  # 调用app模块
        tcp = Tcp()  # 调用Tcp模块
        psql = Postgresql_db()  # 调用Postgresql模块
        web = Web(psql)  # 调用web模块
        sethost(self.entryUrl.text())  # 域名
        setinput(unicode(self.entryCustomerUser.text()), unicode(self.entryCustomerPasswd.text()))  # 初始化input1和input2
        logininfo = self.entryUser.text() + ";" + self.entryPasswd.text() + ";6666"
        web.sysuserlogin(logininfo)  # 保持门户登陆状态,依次是用户名,密码,验证码，不测门户或单测登陆接口时必须屏蔽
        web.configloging()
        tcp.settcp('192.168.6.52', '2103')  # 配置tcp
        psql.setsql('192.168.6.51', 5432, 'postgres', '123456', 'postgres')  # 配置postgresql数据库
        flow = Flow(cus, web, tcp, psql)  # 调用Flow模块

        vmid = self.entryVimID.text()
        vehicleid = self.entryVehicleID.text()
        if vmid == "" or vehicleid == "":
            print "请输入车型id和车辆id"
            return

        if self.radioBtn.isChecked():
            print "start hourfee test"
            flow.feecheck4(unicode(vmid) + ";" + unicode(vehicleid))
        if self.radioBtn2.isChecked():
            print "start minutefee test"
            flow.feecheck1(unicode(vmid) + ";" + unicode(vehicleid))
        if self.radioBtn3.isChecked():
            print "start milefee test"
            flow.feecheck2(unicode(vmid) + ";" + unicode(vehicleid))
        if self.radioBtn4.isChecked():
            print "start minute_Milefee test"
            flow.feecheck3(unicode(vmid) + ";" + unicode(vehicleid))


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

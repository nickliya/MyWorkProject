# coding=utf-8
# create by 401219180 2018/02/10

from Resource.otuWidget import *
from Resource.bsjWidget import *
import os
import cgitb
import sys

cgitb.enable(format='text')  # 解决pyqt5异常只要进入事件循环,程序就崩溃,而没有任何提示

stopsingle = None
waitmsg = None


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.mainwidget = MyView()  # 创建图形视图界面
        self.w1 = OtuMonitor(self.mainwidget)
        self.w2 = BSJMonitor(self.mainwidget)
        self.initUI()
        self.iniGrid()
        self.initmenu()
        self.inittoolBar()

        # 窗口透明度动画类
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(500)  # 持续时间0.5秒

    def showEvent(self, *args, **kwargs):
        self.doShow()

    def closeEvent(self, event):
        self.doClose()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def inittoolBar(self):
        toolbarAction = QAction(u'思锐OTU', self)
        toolbarAction.setStatusTip(u'老思锐平台项目')
        toolbarAction.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        toolbarAction2 = QAction(u'金融BSJ', self)
        toolbarAction2.setStatusTip(u'新金融项目BSJ设备模拟')
        toolbarAction2.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))

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
        menuAction5.triggered.connect(self.doClose)

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
        self.setWindowTitle(u'桴之科测试工具 Version:2019.01.25')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.statusBar()
        self.setWindowIcon(QtGui.QIcon('ui/icon.ico'))
        # self.setWindowOpacity(0.9)

        self.stackedWidget = QStackedWidget(self)
        # 公共空间
        # self.onBtn = QPushButton(u"连接")

    def iniGrid(self):
        # 主窗体
        # self.mainwidget = QGraphicsView()
        # self.scene = TcpBackgroudScene(self.mainwidget)  # 创建场景
        # self.mainwidget.setScene(self.scene)  # 添加场景

        self.mainwidget.setFont(QtGui.QFont("75 10pt Microsoft YaHei"))
        self.maingrid = QGridLayout()
        self.mainwidget.setLayout(self.maingrid)
        self.setCentralWidget(self.mainwidget)
        self.maingrid.setRowStretch(0, 0)
        self.maingrid.addWidget(self.stackedWidget, 0, 0)

        self.stackedWidget.addWidget(self.w1)
        self.stackedWidget.addWidget(self.w2)

    def doShow(self):
        try:
            # 尝试先取消动画完成后关闭窗口的信号
            self.animation.finished.disconnect(self.close)
        except:
            pass
        self.animation.stop()
        # 透明度范围从0逐渐增加到1
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def doClose(self):
        self.animation.stop()
        self.animation.finished.connect(self.close)  # 动画完成则关闭窗口
        # 透明度范围从1逐渐减少到0
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

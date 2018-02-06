# /usr/bin/python
# coding=utf-8
# create by 401219180 2017/10/26

import sys
from PyQt4 import QtGui, QtCore
import HTMLTestRunner
import unittest
import webAutotest.web_Sirui as Case


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.iniGrid()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startest(self):
        indexdic = {self.zxtb: "case1", self.rzck: "case2", self.bdxg: "case3", self.bdzf: "case4", self.yyck: "case5",
                    self.bl: "case6"}
        indexlist = [self.zxtb, self.rzck, self.bdxg, self.bdzf, self.yyck, self.bl]
        testunit = unittest.TestSuite()
        for i in indexlist:
            if i.isChecked():
                print indexdic[i] + "已选择"
                testunit.addTest(Case.Bdxt(indexdic[i]))
        HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result.html'
        fp = open(HtmlFile, "wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
        runner.run(testunit)

    def initUI(self):
        self.resize(400, 300)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.statusBar()
        # self.setWindowOpacity(0.9)

        menuAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        menuAction.setShortcut('Ctrl+Q')
        menuAction.setStatusTip('Exit application')
        menuAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(menuAction)

        toolbarAction = QtGui.QAction(u'保单系统', self)
        toolbarAction.setStatusTip(u'生成保单系统的测试项')
        toolbarAction.triggered.connect(self.bdxtUI)

        toolbar = self.addToolBar("toolbar")
        toolbar.addAction(toolbarAction)

        self.label_user = QtGui.QLabel("user", self)
        self.laber_passwd = QtGui.QLabel("passwd", self)
        self.entry_user = QtGui.QLineEdit()
        self.entry_passwd = QtGui.QLineEdit()

        self.startestbtn = QtGui.QPushButton(u"开始测试")
        self.startestbtn.clicked.connect(self.startest)
        # self.startestbtn.setStyleSheet("border:none")

    def iniGrid(self):
        # 主窗体
        mainwidget = QtGui.QWidget()
        self.maingrid = QtGui.QGridLayout()
        mainwidget.setLayout(self.maingrid)
        self.setCentralWidget(mainwidget)
        self.maingrid.setRowStretch(0, 1)
        self.maingrid.setRowStretch(1, 1)

        # 顶部窗体
        self.topwiget = QtGui.QWidget()
        self.topgrid = QtGui.QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.maingrid.addWidget(self.topwiget, 0, 0)

        self.topgrid.addWidget(self.label_user, 0, 0)
        self.topgrid.addWidget(self.laber_passwd, 0, 2)
        self.topgrid.addWidget(self.entry_user, 0, 1)
        self.topgrid.addWidget(self.entry_passwd, 0, 3)
        self.topgrid.addWidget(self.startestbtn, 1, 3)
        # 中间窗体
        self.bodywiget = QtGui.QWidget()
        self.bodygrid = QtGui.QGridLayout()
        self.bodywiget.setLayout(self.bodygrid)
        self.maingrid.addWidget(self.bodywiget, 1, 0)

        # self.topwiget.setStyleSheet("background-color:grey;")
        # read = open("./style.css","r")
        # fileinfo = read.read()
        # mainwidget.setStyleSheet(fileinfo)
        # self.topgrid.setRowStretch(1, 1)
        # self.grid.setColumnStretch()
        # self.bodywiget.setStyleSheet("background-color:blue;")

    def bdxtUI(self):
        self.zxtb = QtGui.QCheckBox(u"在线投保", self)
        self.rzck = QtGui.QCheckBox(u"保单日志查看", self)
        self.bdxg = QtGui.QCheckBox(u"保单修改", self)
        self.bdzf = QtGui.QCheckBox(u"保单作废", self)
        self.yyck = QtGui.QCheckBox(u"作废原因查看", self)
        self.bl = QtGui.QCheckBox(u"补录", self)
        self.rzck.setDisabled(True)
        self.bdxg.setDisabled(True)
        self.bdzf.setDisabled(True)
        self.yyck.setDisabled(True)
        self.bodygrid.addWidget(self.zxtb, 0, 0)
        self.bodygrid.addWidget(self.rzck, 0, 1)
        self.bodygrid.addWidget(self.bdxg, 0, 2)
        self.bodygrid.addWidget(self.bdzf, 1, 0)
        self.bodygrid.addWidget(self.yyck, 1, 1)
        self.bodygrid.addWidget(self.bl, 1, 2)
        self.zxtb.stateChanged.connect(self.changestate)

    def changestate(self):
        """多选框限制"""
        if self.zxtb.isChecked():
            self.rzck.setDisabled(False)
            self.bdxg.setDisabled(False)
            self.bdzf.setDisabled(False)
            self.yyck.setDisabled(False)
        else:
            self.rzck.setDisabled(True)
            self.bdxg.setDisabled(True)
            self.bdzf.setDisabled(True)
            self.yyck.setDisabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

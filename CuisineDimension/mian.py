# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CuisineDimension'
#
# Created by: 401219180
#
# WARNING! All changes made in this file will be lost!
#
# vervion:2017.11.03

from PyQt4 import QtCore, QtGui
import sys


class Example(QtGui.QWidget):
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

    def initUI(self):
        self.btn = QtGui.QPushButton(u"队伍")
        self.btn = QtGui.QPushButton(u"食灵")
        self.btn = QtGui.QPushButton(u"装备")
        self.btn = QtGui.QPushButton(u"改修工程")
        self.btn = QtGui.QPushButton(u"声优")
        self.btn = QtGui.QPushButton(u"伤害计算")
        self.btn = QtGui.QPushButton(u"关于")

        # self.startestbtn.clicked.connect(self.startest)

    def iniGrid(self):
        self.maingrid = QtGui.QGridLayout()
        self.setLayout(self.maingrid)
        # self.setCentralWidget(mainwidget)
        self.maingrid.setRowStretch(0, 1)
        self.maingrid.setRowStretch(1, 1)

        # 顶部窗体
        self.topwiget = QtGui.QWidget()
        self.topgrid = QtGui.QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.addWidget(self.topwiget, 0, 0)

        self.topgrid.addWidget(self.label_user, 0, 0)
        self.topgrid.addWidget(self.laber_passwd, 0, 2)
        self.topgrid.addWidget(self.entry_user, 0, 1)
        self.topgrid.addWidget(self.entry_passwd, 0, 3)
        self.topgrid.addWidget(self.startestbtn, 1, 3)

        # 中间窗体
        self.bodywiget = QtGui.QWidget()
        self.bodygrid = QtGui.QGridLayout()
        self.bodywiget.setLayout(self.bodygrid)
        self.addWidget(self.bodywiget, 1, 0)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

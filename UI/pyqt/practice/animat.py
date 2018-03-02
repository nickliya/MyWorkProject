# -*- coding:utf8 -*-
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import random
import base64
import os
import cgitb
import sys

cgitb.enable(format='text')


class MyLabel(QLabel):

    def __init__(self, text):
        super().__init__(text)

    def _set_color(self, col):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), col)
        self.setPalette(palette)

    color = pyqtProperty(QColor, fset=_set_color)


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.iniGrid()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.resize(600, 400)
        self.center()
        self.setWindowTitle(u'りりこの料理教室 version:2017.11.30')
        self.setObjectName("mainwindow")
        self.mainwidget = QWidget()
        self.mainwidget.setObjectName("mainWidget")

        self.setWindowOpacity(0.96)

        self.groupbtn = QPushButton(u"首页")
        self.groupbtn.setObjectName("headbtn")

        self.charactorbtn = QPushButton(u"食灵")
        self.charactorbtn.setObjectName("headbtn")
        self.charactorbtn.setMinimumHeight(50)
        self.charactorbtn.installEventFilter(self)

        self.bglabel = MyLabel("123456")

        self.bglabel.setStyleSheet("background-color:rgba(255,50,50,50)")
        self.bglabel.setObjectName("testlabel")

        # self.groupbtn.clicked.connect(self.fortest)
        self.charactorbtn.clicked.connect(self.fortest)
        self.charactorbtn.setFocus()

    def iniGrid(self):
        # mainwindow架构
        self.maingrid = QGridLayout()
        self.mainwidget.setLayout(self.maingrid)
        self.setCentralWidget(self.mainwidget)
        # self.maingrid.setRowStretch(1, 1)
        self.maingrid.setColumnStretch(0, 1)

        self.topwiget = QWidget()
        self.topgrid = QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.maingrid.addWidget(self.topwiget, 0, 0)
        #
        # self.topgrid.addWidget(self.groupbtn, 0, 0)

        self.wigdh = QWidget()
        # self.wigdh.setStyleSheet("QWidget{background-color:#2F4F4F}")

        self.topgrid.addWidget(self.charactorbtn, 0, 0)
        self.topgrid.addWidget(self.bglabel, 1, 0)
        self.topgrid.addWidget(self.groupbtn, 2, 0)

    def fortest(self):
        self.animate = QPropertyAnimation(self.bglabel, b"geometry")
        self.animate.setDuration(3000)
        print(self.charactorbtn.geometry())
        self.animate.setStartValue(QRect(9, 9, 564, 23))
        self.animate.setKeyValueAt(0.5, QRect(100, 9, 122, 156))
        self.animate.setEndValue(QRect(9, 300, 564, 23))
        self.animate.setEasingCurve(QtCore.QEasingCurve.CosineCurve)
        # self.animate.setKeyValueAt(1, 255)
        # self.animate.setLoopCount(-1)
        self.animate2 = QPropertyAnimation(self.bglabel, b"color")
        self.animate2.setDuration(1000)
        self.animate2.setLoopCount(3)
        self.animate2.setStartValue(QColor(30, 20, 30))
        self.animate2.setKeyValueAt(0.5, QColor(255, 0, 0))
        self.animate2.setEndValue(QColor(220, 200, 200))

        self.animate.start()
        self.animate2.start()

    # def eventFilter(self, object, event):
    #     if event.type() == QtCore.QEvent.MouseButtonPress:
    #         print "You pressed the button"
    #         return True
    # 
    #     elif event.type() == QtCore.QEvent.HoverMove:
    #         print "C'mon! CLick-meeee!!!"
    #         return True


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

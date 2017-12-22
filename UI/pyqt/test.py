# -*- coding:utf-8 -*-
#######pyqt绘制点，线，矩形，圆
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from random import *


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(680, 480)
        self.iniUI()

    def iniUI(self):
        self.w1 = QWidget()
        self.w2 = QWidget()
        self.w1.setStyleSheet("background-color: rgba(255,0,0,50)")
        self.w2.setStyleSheet("background-color: rgba(255,0,0,50)")

        self.l1 = QLabel("1",self)
        self.l2 = QLabel("2")
        self.l3 = QLabel("3")
        self.l4 = QLabel("4")
        self.l5 = QLabel("5")
        self.l6 = QLabel("6")
        self.l7 = QLabel("7")
        self.l8 = QLabel("8")
        self.l9 = QLabel("9")
        self.l10 = QLabel("10")
        self.l11 = QLabel("11")
        self.l12 = QLabel("12")
        self.l13 = QLabel("13")

        qss = "QLabel{background-color: rgba(255,0,0,50);border-radius:40px}"
        self.setStyleSheet(qss)
        self.mainGrid = QGridLayout()
        self.setLayout(self.mainGrid)
        self.mainGrid.addWidget(self.w1,0,0)
        self.mainGrid.addWidget(self.w2,0,1)
        # self.mainGrid.addWidget(self.l3,1,2)
        # self.mainGrid.addWidget(self.l4,2,1)
        # self.mainGrid.addWidget(self.l5,2,3)
        # self.mainGrid.addWidget(self.l6,3,0)
        # self.mainGrid.addWidget(self.l7,3,2)
        # self.mainGrid.addWidget(self.l8,3,4)
        # self.mainGrid.addWidget(self.l9,4,1)
        # self.mainGrid.addWidget(self.l10,4,3)
        # self.mainGrid.addWidget(self.l11,5,2)
        # self.mainGrid.addWidget(self.l12,6,1)
        # self.mainGrid.addWidget(self.l13,6,3)

        print self.geometry()
        print self.w1.pos()
        print self.w2.pos()
        print self.w2.frameGeometry()
        # self.size().width()
        # self.size().height()
        self.l1.setGeometry(self.width()/2-40, self.height()/2-40, 80, 80)
        # print self.l1.geometry()
        # self.l2.move(200, 200)
        # self.l3.move(200, 200)
        # self.l4.move(200, 200)
        # self.l5.move(200, 200)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: semishigure
Website: zetcode.com
Last edited: 2018.03.01
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import cgitb
import sys

cgitb.enable(format='text')  # 解决pyqt5异常只要进入事件循环,程序就崩溃,而没有任何提示


class Ball(QObject):

    def __init__(self):
        super().__init__()
        # self.pixmap_item = QGraphicsPixmapItem(QPixmap("ball.png"))
        path = QPainterPath()
        path.moveTo(30, 30)
        path.cubicTo(30, 30, 40, 120, 130, 130)

        self.pixmap_item = QGraphicsPathItem(path)
        self.pixmap_item.setBrush(QColor(122, 163, 39))

        # self.transform = QTransform()
        # self.transform.rotate(45.0)
        # self.transform.translate(-50, -5)

        # self.pixmap_item.setTransform(self.transform)

        self._set_pos(QPointF(5, 30))

    def _set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Myview(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._set_color(QColor(105, 105, 105))
        self.iniAnimation()

    def _set_color(self, col):
        self.palette = QPalette()
        # self.palette.setColor(self.backgroundRole(), col)
        self.palette.setBrush(self.backgroundRole(), col)
        self.setPalette(self.palette)

    def iniAnimation(self):
        self.anim2 = QPropertyAnimation(self, b'color')
        self.anim2.setDuration(1000)
        self.anim2.setStartValue(QColor(105, 105, 105))
        self.anim2.setKeyValueAt(0.1, QColor(255, 255, 240))
        self.anim2.setKeyValueAt(0.3, QColor(219, 225, 171))
        self.anim2.setKeyValueAt(0.7, QColor(148, 214, 184))
        self.anim2.setEndValue(QColor(86, 199, 170))

    color = pyqtProperty(QColor, fset=_set_color)


class Example(Myview):

    def __init__(self):
        super().__init__()

        self.initView()
        self.iniui()

    def initView(self):
        self.ball = Ball()

        self.anim = QPropertyAnimation(self.ball, b'pos')
        self.anim.setDuration(1000)
        self.anim.setStartValue(QPointF(5, 30))

        self.anim.setKeyValueAt(0.3, QPointF(80, 30))
        self.anim.setKeyValueAt(0.5, QPointF(200, 30))
        self.anim.setKeyValueAt(0.8, QPointF(250, 250))
        self.anim.setEndValue(QPointF(290, 30))
        # self.anim.start()

        # self.linearGradient = QLinearGradient(100, 100, 200, 200)
        # self.linearGradient.setColorAt(0.2,QColor(255, 255, 240))
        # self.linearGradient.setColorAt(0.6,QColor(255, 0, 0))
        # self.linearGradient.setColorAt(1.0,QColor(255, 255, 0))
        # self._set_color(self.linearGradient)

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 300, 300)
        self.scene.addItem(self.ball.pixmap_item)
        self.setScene(self.scene)

        self.setWindowTitle("Ball animation")
        self.setRenderHint(QPainter.Antialiasing)
        self.setGeometry(300, 300, 500, 350)
        self.show()

    def iniui(self):
        self.btn = QPushButton("开始")
        self.btn2 = QPushButton("结束")
        self.maingrid = QGridLayout()
        self.setLayout(self.maingrid)
        self.maingrid.addWidget(self.btn, 0, 0)
        self.maingrid.addWidget(self.btn2, 0, 1)
        self.btn.clicked.connect(self.runAnim)

    def runAnim(self):
        self.anim.start()
        self.anim2.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

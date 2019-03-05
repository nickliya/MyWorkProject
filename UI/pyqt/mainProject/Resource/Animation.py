# coding=utf-8
# create by 401219180 2018/02/10

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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


class MyView(QGraphicsView):
    """自定义2d界面"""

    def __init__(self):
        super().__init__()
        self.scene = TcpBackgroudScene(self)  # 创建场景
        self.setScene(self.scene)  # 添加场景()

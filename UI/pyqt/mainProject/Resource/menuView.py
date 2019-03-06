#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2019/3/5 15:55 
@Author : yangqing
@contact: 401219180@qq.com
@File : menuView.py 
@Software: PyCharm
@Version: 1.0.0
@Desc:
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AboutView(QDialog):
    def __init__(self):
        super(AboutView, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉 标题和右上角
        # self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint)  # 去掉右上角

        self.resize(400, 300)

        self.init_UI()
        self.ini_grid()

    def init_UI(self):
        styleqss = open("qss/menuViewStyle.qss", "r", encoding='UTF-8')
        styleinfo = styleqss.read()
        styleqss.close()
        self.setStyleSheet(styleinfo)

        self.iconLabel = QLabel("")
        pix = QPixmap('./Resource/Images/hua.ico')
        self.iconLabel.setPixmap(pix)
        self.iconLabel.setMaximumSize(50, 50)
        self.iconLabel.setScaledContents(True)  # 设置拉伸扩展

        self.versionLabel = QLabel("   otumonitor v2.0.1   (32-bit)")
        self.authurLabel = QLabel("Author: ")
        self.authurLabel2 = QLabel("yangqing")
        self.contactLabel = QLabel("Contact: ")
        self.contactLabel2 = QLabel("401219180@qq.com")
        self.updateLogbox = QGroupBox("更新日志")
        self.okbtn = QPushButton("ok")
        self.okbtn.clicked.connect(self.close)
        self.logBrowser = QTextBrowser()

        logfile = open('Resource/Data/updatalog', 'r', encoding='utf-8')
        log = logfile.read()

        self.logBrowser.setText(log)
        self.logBrowser.setReadOnly(True)

    def ini_grid(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.iconLabel, 0, 0)
        self.grid.addWidget(self.versionLabel, 0, 1)
        self.grid.addWidget(self.authurLabel, 1, 0)
        self.grid.addWidget(self.authurLabel2, 1, 1)
        self.grid.addWidget(self.contactLabel, 2, 0)
        self.grid.addWidget(self.contactLabel2, 2, 1)
        self.grid.addWidget(self.updateLogbox, 3, 0, 1, 2)
        self.grid.addWidget(self.okbtn, 4, 0, 1, 2)

        self.updateLogboxGrid = QGridLayout()
        self.updateLogbox.setLayout(self.updateLogboxGrid)
        self.updateLogboxGrid.addWidget(self.logBrowser, 0, 0)

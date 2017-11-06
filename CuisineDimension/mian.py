# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CuisineDimension'
#
# Created by: 401219180
#
# WARNING! All changes made in this file will be lost!
#
# vervion:2017.11.03

from PyQt4 import QtGui,QtCore
import sys
import sqlite3


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.iniGrid()
        self.wigetIndex = None

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.resize(800, 600)
        self.center()
        self.setWindowTitle(u'次元料理 version:2017.11.03')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        # self.setWindowOpacity(0.9)

        self.groupbtn = QtGui.QPushButton(u"队伍")
        self.charactorbtn = QtGui.QPushButton(u"食灵")
        self.equipbtn = QtGui.QPushButton(u"装备")
        self.projectbtn = QtGui.QPushButton(u"改修工程")
        self.cvbtn = QtGui.QPushButton(u"声优")
        self.damagebtn = QtGui.QPushButton(u"伤害计算")
        self.aboutbtn = QtGui.QPushButton(u"关于")

        self.charactorbtn.clicked.connect(self.cuisinelist)
        self.aboutbtn.clicked.connect(self.aboutinfo)

    def iniGrid(self):
        self.maingrid = QtGui.QGridLayout()
        self.setLayout(self.maingrid)
        # self.setCentralWidget(mainwidget)
        # self.maingrid.setRowStretch(0, 1)
        self.maingrid.setRowStretch(1, 1)

        # 顶部窗体
        self.topwiget = QtGui.QWidget()
        self.topgrid = QtGui.QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.maingrid.addWidget(self.topwiget, 0, 0)

        self.topgrid.addWidget(self.groupbtn, 0, 0)
        self.topgrid.addWidget(self.charactorbtn, 0, 2)
        self.topgrid.addWidget(self.equipbtn, 0, 1)
        self.topgrid.addWidget(self.projectbtn, 0, 3)
        self.topgrid.addWidget(self.cvbtn, 0, 4)
        self.topgrid.addWidget(self.damagebtn, 0, 5)
        self.topgrid.addWidget(self.aboutbtn, 0, 6)

        # 中间窗体
        self.bodywiget = QtGui.QTableWidget()
        self.bodygrid = QtGui.QGridLayout()
        self.bodywiget.setLayout(self.bodygrid)
        self.maingrid.addWidget(self.bodywiget, 1, 0)

    def inibodywiget(self):
        """初始化body"""
        if self.wigetIndex is None:
            pass
        else:
            for i in self.wigetIndex:
                i.deleteLater()

    def cuisinelist(self):
        self.inibodywiget()
        self.tablewiget = QtGui.QTableWidget(100,13)
        self.bodygrid.addWidget(self.tablewiget, 0, 0)
        # self.tablewiget.verticalHeader().setVisible(False)
        # self.tablewiget.horizontalHeader().setVisible(False)
        self.tablewiget.setHorizontalHeaderLabels([u"index", u"No", u"食灵", u"类型", u"生命", u"攻击", u"防御", u"命中", u"闪避",
                                                   u"暴击", u"攻速", u"石油", u"魔力"])
        self.lbp = QtGui.QLabel()
        self.lbp.setPixmap(QtGui.QPixmap("bmf_n.png"))
        self.tablewiget.setCellWidget(0, 0, self.lbp)
        self.tablewiget.resizeRowToContents(2)
        self.tablewiget.resizeColumnsToContents()
        con = sqlite3.connect("llcy")
        cur = con.cursor()
        sql='SELECT SL_NO,SL_NAME,SL_TYPE,SL_HP,SL_GJ,SL_FY,SL_MZ,SL_SB,SL_BJ,SL_GS,SL_SY,SL_ML FROM "fairy_detail";'
        # sql='SELECT * FROM "fairy_info";'
        cur.execute(sql)
        a = cur.fetchall()
        nub = 1
        for i in a[0]:
            print i
            if type(i) == int:
                info = str(i)
            else:
                info = i
            newItem = QtGui.QTableWidgetItem(info)
            newItem.setTextAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignHCenter)
            self.tablewiget.setItem(0, nub, newItem)
            nub += 1

        self.wigetIndex = [self.tablewiget]

    def aboutinfo(self):
        self.inibodywiget()
        self.lablewiget = QtGui.QLineEdit("dsadas")
        self.bodygrid.addWidget(self.lablewiget, 0, 0)
        self.bodygrid.update()
        self.wigetIndex = [self.lablewiget]


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

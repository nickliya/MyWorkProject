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


class Example(QtGui.QMainWindow):
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
        self.resize(1280, 650)
        self.center()
        self.setWindowTitle(u'次元料理 version:2017.11.03')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        styleqss = open("qss/style.qss", "r")
        styleinfo = styleqss.read()
        self.setStyleSheet(styleinfo)
        styleqss.close()

        # self.setAttribute()
        # palette1 = QtGui.QPalette()
        # # palette1.setColor(self.backgroundRole(), QtGui.QColor(50, 50, 50, 80))  # 设置背景颜色
        # palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('ui/btn_add.png')))   # 设置背景图片
        # self.setPalette(palette1)

        self.setWindowOpacity(0.96)

        self.groupbtn = QtGui.QPushButton(u"首页")
        self.charactorbtn = QtGui.QPushButton(u"食灵")
        self.equipbtn = QtGui.QPushButton(u"装备")
        self.projectbtn = QtGui.QPushButton(u"装盘模拟")
        self.cvbtn = QtGui.QPushButton(u"声优")
        self.damagebtn = QtGui.QPushButton(u"伤害计算")
        self.aboutbtn = QtGui.QPushButton(u"关于")

        self.bglabel = QtGui.QLabel()

        self.charactorbtn.clicked.connect(self.cuisinelist)
        self.equipbtn.clicked.connect(self.equiplist)
        self.aboutbtn.clicked.connect(self.aboutinfo)

    def iniGrid(self):
        # self.maingrid = QtGui.QGridLayout()
        # self.setLayout(self.maingrid)
        # self.maingrid.setRowStretch(1, 1)

        # mainwindow架构
        mainwidget = QtGui.QWidget()
        self.maingrid = QtGui.QGridLayout()
        mainwidget.setLayout(self.maingrid)
        self.setCentralWidget(mainwidget)
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
        self.bodywiget = QtGui.QWidget()
        self.bodygrid = QtGui.QGridLayout()
        self.bodywiget.setLayout(self.bodygrid)
        self.maingrid.addWidget(self.bodywiget, 1, 0)

        # self.bodygrid.setRowStretch(0, 1)
        self.bodygrid.setColumnStretch(0, 1)
        self.bodywiget.setWindowOpacity(1)

    def inibodywiget(self):
        """初始化body"""
        if self.wigetIndex is None:
            pass
        else:
            for i in self.wigetIndex:
                i.deleteLater()

    def cuisinelist(self):
        self.inibodywiget()
        self.tablewiget = QtGui.QTableWidget(100, 13)
        self.bodygrid.addWidget(self.tablewiget, 0, 0)
        # self.tablewiget.verticalHeader().setVisible(False)
        # self.tablewiget.horizontalHeader().setVisible(False)
        self.tablewiget.setHorizontalHeaderLabels([u"index", u"No", u"食灵", u"类型", u"生命", u"攻击", u"防御", u"命中", u"闪避",
                                                   u"暴击", u"攻速", u"石油", u"魔力"])

        for x in range(self.tablewiget.columnCount()):
            headItem = self.tablewiget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            headItem.setBackgroundColor(QtGui.QColor(0, 60, 10))  # 设置单元格背景颜色
            headItem.setTextColor(QtGui.QColor(200, 111, 30))

            # self.tablewiget.setShowGrid(False)  # 设置网格线

        self.lbp = QtGui.QLabel()
        self.lbp.setPixmap(QtGui.QPixmap("bmf_n.png"))
        self.tablewiget.setCellWidget(0, 0, self.lbp)

        # self.tablewiget.horizontalHeader().setStretchLastSection(True)
        # self.tablewiget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tablewiget.verticalHeader().setStretchLastSection(True)
        self.tablewiget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # self.tablewiget.resizeRowsToContents()
        # self.tablewiget.resizeColumnsToContents()
        # self.tablewiget.columnResized(1,1,1)
        # self.tablewiget.rowResized(1,1,1)

        self.tablewiget.setColumnWidth(0, 200)
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
        # self.tablewiget.cellClicked.connect(self.fortest)

    def equiplist(self):
        self.inibodywiget()
        self.tablewiget = QtGui.QTableWidget(20,6)
        self.bodygrid.addWidget(self.tablewiget, 0, 0)
        self.tablewiget2 = QtGui.QTableWidget(20,5)
        self.bodygrid.addWidget(self.tablewiget2, 1, 0)
        # self.tablewiget.verticalHeader().setVisible(False)
        # self.tablewiget.horizontalHeader().setVisible(False)
        self.tablewiget.setHorizontalHeaderLabels([u"No", u"名称", u"种类", u"品质", u"基础属性1", u"基础属性2"])
        self.tablewiget2.setHorizontalHeaderLabels([u"No", u"名称", u"套装属性1", u"套装属性2", u"套装属性3"])
        self.wigetIndex = [self.tablewiget, self.tablewiget2]

    def aboutinfo(self):
        self.inibodywiget()

        # 设置左右框架
        self.leftwiget=QtGui.QWidget()
        self.rightwiget=QtGui.QWidget()
        self.bodygrid.addWidget(self.leftwiget, 0, 0)
        self.bodygrid.addWidget(self.rightwiget, 0, 1)
        self.leftgrid = QtGui.QGridLayout()
        self.rightgrid = QtGui.QGridLayout()
        self.leftwiget.setLayout(self.leftgrid)
        self.rightwiget.setLayout(self.rightgrid)

        # 左框架
        self.infolaber = QtGui.QLabel(u"更新历史")
        self.leftgrid.addWidget(self.infolaber, 0, 0)
        self.infolaber.setObjectName("aboutName")

        self.tree = QtGui.QTreeWidget()
        # self.tree.setHeaderLabel(u"更新历史")
        self.tree.headerItem().setBackgroundColor(0, QtGui.QColor(255, 0, 0))
        self.tree.setHeaderHidden(True)
        self.leftgrid.addWidget(self.tree, 1, 0)

        # 设置root为self.tree的子树，所以root就是跟节点  
        root = QtGui.QTreeWidgetItem(self.tree)
        # 设置根节点的名称  
        root.setText(0, 'Version:1.0.0')

        # 为root节点设置子结点  
        child1 = QtGui.QTreeWidgetItem(root)
        child1.setText(0, u'新增食灵、装备功能\n2017.11.07XXXX工具诞生啦!')
        # child4 = QtGui.QTreeWidgetItem(child3)
        # child4.setText(0, 'child4')
        # child4.setText(1, 'name4')

        # 右框架

        self.text=QtGui.QTextBrowser()
        html = open("view/aboutView.html","r")
        htmlinfo = html.read()
        html.close()
        self.text.setHtml(htmlinfo.decode("utf-8"))
        self.text.setAlignment(QtCore.Qt.AlignHCenter)
        self.rightgrid.addWidget(self.text, 0, 0)

        palette1 = QtGui.QPalette()
        # palette1.setColor(self.backgroundRole(), QtGui.QColor(50, 50, 50, 80))  # 设置背景颜色
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('ui/btn_add.png')))   # 设置背景图片
        self.text.setPalette(palette1)

        self.wigetIndex = [self.leftwiget, self.rightwiget]

    def fortest(self):
        a = self.tablewiget.show()
        print a


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

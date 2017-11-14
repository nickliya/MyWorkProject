# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CuisineDimension'
#
# Created by: 401219180
#
# WARNING! All changes made in this file will be lost!
#
# vervion:2017.11.03

from PyQt4 import QtGui, QtCore
import sys
import sqlite3
import random


class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.iniGrid()
        self.wigetIndex = None
        self.ToolFun = ToolFunction()

    def center(self):
        """控件居中"""
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.resize(1180, 650)
        self.center()
        self.setWindowTitle(u'次元料理 version:2017.11.03')
        self.setWindowIcon(QtGui.QIcon('web.png'))
        self.setObjectName("mainwindow")
        bgList = ["bg/homeskin/home_1.png", "bg/homeskin/home_2.png", "bg/homeskin/home_main.png"]
        bg = random.choice(bgList)

        styleqss = open("qss/gameskin.qss", "r")
        styleinfo = styleqss.read()
        self.setStyleSheet(styleinfo)
        styleqss.close()

        # palette添加背景
        # self.setAutoFillBackground(True)
        # palette1 = QtGui.QPalette()
        # # palette1.setColor(self.backgroundRole(), QtGui.QColor(50, 50, 50, 80))  # 设置背景颜色
        # pix = QtGui.QPixmap('ui/homeskin/home_1.png')
        # pix = pix.scaled(self.width(), self.height()).scaled(QtCore.Qt.IgnoreAspectRatio)
        # palette1.setBrush(self.backgroundRole(), QtGui.QBrush(pix))   # 设置背景图片
        # self.setPalette(palette1)

        self.setWindowOpacity(0.96)

        self.groupbtn = QtGui.QPushButton(u"首页")
        self.groupbtn.setObjectName("headbtn")
        self.charactorbtn = QtGui.QPushButton(u"食灵")
        self.charactorbtn.setObjectName("headbtn")
        self.equipbtn = QtGui.QPushButton(u"装备")
        self.equipbtn.setObjectName("headbtn")
        self.projectbtn = QtGui.QPushButton(u"装盘模拟")
        self.projectbtn.setObjectName("headbtn")
        self.cvbtn = QtGui.QPushButton(u"声优")
        self.cvbtn.setObjectName("headbtn")
        self.damagebtn = QtGui.QPushButton(u"伤害计算")
        self.damagebtn.setObjectName("headbtn")
        self.aboutbtn = QtGui.QPushButton(u"关于")
        self.aboutbtn.setObjectName("headbtn")

        self.bglabel = QtGui.QLabel()

        self.groupbtn.clicked.connect(self.mainView)
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
        self.maingrid.setColumnStretch(0, 1)

        # 顶部窗体
        self.topwiget = QtGui.QWidget()
        self.topgrid = QtGui.QGridLayout()
        self.topwiget.setLayout(self.topgrid)
        self.maingrid.addWidget(self.topwiget, 0, 0)

        self.topgrid.addWidget(self.groupbtn, 0, 0)
        self.topgrid.addWidget(self.charactorbtn, 0, 1)
        self.topgrid.addWidget(self.equipbtn, 0, 2)
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
        self.bodywiget.setWindowOpacity(1)

    def inibodywiget(self):
        """初始化body"""
        if self.wigetIndex is None:
            pass
        else:
            for i in self.wigetIndex:
                i.deleteLater()

    def mainView(self):
        self.inibodywiget()
        self.bodygrid.setRowStretch(0, 0)
        self.bodygrid.setRowStretch(1, 0)
        self.bodygrid.setColumnStretch(0, 0)
        self.bodygrid.setColumnStretch(1, 0)

        self.sywiget = QtGui.QWidget()
        self.sywiget.setObjectName("main_sy")  # 首页
        self.bodygrid.addWidget(self.sywiget, 0, 0)
        self.sygrid = QtGui.QGridLayout()
        self.sywiget.setLayout(self.sygrid)


        self.syLabel = QtGui.QLabel(u"使用说明")
        self.syLabel.setObjectName("syLabel")
        self.syLabel.setMaximumHeight(100)
        self.syLabel.setAlignment(QtCore.Qt.AlignTop| QtCore.Qt.AlignHCenter)
        self.sygrid.addWidget(self.syLabel, 0, 1, 1, 2)

        def setsybtn(grid, btnName, row, column):
            """创建首页btn"""
            sybtn = QtGui.QPushButton(btnName)
            sybtn.setFixedSize(100, 30)
            sybtn.setObjectName("sybtn")
            grid.addWidget(sybtn, row, column)
            return sybtn

        self.sybtn1 = setsybtn(self.sygrid, u"声  明", 1, 0)
        self.sybtn2 = setsybtn(self.sygrid, u"食灵说明", 1, 1)
        self.sybtn3 = setsybtn(self.sygrid, u"装备说明", 1, 2)
        self.sybtn4 = setsybtn(self.sygrid, u"少女祈祷中", 1, 3)
        self.sybtn1.clicked.connect(lambda: self.mainViewEdit(1))
        self.sybtn2.clicked.connect(lambda: self.mainViewEdit(2))
        self.sybtn3.clicked.connect(lambda: self.mainViewEdit(3))
        # self.sybtn4.clicked.connect(lambda: self.mainViewEdit(4))

        self.syText = QtGui.QTextBrowser()
        self.syText.setObjectName("syText")
        self.syText.setFixedHeight(390)
        self.syText.append(u"\n\n\n◆欢迎使用本工具！初次使用可以在此处查看使用帮助，有任何疑问和建议可以联系作者。")
        self.syText.append(u"◆本工具所有美术资源或算法由萌百黑大@划破黑夜 破解，破解不易请珍惜成果，任何非法和损害他人利益行为与作者无关！")
        self.syText.append(u"◆本工具旨在辅助玩家了解游戏信息，工具界面大致还原游戏界面是为了让玩家对工具产生亲切感。禁止窃取、泄露本工具美术资源，任何非法和损害他人利益行为与作者无关！")
        self.sygrid.addWidget(self.syText, 3, 0, 1, 4)

        # self.sygrid.setRowStretch(1, 6)
        # self.sygrid.setRowStretch(2, 2)

        self.wigetIndex = [self.sywiget]

    def mainViewEdit(self, index):
        if index == 1:
            self.syText.clear()
            self.syText.append(u"\n\n\n◆欢迎使用本工具！初次使用可以在此处查看使用帮助，有任何疑问和建议可以联系作者。")
            self.syText.append(u"◆本工具所有美术资源或算法由萌百黑大@划破黑夜 破解，破解不易请珍惜成果")
            self.syText.append(u"◆本工具旨在辅助玩家了解游戏信息，工具界面大致还原游戏界面是为了让玩家对工具产生亲切感。禁止窃取、泄露本工具美术资源，任何非法和损害他人利益行为与作者无关！")
        elif index == 2:
            self.syText.clear()
            self.syText.append(u"\n\n\n◆食灵界面目前提供食灵列表和食灵详细信息查看")
            self.syText.append(u"◆搜索功能少女祈祷中...")
        else:
            self.syText.clear()
            self.syText.append(u"\n\n\n◆装备界面提供一个比较自由的功能，请先选择左侧套装，右边即会显示相关信息")

    def cuisinelist(self):
        self.inibodywiget()

        self.bodygrid.setRowStretch(1, 0)
        self.bodygrid.setColumnStretch(0, 1)
        self.bodygrid.setColumnStretch(1, 0)

        con = sqlite3.connect("llcy")
        cur = con.cursor()
        sql = 'SELECT URL_TX,n.SL_NO,SL_NAME,SL_TYPE,SL_HP,SL_GJ,SL_FY,SL_MZ,SL_SB,SL_BJ,SL_GS,SL_SY,SL_ML,MAX_HP,MAX_GJ,MAX_FY,MAX_MZ,MAX_SB,MAX_BJ,MAX_GS,MAX_SY,MAX_ML FROM fairy_detail n,fairy_detail_max m WHERE n.SL_NO=m.SL_NO;'
        # sql='SELECT * FROM "fairy_info";'
        cur.execute(sql)
        info = cur.fetchall()
        cur.close()
        rowcount = len(info)

        self.tablewiget = QtGui.QTableWidget(rowcount, 22)
        self.bodygrid.addWidget(self.tablewiget, 0, 0)

        self.tablewiget.itemClicked.connect(self.slDetail)  # 表格信号
        # self.tablewiget.horizontalHeader().sectionClicked.connect(self.fortest2)  # 表头信号

        # self.tablewiget.verticalHeader().setVisible(False)
        # self.tablewiget.horizontalHeader().setVisible(False)
        self.tablewiget.setHorizontalHeaderLabels([u"头像", u"No", u"食灵", u"类型", u"生命", u"攻击", u"防御", u"命中", u"闪避",
                                                   u"暴击", u"攻速", u"石油", u"魔力", u"满生命", u"满攻击", u"满防御", u"满命中", u"满闪避",
                                                   u"满暴击", u"满攻速", u"满石油", u"满魔力"])

        for x in range(self.tablewiget.columnCount()):
            headItem = self.tablewiget.horizontalHeaderItem(x)  # 获得水平方向表头的Item对象
            headItem.setBackgroundColor(QtGui.QColor(0, 60, 10))  # 设置单元格背景颜色
            headItem.setTextColor(QtGui.QColor(200, 111, 30))

            # self.tablewiget.setShowGrid(False)  # 设置网格线

        # self.lbp = QtGui.QLabel()
        # self.lbp.setPixmap(QtGui.QPixmap(U"card/cutin/bmf_n.png"))
        # self.tablewiget.setCellWidget(0, 0, self.lbp)

        # self.tablewiget.horizontalHeader().setStretchLastSection(True)
        # self.tablewiget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        # self.tablewiget.verticalHeader().setStretchLastSection(True)
        # self.tablewiget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        # self.tablewiget.resizeRowsToContents()
        self.tablewiget.resizeColumnsToContents()
        # self.tablewiget.resizeColumnToContents(1)
        # self.tablewiget.resizeColumnToContents(3)
        # self.tablewiget.resizeColumnToContents(4)

        self.tablewiget.setColumnWidth(0, 200)
        self.tablewiget.setColumnWidth(2, 160)

        rowindex=0
        for i in info:
            columnindex = 0
            for x in i:
                if type(x) == int:
                    info = str(x)
                else:
                    info = x

                if columnindex == 0:
                    self.lbp = QtGui.QLabel()
                    self.lbp.setPixmap(QtGui.QPixmap(info))
                    self.tablewiget.setCellWidget(rowindex, columnindex, self.lbp)
                    columnindex += 1
                    pass
                elif columnindex == 3:
                    self.lbp = QtGui.QLabel()
                    self.lbp.setPixmap(QtGui.QPixmap('ui/hero/'+info+'.png'))
                    self.tablewiget.setCellWidget(rowindex, columnindex, self.lbp)
                    columnindex += 1
                else:
                    self.newItem = QtGui.QTableWidgetItem(info)
                    self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.tablewiget.setItem(rowindex, columnindex, self.newItem)
                    columnindex += 1
                    self.newItem.setWhatsThis(info)
            rowindex += 1

        self.wigetIndex = [self.tablewiget]
        # self.tablewiget.cellClicked.connect(self.slDetail)

    def equiplist(self):
        self.inibodywiget()

        sql = 'SELECT TZ_NAME FROM "equip_suit";'
        info = ToolFunction.getsqliteInfo(sql)

        self.tablewiget = QtGui.QTableWidget(3, 1)
        self.tablewiget.horizontalHeader().setStretchLastSection(True)
        self.tablewiget.verticalHeader().setStretchLastSection(True)
        self.tablewiget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tablewiget.setFixedHeight(100)
        self.tablewiget.setHorizontalHeaderLabels([u"套装属性"])
        self.tablewiget.verticalHeader().setVisible(False)
        self.bodygrid.addWidget(self.tablewiget, 0, 1)

        self.tablewiget2 = QtGui.QTableWidget(10, 5)
        self.tablewiget2.setHorizontalHeaderLabels([u"名称", u"品质", u"类型", u"基础属性1", u"基础属性2"])
        self.tablewiget2.verticalHeader().setVisible(False)

        self.tablewiget2.verticalHeader().setStretchLastSection(True)
        self.tablewiget2.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.bodygrid.addWidget(self.tablewiget2, 1, 1)
        self.equipTzList = QtGui.QListWidget()
        for tzNameIndex in info:
            newItem = QtGui.QListWidgetItem(tzNameIndex[0])
            newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.equipTzList.addItem(newItem)

        self.equipTzList.itemClicked.connect(self.equipEdit)
        self.bodygrid.addWidget(self.equipTzList, 0, 0, 0, 1)

        self.bodygrid.setColumnStretch(0, 0)
        self.bodygrid.setColumnStretch(1, 1)

        # self.tablewiget.verticalHeader().setVisible(False)
        # self.tablewiget.horizontalHeader().setVisible(False)

        self.wigetIndex = [self.tablewiget, self.tablewiget2, self.equipTzList]

    def equipEdit(self):
        listItemName = unicode(self.equipTzList.currentItem().text())
        sql = "select TZ_ATTR_FIR, TZ_ATTR_SEC, TZ_ATTR_TRI, b1.code_name, b2.code_name, s.tz_name||e_type_sub equip_name, e_attr_fir, e_attr_sec from equip_info t, equip_suit s, (select code, code_name from bas_code where code_id = 'equip_type') b2, (select code, code_name from bas_code where code_id = 'equip_level') b1 where t.e_level = b1.code and t.e_type = b2.code and t.e_tz = s.tz_no and s.TZ_NAME = '"+listItemName+"' order by t.E_TYPE"
        datainfo = ToolFunction.getsqliteInfo(sql)
        # print datainfo
        self.tablewiget.clear()
        self.tablewiget2.clear()
        self.tablewiget.setHorizontalHeaderLabels([u"套装属性"])
        self.tablewiget2.setHorizontalHeaderLabels([u"名称", u"品质", u"类型", u"基础属性1", u"基础属性2"])

        typeIndex={u"食器":1, u"厨具":2, u"餐具":3}
        rowindex = 0
        for rowData in datainfo:
            columnindex = 0
            for columnData in rowData:
                if type(columnData) == int:
                    info = str(columnData)
                else:
                    info = columnData

                if columnindex < 3:
                    self.newItem = QtGui.QTableWidgetItem(info)
                    # self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.tablewiget.setItem(columnindex, 0, self.newItem)
                    self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    columnindex += 1
                elif columnindex == 4:
                    self.newItem = QtGui.QTableWidgetItem(info)
                    self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.tablewiget2.setItem(rowindex, columnindex-3, self.newItem)
                    self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.newItem.setIcon(QtGui.QIcon('ui/equip/'+str(typeIndex[info])+'.png'))
                    columnindex += 1
                else:
                    self.newItem = QtGui.QTableWidgetItem(info)
                    self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                    self.tablewiget2.setItem(rowindex, columnindex-3, self.newItem)
                    self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
                    columnindex += 1
            rowindex += 1

    def aboutinfo(self):
        self.inibodywiget()

        self.bodygrid.setRowStretch(1, 0)
        self.bodygrid.setColumnStretch(0, 1)
        self.bodygrid.setColumnStretch(1, 0)

        # 设置左右框架
        self.leftwiget = QtGui.QWidget()
        self.rightwiget = QtGui.QWidget()
        self.bodygrid.addWidget(self.leftwiget, 0, 0)
        self.bodygrid.addWidget(self.rightwiget, 0, 1)
        self.leftgrid = QtGui.QGridLayout()
        self.rightgrid = QtGui.QGridLayout()
        self.leftwiget.setLayout(self.leftgrid)
        self.rightwiget.setLayout(self.rightgrid)
        self.leftwiget.setObjectName("aboutLeft")
        self.leftwiget.setObjectName("aboutRight")

        # 左框架
        self.infolaber = QtGui.QLabel(u"更新历史")
        self.leftgrid.addWidget(self.infolaber, 0, 0)
        self.infolaber.setObjectName("aboutName")

        self.tree = QtGui.QTreeWidget()
        # self.tree.setHeaderLabel(u"更新历史")
        self.tree.headerItem().setBackgroundColor(0, QtGui.QColor(255, 0, 0))
        self.tree.setHeaderHidden(True)
        self.leftgrid.addWidget(self.tree, 1, 0)
        self.tree.setWindowOpacity(0.1)

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
        self.text=QtGui.QTextEdit()
        self.text.setObjectName("rightInfo")
        self.text.setHtml("<img src='ui/yzs.png'>")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.append(u"\n欢迎加入我们\nQQ群:xxxxxx\n")
        self.text.setTextColor(QtGui.QColor("#FFF3EE"))
        self.text.setFontPointSize(20)
        self.text.append(u"界面设计")
        self.text.setFontPointSize(14)
        self.text.append(u"XXX\n")
        self.text.setFontPointSize(20)
        self.text.append(u"开发制作")
        self.text.setFontPointSize(14)
        self.text.append(u"XXX\n")
        self.text.setFontPointSize(20)
        self.text.append(u"数据")
        self.text.setFontPointSize(14)
        self.text.append(u"XXX\n")
        self.text.setFontPointSize(20)
        self.text.append(u"美工/UI")
        self.text.setFontPointSize(14)
        self.text.append(u"期待您的加入\n")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.rightgrid.addWidget(self.text, 0, 0)
        self.wigetIndex = [self.leftwiget, self.rightwiget]

    def slDetail(self):
        indexRow = self.tablewiget.currentRow()
        slnumb = self.tablewiget.item(indexRow, 1).text()
        sql = 'SELECT URL_LH,URL_LH2,SL_NAME,SL_LEVEL,TJ_HP,TJ_GJ,TJ_GJ,TJ_MZ,TJ_FY,TJ_SB,SKILL_NAME,SKILL_DESC,SKILL_GY_NAME,SKILL_GY_DESC,GROUP_DECS,SL_TYPE FROM "fairy_detail" WHERE SL_NO = '+str(slnumb)+';'
        print sql
        info = ToolFunction.getsqliteInfo(sql)
        print info

        self.inibodywiget()

        self.detailWidget = QtGui.QWidget()
        self.detailFrameGrid = QtGui.QGridLayout()
        self.detailWidget.setLayout(self.detailFrameGrid)
        self.bodygrid.addWidget(self.detailWidget, 0, 0)
        self.detailWidget.setObjectName("SLdetail")
        self.detailFrameGrid.setColumnStretch(0, 1)
        self.detailFrameGrid.setColumnStretch(1, 1)

        # 左边贴图
        self.cuisineLable = QtGui.QLabel()
        self.cuisineLable.setObjectName("lhLable")
        self.detailFrameGrid.addWidget(self.cuisineLable, 0, 0)
        stylesheet = "QLabel#lhLable{border-image: url("+info[0][0]+");}" + \
                     "QLabel#lhLable::hover{border-image: url("+info[0][1]+");}"
        self.cuisineLable.setStyleSheet(stylesheet)

        # 右边窗体
        self.attributeList = QtGui.QTableWidget(15, 4)
        self.attributeList.setObjectName("sl_Attri")
        self.detailFrameGrid.addWidget(self.attributeList, 0, 1)
        self.attributeList.verticalHeader().setVisible(False)
        self.attributeList.horizontalHeader().setVisible(False)
        self.attributeList.setShowGrid(False)
        self.attributeList.setSpan(0, 0, 1, 2)
        self.attributeList.setSpan(1, 0, 1, 2)
        self.attributeList.setSpan(7, 0, 2, 4)
        self.attributeList.setSpan(10, 0, 2, 4)
        self.attributeList.setSpan(13, 0, 2, 4)

        self.newItem = QtGui.QTableWidgetItem(info[0][2])
        self.lbp2 = QtGui.QLabel()
        self.lbp2.setPixmap(QtGui.QPixmap('ui/hero/'+str(info[0][15])+'.png'))
        self.attributeList.setCellWidget(0, 0, self.lbp2)
        self.newItem.setFont(QtGui.QFont("youyuan", 18, 100))
        # self.newItem.setIcon(QtGui.QIcon('ui/hero/'+str(info[0][15])+'.png'))
        self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.attributeList.setItem(0, 0, self.newItem)
        self.lbp2 = QtGui.QLabel()
        self.lbp2.setPixmap(QtGui.QPixmap('ui/hero/star'+str(info[0][3])+'.png'))
        self.attributeList.setCellWidget(1, 0, self.lbp2)

        self.slDetailEdit(u'技能', info[0][4], 2, 0)
        self.slDetailEdit(u'装盘', info[0][4], 2, 1)
        self.slDetailEdit(u'生命', info[0][4], 3, 0)
        self.slDetailEdit(u'攻击', info[0][5], 3, 1)
        self.slDetailEdit(u'攻速', info[0][6], 4, 0)
        self.slDetailEdit(u'命中', info[0][7], 4, 1)
        self.slDetailEdit(u'防御', info[0][8], 5, 0)
        self.slDetailEdit(u'闪避', info[0][9], 5, 1)

        self.newItem = QtGui.QTableWidgetItem(u"料理技")
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.newItem.setFont(QtGui.QFont("youyuan", 14, 100))
        self.attributeList.setItem(6, 0, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(info[0][10])
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.attributeList.setItem(6, 1, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(info[0][11])
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.attributeList.setItem(7, 0, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(u"固有技")
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.newItem.setFont(QtGui.QFont("youyuan", 14, 100))
        self.attributeList.setItem(9, 0, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(info[0][12])
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.attributeList.setItem(9, 1, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(info[0][13])
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.attributeList.setItem(10, 0, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(u"装盘效果")
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.newItem.setFont(QtGui.QFont("youyuan", 14, 100))
        self.attributeList.setItem(12, 0, self.newItem)

        self.newItem = QtGui.QTableWidgetItem(info[0][14])
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)
        self.attributeList.setItem(13, 0, self.newItem)

        self.wigetIndex = [self.detailWidget]

    def slDetailEdit(self, attr, info, row, column):
        """食灵属性编辑"""
        msg = attr + "  " + info
        iconUrl = {u"技能": 'ui/hero/skill.png', u"装盘": 'ui/hero/skill.png', u"生命": 'ui/hero/hp.png',
                   u"攻击": 'ui/hero/atk.png', u"攻速": 'ui/hero/atkSpeed.png', u"命中": 'ui/hero/hit.png',
                   u"防御": 'ui/hero/phyDef.png', u"闪避": 'ui/hero/miss.png',}
        self.newItem = QtGui.QTableWidgetItem(msg)
        self.newItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.newItem.setFlags(QtCore.Qt.ItemIsEnabled)  # 不允许点击表格内容
        self.newItem.setIcon(QtGui.QIcon(iconUrl[attr]))
        self.attributeList.setItem(row, column, self.newItem)

    def fortest(self):
        pass


class ToolFunction:
    def __init__(self):
        pass

    @staticmethod
    def getsqliteInfo(sql):
        con = sqlite3.connect("llcy")
        cur = con.cursor()
        cur.execute(sql)
        info = cur.fetchall()
        cur.close()
        return info


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

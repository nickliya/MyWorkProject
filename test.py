# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class Stacked(QDialog):
    def __init__(self, parent=None):
        super(Stacked, self).__init__(parent)
        self.setWindowTitle(self.tr("StackedWidget"))

        leftlist = QListWidget(self)
        leftlist.insertItem(0, 'window1')
        leftlist.insertItem(1, 'window2')
        leftlist.insertItem(2, 'window3')

        label1 = QLabel('windowTest1\n11111111 ')
        label2 = QLabel('windowTest2\n22222222 ')
        # label3 = QLabel('windowTest3\n33333333 ')

        self.stack = QStackedWidget(self)
        self.stack.addWidget(label1)
        self.stack.addWidget(label2)
        # self.stack.addWidget(label3)

        mainLayout = QHBoxLayout(self)
        mainLayout.addWidget(leftlist)
        mainLayout.addWidget(self.stack, 0, Qt.AlignHCenter)
        mainLayout.setStretchFactor(leftlist, 1)
        mainLayout.setStretchFactor(self.stack, 3)  # 设定了list与self.stack比例为1:3。
        leftlist.currentRowChanged.connect(lambda:self.stack.setCurrentIndex(1))


class Laber1(Stacked):
    def __init__(self):
        super(Laber1, self).__init__()
        label3 = QLabel('windowTest3\n33333333 ')
        self.stack.addWidget(label3)


class Mainloop(Laber1):
    def __init__(self):
        super(Mainloop, self).__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Mainloop()
    main.show()
    app.exec_()

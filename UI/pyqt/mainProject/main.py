#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time : 2019/3/5 15:19 
@Author : yangqing
@contact: 401219180@qq.com
@File : main.py 
@Software: PyCharm
@Version: 1.0.0
@Desc:
"""
from Resource.mainWidget import *
import os
import sys


def main():
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    """检查是否有缓存文件 START"""
    isexisted = os.path.exists('./Tcptemp')
    if not isexisted:
        os.makedirs('./Tcptemp')
    else:
        pass
    """检查是否有缓存文件 END"""

    main()

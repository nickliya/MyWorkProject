#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import math
import requests

from PyQt4 import QtCore, QtGui, QtOpenGL
from OpenGL import GL

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

s = requests.session()
payload = {

}

# filename = "marry.png"
#
#
# # url = "http://211.152.2.24:7000/playtest-update-repo/1.4.75/res/card/normal/" + filename
# # url = "http://res.llcy.punchbox.info/android/1.5.9/res/card/normal/" + filename
# url = "http://res.llcy.punchbox.info/android/1.5.9/res/background/" + filename
url = "http://192.168.1.82:8000/yq123/"
r = s.get(url, params=payload, headers=header)
img = r.json()
print img
# imgfile = open("C:\\Users\\fuzhi\\Desktop\\normal\\" + filename, "wb+")
# imgfile.write(img)
# imgfile.close()

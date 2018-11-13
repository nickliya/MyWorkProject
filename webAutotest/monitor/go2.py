# /usr/bin/python
# -*- coding: utf-8 -*-

import HTMLTestRunner
import unittest
# import myTestSuite as Case
from monitor.myTestSuite import Qxgl
testunit = unittest.TestSuite()

# testunit.addTest(Case.Clgl("case1"))
# testunit.addTest(Case.Xxgl("case5"))
testunit.addTest(Qxgl("case2"))

HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

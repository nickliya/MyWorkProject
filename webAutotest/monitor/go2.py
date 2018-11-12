# /usr/bin/python
# -*- coding: utf-8 -*-

import HTMLTestRunner
import unittest
import myTestSuite as Case

testunit = unittest.TestSuite()

# testunit.addTest(Case.Clgl("case1"))
# testunit.addTest(Case.Xxgl("case5"))
testunit.addTest(Case.Qxgl("case3"))

HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result2.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

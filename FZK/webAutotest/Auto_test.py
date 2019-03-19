# /usr/bin/python
# coding=utf-8
# create by 15025463191 2017/05/11
import HTMLTestRunner
import unittest
import web_Sirui as Case

testunit = unittest.TestSuite()

testunit.addTest(Case.Rygl("case1"))
testunit.addTest(Case.Rygl("case2"))
testunit.addTest(Case.Rygl("case3"))
testunit.addTest(Case.Rygl("case4"))
testunit.addTest(Case.Rygl("case5"))
testunit.addTest(Case.Rygl("case6"))
testunit.addTest(Case.Dagl("case1"))
# test= unittest.TestLoader().loadTestsFromTestCase(dotest)
# testunit.addTest(unittest.makeSuite(case.Sirui))
HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

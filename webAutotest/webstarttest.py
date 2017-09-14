# /usr/bin/python
# coding=utf-8
# create by 15025463191 2017/05/11
import HTMLTestRunner
import unittest
import webAutotest.web_Sirui as case

testunit = unittest.TestSuite()
# testunit.addTest(case.Tgxf("case1"))
testunit.addTest(case.Tgxf("case3"))
# testunit.addTest(case.Bdxt("case1"))
# testunit.addTest(case.Bdxt("case2"))
# testunit.addTest(case.Bdxt("case3"))
# testunit.addTest(case.Bdxt("case4"))
# testunit.addTest(case.Bdxt("case5"))
# testunit.addTest(case.Bdxt("case6"))
# test= unittest.TestLoader().loadTestsFromTestCase(dotest)
# testunit.addTest(unittest.makeSuite(case.Sirui))
HtmlFile = 'C:\Users\YangQ\Desktop\Result.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

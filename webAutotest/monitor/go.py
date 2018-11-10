# /usr/bin/python
# -*- coding: utf-8 -*-

from HtmlTestRunner import HTMLTestRunner
import unittest
import myTestSuite as Case

testunit = unittest.TestSuite()

testunit.addTest(Case.Clgl("case1"))
testunit.addTest(Case.Clgl("case2"))

runner = HTMLTestRunner(output="example_suite", report_title="自动化")
runner.run(testunit)

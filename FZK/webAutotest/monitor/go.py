# /usr/bin/python
# -*- coding: utf-8 -*-
"""
python2.7
"""

from HtmlTestRunner import HTMLTestRunner
import unittest
import myTestSuite as Case

testunit = unittest.TestSuite()

testunit.addTest(Case.Clgl("case1"))
testunit.addTest(Case.Clgl("case2"))
# testunit.addTest(Case.Rygl("case3"))

runner = HTMLTestRunner(output="example_suite", report_title="自动化")
runner.run(testunit)

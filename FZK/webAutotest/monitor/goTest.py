# /usr/bin/python
# -*- coding: utf-8 -*-
"""
python3.6
"""

from HtmlTestRunner import HTMLTestRunner
import unittest
import myTestSuite
import myTestSuite2

# 先打开浏览器
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

testunit = unittest.TestSuite()

# 设置用例
testunit.addTest(myTestSuite2.Sbgl("case1"))
# testunit.addTest(myTestSuite2.Shgl("case2"))
# testunit.addTest(myTestSuite2.Shgl("case3"))

# 报告输出
runner = HTMLTestRunner(output="example_suite", report_title="自动化", report_name="MyReport")
runner.run(testunit)

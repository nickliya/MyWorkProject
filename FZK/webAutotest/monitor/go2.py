"""
自动化项目清单
Clgl: 车辆管理
case1: 编辑车辆
case2: 删除车辆,没有关联
case3: 删除车辆,有关联

Sbgl: 设备管理
case1: 配置新增
case2: 配置编辑
case3: 配置删除

Shgl: 商户管理
case1: 商户新增
case2: 商户编辑
case3: 商户冻结
case4: 商户解冻

Xxgl: 消息管理
case1: 公告新增
case2: 公告公告删除

Qxgl: 权限管理
case1: 成员新增
case2: 成员编辑-修改成员姓名
case3: 成员编辑-修改成员密码

使用testunit.addTest(Qxgl("case2"))来添加测试用例

"""
# /usr/bin/python
# -*- coding: utf-8 -*-
import HTMLTestRunner
import unittest
import myTestSuite
import myTestSuite2

# 先打开浏览器
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\selenum\AutomationProfile"

testunit = unittest.TestSuite()


# 设置用例
testunit.addTest(myTestSuite.Xxgl("case1"))
testunit.addTest(myTestSuite.Xxgl("case2"))

HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

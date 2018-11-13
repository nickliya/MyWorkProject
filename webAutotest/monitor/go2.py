"""
自动化项目清单
Clgl: 车辆管理
case1: 编辑车辆
case2: 删除车辆,没有关联

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
case4: 成员新增
case5: 成员新增

使用testunit.addTest(Qxgl("case2"))来添加测试用例

"""
# /usr/bin/python
# -*- coding: utf-8 -*-

import HTMLTestRunner
import unittest
from monitor.myTestSuite import Qxgl
testunit = unittest.TestSuite()

# 设置用例
# testunit.addTest(Case.Clgl("case1"))
# testunit.addTest(Case.Xxgl("case5"))
testunit.addTest(Qxgl("case2"))

HtmlFile = 'C:\\Users\\fuzhi\\Desktop\\Result.html'
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'4S门户自动化测试', description=u'用例测试情况')
runner.run(testunit)

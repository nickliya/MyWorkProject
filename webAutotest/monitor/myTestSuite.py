# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from mainfun import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest

br = Mainfun()
pubfun = SupportFun()


# class ParametrizedTestCase(unittest.TestCase):
#     """ TestCase classes that want to be parametrized should
#         inherit from this class.
#     """
#     def __init__(self, methodName='runTest', param=None):
#         super(ParametrizedTestCase, self).__init__(methodName)
#         self.param = param
#     @staticmethod
#     def parametrize(testcase_klass, param=None):
#         """ Create a suite containing all tests taken from the given
#             subclass, passing them the parameter 'param'.
#         """
#         testloader = unittest.TestLoader()
#         testnames = testloader.getTestCaseNames(testcase_klass)
#         suite = unittest.TestSuite()
#         for name in testnames:
#             suite.addTest(testcase_klass(name, param=param))
#         return suite


class Clgl(unittest.TestCase):
    """车辆管理"""
    # def setUpClass(self):
    #     print "classkaishi"
    #
    # def tearDownClass(self):
    #     print "classjieshu"

    def setUp(self):
        print("kaishi")

    def tearDown(self):
        print("jieshu")

    def case1(self):
        """tthisjid发sa"""
        testcase_name = "dsa"
        # time.sleep(2)
        # br.browser.find_element_by_id('/car').click()
        # time.sleep(1)
        # br.browser.find_element_by_id('monitor').click()
        # WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "tableAdd")))
        # br.browser.find_element_by_id('keyword').send_keys("DAUT8L7R4322H0809")
        # br.browser.find_element_by_id('tableSearch').click()
        #
        # time.sleep(1)
        # br.browser.find_element_by_id('edit-DAUT8L7R4322H0809').click()
        #
        # time.sleep(1)
        # br.browser.find_element_by_id('vin').send_keys()
        # br.browser.find_element_by_id('plateNum').send_keys()
        #
        # br.browser.find_element_by_id("submit").click()
        print "1"
        self.assertIs(1, 1, "参数错误")

    @staticmethod
    def case2():
        """删除车辆得准备一个没有关联，能删除的车辆"""
        print "2"


class Rygl(unittest.TestCase):
    u"""账号管理"""

    # def setUp(self):
    # br.browser._switch_to.frame('iframepage')
    # br.browser._switch_to.frame('leftframe')

    def tearDown(self):
        br.browser.refresh()

    @staticmethod
    def case1():
        u"""新注册账号"""
        time.sleep(2)
        br.browser.find_element_by_id('/permission').click()
        time.sleep(1)
        br.browser.find_element_by_id('members').click()
        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "tableAdd")))
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_id('realName').send_keys(u"自动化测试")
        br.browser.find_element_by_id('roleIdList').click()
        time.sleep(1)
        br.browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/ul/li[1]").click()
        br.browser.find_element_by_id("userName").send_keys("15025466668")
        br.browser.find_element_by_id("password").send_keys("123456")
        br.browser.find_element_by_id("submit").click()

        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "keyword")))
        br.browser.find_element_by_id('keyword').send_keys('15025466668')
        br.browser.find_element_by_id('tableSearch').click()
        data = br.browser.find_element_by_xpath(
            '//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]/div/p')
        t = data.text
        print t

    @staticmethod
    def case2():
        u"""新注册账号"""
        time.sleep(2)
        br.browser.find_element_by_id('/equipment').click()
        time.sleep(1)
        br.browser.find_element_by_id('device').click()
        br.browser.find_element_by_id('keyword').send_keys("864244025785154")
        br.browser.find_element_by_id('tableSearch').click()
        time.sleep(1)
        br.browser.find_element_by_id('bind-864244025785154').click()
        time.sleep(1)
        br.browser.find_element_by_name('file').click()
        print "ok"

# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from mainfun import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import unittest
import json

br = Mainfun()
pubfun = SupportFun()


class Clgl(unittest.TestCase):
    """车辆管理"""
    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/clgl.js", "r")
        cls.jsoninfo = json.load(jsonfile)

    # def setUp(self):
    #     print("kaishi")
    #
    # def tearDown(self):
    #     print("jieshu")

    @staticmethod
    def goto():
        """进入车辆管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/car').click()
        time.sleep(1)
        br.browser.find_element_by_id('monitor').click()

    def case1(self):
        """编辑车辆"""
        self.goto()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case1"]["oldVin"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('edit-'+self.jsoninfo["case1"]["oldVin"]).click()

        time.sleep(1)
        br.browser.find_element_by_id('vin').clear()
        br.browser.find_element_by_id('vin').send_keys(self.jsoninfo["case1"]["newVin"])
        br.browser.find_element_by_id('plateNum').clear()
        br.browser.find_element_by_id('plateNum').send_keys(self.jsoninfo["case1"]["newplateNum"])

        # br.browser.find_element_by_id("submit").click()
        print "1"
        self.assertIs(1, 1, "参数错误")
        return "123"

    def case2(self):
        """删除车辆,没有关联"""
        self.goto()
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

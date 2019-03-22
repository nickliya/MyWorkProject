# -*- coding: utf-8 -*-
"""新监控2.0"""
import unittest
from mainfun import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

br = Mainfun()
pubfun = SupportFun()


class Shgl(unittest.TestCase):
    u"""商户管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/shgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    # def tearDown(self):
    # br.browser.refresh()
    # time.sleep(3)

    # @classmethod
    # def tearDownClass(cls):
    #     br.browser.quit()

    @staticmethod
    def goto():
        """进入配置管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/customer').click()
        time.sleep(1)
        br.browser.find_element_by_id('merchants').click()

    def case1(self):
        u"""电子围栏查询"""
        # 浏览器找到车辆管理点击
        br.browser.find_element_by_id('/car').click()

        time.sleep(2)

        # 电子围栏点击
        br.browser.find_element_by_id('eleFence').click()

        time.sleep(2)
        # 输入栏，输入234
        br.browser.find_element_by_id('keyword').send_keys('234')

        time.sleep(2)
        # 点击搜索
        br.browser.find_element_by_id('tableSearch').click()

        # 固定等待
        time.sleep(2)

        # 隐形等待
        br.browser.implicitly_wait(3)

        # 显性等待
        WebDriverWait(br.browser, 30).until(EC.element_to_be_selected(By.ID('eleFecen')))


class Sbgl(unittest.TestCase):
    u"""设备管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/shgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    # def tearDown(self):
    # br.browser.refresh()
    # time.sleep(3)

    # @classmethod
    # def tearDownClass(cls):
    #     br.browser.quit()

    @staticmethod
    def goto():
        """进入配置管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/customer').click()
        time.sleep(1)
        br.browser.find_element_by_id('merchants').click()

    def case1(self):
        u"""电子围栏查询"""
        # 浏览器找到车辆管理点击
        br.browser.find_element_by_id('/car').click()
        time.sleep(2)

        # 电子围栏点击
        br.browser.find_element_by_id('eleFence').click()

        time.sleep(2)
        # 输入栏，输入234
        # br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo['case1']['name'])
        br.browser.find_element_by_id('keyword').send_keys('321hufjisdjfi')

        time.sleep(2)
        # 点击搜索
        br.browser.find_element_by_id('tableSearch').click()

        # 固定等待
        # time.sleep(2)

        # 隐形等待
        # br.browser.implicitly_wait(3)

        # 显性等待
        # WebDriverWait(br.browser, 30).until(EC.element_to_be_selected(By.ID('eleFecen')))

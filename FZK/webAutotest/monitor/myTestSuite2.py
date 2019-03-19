# -*- coding: utf-8 -*-
import unittest
from mainfun import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

br = Mainfun()
pubfun = SupportFun()


class Qxgl(unittest.TestCase):
    u"""权限管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/qxgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    def tearDown(self):
        br.browser.refresh()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        br.browser.quit()

    @staticmethod
    def goto_cygl():
        """
        进入xxx
        """
        time.sleep(2)
        br.browser.find_element_by_id('/permission').click()
        time.sleep(1)
        br.browser.find_element_by_id('members').click()

    @staticmethod
    def goto_jsgl():
        time.sleep(2)
        br.browser.find_element_by_id('/permission').click()
        time.sleep(1)
        br.browser.find_element_by_id('role').click()

    def case1(self):
        u"""成员新增"""
        self.goto_cygl()
        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "tableAdd")))
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_id('realName').send_keys(self.jsoninfo["member"]["case1"]["realName"])
        br.browser.find_element_by_id('roleIdList').click()
        time.sleep(1)
        br.browser.find_element_by_xpath("/html/body/div[5]/div[1]/div[1]/ul/li[1]").click()
        br.browser.find_element_by_id("userName").send_keys(self.jsoninfo["member"]["case1"]["userName"])
        br.browser.find_element_by_id("password").send_keys(self.jsoninfo["member"]["case1"]["password"])
        br.browser.find_element_by_id("submit").click()

        # 断言
        try:
            newwindow = 'window.open("' + br.initdata["shopUrl"] + '")'
            br.browser.execute_script(newwindow)

            # 切换到新的窗口
            time.sleep(1)
            self.handles = br.browser.window_handles
            br.browser.switch_to_window(self.handles[-1])

            time.sleep(3)
            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
            br.browser.find_element_by_id('username').send_keys(self.jsoninfo["member"]["case1"]["userName"])
            br.browser.find_element_by_id('password').send_keys(self.jsoninfo["member"]["case1"]["password"])

            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
            temp_img = '1.png'
            code = br.getcode(temp_img)
            br.browser.find_element_by_id("captcha").send_keys(code)
            time.sleep(1)
            br.browser.find_element_by_id('submit').click()

            time.sleep(5)
            username = br.browser.find_element_by_class_name("name").text
            self.assertEqual(self.jsoninfo["member"]["case1"]["userName"], username, u"登录不成功")
        except Exception as msg:
            self.assertTrue(False, msg.__context__)

        br.browser.close()
        br.browser.switch_to_window(self.handles[0])

    def case2(self):
        u"""成员编辑-修改成员姓名"""
        self.goto_cygl()

        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "keyword")))
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["member"]["case2"]["userName"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('bind-'+self.jsoninfo["member"]["case2"]["userName"]).click()
        time.sleep(1)
        br.browser.find_element_by_name('realName').clear()
        br.browser.find_element_by_name('realName').send_keys(self.jsoninfo["member"]["case2"]["newRealName"])
        br.browser.find_element_by_name('submit').click()

        time.sleep(2)
        userElement = br.browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div/div/div[1]/div[2]/div[2]/div[3]/table/tbody/tr/td[1]/div/p')
        userName = userElement.text
        self.assertEqual(userName, self.jsoninfo["member"]["case2"]["newRealName"], "修改不匹配\r期望:"+self.jsoninfo["member"]["case2"]["newRealName"]+"\r实际:"+userName)

    def case3(self):
        u"""成员编辑-修改成员密码"""
        self.goto_cygl()

        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "keyword")))
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["member"]["case3"]["userName"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('bind-' + self.jsoninfo["member"]["case3"]["userName"]).click()
        time.sleep(1)
        br.browser.find_element_by_name('password').clear()
        br.browser.find_element_by_name('password').send_keys(self.jsoninfo["member"]["case3"]["newPassword"])
        br.browser.find_element_by_name('submit').click()

        # 断言
        try:
            time.sleep(1)
            newwindow = 'window.open("' + br.initdata["shopUrl"] + '")'
            br.browser.execute_script(newwindow)

            # 切换到新的窗口
            self.handles = br.browser.window_handles
            br.browser.switch_to_window(self.handles[-1])

            time.sleep(3)
            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
            br.browser.find_element_by_id('username').send_keys(self.jsoninfo["member"]["case3"]["userName"])
            br.browser.find_element_by_id('password').send_keys(self.jsoninfo["member"]["case3"]["newPassword"])

            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
            temp_img = '1.png'
            code = br.getcode(temp_img)
            br.browser.find_element_by_id("captcha").send_keys(code)
            time.sleep(1)
            br.browser.find_element_by_id('submit').click()

            time.sleep(5)
            username = br.browser.find_element_by_class_name("name").text
            self.assertEqual(self.jsoninfo["member"]["case3"]["userName"], username, u"登录不成功")
        except Exception as msg:
            self.assertTrue(False, msg)
        br.browser.close()
        br.browser.switch_to_window(self.handles[0])

    def case4(self):
        u"""角色新增"""
        self.goto_jsgl()

        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "keyword")))
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_name('roleName').send_keys(self.jsoninfo["member"]["case5"]["roleName"])
        br.browser.find_element_by_name('remark').send_keys(self.jsoninfo["member"]["case5"]["remark"])
        br.browser.find_element_by_name('submit').click()

        time.sleep(3)
        br.browser.find_element_by_name('roleName').send_keys(self.jsoninfo["member"]["case5"]["roleName"])
        br.browser.find_element_by_name('tableSearch').click()

        # 角色未完成


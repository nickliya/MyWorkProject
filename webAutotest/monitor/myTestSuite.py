# -*- coding: utf-8 -*-
import unittest
from mainfun import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

br = Mainfun()
pubfun = SupportFun()


class Clgl(unittest.TestCase):
    """车辆管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/clgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    # def setUp(self):
    #     print("kaishi")
    #
    def tearDown(self):
        time.sleep(1)
        br.browser.refresh()
        time.sleep(2)

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
        br.browser.find_element_by_id('edit-' + self.jsoninfo["case1"]["oldVin"]).click()

        time.sleep(1)
        br.browser.find_element_by_id('vin').clear()
        br.browser.find_element_by_id('vin').send_keys(self.jsoninfo["case1"]["newVin"])
        br.browser.find_element_by_id('plateNum').clear()
        br.browser.find_element_by_id('plateNum').send_keys(self.jsoninfo["case1"]["newplateNum"])
        br.browser.find_element_by_id("submit").click()

        time.sleep(2)
        br.browser.find_element_by_id('keyword').clear()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case1"]["newVin"])
        br.browser.find_element_by_id('tableSearch').click()
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case1"]["newVin"]).is_enabled()
        self.assertTrue(result, "修改失败")

    def case2(self):
        """删除车辆,没有关联"""
        self.goto()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case2"]["vin"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('delete-' + self.jsoninfo["case2"]["vin"]).click()
        br.browser.find_element_by_id('confirm').click()

        time.sleep(1)
        br.browser.find_element_by_id('keyword').clear()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case2"]["vin"])
        br.browser.find_element_by_id('tableSearch').click()

        result = br.browser.find_element_by_id('delete-' + self.jsoninfo["case2"]["vin"]).is_enabled()
        self.assertFalse(result, "验证失败")

    def case3(self):
        """删除车辆,有关联"""
        self.goto()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case3"]["vin"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('delete-' + self.jsoninfo["case3"]["vin"]).click()
        br.browser.find_element_by_id('confirm').click()

        time.sleep(1)
        br.browser.find_element_by_id('keyword').clear()
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case3"]["vin"])
        br.browser.find_element_by_id('tableSearch').click()

        result = br.browser.find_element_by_id('delete-' + self.jsoninfo["case3"]["vin"]).is_enabled()
        self.assertTrue(result, "验证失败")


class Sbgl(unittest.TestCase):
    u"""设备管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/pzgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    def tearDown(self):
        time.sleep(1)
        br.browser.refresh()
        time.sleep(2)

    @staticmethod
    def goto_pzgl():
        """进入配置管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/car').click()
        time.sleep(1)
        br.browser.find_element_by_id('model').click()

    @staticmethod
    def goto_sblb():
        """进入设备列表"""
        time.sleep(2)
        br.browser.find_element_by_id('/car').click()
        time.sleep(1)
        br.browser.find_element_by_id('device').click()

    def case1(self):
        u"""配置新增"""
        self.goto_pzgl()
        time.sleep(1)
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_id('cfgName').send_keys(self.jsoninfo["case1"]["cfgName"])
        br.browser.find_element_by_id('productCode').send_keys(self.jsoninfo["case1"]["productCode"])
        br.browser.find_element_by_id('remark').send_keys(self.jsoninfo["case1"]["remark"])
        br.browser.find_element_by_id('cfgParam').send_keys(self.jsoninfo["case1"]["cfgParam"])
        br.browser.find_element_by_id('submit').click()

        time.sleep(2)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case1"]["productCode"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case1"]["productCode"]).is_enabled()
        self.assertTrue(result, u"新建失败")

    def case2(self):
        u"""配置编辑"""
        self.goto_pzgl()
        time.sleep(1)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case2"]["productCode"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('edit-' + self.jsoninfo["case2"]["productCode"]).click()

        time.sleep(1)
        br.browser.find_element_by_id('cfgName').send_keys(self.jsoninfo["case2"]["cfgName"])
        br.browser.find_element_by_id('productCode').send_keys(self.jsoninfo["case2"]["productCode"])
        br.browser.find_element_by_id('remark').send_keys(self.jsoninfo["case2"]["remark"])
        br.browser.find_element_by_id('cfgParam').send_keys(self.jsoninfo["case2"]["cfgParam"])
        br.browser.find_element_by_id('submit').click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case2"]["productCode"]).is_enabled()
        self.assertTrue(result, u"编辑失败")

    def case3(self):
        u"""配置删除"""
        self.goto_pzgl()
        time.sleep(1)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case3"]["productCode"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('delete-' + self.jsoninfo["case3"]["productCode"]).click()
        br.browser.find_element_by_id('confirm').click()

        time.sleep(1)
        br.browser.find_element_by_id('keyWord').clear()
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case3"]["productCode"])
        br.browser.find_element_by_id('tableSearch').click()

        result = br.browser.find_element_by_id('delete-' + self.jsoninfo["case3"]["productCode"]).is_enabled()
        self.assertFalse(result, u"删除失败")


class Shgl(unittest.TestCase):
    u"""商户管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/shgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    def tearDown(self):
        br.browser.refresh()
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        br.browser.quit()

    @staticmethod
    def goto():
        """进入配置管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/customer').click()
        time.sleep(1)
        br.browser.find_element_by_id('merchants').click()

    def case1(self):
        u"""商户新增"""
        self.goto()
        time.sleep(1)
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_id('orgName').send_keys(self.jsoninfo["case1"]["orgName"])
        br.browser.find_element_by_id('manageUser').send_keys(self.jsoninfo["case1"]["manageUser"])
        br.browser.find_element_by_id('password').send_keys(self.jsoninfo["case1"]["password"])
        br.browser.find_element_by_id('contactUser').send_keys(self.jsoninfo["case1"]["contactUser"])
        br.browser.find_element_by_id('contactPhone').send_keys(self.jsoninfo["case1"]["contactPhone"])
        br.browser.find_element_by_id('contactAddress').send_keys(self.jsoninfo["case1"]["contactAddress"])
        br.browser.find_element_by_id('submit').click()

        time.sleep(2)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case1"]["manageUser"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case1"]["manageUser"]).is_enabled()
        self.assertTrue(result, u"新建失败")

    def case2(self):
        u"""商户编辑"""
        self.goto()
        time.sleep(1)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case2"]["orgName"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('edit-' + self.jsoninfo["case2"]["orgName"]).click()

        time.sleep(1)
        br.browser.find_element_by_id('orgName').clear()
        br.browser.find_element_by_id('orgName').send_keys(self.jsoninfo["case2"]["orgName"])
        br.browser.find_element_by_id('password').clear()
        br.browser.find_element_by_id('password').send_keys(self.jsoninfo["case2"]["password"])
        br.browser.find_element_by_id('contactUser').clear()
        br.browser.find_element_by_id('contactUser').send_keys(self.jsoninfo["case2"]["contactUser"])
        br.browser.find_element_by_id('contactPhone').clear()
        br.browser.find_element_by_id('contactPhone').send_keys(self.jsoninfo["case2"]["contactPhone"])
        br.browser.find_element_by_id('contactAddress').clear()
        br.browser.find_element_by_id('contactAddress').send_keys(self.jsoninfo["case2"]["contactAddress"])
        br.browser.find_element_by_id('submit').click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case2"]["orgName"]).is_enabled()
        self.assertTrue(result, u"编辑失败")

    def case3(self):
        u"""商户冻结"""
        self.goto()
        time.sleep(1)
        WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "keyword")))
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case3"]["manageUser"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('freeze-' + self.jsoninfo["case3"]["manageUser"]).click()
        br.browser.find_element_by_id('confirm').click()

        # 断言
        try:
            time.sleep(1)
            newwindow = 'window.open("' + br.initdata["shopUrl"] + '")'
            br.browser.execute_script(newwindow)

            # 切换到新的窗口
            time.sleep(1)
            self.handles = br.browser.window_handles
            br.browser.switch_to_window(self.handles[-1])

            time.sleep(3)
            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
            br.browser.find_element_by_id('username').send_keys(self.jsoninfo["case3"]["manageUser"])
            br.browser.find_element_by_id('password').send_keys(self.jsoninfo["case3"]["passwd"])

            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
            temp_img = '1.png'
            code = br.getcode(temp_img)
            br.browser.find_element_by_id("captcha").send_keys(code)
            time.sleep(1)
            br.browser.find_element_by_id('submit').click()

            time.sleep(5)
            try:
                username = br.browser.find_element_by_class_name("name").text
                self.assertNotEqual(self.jsoninfo["case4"]["manageUser"], username, "登录不成功")
            except Exception as msg:
                self.assertNotEqual(self.jsoninfo["case4"]["manageUser"], "", "登录不成功")
        except Exception as msg:
            print(msg)
            self.assertTrue(False, msg)

        br.browser.close()
        br.browser.switch_to_window(self.handles[0])

    def case4(self):
        u"""商户解冻"""
        self.goto()
        time.sleep(1)
        br.browser.find_element_by_id('keyword').send_keys(self.jsoninfo["case4"]["manageUser"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('freeze-' + self.jsoninfo["case4"]["manageUser"]).click()

        # 断言
        try:
            time.sleep(1)
            newwindow = 'window.open("' + br.initdata["shopUrl"] + '")'
            br.browser.execute_script(newwindow)
    
            # 切换到新的窗口
            time.sleep(1)
            self.handles = br.browser.window_handles
            br.browser.switch_to_window(self.handles[-1])
    
            time.sleep(3)
            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.ID, "username")))
            br.browser.find_element_by_id('username').send_keys(self.jsoninfo["case4"]["manageUser"])
            br.browser.find_element_by_id('password').send_keys(self.jsoninfo["case4"]["passwd"])
    
            WebDriverWait(br.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
            temp_img = '1.png'
            code = br.getcode(temp_img)
            br.browser.find_element_by_id("captcha").send_keys(code)
            time.sleep(1)
            br.browser.find_element_by_id('submit').click()
    
            time.sleep(5)
            username = br.browser.find_element_by_class_name("name").text
            self.assertEqual(self.jsoninfo["case4"]["manageUser"], username, "登录不成功")
        except Exception as msg:
            print(msg)
            self.assertTrue(False, msg)
            
        br.browser.close()
        br.browser.switch_to_window(self.handles[0])


class Xxgl(unittest.TestCase):
    u"""消息管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/shgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    def tearDown(self):
        br.browser.refresh()
        time.sleep(3)

    @staticmethod
    def goto():
        """进入配置管理"""
        time.sleep(2)
        br.browser.find_element_by_id('/message').click()
        time.sleep(1)
        br.browser.find_element_by_id('notice').click()

    def case1(self):
        u"""公告新增"""
        self.goto()
        time.sleep(1)
        br.browser.find_element_by_id('tableAdd').click()

        time.sleep(1)
        br.browser.find_element_by_id('orgName').send_keys(self.jsoninfo["case1"]["orgName"])
        br.browser.find_element_by_id('manageUser').send_keys(self.jsoninfo["case1"]["manageUser"])
        br.browser.find_element_by_id('password').send_keys(self.jsoninfo["case1"]["password"])
        br.browser.find_element_by_id('contactUser').send_keys(self.jsoninfo["case1"]["contactUser"])
        br.browser.find_element_by_id('contactPhone').send_keys(self.jsoninfo["case1"]["contactPhone"])
        br.browser.find_element_by_id('contactAddress').send_keys(self.jsoninfo["case1"]["contactAddress"])
        br.browser.find_element_by_id('submit').click()

        time.sleep(2)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case1"]["manageUser"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case1"]["manageUser"]).is_enabled()
        self.assertTrue(result, u"新建失败")

    def case2(self):
        u"""公告删除"""
        self.goto()
        time.sleep(1)
        br.browser.find_element_by_id('keyWord').send_keys(self.jsoninfo["case2"]["orgName"])
        br.browser.find_element_by_id('tableSearch').click()

        time.sleep(1)
        br.browser.find_element_by_id('delete-' + self.jsoninfo["case2"]["orgName"]).click()
        br.browser.find_element_by_id("confirm").click()

        time.sleep(1)
        result = br.browser.find_element_by_id('edit-' + self.jsoninfo["case2"]["orgName"]).is_enabled()
        self.assertTrue(result, u"编辑失败")


class Qxgl(unittest.TestCase):
    u"""权限管理"""

    @classmethod
    def setUpClass(cls):
        jsonfile = open("jsondata/qxgl.json", "r", encoding="utf-8")
        cls.jsoninfo = json.load(jsonfile)

    def tearDown(self):
        br.browser.refresh()
        time.sleep(3)

    @staticmethod
    def goto_cygl():
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

        time.sleep(1)
        br.browser.find_element_by_name('roleName').send_keys(self.jsoninfo["member"]["case5"]["roleName"])
        br.browser.find_element_by_name('tableSearch').click()

        # 角色未完成





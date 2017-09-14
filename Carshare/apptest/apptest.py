# operating_deck:Windows
# coding=utf-8
# creat by 15025463191 2017/08/22

import time

class Swipe:
    def __init__(self, driver):
        self.driver = driver

    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def swipeUp(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipeDown(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.25)
        y2 = int(l[1] * 0.75)
        self.driver.swipe(x1, y1, x1, y2, t)

    def swipLeft(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.05)
        self.driver.swipe(x1, y1, x2, y1, t)

    def swipRight(self, t):
        l = self.getSize()
        x1 = int(l[0] * 0.05)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)


class TestEvent:
    def __init__(self, driver, username, password, peccancytime):
        self.driver = driver
        self.username = username
        self.password = password
        self.peccancytime = peccancytime
        self.swipe = Swipe(self.driver)

    def setup(self):
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/iv_baidu_three").click()

    def login(self, phone, passwd):
        u"""登陆"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_login").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_login_username").send_keys(phone)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_login_pwd").send_keys(passwd)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_login_login").click()

    def changepasswd(self):
        u"""修改密码"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_left_head").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_user_center_change_pwd").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/bt_change_pwd_getcode").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_change_pwd_code").send_keys("6666")
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_change_pwd_pwd1").send_keys(self.password)
        if self.password == "456789":
            self.password = "123456"
        else:
            self.password = "456789"
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_change_pwd_pwd2").send_keys(self.password)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_change_pwd_pwd3").send_keys(self.password)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_change_pwd_sure").click()
        self.login(self.username, self.password)

    def order(self):
        u"""订单"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_order").click()
        self.swipe.swipeUp(2000)
        time.sleep(1)
        self.swipe.swipeDown(1000)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()

    def coupon(self):
        u"""优惠券"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_money").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_wallet_youhuijuan").click()
        self.swipe.swipeUp(1000)
        time.sleep(1)
        self.swipe.swipeDown(1000)
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()

    def refund(self):
        u"""退押金"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_money").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_wallet_return_deposit").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_wallet_wxpay").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_wallet_alipay").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_wallet_wxpay").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_wallet_alipay").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_return_deposit_p").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()

    def invoice(self, OrdinaryorSpecial=1, EleorPapr=1, CmpanyorPri=1):
        u"""发票"""
        # OrdinaryorSpecial= random.choice([1, 2])
        # EleorPapr= random.choice([1, 2])
        # CmpanyorPri= random.choice([1, 2])
        # print OrdinaryorSpecial + ";" + EleorPapr + ";" + CmpanyorPri
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_money").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_wallet_invoice").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_invoice_select").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/iv_invoice_next").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_positive").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_taxpayer_id").send_keys("123456789")
        if OrdinaryorSpecial == 1:
            if CmpanyorPri == 1:
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_rise").send_keys(u"普通公司发票")
            else:
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rb_invoice_type_personal").click()
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_rise").send_keys(u"普通个人发票")

            if EleorPapr == 1:
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_email").send_keys(
                    "401219180@qq.com")
            else:
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rb_invoice_mode_paper").click()
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_addressee").send_keys(u"纸质发票")
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_adress").send_keys(u"重庆纸质XXX")
            self.swipe.swipeUp(500)
        else:
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rb_invoice_vip").click()
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_rise").send_keys(u"专用公司发票")
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_code").send_keys("123456789")
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_bank").send_keys(u"农业银行")
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_account").send_keys(
                "6214830286959969")
            self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_adress").send_keys(
                u"重庆光电园农业银行支行")
            if EleorPapr == 1:
                self.swipe.swipeUp(500)
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_phone").send_keys("68452189")
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_email").send_keys(
                    "401219180@qq.com")
            else:
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rb_invoice_mode_paper").click()
                self.swipe.swipeUp(500)
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_incoice_vip_phone").send_keys("68452189")
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_addressee").send_keys(u"纸质发票")
                self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_adress").send_keys(u"重庆纸质XXX")

        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_invoice_phone").send_keys("15025463191")
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_invoice_sure").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()

    def representation(self):
        u"""申诉"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_fankui").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/et_feedback_problem").send_keys(u"自动化申诉")
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/iv_feedback_user").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/check_view").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/button_apply").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_feedback_submit").click()

    def peccancy(self):
        """违章"""
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/ll_left_weizhang").click()
        self.driver.find_element_by_name(self.peccancytime).click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()
        self.driver.find_element_by_id("com.mysirui.carshare.carshare:id/rl_title_bar_back").click()

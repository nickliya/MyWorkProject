# operating_deck:Windows
# coding=utf-8
# creat by 15025463191 2017/08/22
import selenium

from apptest import *
from appium import webdriver
import random

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '4.4.1',
    # 'deviceName': 'ce0916094b47d61005',  # samsung
    # 'deviceName': 'CAI7QSCM5H8HFU8T',  # oppo
    'deviceName': 'HT65G0101207',  # HTC
    # 'deviceName': '8362d0dc',  # 联想
    # 'deviceName': 'GWY0217122005515',  # HUAWEI
    'appPackage': 'com.mysirui.carshare.carshare',
    'appActivity': '.ui.HomeActivity',
    'unicodeKeyboard': 'True',
    'resetKeyboard': 'True'
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(3)
testfun = TestEvent(driver, "15025463191", "456789", "2017-08-11 15:55:55")
try:
    driver.find_element_by_id("com.mysirui.carshare.carshare:id/tv_coupon_confirm").click()
except selenium.common.exceptions.NoSuchElementException, msg:
    print msg
driver.find_element_by_id("com.mysirui.carshare.carshare:id/iv_baidu_three").click()


class Testapp:
    def __init__(self):
        self.driver = driver

    def test_changepasswd(self):
        testfun.changepasswd()

    def test_order(self):
        testfun.order()

    def test_coupon(self):
        testfun.coupon()

    def test_refund(self):
        testfun.refund()

    def test_invoice(self):
        OrdinaryorSpecial= random.choice([1, 2])
        EleorPapr= random.choice([1, 2])
        CmpanyorPri= random.choice([1, 2])
        print str(OrdinaryorSpecial) + ";" + str(EleorPapr) + ";" + str(CmpanyorPri)
        testfun.invoice(OrdinaryorSpecial, EleorPapr, CmpanyorPri)

    def test_representation(self):
        testfun.representation()

    def test_peccancy(self):
        testfun.peccancy()


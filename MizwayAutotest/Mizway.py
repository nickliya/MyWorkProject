# operating_deck:Windows
# coding=utf-8
# creat by 15025463191 2017/06/08

import time
import socket
import re
from appium import webdriver
import requests
import random
import string
import HTMLTestRunner
import unittest
import sys
import pymssql

test_method_name = 1


def getSize():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return x, y


def swipeUp(t):
    l = getSize()
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.75)
    y2 = int(l[1] * 0.25)
    driver.swipe(x1, y1, x1, y2, t)


def swipeDown(t):
    l = getSize()
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.25)
    y2 = int(l[1] * 0.75)
    driver.swipe(x1, y1, x1, y2, t)


def swipLeft(t):
    l = getSize()
    x1 = int(l[0] * 0.75)
    y1 = int(l[1] * 0.5)
    x2 = int(l[0] * 0.05)
    driver.swipe(x1, y1, x2, y1, t)


def swipRight(t):
    l = getSize()
    x1 = int(l[0] * 0.05)
    y1 = int(l[1] * 0.5)
    x2 = int(l[0] * 0.75)
    driver.swipe(x1, y1, x2, y1, t)


def decision():
    protocol_dic = {
        "511": u"上锁", "512": u"解锁", "513": u"寻车", "514": u"静音", "515": u"点火",
        "516": u"熄火", "517": u"关门窗", "518": u"开门窗", "519": u"关天窗", "51A": u"开天窗",
        "51B": u"通油", "51C": u"断油", }
    data = s.recv(1024)
    r = r'\(\*..\|7\|\d\d\w,\w*?,1\|\)'
    datainfo = re.findall(r, data)
    try:
        str_data = str(datainfo[0])
        print('recv:' + protocol_dic[str_data[7:10]] + str_data)
        a = str_data[0] + '1' + str_data[1:5] + '8' + str_data[6:]
        s.send(a)
        print('send:' + a)
        b = a[0:6] + '7|4' + a[9:12] + '1,1|)'
        s.send(b)
        print(b)
    except IndexError, msg:
        print msg


def Auto_dl():
    u'登陆'
    driver.find_element_by_id('com.sirui.ui:id/username').send_keys(username)
    driver.find_element_by_id('com.sirui.ui:id/password').send_keys(passwd)
    driver.find_element_by_id('com.sirui.ui:id/buttonLogin').click()


def passwdfy():
    u'防密码校验'
    try:
        driver.find_element_by_id('com.sirui.ui:id/editView').send_keys(passwd)
    except:
        pass
    sys.exc_clear()


#####操作事件#####
class event(unittest.TestCase):
    def dl(self):
        u'登陆'
        driver.find_element_by_id('com.sirui.ui:id/username').send_keys(username)
        driver.find_element_by_id('com.sirui.ui:id/password').send_keys(passwd)
        driver.find_element_by_id('com.sirui.ui:id/buttonLogin').click()

    def zx(self):
        u'注销'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/accountSecurity').click()
        driver.find_element_by_id('com.sirui.ui:id/logOutText').click()

    def zc(self):
        u'注册'
        driver.find_element_by_id('com.sirui.ui:id/register_account').click()
        driver.find_element_by_id('com.sirui.ui:id/mobile').send_keys(phone_num)
        driver.find_element_by_id('com.sirui.ui:id/register_get_captcha').click()
        # url='http://192.168.6.52:8080/provider/testProvide/sendAuthCode?phone=13508320770'
        # def get_identifyingcode(url):
        #     r=requests.get(url)
        #     info=r.text
        #     code=info[23:27]
        #     return code
        # i_code=get_identifyingcode(url)
        driver.find_element_by_id('com.sirui.ui:id/regisetr_captcha').send_keys('1521')
        driver.find_element_by_id('com.sirui.ui:id/password').send_keys('123456')
        driver.find_element_by_id('com.sirui.ui:id/register_button').click()
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/accountSecurity').click()
        driver.find_element_by_id('com.sirui.ui:id/logOutText').click()
        driver.find_element_by_id('com.sirui.ui:id/username').send_keys(phone_num)
        driver.find_element_by_id('com.sirui.ui:id/password').send_keys('123456')
        driver.find_element_by_id('com.sirui.ui:id/buttonLogin').click()

    def bk(self):
        u'来回切地图测崩溃'
        driver.implicitly_wait(3)
        for i in range(30):
            driver.find_element_by_id('com.sirui.ui:id/location').click()
            driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def map(self):
        u'测崩溃'
        driver.implicitly_wait(3)
        driver.find_element_by_id('com.sirui.ui:id/location').click()
        el = driver.find_element_by_class_name('android.view.View')
        time.sleep(2)
        driver.pinch(el, 20)  # 值越高缩小越多
        time.sleep(3)
        driver.zoom(el)
        driver.find_element_by_id('com.sirui.ui:id/buttonUserLocation').click()
        time.sleep(3)
        driver.find_element_by_id('com.sirui.ui:id/buttonCarLocation').click()
        time.sleep(3)
        driver.find_element_by_id('com.sirui.ui:id/buttonMapSwitch').click()
        time.sleep(3)
        driver.find_element_by_id('com.sirui.ui:id/buttonUserLocation').click()
        time.sleep(3)
        driver.find_element_by_id('com.sirui.ui:id/buttonCarLocation').click()
        el2 = driver.find_element_by_class_name('android.view.View')
        # driver.switch_to.context("NATIVE_APP")
        # ActionChains(driver).double_click(el2).perform()
        # driver.find_element_by_id('com.sirui.ui:id/back_text').click()


class app(unittest.TestCase):
    def setUp(self):
        sys.exc_clear()
        driver.find_element_by_name('我').click()

    def zhaq_1(self):
        u'更改用户名'
        driver.find_element_by_id('com.sirui.ui:id/accountSecurity').click()
        driver.find_element_by_name('更改用户名').click()
        driver.implicitly_wait(3)
        global username
        username = ''.join(random.choice(string.digits + string.uppercase) for i in range(6))
        driver.find_element_by_id('com.sirui.ui:id/username').send_keys(username)
        driver.find_element_by_id('com.sirui.ui:id/finish').click()
        driver.find_element_by_id('com.sirui.ui:id/editView').send_keys(passwd)
        name = driver.find_element_by_id('com.sirui.ui:id/text_custUserName').get_attribute('name')
        if name == username:
            print u'修改成功:' + username
        else:
            test_method_name = self._testMethodName
            driver.save_screenshot("C:\Users\YangQ\Desktop\%s.jpg" % test_method_name)
            print u'修改失败，应为：' + username
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def zhaq_2(self):
        u'更改密码'
        driver.find_element_by_id('com.sirui.ui:id/accountSecurity').click()
        driver.find_element_by_name('更改密码').click()
        driver.implicitly_wait(3)
        global passwd
        driver.find_element_by_id('com.sirui.ui:id/old_password').send_keys(passwd)
        if int(passwd) == 123456:
            passwd = '456789'
        else:
            passwd = '123456'
        driver.find_element_by_id('com.sirui.ui:id/password').send_keys(passwd)
        print passwd
        driver.find_element_by_id('com.sirui.ui:id/show_password').clear()
        passtext = driver.find_element_by_id('com.sirui.ui:id/password').get_attribute('name')
        if passtext == passwd:
            print u'密码显示功能正常'
        else:
            print u'密码显示功能失败'
        driver.find_element_by_id('com.sirui.ui:id/finish').click()
        driver.find_element_by_id('com.sirui.ui:id/logOutText').click()
        driver.implicitly_wait(3)
        Auto_dl()

    def zdgl_1(self):
        u'添加车辆'
        driver.implicitly_wait(3)
        driver.find_element_by_id('com.sirui.ui:id/terminalManage').click()
        driver.find_element_by_name('终端更换或添加').click()
        driver.find_element_by_id('com.sirui.ui:id/scanBrand').click()
        time.sleep(2)
        driver.find_element_by_name('ALPINA').click()
        driver.find_element_by_name('B4 BITURBO').click()
        driver.find_element_by_name('2016款 B4 BITURBO Coupe').click()
        driver.find_element_by_id('com.sirui.ui:id/buttonDone').click()
        conn = pymssql.connect(host=sqlserver_ip, user='sa', password=sqlserver_passwd)
        cur = conn.cursor()
        cur.execute("SELECT IMEI FROM [sirui].[dbo].[Terminal] where Status='2' and ClientType='3'")
        info = random.choice(cur.fetchall())
        global IMEI
        IMEI = str(info)[3:-3]
        driver.find_element_by_id('com.sirui.ui:id/terminalNumber').send_keys(IMEI)
        driver.find_element_by_id('com.sirui.ui:id/finish').click()
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def zdgl_2(self):
        u'终端更换'
        driver.find_element_by_id('com.sirui.ui:id/terminalManage').click()
        driver.find_element_by_name('终端更换或添加').click()
        driver.find_element_by_id('com.sirui.ui:id/plateNumber').click()
        driver.find_element_by_id('android:id/button1').click()
        time.sleep(1)
        # conn=pymssql.connect(host=sqlserver_ip,user='sa',password=sqlserver_passwd)
        # cur=conn.cursor()
        # cur.execute("SELECT IMEI FROM [sirui].[dbo].[Terminal] where Status='2' and ClientType='3'")
        # info = random.choice(cur.fetchall())
        global IMEI
        # IMEI = str(info)[3:-3]
        if IMEI == '862446035389644':
            IMEI = '862446035392325'
        else:
            IMEI = '862446035389644'
        driver.find_element_by_id('com.sirui.ui:id/terminalNumber').send_keys(IMEI)
        print IMEI
        driver.find_element_by_id('com.sirui.ui:id/finish').click()
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def yyqd(self):
        u'预约启动'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/orderStart').click()
        driver.implicitly_wait(3)
        driver.find_element_by_id('com.sirui.ui:id/add').click()
        driver.implicitly_wait(3)
        driver.find_element_by_name('重复').click()
        driver.find_element_by_id('com.sirui.ui:id/bt_Wed').click()
        driver.find_element_by_id('com.sirui.ui:id/bt_Sun').click()
        driver.find_element_by_id('com.sirui.ui:id/sure_textview').click()
        driver.find_element_by_name('车辆').click()
        driver.find_element_by_id('android:id/button1').click()
        driver.find_element_by_name('启动时长').click()
        driver.find_element_by_id('android:id/button1').click()
        driver.find_element_by_id('com.sirui.ui:id/finish').click()
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def xxzx(self):
        u'消息中心'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/messageCenter').click()
        driver.implicitly_wait(3)
        driver.find_element_by_name('告警类').click()
        swipeDown(1000)
        driver.implicitly_wait(3)
        driver.find_element_by_name('提醒类').click()
        time.sleep(1)
        swipeDown(1000)
        driver.implicitly_wait(3)
        driver.find_element_by_name('推送类').click()
        time.sleep(1)
        swipeDown(1000)
        driver.implicitly_wait(3)
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def clzl(self):
        u'车辆资料'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/vehicleInfo').click()
        plate_num = u'渝' + ''.join(random.choice(string.digits + string.uppercase) for i in range(6))
        driver.find_element_by_class_name('android.widget.EditText').clear()
        driver.find_element_by_class_name('android.widget.EditText').send_keys(plate_num)
        driver.find_element_by_id('com.sirui.ui:id/save').click()
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()
        driver.find_element_by_name('车卫士').click()
        car_name = driver.find_element_by_id('com.sirui.ui:id/plate_number').get_attribute('name')
        if car_name == plate_num:
            print u'修改车牌成功'
        else:
            test_method_name = self._testMethodName
            driver.save_screenshot("C:\Users\YangQ\Desktop\%s.jpg" % test_method_name)
            print u'修改车牌失败，应为：' + plate_num

    def zxkf(self):
        u'在线客服'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/onlineService').click()
        driver.find_element_by_id('com.sirui.ui:id/sendText').send_keys('Autotest')
        driver.find_element_by_id('com.sirui.ui:id/send').click()
        swipeUp(1000)
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def gywm(self):
        u'关于我们'
        driver.find_element_by_name('我').click()
        driver.find_element_by_id('com.sirui.ui:id/about').click()
        driver.implicitly_wait(3)
        driver.find_element_by_name('功能介绍').click()
        time.sleep(1)
        swipeUp(2000)
        time.sleep(1)
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()
        driver.find_element_by_name('帮助').click()
        time.sleep(2)
        swipeUp(2000)
        time.sleep(1)
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()
        driver.implicitly_wait(3)
        driver.find_element_by_name('推荐我们').click()
        driver.find_element_by_name('取消').click()
        driver.find_element_by_id('com.sirui.ui:id/back_text').click()

    def tearDown(self):
        if sys.exc_info()[0]:
            global test_method_name
            print sys.exc_info()
            print test_method_name
            # test_method_name = self._testMethodName
            driver.save_screenshot("C:\Users\YangQ\Desktop\%s.jpg" % test_method_name)
            test_method_name = test_method_name + 1
            sys.exc_clear()
            driver.close_app()
            time.sleep(1)
            driver.launch_app()
            time.sleep(3)
            Auto_dl()
        else:
            pass
            # super(control, self).tearDown()

s = None


class control(unittest.TestCase):
    def setUp(self):
        sys.exc_clear()
        driver.find_element_by_name('车卫士').click()
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((tcp_ip, int(tcp_port)))
        s.send('(1*7c|a3|106,201|101,' + str(
            IMEI) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
        # s.send('(1*7c|a3|106,201|101,867715028812928|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
        time.sleep(2)

    def qd(self):
        u'启动'
        s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')
        driver.find_element_by_id('com.sirui.ui:id/startEngine').click()
        passwdfy()
        try:
            driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        except:
            pass
        sys.exc_clear()
        decision()

    def xc(self):
        u'寻车'
        s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')
        driver.find_element_by_id('com.sirui.ui:id/btn_car_call').click()
        passwdfy()
        try:
            driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        except:
            pass
        sys.exc_clear()
        decision()

    def jc(self):
        u'降窗'
        s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')
        driver.find_element_by_id('com.sirui.ui:id/carLinearlayout').click()
        driver.find_element_by_id('com.sirui.ui:id/car_fall_window').click()
        passwdfy()
        try:
            driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        except:
            pass
        sys.exc_clear()
        decision()
        # '升窗'
        time.sleep(2)
        driver.find_element_by_id('com.sirui.ui:id/car_rose_window').click()
        driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        decision()
        # 开天窗
        time.sleep(2)
        driver.find_element_by_id('com.sirui.ui:id/car_open_sunroof').click()
        driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        decision()
        # 关天窗
        time.sleep(2)
        driver.find_element_by_id('com.sirui.ui:id/car_close_sunroof').click()
        driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        decision()
        # #上锁
        # time.sleep(1)
        # driver.find_element_by_id('com.sirui.ui:id/car_lock').click()
        # time.sleep(3)
        # driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        # decision()
        # #解锁
        # time.sleep(1)
        # driver.find_element_by_id('com.sirui.ui:id/car_unlock').click()
        # time.sleep(3)
        # driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        # decision()
        # #熄火
        # time.sleep(1)
        # driver.find_element_by_id('com.sirui.ui:id/car_shut_down').click()
        # time.sleep(3)
        # driver.find_element_by_id('com.sirui.ui:id/confirm').click()
        # decision()
        time.sleep(2)
        driver.find_element_by_id('com.sirui.ui:id/arrows').click()

    def tearDown(self):
        s.shutdown(2)
        s.close()
        if sys.exc_info()[0]:
            global test_method_name
            print sys.exc_info()
            print test_method_name
            driver.save_screenshot("C:\Users\YangQ\Desktop\%s.jpg" % test_method_name)
            test_method_name += 1
            sys.exc_clear()
            driver.close_app()
            time.sleep(1)
            driver.launch_app()
            time.sleep(3)
            Auto_dl()
        else:
            pass


#####操作事件#####

##################################测试编辑##################################
username = 'W4SL6Z'
passwd = '123456'
IMEI = '869651023077811'
phone_num = '15025463191'
tcp_ip = '192.168.6.52'
tcp_port = '2103'
sqlserver_ip = '192.168.6.51'
sqlserver_passwd = 'test2017'
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0.1'
# desired_caps['deviceName'] = 'CAI7QSCM5H8HFU8T'  #oppo
# desired_caps['deviceName'] = 'ce0916094b47d61005'  # samsung
desired_caps['deviceName'] = 'HT65G0101207'  #HTC
# desired_caps['deviceName'] = '8362d0dc'  #联想
# desired_caps['deviceName'] = 'GWY0217122005515'  #HUAWEI
desired_caps['appPackage'] = 'com.sirui.ui'
desired_caps['appActivity'] = '.activity.SplashActivity'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(3)

#####自动登录#####
try:
    Auto_dl()
except:
    pass
sys.exc_clear()
#####自动登录#####

casedic = {'更改用户名': "zhaq_1", '更改密码': "zhaq_2", '终端更换': "zdgl_2", '预约启动': "yyqd",
           '消息中心': "xxzx", '车辆资料': "clzl", '在线客服': "zxkf", '关于我们': "gywm", '启动': "qd",
           '寻车': "xc", '降窗': "jc"
           }

testunit = unittest.TestSuite()
# testunit.addTest(event('bk'))  #添加用例
# testunit.addTest(app('zdgl_1'))
for i in range(30):
    case = random.choice(casedic.items())[1]
    if case == 'qd' or case == 'xc' or case == 'jc':
        testunit.addTest(control(case))
        print case
    else:
        testunit.addTest(app(case))
        print case
##################################测试编辑##################################

HtmlFile = 'C:\Users\YangQ\Desktop\AppResult.html'  # 结果文件生成路径
fp = open(HtmlFile, "wb")
runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'咪智汇自动化测试', description=u'用例测试情况')
runner.run(testunit)
time.sleep(10)
driver.close_app()

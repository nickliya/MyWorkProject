#coding=utf-8
import time
import socket
import re
from appium import webdriver

IMEI = input('请输入IMEI号：')
admin = raw_input('请输入账号:')
passwd = raw_input('请输入密码:')
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
# desired_caps['deviceName'] = '99KSAQPF99999999'
# desired_caps['deviceName'] = 'ce0916094b47d61005'
desired_caps['deviceName'] = 'CAI7QSCM5H8HFU8T'
desired_caps['appPackage'] = 'com.chinapke.sirui'
desired_caps['appActivity'] = '.ui.activity.LoadingActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
time.sleep(5)
driver.find_element_by_id('com.chinapke.sirui:id/textAccount').send_keys(admin)
driver.find_element_by_id('com.chinapke.sirui:id/textPassword').send_keys(passwd)
driver.find_element_by_id('com.chinapke.sirui:id/buttonLogin').click()

time.sleep(5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.6.52',2103))
s.send('(1*7c|a3|106,201|101,'+str(IMEI)+'|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')

print('device is online')
time.sleep(2)
s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')

driver.find_element_by_id('com.chinapke.sirui:id/buttonCalling').click()
driver.find_element_by_id('com.chinapke.sirui:id/sure_textview').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)

def panding():
    time.sleep(2)
    data = s.recv(1024)
    r = r'\(\*..\|7\|\d\d\w,\w*?,1\|\)'
    datainfo = re.findall(r,data)
    str_data = str(datainfo[0])
    print('recv:'+str_data)
    a = str_data[0]+'1'+str_data[1:5]+'8'+str_data[6:]
    s.send(a)
    print('send:'+a)
    b = a[0:6]+'7|4'+a[9:12]+'1,1|)'
    s.send(b)
    print(b)

panding()

driver.implicitly_wait(2)
driver.find_element_by_id('com.chinapke.sirui:id/buttonLockOff').click()
driver.find_element_by_id('com.chinapke.sirui:id/sure_textview').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
panding()

driver.implicitly_wait(2)
driver.find_element_by_id('com.chinapke.sirui:id/buttonEngineOn').click()
driver.find_element_by_id('com.chinapke.sirui:id/sure_textview').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
panding()

driver.implicitly_wait(2)
driver.find_element_by_id('com.chinapke.sirui:id/buttonEngineOff').click()
driver.find_element_by_id('com.chinapke.sirui:id/sure_textview').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
panding()

# driver.implicitly_wait(2)
# driver.find_element_by_id('com.chinapke.sirui:id/buttonLockOn').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
# panding()
#
# driver.find_element_by_id('com.chinapke.sirui:id/rb_tab_my').click()
# # driver.implicitly_wait(2)
# driver.find_element_by_id('com.chinapke.sirui:id/ll_account_security').click()
# # driver.implicitly_wait(2)
# driver.find_element_by_id('com.chinapke.sirui:id/layout_oil').click()
# # driver.implicitly_wait(2)
# driver.find_element_by_id('com.chinapke.sirui:id/ctrl_oil_on').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
# panding()
# driver.implicitly_wait(2)
# driver.find_element_by_id('com.chinapke.sirui:id/ctrl_oil_off').click()
# driver.find_element_by_id('com.chinapke.sirui:id/inputPopUp').send_keys(passwd)
# panding()
# driver.implicitly_wait(2)

s.close()
print('Test was completed,The app will be closed in 5 sec later')
time.sleep(5)
driver.close_app()
#coding=utf-8
import time
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '4.4.2'
# desired_caps['deviceName'] = 'HT65G0101207'
# desired_caps['deviceName'] = 'ce0916094b47d61005'
desired_caps['deviceName'] = 'YT910XP3R9'
desired_caps['appPackage'] = 'com.mysirui.om'
desired_caps['appActivity'] = '.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

print('now is app')
time.sleep(17)
print('开始测试')
# driver.find_element_by_name('密码').send_keys('123456')

x=driver.get_window_size()['width']
y=driver.get_window_size()['height']
x1=1
y1=int(int(y)*0.5)
x2=int(int(x)*0.75)


driver.swipe(x1,y1,x2,y1)

time.sleep(10)
driver.close_app()

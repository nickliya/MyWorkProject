#coding=utf-8
from selenium import webdriver
import time
import pymssql
import random
import string
import sys
from selenium.webdriver.support.ui import Select
import unittest
from selenium.webdriver.common.keys import Keys

chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(chromepath)
browser.get('http://192.168.1.151:3000/static/login.html')
browser.find_element_by_name('user').send_keys('admin')
browser.find_element_by_name('pw').send_keys('Wg123456')
input(u'请在网页手动输入验证码:'.encode('gbk'))
browser.find_element_by_partial_link_text('提交').click()
browser.implicitly_wait(5)
time.sleep(1)
browser.maximize_window()
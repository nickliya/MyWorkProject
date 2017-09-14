#/usr/bin/python
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
# browser.get('http://192.168.6.52:8090/')
browser.get('http://192.168.6.205:3000/static/sys/user/login.html')
browser.find_element_by_name('user').send_keys('admin')
browser.find_element_by_name('pw').send_keys('Sys123456')
browser.find_element_by_name('inputRandomCode').send_keys('zxcv')
time.sleep(2)
browser.find_element_by_name('submit').click()
browser.implicitly_wait(5)
time.sleep(1)
browser.maximize_window()

time.sleep(3)
browser.find_element_by_name('t_1').click()
browser.find_element_by_name('t_1-1').click()
browser.find_element_by_link_text('删除').send_keys('zxcv')

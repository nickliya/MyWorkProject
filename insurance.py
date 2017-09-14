#/usr/bin/python
#coding=utf-8
from selenium import webdriver
import random

phone = random.choice(['139','188','185','136','158','151'])+''.join(random.choice("0123456789") for i in range(8))
idcard = '5'+''.join(random.choice("0123456789") for i in range(17))
price = ''.join(random.choice("123456789") for i in range(6))+'.'+''.join(random.choice("0123456789") for i in range(3))
chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(chromepath)
browser.get('http://192.168.6.148:60/')
browser.find_element_by_id('name').send_keys('gaomin')
browser.find_element_by_id('password').send_keys('123456')
browser.find_element_by_id('loginButton').click()
browser.implicitly_wait(5)

def bxcompany():
    browser.find_element_by_link_text('保险公司').click()
    browser.find_element_by_link_text('保险公司管理').click()
    browser.find_element_by_id('addModalBtn').click()
    company = raw_input('公司名称:'.decode('utf-8').encode('gbk'))
    Insurance_num = input('保险单号:'.decode('utf-8').encode('gbk'))
    browser.find_element_by_id('name').send_keys(company.decode('utf-8').encode('gbk')).decode('gbk')
    browser.find_element_by_id('policyNum').send_keys(Insurance_num)
    browser.find_element_by_class_name('layui-upload-file').click()
    input('请上传附件，完成后输入1:'.decode('utf-8').encode('gbk'))
    browser.find_element_by_id('addBtn').click()

def bdxz():
    browser.find_element_by_link_text('保单').click()
    browser.find_element_by_link_text('保单管理').click()
    browser.find_element_by_id('addModalBtn').click()
    browser.find_element_by_id('ownerMobile').send_keys(phone)
    browser.find_element_by_id('contactAddress').send_keys('chongqing')
    browser.find_element_by_id('ownerIdentifyNum').send_keys(idcard)
    browser.find_element_by_id('brandModel').send_keys('11')
    browser.find_element_by_id('vinCode').send_keys('LJDJAA147D0214447')
    browser.find_element_by_id('engineNumber').send_keys('11')
    browser.find_element_by_id('price').send_keys(price)
    browser.find_element_by_id('vinCode').send_keys('LJDJAA147D0214447')
    browser.find_element_by_id('billingDate').click()
    browser.find_element_by_id('laydate_ok').click()
    browser.find_element_by_id('serialNum').send_keys('C1000000018')
    browser.find_element_by_id('loanTime').send_keys('11')

kzl = input('1.保险公司新增\n2.保单在线投保\n请输入'.decode('utf-8').encode('gbk'))
if kzl==1:
    bxcompany()
elif kzl==2:
    bdxz()
else:print('谢谢使用')
#/usr/bin/python
#coding=utf-8
#creat by 15025463191 2017/5/2
from selenium import webdriver
import time
import pymssql
import random
import string
import sys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
phone = random.choice(['139','188','185','136','158','151'])+''.join(random.choice("0123456789") for i in range(8))
plate_num = u'渝'+''.join(random.choice(string.uppercase) for i in range(1))+''.join(random.choice(string.digits)for i in range(6))
frame_num = ''.join(random.choice(string.letters) for i in range(16))
cusadmin = ''.join(random.choice(string.letters) for i in range(6))
cuspasswd = random.choice(string.uppercase)+random.choice(string.lowercase)+''.join(random.choice("0123456789") for i in range(6))
idcard = '5'+''.join(random.choice("0123456789") for i in range(17))
price = ''.join(random.choice("123456789") for i in range(6))+'.'+''.join(random.choice("0123456789") for i in range(3))

chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(chromepath)
browser.get('http://192.168.6.148:8080/')
browser.find_element_by_id('name').send_keys('yqmd')
browser.find_element_by_id('password').send_keys('Wg123456')
input(u'请在网页手动输入验证码:'.encode('gbk'))
browser.find_element_by_id('loginButton').click()
browser.implicitly_wait(5)
time.sleep(1)
browser.maximize_window()

def xgmm():
    browser._switch_to.frame('iframepage')
    browser._switch_to.frame('header')
    browser.find_element_by_xpath("//*[contains(@href,'/purview/user/toChangePassword')]").click()
    time.sleep(1)
    browser._switch_to.parent_frame()
    browser._switch_to.frame('middleframe')
    browser.find_element_by_id('oldPassword').send_keys(sys.argv[2])
    input(u'请在网页手动输入新密码:'.encode('gbk'))

def xzkh():
    browser._switch_to.frame('iframepage')
    browser._switch_to.frame('leftframe')
    browser.find_element_by_id('idMenu2_1').click()
    time.sleep(1)
    browser.find_element_by_id('jcsj').click()
    browser.find_element_by_link_text('客户管理').click()
    time.sleep(1)
    browser._switch_to.parent_frame()
    browser._switch_to.frame('middleframe')
    browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
    #####数据库查找主机号码#####
    conn=pymssql.connect(host='192.168.6.70',user='sa',password='123456')
    cur=conn.cursor()
    cur.execute("SELECT BarCode FROM [sirui].[dbo].[Terminal] where Status=2 and BarCode like 'ot%'")
    info = random.choice(cur.fetchall())
    a = str(info)[3:-3]
    print a
    carhost_num = str(info)[3:-3]
    cur.close()
    conn.close()
    #####数据库查找主机号码#####
    browser.find_element_by_id('Terminal_barCode').send_keys(carhost_num)
    browser.find_element_by_id('vehicleModelID_select').click()
    browser.find_element_by_id('_divBrand').click()
    browser.find_element_by_link_text('未定义').click()
    time.sleep(1)
    browser.find_element_by_id('_divSeries').click()
    browser.find_element_by_link_text('未定义').click()
    time.sleep(1)
    browser.find_element_by_id('_divSpec').click()
    browser.find_element_by_link_text('未定义').click()
    browser.find_element_by_id('plateNumber').send_keys(plate_num)
    browser.find_element_by_id('vin').send_keys(frame_num)
    browser.find_element_by_id('giftMaintenanceTimes').send_keys('1')
    browser.find_element_by_id('customerUserName').send_keys(cusadmin)
    browser.find_element_by_id('customerPhone').send_keys(phone)
    browser.find_element_by_id('customerPassword').send_keys(cuspasswd)
    browser.find_element_by_id('customerConfirmPassword').send_keys(cuspasswd)
    time.sleep(1)
    browser.find_element_by_class_name('form_button').click()
    print 'your admin: '+cusadmin
    print 'your password: '+cuspasswd

def xzmd():
    browser._switch_to.frame('iframepage')
    browser._switch_to.frame('leftframe')
    browser.find_element_by_id('idMenu2_1').click()
    time.sleep(1)
    browser.find_element_by_id('xtgl').click()
    browser.find_element_by_link_text('门店管理').click()
    time.sleep(1)
    browser._switch_to.parent_frame()
    browser._switch_to.frame('middleframe')
    browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
    time.sleep(1)
    browser.find_element_by_id('treeDemo_4_switch').click()
    time.sleep(1)
    browser.find_element_by_id('treeDemo_15_check').click()
    time.sleep(1)
    browser.find_element_by_id('treeDemo_103_check').click()
    mdname=''.join(random.choice(string.letters) for i in range(6))
    browser.find_element_by_id('name').send_keys(mdname)
    city = browser.find_element_by_id('province')
    Select(city).select_by_index(random.choice(range(13)))
    browser.find_element_by_id('address').click()
    browser.implicitly_wait(3)
    browser._switch_to.frame('xubox_iframe1')
    browser.find_element_by_css_selector('#textarea>input').send_keys('chongqing')
    browser.find_element_by_xpath("//*[contains(@value,'查询')]").click()
    browser._switch_to.parent_frame()
    browser.find_element_by_xpath("//*[@id='xubox_layer1']/div[1]/span[1]/a[3]").click()
    browser.find_element_by_id('contractPerson').send_keys(mdname)
    browser.find_element_by_id('contractPersonPhone').send_keys(phone)
    browser.find_element_by_xpath("//*[@id='addForm']/div/div/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/button").click()
    print 'mdname:'+mdname

def bdxz():
    browser._switch_to.frame('iframepage')
    browser._switch_to.frame('leftframe')
    browser.find_element_by_id('idMenu2_1').click()
    time.sleep(1)
    browser.find_element_by_id('yxgl').click()
    time.sleep(1)
    browser.find_element_by_xpath("//*[contains(@href,'JSESSIONID=72FADAFA8E70181E2FD4DC57FE9691CB')").click()
    browser._switch_to.parent_frame()
    browser._switch_to.frame('middleframe')
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
    browser.find_element_by_xpath("//*[@id='laydate_table']/tbody/tr[1]/td[2]").click()
    browser.find_element_by_id('serialNum').send_keys('C1000000018')
    browser.find_element_by_id('loanTime').send_keys('11')

def bxcompany():
    browser._switch_to.frame('iframepage')
    browser._switch_to.frame('leftframe')
    browser.find_element_by_id('idMenu2_1').click()
    time.sleep(1)
    browser.find_element_by_id('yxgl').click()
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="yxglcontent"]/li[5]/a/span/p[1]').click()
    browser._switch_to.parent_frame()
    browser._switch_to.frame('middleframe')
    browser.find_element_by_id('addModalBtn').click()
    company = raw_input('公司名称:'.decode('utf-8').encode('gbk'))
    Insurance_num = input('保险单号:'.decode('utf-8').encode('gbk'))
    browser.find_element_by_id('name').send_keys(company.decode('gbk'))
    browser.find_element_by_id('policyNum').send_keys(Insurance_num)
    browser.find_element_by_class_name('layui-upload-file').click()
    input('请上传附件，完成后输入1:'.decode('utf-8').encode('gbk'))
    browser.find_element_by_id('addBtn').click()


kzl = input(u'1.修改密码\n2.新增客户\n3.新增门店\n4.新增保单\n5.新增保险公司\n请输入'.encode('gbk'))
if kzl==1:
    xgmm()
elif kzl==2:
    xzkh()
elif kzl==3:
    xzmd()
elif kzl==4:
    bdxz()
elif kzl==5:
    bxcompany()
else:print('谢谢使用')
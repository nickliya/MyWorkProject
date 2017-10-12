# /usr/bin/python
# coding=utf-8

from selenium import webdriver
import time
import pymssql
import random
import string
from selenium.webdriver.support.ui import Select
import unittest
from selenium.webdriver.common.keys import Keys
import pytesseract
from PIL import Image


def getcode(imgurl):
    """识别图片"""
    browser.get_screenshot_as_file(imgurl)
    imgprocess(imgurl)
    image = Image.open(imgurl)
    vcode = pytesseract.image_to_string(image)
    if vcode == "" or len(vcode) > 4:
        browser.refresh()
        browser.get_screenshot_as_file(imgurl)
        imgprocess(imgurl)
        image = Image.open(imgurl)
        vcode = pytesseract.image_to_string(image)
    else:
        pass
    return vcode


def imgprocess(imgurl):
    """截图处理"""
    img = Image.open(imgurl)
    region = (350, 458, 469, 499)
    cropImg = img.crop(region)  # 切割图片
    cropImg.save(imgurl)


phone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
    random.choice("0123456789") for i in range(8))
plate_num = u'渝' + ''.join(random.choice(string.uppercase) for i in range(1)) + ''.join(
    random.choice(string.digits) for i in range(6))
frame_num = ''.join(random.choice(string.letters) for i in range(16))
cusadmin = ''.join(random.choice(string.letters) for i in range(6))
cuspasswd = random.choice(string.uppercase) + random.choice(string.lowercase) + ''.join(
    random.choice("0123456789") for i in range(6))
idcard = '5' + ''.join(random.choice("0123456789") for i in range(17))
price = ''.join(random.choice("123456789") for i in range(6)) + '.' + ''.join(
    random.choice("0123456789") for i in range(3))

chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(chromepath)
browser.get('http://192.168.6.52:8080/')
browser.find_element_by_id('name').send_keys('admin')
browser.find_element_by_id('password').send_keys('Wg123456')

temp_img = 'C:\Users\YangQ\Desktop\getImg.png'
code = getcode(temp_img)

browser.find_element_by_id("authcode").send_keys(code)
browser.find_element_by_id('loginButton').click()
browser.implicitly_wait(5)
time.sleep(1)
browser.maximize_window()


class Rygl(unittest.TestCase):
    """人员管理"""
    def setUp(self):
        browser._switch_to.frame('iframepage')
        browser._switch_to.frame('leftframe')

    def tearDown(self):
        browser._switch_to.default_content()
        browser.refresh()

    def case1(self):
        u'新增门店'
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
        mdname = ''.join(random.choice(string.letters) for i in range(6))
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
        browser.find_element_by_xpath(
            "//*[@id='addForm']/div/div/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/button").click()
        print 'mdname:' + mdname

    def case2(self):
        u'新增区域负责人'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('xtgl').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('区域管理').click()
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        time.sleep(2)
        browser.find_element_by_id('xuanfzrAdd').click()
        browser.implicitly_wait(3)
        browser._switch_to.frame('xubox_iframe1')
        time.sleep(1)
        # browser.find_element_by_xpath("//*[@id='glcontent']/button[2]").click()
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        qyname = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('nickName').send_keys(qyname)
        browser.find_element_by_id('name').send_keys(qyname)
        qyphone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
            random.choice("0123456789") for i in range(8))
        browser.find_element_by_id('phone').send_keys(qyphone)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="addForm"]/div/div/div/div[2]/table/tbody/tr[5]/td[2]/button').click()
        print('qyname:' + qyname)

    def case3(self):
        u'新增安装工'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('xtgl').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('区域管理').click()
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        time.sleep(2)
        browser.find_element_by_id('xuanry').click()
        browser.implicitly_wait(3)
        browser._switch_to.frame('xubox_iframe1')
        time.sleep(1)
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        azgname = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('nickName').send_keys(azgname)
        browser.find_element_by_id('name').send_keys(azgname)
        azgphone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
            random.choice("0123456789") for i in range(8))
        browser.find_element_by_id('phone').send_keys(azgphone)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="addForm"]/div/div/div/div[2]/table/tbody/tr[5]/td[2]/button').click()
        print('azgname:' + azgname)

    def case4(self):
        u'新增安装工主管'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('xtgl').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('区域管理').click()
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        time.sleep(2)
        browser.find_element_by_id('xuanzgAdd').click()
        browser.implicitly_wait(3)
        browser._switch_to.frame('xubox_iframe1')
        time.sleep(1)
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        zgname = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('nickName').send_keys(zgname)
        browser.find_element_by_id('name').send_keys(zgname)
        zgphone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
            random.choice("0123456789") for i in range(8))
        browser.find_element_by_id('phone').send_keys(zgphone)
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="addForm"]/div/div/div/div[2]/table/tbody/tr[5]/td[2]/button').click()
        print('zgname:' + zgname)

    def case5(self):
        u'新增角色'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('xtgl').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('角色管理').click()
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        time.sleep(1)
        character = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('label').send_keys(character)
        browser.find_element_by_id('treeDemo_1_check').click()
        browser.find_element_by_id('treeDemo_3_check').click()
        browser.implicitly_wait(3)
        browser.find_element_by_id('treeDemo_101_check').click()
        browser.find_element_by_id('treeDemo_110_check').click()
        browser.find_element_by_id('treeDemo_117_check').click()
        browser.find_element_by_xpath(
            '//*[@id="addForm"]/div/div/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[4]/td[2]/button').click()
        print('character:' + character)

    def case6(self):
        u'新增用户'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('xtgl').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('用户管理').click()
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        time.sleep(1)
        yhname = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('nickName').send_keys(yhname)
        browser.find_element_by_id('name').send_keys(yhname)
        yhpasswd = random.choice(string.uppercase) + random.choice(string.lowercase) + ''.join(
            random.choice("0123456789") for i in range(6))
        browser.find_element_by_id('password').send_keys(yhpasswd)
        browser.find_element_by_id('password2').send_keys(yhpasswd)
        yhphone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
            random.choice("0123456789") for i in range(8))
        browser.find_element_by_id('phone').send_keys(yhphone)
        browser.find_element_by_xpath('//*[@id="addForm"]/div/div/div/div[2]/table/tbody/tr[6]/td[2]/button').click()
        print('yhname:' + yhname)
        print('yhpasswd:' + yhpasswd)


class Dagl(unittest.TestCase):
    """档案管理"""
    def setUp(self):
        browser._switch_to.frame('iframepage')
        browser._switch_to.frame('leftframe')

    def tearDown(self):
        browser._switch_to.default_content()
        browser.refresh()

    def case1(self):
        u'新增客户'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_id('jcsj').click()
        browser.find_element_by_link_text('客户管理').click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_xpath("//*[contains(@successsubmit,'afterLoadAddTmpl(result);')]").click()
        #####数据库查找主机号码#####
        conn = pymssql.connect(host='192.168.6.70', user='sa', password='123456')
        cur = conn.cursor()
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
        print 'your admin: ' + cusadmin
        print 'your password: ' + cuspasswd


class Bdxt(unittest.TestCase):
    def setUp(self):
        browser._switch_to.frame('iframepage')
        browser._switch_to.frame('leftframe')

    def tearDown(self):
        time.sleep(3)
        browser._switch_to.default_content()
        browser.refresh()

    def case1(self):
        u"""保单新增"""
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('addModalBtn').click()
        time.sleep(3)
        browser.find_element_by_id('ownerMobile').send_keys(phone)
        browser.find_element_by_id('contactAddress').send_keys('chongqing')
        time.sleep(1)
        browser.find_element_by_id('ownerIdentifyNum').send_keys(idcard)
        time.sleep(1)
        browser.find_element_by_id('brandModel').send_keys('11')
        browser.find_element_by_id('engineNumber').send_keys('11')
        browser.find_element_by_id('price').send_keys(price)
        ######生成车架号######
        global TrueVIN
        digipercase = string.digits + string.uppercase  # 数字大写字母集合
        digiper1 = digipercase.replace('I', '')  # 去大写I
        digiper2 = digiper1.replace('O', '')  # 去大写O
        digiper3 = digiper2.replace('Q', '')  # 去大写Q
        digiper4 = digiper3.replace('Z', '')  # 去大写Z
        VIN_number = ''.join(random.choice(digiper4) for i in range(8)) + random.choice(string.digits) + random.choice(
            string.digits) + ''.join(random.choice(digiper4) for i in range(3)) + ''.join(
            random.choice(string.digits) for i in range(4))
        hs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
              'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
              'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, }
        VIN = (hs[VIN_number[0]] * 8 + hs[VIN_number[1]] * 7 + hs[VIN_number[2]] * 6 + hs[VIN_number[3]] * 5 + hs[
            VIN_number[4]] * 4 + hs[VIN_number[5]] * 3 + hs[VIN_number[6]] * 2 + hs[VIN_number[7]] * 10 + hs[
                   VIN_number[9]] * 9 + hs[VIN_number[10]] * 8 + hs[VIN_number[11]] * 7 + hs[VIN_number[12]] * 6 + hs[
                   VIN_number[13]] * 5 + hs[VIN_number[14]] * 4 + hs[VIN_number[15]] * 3 + hs[VIN_number[16]] * 2) % 11
        if VIN == 10:
            VIN = 'X'
        else:
            pass
        TrueVIN = VIN_number[:8] + str(VIN) + VIN_number[9:]
        ######生成车架号######
        browser.find_element_by_id('vinCode').send_keys(TrueVIN)
        # browser.find_element_by_id('billingDate').click()
        # browser.find_element_by_xpath("//*[@id='laydate_table']/tbody/tr[1]/td[2]").click()
        browser.find_element_by_id('serialNum').send_keys('C1000000018')
        browser.find_element_by_id('loanTime').send_keys('60')
        global kh_name
        kh_name = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('name').send_keys(kh_name)
        home_phone = '68' + ''.join(random.choice("0123456789") for i in range(6))
        browser.find_element_by_id('fixedTelephone').send_keys(home_phone)
        browser.find_element_by_id('depName').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('yqmd').click()
        time.sleep(1)
        try:
            browser.find_element_by_id('addressSure').click()
        except:
            pass
        time.sleep(1)
        browser.find_element_by_id('previewBtn').click()
        browser.implicitly_wait(5)
        time.sleep(2)
        browser.find_element_by_id('createBtn').click()
        print (u'保单名称:' + kh_name)

    def case2(self):
        u'保单日志查看'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('keyWord').send_keys(kh_name)
        browser.find_element_by_id('searchBut').click()
        time.sleep(1)
        browser.find_element_by_id('orderLog').click()
        time.sleep(3)
        print(u'已查看')
        browser.find_element_by_xpath('//*[@id="historyDiv"]/div/div/div[2]/div/button').click()
        print(u'退出')

    def case3(self):
        u'保单修改'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)  # 等待加载完成
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('keyWord').send_keys(kh_name)
        browser.find_element_by_id('searchBut').click()
        time.sleep(1)
        browser.find_element_by_id('updateOrder').click()
        global kh_name2
        kh_name2 = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('name').send_keys(Keys.CONTROL + 'a')
        browser.find_element_by_id('name').send_keys(Keys.CONTROL + 'x')
        browser.find_element_by_id('name').send_keys(kh_name2)
        time.sleep(2)
        browser.find_element_by_id('previewBtn').click()
        browser.implicitly_wait(5)
        time.sleep(2)
        browser.find_element_by_id('createBtn').click()
        print(u'新保单名称:' + kh_name2)

    def case4(self):
        u'保单作废'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)  # 等待加载完成
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('keyWord').send_keys(kh_name2)
        browser.find_element_by_id('searchBut').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="cancelOrder"]').click()
        time.sleep(1)
        browser.find_element_by_id('reason').send_keys(u'测试作废')
        browser.find_element_by_xpath('//*[@id="delModal"]/div/div/div[3]/button[2]').click()
        print(u'作废成功')

    def case5(self):
        u'作废原因查看'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)  # 等待加载完成
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('keyWord').send_keys(kh_name2)
        browser.find_element_by_id('searchBut').click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="datatable"]/tbody/tr/td[16]/button[4]').click()
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="delCancelBtn"]').click()

    def case6(self):
        u'补录'
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('保单系统').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("保单管理").click()
        time.sleep(1)  # 等待加载完成
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('additionalModalBtn').click()
        time.sleep(3)
        # lsh='0000'+''.join(random.choice("0123456789") for i in range(6))
        # browser.find_element_by_id('serialNumberAdditional').send_keys(lsh)
        browser.find_element_by_id('ownerMobileAdditional').send_keys(phone)
        browser.find_element_by_id('contactAddressAdditional').send_keys('chongqing')
        time.sleep(1)
        browser.find_element_by_id('ownerIdentifyNumAdditional').send_keys(idcard)
        time.sleep(1)
        browser.find_element_by_id('brandModelAdditional').send_keys('11')
        browser.find_element_by_id('engineNumberAdditional').send_keys('11')
        browser.find_element_by_id('priceAdditional').send_keys(price)
        ######生成车架号######
        digipercase = string.digits + string.uppercase  # 数字大写字母集合
        digiper1 = digipercase.replace('I', '')  # 去大写I
        digiper2 = digiper1.replace('O', '')  # 去大写O
        digiper3 = digiper2.replace('Q', '')  # 去大写Q
        digiper4 = digiper3.replace('Z', '')  # 去大写Z
        VIN_number = ''.join(random.choice(digiper4) for i in range(8)) + random.choice(string.digits) + random.choice(
            string.digits) + ''.join(random.choice(digiper4) for i in range(3)) + ''.join(
            random.choice(string.digits) for i in range(4))
        hs = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
              'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
              'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, }
        VIN = (hs[VIN_number[0]] * 8 + hs[VIN_number[1]] * 7 + hs[VIN_number[2]] * 6 + hs[VIN_number[3]] * 5 + hs[
            VIN_number[4]] * 4 + hs[VIN_number[5]] * 3 + hs[VIN_number[6]] * 2 + hs[VIN_number[7]] * 10 + hs[
                   VIN_number[9]] * 9 + hs[VIN_number[10]] * 8 + hs[VIN_number[11]] * 7 + hs[VIN_number[12]] * 6 + hs[
                   VIN_number[13]] * 5 + hs[VIN_number[14]] * 4 + hs[VIN_number[15]] * 3 + hs[VIN_number[16]] * 2) % 11
        if VIN == 10:
            VIN = 'X'
        else:
            pass
        TrueVIN2 = VIN_number[:8] + str(VIN) + VIN_number[9:]
        ######生成车架号######
        browser.find_element_by_id('vinCodeAdditional').send_keys(TrueVIN2)
        browser.find_element_by_id('billingDateAdditional').click()
        browser.find_element_by_xpath("//*[@id='laydate_table']/tbody/tr[1]/td[2]").click()
        browser.find_element_by_id('serialNumAdditional').send_keys('C1000000018')
        browser.find_element_by_id('loanTimeAdditional').send_keys('60')
        bl_name = ''.join(random.choice(string.letters) for i in range(6))
        browser.find_element_by_id('nameAdditional').send_keys(bl_name)
        home_phone = '68' + ''.join(random.choice("0123456789") for i in range(6))
        browser.find_element_by_id('fixedTelephoneAdditional').send_keys(home_phone)
        browser.find_element_by_id('depNameAdditional').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('yqmd').click()
        browser.find_element_by_id('additionalBtn').click()

    def bxcompany(self):
        # browser.find_element_by_id('idMenu2_1').click( )
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


class Tgxf(unittest.TestCase):
    def setUp(self):
        browser._switch_to.frame('iframepage')
        browser._switch_to.frame('leftframe')

    def tearDown(self):
        time.sleep(3)
        browser._switch_to.default_content()
        browser.refresh()

    def case1(self):
        u"""店面新增"""
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('推广续费').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("店面管理").click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('addModalBtn').click()
        browser.find_element_by_id('name').send_keys(u"杨卿自动化店面")
        browser.find_element_by_id('address').send_keys(u"重庆自动化地址")
        browser.find_element_by_id('minPrice').send_keys("100")
        browser.find_element_by_id('maxPrice').send_keys("1500")
        browser.find_element_by_id('comment').send_keys(u"备注拿的急撒考虑到啥借口放假快乐撒娇快乐大收到了三撒就多了撒就多了撒简单")
        browser.find_element_by_id('addBtn').click()

    def case2(self):
        u"""删除"""
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('推广续费').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("店面管理").click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('keyWord').send_keys(u"杨卿自动化店面")
        browser.find_element_by_id('searchBut').click()
        time.sleep(1)
        browser.find_element_by_css_selector('#datatable > tbody > tr > td:nth-child(9) > button.btn.btn-danger.btn-xs').click()
        browser.find_element_by_css_selector('#datatable > tbody > tr > td:nth-child(9) > button.btn.btn-primary.btn-xs').click()

    def case3(self):
        u"""定价新增"""
        browser.find_element_by_id('idMenu2_1').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text('推广续费').click()
        time.sleep(1)
        browser.find_element_by_partial_link_text("定价策略").click()
        time.sleep(1)
        browser._switch_to.parent_frame()
        browser._switch_to.frame('middleframe')
        browser.find_element_by_id('addModalBtn').click()
        browser.find_element_by_id('name').send_keys(u"杨卿自动化定价策略")
        browser.find_element_by_id('price').send_keys("100")
        browser.find_element_by_id('yearNum').send_keys("1")
        browser.find_element_by_id('addBtn').click()


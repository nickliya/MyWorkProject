# coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import string
import pytesseract
from PIL import Image
import base64
import json


class Mainfun:
    def __init__(self):
        jsonfile = open("jsondata/main.json", "r")
        self.initdata = json.load(jsonfile)

        option = webdriver.ChromeOptions()
        # option.add_argument(self.initdata["datapath"]) #去掉data;,
        chromepath = self.initdata["chromepath"]
        self.browser = webdriver.Chrome(chromepath, chrome_options=option)

        self.browser.get(self.initdata["monitorUrl"])
        self.browser.maximize_window()
        self.browser.implicitly_wait(7)

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "username")))

        self.browser.find_element_by_id('username').send_keys('admin')
        self.browser.find_element_by_id('password').send_keys('123456')

        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
        temp_img = '1.png'
        code = self.getcode(temp_img)
        self.browser.find_element_by_id("captcha").send_keys(code)
        time.sleep(1)
        self.browser.find_element_by_id('submit').click()
        print("已点击登录")

        time.sleep(1)

    def getcode(self, imgurl):
        u"""识别图片"""
        while 1:
            WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "authcodeImg")))
            imgdatabase64 = self.browser.find_element_by_class_name('authcodeImg').get_attribute("src")[22:]
            imgdata = base64.b64decode(imgdatabase64)

            f1 = open("1.png", "wb")
            f1.write(imgdata)
            f1.close()

            image = Image.open(imgurl)
            vcode = pytesseract.image_to_string(image)
            print(vcode)
            if len(vcode) == 4 and "0" not in vcode and "O" not in vcode and "|" not in vcode and "]" not in vcode and "2" not in vcode and "I" not in vcode and " " not in vcode:
                print("recognize ok")
                break
            else:
                print("difficult code, change the next")
                self.browser.find_element_by_class_name('authcodeImg').click()
                time.sleep(1)
        return vcode

    @staticmethod
    def imgprocess(imgurl):
        u"""截图处理"""
        img = Image.open(imgurl)
        region = (351, 460, 468, 498)
        cropImg = img.crop(region)  # 切割图片
        cropImg.save(imgurl)


class SupportFun:
    def __init__(self):
        pass

    @staticmethod
    def get_phone():
        phone = random.choice(['139', '188', '185', '136', '158', '151']) + ''.join(
            random.choice("0123456789") for i in range(8))
        return phone

    @staticmethod
    def get_plate_num():
        plate_num = u'渝' + ''.join(random.choice(string.ascii_uppercase) for i in range(1)) + ''.join(
            random.choice(string.digits) for i in range(6))
        return plate_num

    @staticmethod
    def get_frame_num():
        frame_num = ''.join(random.choice(string.ascii_letters) for i in range(16))
        return frame_num

    @staticmethod
    def get_cusadmin():
        cusadmin = ''.join(random.choice(string.ascii_letters) for i in range(6))
        return cusadmin

    @staticmethod
    def get_cuspasswd():
        cuspasswd = random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) + ''.join(
            random.choice("0123456789") for i in range(6))
        return cuspasswd

    @staticmethod
    def get_idcard():
        idcard = '5' + ''.join(random.choice("0123456789") for i in range(17))
        return idcard

    @staticmethod
    def get_price():
        price = ''.join(random.choice("123456789") for i in range(6)) + '.' + ''.join(
            random.choice("0123456789") for i in range(3))
        return price

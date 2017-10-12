# /usr/bin/python
# coding=utf-8

import pytesseract
from PIL import Image,ImageEnhance
from selenium import webdriver
import time


def getcode(imgurl):
    """识别图片"""
    image = Image.open(imgurl)
    # imgry = image.convert('L')#图像加强，二值化
    # sharpness =ImageEnhance.Contrast(imgry)#对比度增强
    # sharp_img = sharpness.enhance(2.0)
    # sharp_img.save('C:\Users\YangQ\Desktop\getImg2.png')
    vcode = pytesseract.image_to_string(image)
    return vcode


def imgprocess(imgurl):
    """截图处理"""
    img = Image.open(imgurl)
    region = (516, 373, 614, 422)
    cropImg = img.crop(region)  # 切割图片
    cropImg.save(imgurl)

# chromepath = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# browser = webdriver.Chrome(chromepath)
# browser.get('http://192.168.6.52:8090/')
# time.sleep(2)  # 等待验证码加载完成
temp_img = 'C:\Users\YangQ\Desktop\getImg2.png'
# browser.get_screenshot_as_file(temp_img)  # 截图
# imgprocess(temp_img)
code = getcode(temp_img)
# browser.find_element_by_name("authCode").send_keys(code)
print code
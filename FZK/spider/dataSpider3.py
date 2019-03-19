# coding=utf-8
# 运维日志爬虫
# 共享车监控页面爬轨迹所有数据

import requests
import json
import xlrd
import re


def regnizeAuthcode(session, codeurl):
    """识别验证码"""

    # 保存图片到本地
    url = codeurl
    rcode = session.get(url)
    codefile = open("C:\\Users\\fuzhi\\Desktop\\code.png", 'wb')
    codefile.write(rcode.content)
    codefile.close()

    # image = Image.open("C:\\Users\\fuzhi\\Desktop\\code.png")
    # code = pytesseract.image_to_string(image)
    # return code


def getAdress(lat, lng):
    url = "http://api.map.baidu.com/geocoder/v2/?"
    payload = {
        "coordtype": "gcj02ll",
        "location": str(lat) + "," + str(lng),
        "output": "json",
        "pois": "1",
        "ak": "K52pNzWT61z1EHvdZptaSmlPRc7mKbjC",
    }
    r = s.get(url, params=payload)
    jsoninfo = json.loads(r.text)
    adressResult = jsoninfo['result']
    adress = adressResult['formatted_address'] + adressResult['sematic_description']
    return adress


def verify(starttime, endtime):
    url = ip + "/car/monitor/queryTripByTime?vehicleID=676&startTime=" + starttime + "&endTime=" + endtime
    data = {
        "vehicleID": '676',
        "startTime": starttime,
        "endTime": endtime,

    }
    r2 = s.post(url, data=data)
    jsoninfo = json.loads(r2.text)
    if jsoninfo['entity']:
        for datajson in jsoninfo['entity']:
            startgps = datajson['data'][0]
            startgpsLng = startgps['lng']
            startgpsLat = startgps['lat']
            startAdr = getAdress(startgpsLat, startgpsLng)
            endgps = datajson['data'][-1]
            endgpsLng = endgps['lng']
            endgpsLat = endgps['lat']
            endAdr = getAdress(endgpsLat, endgpsLng)
            time = datajson['time']
            usetime = datajson['period']
            mileage = datajson['mileage']
            print(starttime, time, usetime, mileage, startAdr, endAdr)
    else:
        print(starttime + '没有轨迹')


timelist = []
timeindex = "2018-09-"
count = 24
for i in range(7):
    timelist.append(timeindex + str(count).zfill(2))
    count += 1

timeindex = "2018-10-"
count = 1
for i in range(31):
    timelist.append(timeindex + str(count).zfill(2))
    count += 1

timeindex = "2018-11-"
count = 1
for i in range(30):
    timelist.append(timeindex + str(count).zfill(2))
    count += 1

s = requests.session()
ip = "http://blacktea.mysirui.com:30011"
url = ip + "/sys/user/getImg"
regnizeAuthcode(s, url)

url = ip + "/sys/user/login?username=admin&password=Admin@fastgo123"
payload = {
    "username": "admin",
    "password": "admin123456"
}
code = input("验证码:")
data = {
    "inputRandomCode": code
}
r1 = s.post(url, data=data)
if r1.status_code == 200:
    print("登陆成功")
else:
    exit()

for i in timelist:
    starttime = i
    endtime = i
    verify(starttime, endtime)

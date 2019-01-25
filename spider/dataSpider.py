# coding=utf-8
# 运维日志爬虫
# 查询异常数据

import requests
from PIL import Image
import pytesseract
import json
import xlrd
import re


def regnizeAuthcode(session, codeurl):
    # 识别验证码
    url = codeurl
    rcode = session.get(url)
    codefile = open("C:\\Users\\fuzhi\\Desktop\\code.png", 'wb')
    codefile.write(rcode.content)
    codefile.close()

    # image = Image.open("C:\\Users\\fuzhi\\Desktop\\code.png")
    # code = pytesseract.image_to_string(image)
    # return code


def verify(imei, starttime, endtime, sheet):
    url = ip + "/log/getList_client?"
    data = {
        "con1Op": 1,
        "con1Value": 331,
        "con2Op": 1,
        "con2Value": "",
        "con3Op": 1,
        "con3Value": "",
        "con4Op": 1,
        "con4Value": "",
        "entityid": imei,
        "clienttype": 3,
        "startTime": starttime,
        "endTime": endtime,
        "convertAddress": 0,
        "sorter": -1,
        "page": 1,
        "rows": 5000
    }
    r2 = s.post(url, data=data)
    jsoninfo = json.loads(r2.text)
    # print(jsoninfo)

    # 初始化
    rowindex = 0
    oldmiles = None
    mileinfo = "里程一样,"
    mileslist = []
    # 遍历json信息,检测里程
    for info in jsoninfo["rows"]:
        # 只筛选上行消息
        if info['EVENTID'] == "上行":
            # 截取331
            r = r'\|\d\|331,.*?\|'
            result = re.findall(r, info['CONTENT'])

            # 如果没有匹配到则退出
            if "" in result or result == []:
                continue
            infolist = result[0].split(",")
            miles = infolist[17]

            if rowindex == 0:
                mileslist.append(int(miles, 16))
            else:
                if miles != oldmiles:
                    mileslist.append(int(miles, 16))

            # 叠加
            oldmiles = miles
            rowindex += 1
        else:
            pass

    if len(mileslist) == 1:
        pass
    elif len(mileslist) == 0:
        print(imei + '设备无331信息')
        return
    else:
        mileinfo = "里程不一样!最小:" + str(min(mileslist)) + ";最大:" + str(max(mileslist))+";相差:"+str(max(mileslist)-min(mileslist))+"。"

    # 初始化
    rowindex = 0
    olddangwei = None
    dangweilist = []
    # 遍历json信息,检测档位
    for info in jsoninfo["rows"]:
        # 只筛选上行消息
        if info['EVENTID'] == "上行":
            # 截取331
            r = r'\|\d\|331,.*?\|'
            result = re.findall(r, info['CONTENT'])

            # 如果没有匹配到则退出
            if "" in result or result == []:
                continue
            infolist = result[0].split(",")
            dangwei = infolist[16]

            if rowindex == 0:
                dangweilist.append(dangwei)
            else:
                if dangwei != olddangwei:
                    dangweilist.append(dangwei)

            # 叠加
            olddangwei = dangwei
            rowindex += 1
        else:
            pass

    dangweiinfo = "历史档位有" + str(set(dangweilist)) + "。"

    # 初始化
    rowindex = 0
    oldtime = None

    # 遍历json信息,检测分钟
    for info in jsoninfo["rows"]:
        # 只筛选上行消息
        if info['EVENTID'] == "上行":
            # 截取331
            r = r'\|\d\|331,.*?\|'
            result = re.findall(r, info['CONTENT'])

            # 如果没有匹配到则退出
            if "" in result or result == []:
                continue
            infolist = result[0].split(",")
            time = infolist[1]

            if rowindex == 0:
                oldtime = time
                rowindex += 1
            else:
                if time == oldtime:
                    if "FFFF" in time:
                        print(mileinfo + dangweiinfo + "时间为FFFFFFF,设备为" + imei)
                        return
                    elif time == "":
                        print(mileinfo + dangweiinfo + "时间为空,设备为" + imei)
                        return
                    else:
                        print(mileinfo + dangweiinfo + "时间一样!,设备为" + imei)
                        return

    print(mileinfo + dangweiinfo + "时间不一样，设备为" + imei)


s = requests.session()
ip = "http://blacktea.mysirui.com:40000"
url = ip + "/login/getAuthcodeImg"
regnizeAuthcode(s, url)

url = ip + "/login?Name=admin&password=admin123456"
payload = {
    "Name": "admin",
    "password": "admin123456"
}
code = input("验证码:")
data = {
    "authcode": code
}
r1 = s.post(url, data=data)
if r1.status_code == 200:
    print("登陆成功")
else:
    exit()

readbook = xlrd.open_workbook(r'C:\Users\fuzhi\Desktop\12月没有里程数据(10分钟以上).xls')
sheet = readbook.sheet_by_index(0)
row = 1
for i in range(100):
    rowinfo = sheet.row_values(row)
    imei = rowinfo[5]
    starttime = rowinfo[6]
    endtime = rowinfo[7]
    verify(imei, starttime, endtime, sheet)
    row += 1

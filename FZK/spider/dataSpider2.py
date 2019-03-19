# coding=utf-8
# 运维日志爬虫
# 331查询历程

import requests
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
        "rows": 50000
    }
    r2 = s.post(url, data=data)
    jsoninfo = json.loads(r2.text)
    # print(jsoninfo)

    # 初始化
    rowindex = 0
    oldmiles = None
    data331List = []
    mileslist = []
    # 遍历json信息,检测里程
    for info in jsoninfo["rows"]:
        # 只筛选上行消息
        if info['EVENTID'] == "上行":
            # 截取331
            r = r'\|\d\|331,.*?\|'
            result = re.findall(r, info['CONTENT'])

            # 如果没有匹配到则退出进入下一个循环
            if "" in result or result == []:
                continue
            if ",,,,,,," in result[0] or "FFFFFF" in result[0]:
                continue
            time = info['TIME']
            data331List.append([time, result])
            break

        else:
            pass

    # # 开始
    # startmileinfo = data331List[-1]
    # infolist = startmileinfo[0].split(",")
    # startmiles = infolist[17]
    #
    # # 结束
    # endmileinfo = data331List[0]
    # infolist = endmileinfo[0].split(",")
    # endmile = infolist[17]
    if data331List:
        info = data331List[0]
        time = info[0]
        timestamp = info[1][0].split(",")[1]
        print(time, timestamp)
    else:
        print("该时间段没有找到331数据")

    # print(data331List)


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

readbook = xlrd.open_workbook(r'C:\Users\fuzhi\Desktop\imei.xlsx')
sheet = readbook.sheet_by_index(0)
row = 583
for i in range(1):
    rowinfo = sheet.row_values(row)
    imei = rowinfo[0]
    # starttime = rowinfo[1]
    starttime = "2019-01-26 18:00:00"
    # endtime = rowinfo[2]
    endtime = "2019-01-29 17:00:00"
    verify(imei, starttime, endtime, sheet)
    row += 1

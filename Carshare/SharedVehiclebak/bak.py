cus = App()  # 调用app接口
for i in case:
    value = case[i]["value"]
    rescode = cus.authcode(value)
    if case[i]["expect"] == True:
        if not bool(rescode[0]) == case[i]["expect"]:
            pass
        else:
            print i + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + " resultMessage:" + rescode[1][
                "resultMessage"]
    else:
        if not bool(rescode[0]) == case[i]["expect"] and rescode[1]["resultMessage"] == case[i]["rmak"]:
            pass
        else:
            print i + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + " resultMessage:" + rescode[1][
                "resultMessage"]









# coding=utf-8
from SharedVehicle.api import *

sethost('http://192.168.6.52:8080')  # 域名

case = {
    "case1": {"value": "15025463191", "expect": True, "rmak": u"正确"},
    "case2": {"value": "", "expect": False, "rmak": u"未输入手机号"},
    "case3": {"value": "dsadsa", "expect": False, "rmak": u"输入的不是数字"},
    "case4": {"value": "1561564894981561654654561", "expect": False, "rmak": u"输入长度超过限制"},
}

cus = App()  # 调用app接口
for i in case:
    value = case[i]["value"]
    rescode = cus.authcode(value)
    if not bool(rescode[0]) == case[i]["expect"]:
        pass
    else:
        print i + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + " resultMessage:" + rescode[1][
            "resultMessage"]
# coding=utf-8
from SharedVehicle.api import *

cus = App()  # 调用app模块
web = Web()  # 调用web模块
tcp = Tcp()  # 调用Tcp模块

sethost('http://192.168.6.113:8090')  # 域名
tcp.settcp('192.168.6.52', '2103')  # 配置tcp
# setinput('18523641110', '123456')  # app测试某些接口前需初始化,第一个是用户名,第二个是密码
web.sysuserlogin("admin;123456;")  # 保持门户登陆状态，依次是用户名，密码，验证码，不测门户接口或单测登陆接口时必须屏蔽

case = {
    "case1": {"value": "YangQ;yqtest;1;1/2/3", "expect": True, "rmak": u"正确"},
}

# 执行接口测试，并判断结果
for i in case:
    valueinfo = case[i]["value"]
    rescode = cus.reg(valueinfo)  # 调用接口
    if not bool(rescode[0]) == case[i]["expect"]:
        pass
    else:
        print i + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + " resultMessage:" + rescode[1][
            "resultMessage"]

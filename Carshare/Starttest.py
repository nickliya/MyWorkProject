# coding=utf-8
# version:2017/07/31 16:19

from SharedVehicle.flow import *
from SharedVehicle.DataCreator import *
import itertools


class Startest:
    def __init__(self):
        pass

    # 单接口测试使用
    @staticmethod
    def interfacetest(case, interface):
        for i in case:
            try:
                valueinfo = case[i]["value"]
                rescode = interface(valueinfo)  # 调用接口
                if not bool(rescode[0]) == case[i]["expect"]:
                    pass
                else:
                    print i + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + \
                          " resultMessage:" + rescode[1]["resultMessage"]
                    print i + rescode
            except (ValueError, IndexError), msg:
                if str(msg) == "No JSON object could be decoded":
                    print '未收到响应信息'
                elif str(msg) == "list index out of range":
                    print '传入参数错误,请检查用例或封装方法'
                else:
                    print '脚本错误,' + str(msg)

    # 自动化生成的用例使用
    @staticmethod
    def autocasetest(case, interface):
        for i in case:
            try:
                valueinfo = i[0]
                rescode = interface(valueinfo)  # 调用接口
                if not bool(rescode[0]) == i[2]:
                    pass
                else:
                    print i[1] + " error    Log: resultCode:" + str(rescode[1]["resultCode"]) + " resultMessage:" + \
                          rescode[1][
                              "resultMessage"]
                    # print i[1] + strrescode
            except (ValueError, IndexError), msg:
                if str(msg) == "No JSON object could be decoded":
                    print '未收到响应信息'
                elif str(msg) == "list index out of range":
                    print '传入参数错误,请检查用例或封装方法'
                else:
                    print '脚本错误,' + msg

    # 接口流程测试
    @staticmethod
    def flowtest(case, interface):
        for i in case:
            value = i["value"]
            resultinfo = interface(value)
            if resultinfo == i["expect"]:
                pass
            else:
                print str(i["caseid"]) + " error"


def isdependent(value):
    if "dependent" in value:
        return False
    else:
        return True


def modificationcase(combinationlist):
    autocase = []
    caseid = 1
    casefile = open("D:/caselist2.csv", "w+")  # 生成一个csv用于保存自动化生成的用例
    for combination in combinationlist:  # 排列组合出所有case
        # print combination

        # 数据加工，把combination加工成我们规定的格式
        com_tuple = ()  # 新建元祖用于加工元数据
        for x in range(len(combination)):
            com_tuple = com_tuple + combination[x]
        # print com_tuple
        com_list = list(com_tuple)  # 把元祖转成列表进行进一步加工
        while True in com_list:
            com_list.remove(True)
        else:
            pass

        while False in com_list:
            com_list.remove(False)
        else:
            pass

        # print com_list
        com_str = ';'.join(com_list)  # 把列表转成字符串进行进一步加工
        if False in com_tuple:
            autocase.append((com_str, "case" + str(caseid), False))
            casefile.write(com_str.decode('utf-8').encode('gbk') + ";case" + str(caseid) + ";" + str(False) + '\n')
        else:
            autocase.append((com_str, "case" + str(caseid), True))
            casefile.write(com_str.decode('utf-8').encode('gbk') + ";case" + str(caseid) + ";" + str(True) + '\n')
        caseid += 1
    casefile.close()
    return autocase


def creatcaselist(*value):
    cases1 = []  # 相互独立,没有联系,加法组合
    for para in value:
        if "dependent" in para:
            para = para[0]
        else:
            pass
        for pValue in para:
            case1 = []
            for indexPara in value:
                if "dependent" in indexPara:
                    indexPara = indexPara[0]
                else:
                    pass
                if para == indexPara:
                    case1.append(pValue)
                else:
                    case1.append(indexPara[0])
            cases1.append(tuple(case1))

    valuelist = []  # 有联系,乘法组合
    for i in value:
        if isdependent(i):
            case2 = [i[0]]
            valuelist.append(case2)
        else:
            valuelist.append(i[0])
    tuplevalue = list(valuelist)
    cases2 = list(itertools.product(*tuplevalue))
    cases = set(cases1) | set(cases2)  # 取并集
    print len(cases)
    return modificationcase(cases)

cus = App()  # 调用app模块
tcp = Tcp()  # 调用Tcp模块
psql = Postgresql()  # 调用Postgresql模块
web = Web(psql)  # 调用web模块

sethost('http://192.168.6.52:8090')  # 域名
setinput('15025463191', '123456')  # 初始化input1和input2
# setinput('18523641110', '123456')  # 初始化input1和input2
web.sysuserlogin("admin;123456;6666")  # 保持门户登陆状态,依次是用户名,密码,验证码，不测门户或单测登陆接口时必须屏蔽
# web.sysuserlogin("admin;123456;1231")  # 保持门户登陆状态,依次是用户名,密码,验证码，不测门户或单测登陆接口时必须屏蔽
web.configloging()
tcp.settcp('192.168.6.52', '2103')  # 配置tcp
psql.setsql('192.168.6.51', 5432, 'postgres', '123456', 'postgres')  # 配置postgresql数据库
flow = Flow(cus, web, tcp, psql)  # 调用Flow模块
startest = Startest()  # 调用Startest模块


# 单接口用例
caselist = {
    "case1": {"value": "rbfONzWcDosb;1;2017-08-14 13:00:00;2018-08-14 13:00:00;0", "expect": True, "rmak": u"时间不在点上"},
    "case2": {"value": "优惠券杨卿满减;1;2017-08-14 13:00:00;2018-08-14 13:00:00;!#$%&()*+-./<=>?@[]^_`{|}~", "expect": True,"rmak": u"时间不在点上"},
    "case3": {"value": ";1;2017-08-14 13:00:00;2018-08-14 13:00:00;0", "expect": True, "rmak": u"时间不在点上"},
    "case4": {"value": "优惠券杨卿满减;1;2017-08-15 09:10:1;2018-08-14 13:00:00;0", "expect": True, "rmak": u"时间不在点上"},
    "case5": {"value": "优惠券杨卿满减;1;2017-08-14 13:00:00;2018-08-14 13:00:00;", "expect": True, "rmak": u"时间不在点上"},
}
# 接口流程测试
flowcase = [

    {"caseid": "case1", "value": "杨卿TCP666;2017-08-11 15:55:56", "expect": True, "rmak": u"ok"}
]

# 自动生成用例
# platenumbernamem = NameType().all('杨卿TCP666')
# timem = TimeType(False, True).all('2017-08-12 13:43:99')
# addressmemom = MemTpye().all('重庆渝北高速路段')
# contentmemom = MemTpye(False, True).all('超速驾驶')
# scorenumm = NameType().all('3')
# finenumm = NameType().all('300')
# pay_amountnumm = NameType().all('900')
# pic_urlurlm = UrlType().all('/it/u=29138290541862516083&fm=26&gp=0.jpg')
# statuenumm = NameType().all('0')
# remarkmemom = MemTpye().all('多次违章', 1)
# customerididm = [('5', True), ("", True)]

# auto_caselist = creatcaselist(platenumbernamem, timem, addressmemom, contentmemom, scorenumm, finenumm, pay_amountnumm,
#                               pic_urlurlm, statuenumm, remarkmemom, customerididm)

# web.testdeleteOrg(32)  # 删除机构,填orgid
# web.testdeleteVehicleModel(48)  # 删除车型,填vmid
# startest.interfacetest(caselist, web.activititycouponlist)

# web.activititycouponadd("优惠券杨卿满100减100;100;1;100;2017-08-12 17:00:00;2018-08-12 17:30:00;1000;2;0;")
# print web.orderurgentOrderfinish("42;处里;50")[1]["resultMessage"]

# flow.feecheck("4;13")
# flow.feecheck("53;9")
flow.appflow("杨卿车辆;83VXGV8U548C08581;杨卿自动化车型;15025463191;王来福")
# flow.order("11")
# flow.peccancy("杨卿车辆;2017-09-04 15:51:50;15025463191")

# print cus.sysdetail("")
# 车型定价
# feeinfo = "检查计费;4;检查计费是否正确;0.3;7;0.5;9:00;16:00;0.6;2017-08-18;2017-08-25;1;12:00;14:00;1.2"
# print web.carvehicleModelsetFee(feeinfo)[1]["resultMessage"]

# 租车还车全套
# print cus.carrent("120")
# print cus.caruserCar("53")[1]["resultMessage"]
# print cus.carreturnCar("5;false")[1]["resultMessage"]
# print web.orderurgentOrderfinish("7;meme;100")
# print cus.currentOrder("")

# 支付
# print web.payCallbackwxWebFinishPayCallback("1117090113465806")
# print web.payCallbackaliWebPayFinishPayCallback("2117091316032325")

# print web.configaviableset("false;false;false;false")[1]["resultMessage"]

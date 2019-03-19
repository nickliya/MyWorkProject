# coding=utf-8
# create by 15025463191 2017/07/10
# _metaclass_ = type
import requests
import socket
import re
import time
import datetime


def sethost(x):
    # 设置域名
    global host
    host = x


def setinput(uservalue, passwdvalue):
    # 获取input
    def getinput(msg):
        url = 'http://192.168.6.52:40000/macCode/encode4Lan'
        payload = {
            "content": msg
        }
        inputinfo = websession.get(url, params=payload)
        print inputinfo.json()["result"]["resultMessage"]
        return inputinfo.json()["result"]["resultMessage"]
    global user, passwd
    user = getinput(uservalue)
    passwd = getinput(passwdvalue)
    # print user
    # print passwd


def hextime():
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)

    def local2utc(local_st):
        time_struct = time.mktime(local_st.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st
    utc_tran = local2utc(local_time)
    nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
    month = utc_tran.strftime('%m')
    day = utc_tran.strftime('%d')
    hour = utc_tran.strftime('%H')
    minute = utc_tran.strftime('%M')
    newminute = int(minute)-3
    second = utc_tran.strftime('%S')
    m = '%x' % int(month)
    d = '%x' % int(day)
    H = '%x' % int(hour)
    M = '%x' % newminute
    S = '%x' % int(second)
    strhextime = str(m)+','+str(d)+','+str(H)+','+str(M)+','+str(S)
    time.sleep(3)
    return strhextime


class Tcp:
    def __init__(self):
        pass

    def settcp(self, tcpadress, tcpport):
        self.tcpadress = tcpadress
        self.tcpport = tcpport

    def connect(self):
        self.t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.t.connect((self.tcpadress, int(self.tcpport)))

    def send(self, msg):
        self.t.send(msg)


class App:
    def __init__(self):
        pass

    def req_get(self, url, payload):
        r = appsession.get(url, params=payload)
        return r.json()

    def req_post(self, url, payload):
        r = appsession.post(url, data=payload)
        return r.json()

    # ##########客户模块##########

    def authcode(self, case):
        # u'获取验证码'
        value = str(case).split(';')
        interface = '/customer/authcode'
        url = host + interface
        # phone=random.choice(['139','188','185','136','158','151'])+''.join(random.choice("0123456789") for i in range(8))
        payload = {
            "phone": value[0]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]
        # return json["result"]

    def reg(self, case):
        # u'注册'
        value = str(case).split(';')
        authcodeinfo = App().authcode(value[0])
        authcode = authcodeinfo[1]["resultMessage"]
        interface = '/customer/reg'
        url = host + interface
        payload = {
            "phone": value[0],
            "authcode": authcode,
            "password": value[1]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def postAuthenticationData(self, case):
        # u'提交客户认证资料'
        value = str(case).split(';')
        interface = '/customer/postAuthenticationData'
        url = host + interface
        payload = {
            "name": value[0],
            "id_number": value[1],
            "id_front_pic": value[2],
            "id_rear_pic": value[3],
            "license_front_pic": value[4],
            "license_rear_pic": value[5],
            "id_inhand_pic": value[6],
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def modifyPass(self, case):
        # u'修改密码'
        value = str(case).split(';')
        interface = '/customer/modifyPass'
        url = host + interface
        authcodeinfo = App().authcode(value[2])
        authcode = authcodeinfo[1]["resultMessage"]
        payload = {
            "oldPassword": value[0],
            "newPassword": value[1],
            "authcode": authcode,
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def forgetPassword(self, case):
        # u'忘记密码'
        value = str(case).split(';')
        authcodeinfo = App().authcode(value[0])
        authcode = authcodeinfo[1]["resultMessage"]
        interface = '/customer/forgetPassword'
        url = host + interface
        payload = {
            "phone": value[0],
            "idNumber": value[1],
            "authcode": authcode,
            "newPassword": value[2],
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def login(self, case):
        # u'登陆'
        global appsession
        appsession = requests.Session()
        value = str(case).split(';')
        interface = '/customer/login'
        url = host + interface
        setinput(value[0], value[1])
        payload = {
            "phone": user,
            "password": passwd,
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def customerdetail(self, case):
        # u'查询客户信息'
        value = str(case).split(';')
        interface = '/customer/detail'
        url = host + interface
        payload = {
            "phone": value[0],
            "password": value[1],
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def detailDepositPayInfo(self):
        # u'获取押金缴纳信息'
        interface = '/customer/detailDepositPayInfo'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def customerlogout(self):
        # u'登出'
        interface = '/customer/logout'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        global appsession
        appsession = requests.Session()
        return json["result"]["resultCode"], json["result"]

    # ##########租车用车模块##########

    def carlist(self):
        # u'查询可租车辆'
        interface = '/car/list'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def cardetail(self, vehicleid):
        # u'查询车辆详情'
        interface = '/car/detail'
        url = host + interface
        payload = {
            "vehicleid": vehicleid,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carrent(self, vehicleid):
        # u'预约租用车辆'
        interface = '/car/rent'
        url = host + interface
        payload = {
            "vehicleid": vehicleid,
            "input1": user,
            "inpur2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"], json["order"]

    def carcontrol(self, vehicleid, command):
        # u'车辆控制'
        interface = '/car/control'
        url = host + interface
        payload = {
            "vehicleid": vehicleid,
            "command": command,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carupdateStatus(self, vehicleid, status):
        # u'上报车辆状态'
        interface = '/car/updateStatus'
        url = host + interface
        payload = {
            "vehicleid": vehicleid,
            "status": status,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def caruserCar(self, orderid):
        # u'取车'
        interface = '/car/userCar'
        url = host + interface
        payload = {
            "orderid": orderid,
            "input1": user,
            "inpur2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carreturnCar(self, orderid):
        # u'还车'
        interface = '/car/returnCar'
        url = host + interface
        payload = {
            "orderid": orderid,
            "input1": user,
            "inpur2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carreturnStatus(self, vehicleid):
        # u'查询还车状态'
        interface = '/car/returnStatus'
        url = host + interface
        payload = {
            "vehicleid": vehicleid,
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carlistStation(self):
        # u'获取网店列表'
        interface = '/car/listStation'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carcancelOrder(self):
        # u'取消订单'
        interface = '/car/cancelOrder'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########订单模块##########

    def currentOrder(self):
        # u'查询当前订单'
        interface = '/order/currentOrder'
        url = host + interface
        payload = {
            "input1": user,
            "inpur2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"], json["entity"]

    def detailOrderPayInfo(self):
        # u'获取缴费接口信息'
        interface = '/order/detailOrderPayInfo'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        # 暂定不测试

    def orderlist(self, maxOrderID, size):
        # u'获取订单接口'
        interface = '/order/list'
        url = host + interface
        payload = {
            "maxOrderID": maxOrderID,
            "size": size,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def representation(self, pics, memo):
        # u'故障申诉'
        interface = '/order/representation'
        url = host + interface
        payload = {
            "pics": pics,
            "memo": memo,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def orderdetail(self, orderid):
        # u'查询订单信息'
        interface = '/order/detail'
        url = host + interface
        payload = {
            "orderid": orderid,
            "input1": user,
            "input2": passwd
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########系统信息模块##########
    def sysdetail(self):
        # u'查询系统信息'
        interface = '/sys/list'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuploadFile(self, adress):
        # u'上传文件'
        file = {'file': open(adress, 'rb')}
        # file = open('D:\untitled\UI\logo.jpg', 'wb')
        interface = '/sys/uploadFile'
        url = host + interface
        a = appsession.post(url, files=file)
        # print a.json()
        # print 'http://sirui-img.oss-cn-hangzhou.aliyuncs.com/'+a.json()["result"]["resultMessage"]
        return 'http://sirui-img.oss-cn-hangzhou.aliyuncs.com/'+a.json()["result"]["resultMessage"]

    # ##########流程测试##########

    def carlistyz(self, vehicle):
        # 判断车辆是否可用
        interface = '/car/list'
        url = host + interface
        payload = {
            "input1": user,
            "input2": passwd
        }
        json = self.req_post(url, payload)
        r = r"\"vehicleid\": (\d*?),"
        vehicleidlist = re.findall(r, json)
        if vehicle in vehicleidlist:
            return True
        else:
            return False

    def carusable(self, vehicle, imei, oil, voltage, power, coordinateE, coordinateN):
        # '验证可用车状态是否正确'
        otuloging = '(1*7c|a3|106,201|101,'+imei + '|102,460079241205511|103,898600D23113837|104,otu.ost,' \
                                                   '01022300|105,a1,18|622,a1c2|)'
        oil = '(1*e7|5|614,3,7#b312,1,'+oil+',3C#|)'
        vtg = '(1*88|7|316,2,2,4B0,'+voltage+'|)'
        powr = '(1*ed|5|614,3,7#b313,1,'+power+',3C#|)'
        coordinate = '(1*b2|7|30d,11,'+hextime()+',E,'+coordinateE+',N,'+coordinateN+',0,10,c,1,1,-1,79|)'
        Tcp().connect()
        Tcp().send(otuloging)
        Tcp().send(oil)
        Tcp().send(powr)
        Tcp().send(coordinate)
        return self.carlistyz(vehicle)

    def order(self, vehicle):
        # 订单流程
        orderid = self.carrent(vehicle)[2]["orderid"]  # 租车
        if self.currentOrder()[2]["status"] == 1 and self.carlistyz(vehicle) == False:
            self.carcancelOrder()  # 取消订单
            if self.currentOrder()[2]["status"] == 0 and self.carlistyz(vehicle) == True:
                orderid = self.carrent(vehicle)[2]["orderid"]  # 租车
                if self.currentOrder()[2]["status"] == 1 and self.carlistyz(vehicle) == False:
                    time.sleep(60)  # 等待超时自动取消
                    if self.currentOrder()[2]["status"] == 0 and self.carlistyz(vehicle) == True:
                        orderid = self.carrent(vehicle)[2]["orderid"]  # 租车
                        if self.currentOrder()[2]["status"] == 1 and self.carlistyz(vehicle) == False:
                            self.caruserCar(orderid)  # 取车
                            if self.currentOrder()[2]["status"] == 1 and self.carlistyz(vehicle) == False:
                                self.carreturnCar(orderid)  # 还车
                                if self.currentOrder()[2]["status"] == 0 and self.carlistyz(vehicle) == True:
                                    print 'dd'
                                else:print u'还车错误'
                            else:print u'取车错误'
                        else:print u'第三次租车错误'
                    else:print u'自动取消错误'
                else:print u'第二步租车错误'
            else:print u'第一步取消订单错误'
        else:print u'第一步租车错误'


class Web:
    def __init__(self):
        pass

    def req_get(self, url, payload):
        r = websession.get(url, params=payload)
        return r.json()

    def req_post(self, url, payload):
        r = websession.post(url, data=payload)
        return r.json()

    def req_headpost(self, url, payload):
        headers = 'application/x-www-form-urlencoded'
        r = websession.post(url, data=payload, headers=headers)
        return r.json()

    # ##########系统管理##########

    def sysorgadd(self, case):
        # u'增加机构'
        value = str(case).split(';')
        interface = '/sys/org/add'
        url = host + interface
        payload = {
            "name": value[0],
            "memo": value[1],
            "orgPermission": value[2],
            "parentOrgLevelCode": value[3]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorgupdate(self, case):
        # u'修改机构'
        value = str(case).split(';')
        interface = '/sys/org/update'
        url = host + interface
        payload = {
            "name": value[0],
            "memo": value[1],
            "orgid":value[2],
            "orgPermission": value[3]
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorglist(self, case):
        # u'机构列表'
        value = str(case).split(';')
        interface = '/sys/org/list'
        url = host + interface
        payload = {
            "name": value[0],
            "levelCode": value[1]
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorgdelete(self, case):
        # u'删除机构'
        value = str(case).split(';')
        interface = '/sys/org/delete'
        url = host + interface
        payload = {
            "orgid": value[0],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorgtoUpdate(self, case):
        # u'增加机构前初始化机构信息'
        value = str(case).split(';')
        interface = 'sys/org/toUpdate'
        url = host + interface
        payload = {
            "orgid": value[0],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorgquerySelfAndChildren(self):
        # u'机构查询自身和下级的树'
        interface = '/sys/org/querySelfAndChildren'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysorgqueryPermissionByLevelCode(self, orgLevelCode):
        # u'机构管理-根据机构ID查询机构的权限'
        interface = '/sys/org/querySelfAndChildren'
        url = host + interface
        payload = {
            "orgLevelCode": orgLevelCode
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysroleadd(self, case):
        # u'增加角色'
        value = str(case).split(';')
        interface = '/sys/role/add'
        url = host + interface
        payload = {
            "name": value[0],
            "memo": value[1],
            "rolePermission": value[3]
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysroleupdate(self, case):
        # u'修改角色'
        value = str(case).split(';')
        interface = '/sys/role/update'
        url = host + interface
        payload = {
            "roleid": value[0],
            "name": value[1],
            "memo": value[2],
            "rolePermission": value[3]
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysrolelist(self, name):
        # u'角色列表'
        interface = '/sys/role/list'
        url = host + interface
        payload = {
            "name": name,
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysroledelete(self, case):
        # u'删除角色'
        value = str(case).split(';')
        interface = '/sys/role/delete'
        url = host + interface
        payload = {
            "roleid": value[0],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysrolequeryByLevelCode(self, case):
        # u'查询机构下所有角色'
        value = str(case).split(';')
        interface = '/sys/role/queryByLevelCode'
        url = host + interface
        payload = {
            "levelCode": value[0],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuseradd(self, case):
        # u'增加账号'
        value = str(case).split(';')
        interface = '/sys/user/add'
        url = host + interface
        payload = {
            "name": value[0],
            "username": value[1],
            "password": value[2],
            "secondPassword": value[3],
            "phone": value[4],
            "email": value[5],
            "memo": value[6],
            "levelcode": value[7],
            "roleids": value[8],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuseruptatePwd(self, case):
        # u'修改账号密码'
        value = str(case).split(';')
        interface = '/sys/user/uptatePwd'
        url = host + interface
        payload = {
            "oldPwd": value[0],
            "newPwd": value[1],
            "sNewPwd": value[2],
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserresetPassword(self, case):
        # u'重置账号密码'
        value = str(case).split(';')
        interface = '/sys/user/resetPassword'
        url = host + interface
        payload = {
            "userid": value[0],
            "newPwd": value[1],
            "sNewPwd": value[2]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserupdate(self, case):
        # u'修改账号信息'
        value = str(case).split(';')
        interface = '/sys/user/update'
        url = host + interface
        payload = {
            "userid": value[0],
            "name": value[1],
            "phone": value[2],
            "roleids": value[3],
            "email": value[4],
            "memo": value[5],
            "levelcode": value[6]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserdetail(self, case):
        # u'查看账号详情'
        value = str(case).split(';')
        interface = '/sys/user/detail'
        url = host + interface
        payload = {
            "userid": value[0],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserdelete(self, case):
        # u'删除账号'
        value = str(case).split(';')
        interface = '/sys/user/delete'
        url = host + interface
        payload = {
            "userid": value[0],
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserlist(self, case):
        # u'账号列表'
        value = str(case).split(';')
        interface = '/sys/user/list'
        url = host + interface
        payload = {
            "name": value[0],
            "username": value[1],
            "rows": value[2],
            "page": value[3],
            "phone": value[4],
            "queryLevelcode": value[5]
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysusergetImg(self):
        # u'登录获取验证码'
        interface = '/sys/user/getImg'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json

    def sysuserlogin(self, case):
        # u'登录帐号密码校验'
        global websession
        websession = requests.Session()
        value = str(case).split(';')
        interface = '/sys/user/login'
        url = host + interface
        payload = {
            "username": value[0],
            "password": value[1],
            "inputRandomCode": value[2]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def sysuserloginOut(self):
        # u'登出'
        interface = '/sys/user/loginOut'
        url = host + interface
        payload = {
        }
        json = self.req_post(url, payload)
        global websession
        websession = requests.Session()
        return json["result"]["resultCode"], json["result"]

    # ##########配置管理##########

    def configpayset(self, case):
        # u'支付接口配置/修改'
        value = str(case).split(';')
        interface = '/config/pay/set'
        url = host + interface
        payload = {
            "settingID": value[0],
            "type": value[1],
            "saveCode": value[2],
            "params": value[3]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configpaylist(self):
        # u'获取支付配置'
        interface = '/config/pay/list'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configruleset(self, case):
        # u'规则设置'
        value = str(case).split(';')
        interface = '/config/rule/set'
        url = host + interface
        payload = {
            "type": value[0],
            "params": value[1],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configrulelist(self):
        # u'规则列表'
        interface = '/config/rule/list'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configcustomerServiceset(self, case):
        # u'客服查询'
        value = str(case).split(';')
        interface = '/config/customerService/set'
        url = host + interface
        payload = {
            "settingID": value[0],
            "phone": value[1],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configcustomerServicedetail(self, case):
        # u'客服查询'
        value = str(case).split(';')
        interface = '/config/customerService/detail'
        url = host + interface
        payload = {
            "type": value[0],
            "params": value[1],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configdepositset(self, case):
        # u'押金设置'
        value = str(case).split(';')
        interface = '/config/deposit/set'
        url = host + interface
        payload = {
            "price": value[0],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configdepositdetail(self):
        # u'押金查询'
        interface = '/config/deposit/detail'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def configpaygetSaveCode(self):
        # u'获取支付配置安全验证码'
        interface = '/config/pay/getSaveCode'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########车辆管理##########

    def carvehicleModeladd(self, case):
        # u'车型管理新增'
        value = str(case).split(';')
        interface = '/car/vehicleModel/add'
        url = host + interface
        payload = {
            "displacement_value": value[0],
            "name": value[1],
            "serialname": value[2],
            "model_year": value[3],
            "classfy": value[4],
            "gearbox_type": value[5],
            "electric": value[6],
            "seat_number": value[7],
            "oil_type": value[8],
            "brandname": value[9],
            "displacement_type": value[10],
            "left_oil_type": value[11],
            "tankage": value[12],
            "max_mileage": value[13],
            "pic_uri": value[14],
            "mile_price": value[16],
            "time_price": value[17],
            "sirui_vmid": value[18]
        }
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleModellist(self, case):
        # u'车型管理列表'
        value = str(case).split(';')
        interface = '/car/vehicleModel/list'
        url = host + interface
        payload = {
            "brandname": value[0],
            "name": value[1],
        }
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleModelupdate(self, case):
        # u'车型管理列表'
        value = str(case).split(';')
        interface = '/car/vehicleModel/update'
        url = host + interface
        payload = {
            "displacement_value": value[0],
            "name": value[1],
            "serialname": value[2],
            "model_year": value[3],
            "classfy": value[4],
            "gearbox_type": value[5],
            "electric": value[6],
            "seat_number": value[7],
            "oil_type": value[8],
            "brandname": value[9],
            "displacement_type": value[10],
            "left_oil_type": value[11],
            "tankage": value[12],
            "max_mileage": value[13],
            "pic_uri": value[14],
            "mile_price": value[16],
            "time_price": value[17],
            "sirui_vmid": value[18],
            "vmid": value[19]
        }
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleModeldelete(self, vmid):
        # u'车型管理删除'
        interface = '/car/vehicleModel/delete'
        url = host + interface
        payload = {
            "vmid": vmid
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleModelqueryVMTree(self):
        # u'车型管理-查询车型树'
        interface = '/car/vehicleModel/queryVMTree'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carfeedetail(self, feeID):
        # u'车型管理-查询相应的计费'
        interface = '/car/fee/detail'
        url = host + interface
        payload = {
            "feeID": feeID,
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleModeldetail(self, vmid):
        # u'车型管理-详情'
        interface = '/car/vehicleModel/detail'
        url = host + interface
        payload = {
            "vmid": vmid
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleadd(self, case):
        # u'车辆管理新增'
        value = str(case).split(';')
        interface = '/car/vehicle/add'
        url = host + interface
        payload = {
            "vmid": value[0],
            "vin": value[1],
            "platenumber": value[2],
            "color": value[3],
            "available": value[4],
            "buy_date": value[5],
            "annual_date": value[6],
            "insurance_date": value[7],
            "oil_type": value[8],
            "published": value[9],
            "under_maintain": value[10],
        }
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicleupdate(self, case):
        # u'车辆管理更新'
        value = str(case).split(';')
        interface = '/car/vehicle/update'
        url = host + interface
        payload = {
            "vmid": value[0],
            "platenumber": value[1],
            "color": value[2],
            "available": value[3],
            "buy_date": value[4],
            "annual_date": value[5],
            "insurance_date": value[6],
            "oil_type": value[7],
            "published": value[8],
            "under_maintain": value[9],
            "vehicleid": value[10],
        }
        
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehiclelist(self):
        # u'车辆管理列表'
        interface = '/car/vehicle/list'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehicledelete(self, vehicleid):
        # u'车辆管理删除'
        interface = '/car/vehicle/delete'
        url = host + interface
        payload = {
            "vehicleid": vehicleid
        }
        json = self.req_headpost(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carmonitorlist(self):
        # u'车辆监控列表'
        interface = '/car/monitor/list'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carmonitortripList(self):
        # u'车辆监控历史轨迹'
        interface = '/car/monitor/tripList'
        url = host + interface
        payload = {

        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def carvehiclestatus(self):
        # u'车辆监控当前状态'
        interface = '/car/vehicle/status'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def caralarmvehicleList(self):
        # u'报警管理当前车辆列表'
        interface = '/car/alarm/vehicleList'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def caralarmhistoryList(self):
        # u'报警管理历史记录列表'
        interface = '/car/alarm/historyList'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########网点管理##########

    def stationstationadd(self, case):
        # u'网点管理新增'
        value = str(case).split(';')
        interface = '/station/station/add'
        url = host + interface
        payload = {
            "name": value[0],
            "address": value[1],
            "baidu_address": value[2],
            "lat": value[3],
            "lng": value[4],
            "number_of_park": value[5],
            "levelcode": value[6],
            "keyword": value[7],
            "published": value[8],
            "range": value[9]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def stationstationupdate(self, case):
        # u'网点管理更新'
        value = str(case).split(';')
        interface = '/station/station/update'
        url = host + interface
        payload = {
            "stationid": value[0],
            "name": value[1],
            "address": value[2],
            "baidu_address": value[3],
            "lat": value[4],
            "lng": value[5],
            "number_of_park": value[6],
            "levelcode": value[7],
            "keyword": value[8],
            "published": value[9],
            "range": value[10]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def stationstationlist(self, case):
        # u'网点管理列表'
        value = str(case).split(';')
        interface = '/station/station/list'
        url = host + interface
        payload = {
            "keyWord": value[0],
            "levelcode": value[1],
            "published": value[2],
            "rows": value[3],
            "page": value[4],
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def stationstationdelete(self, stationid):
        # u'网点管理删除'
        interface = '/station/station/delete'
        url = host + interface
        payload = {
            "stationid": stationid
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########客户管理##########

    def customercustomerlist(self, case):
        # u'客户管理列表'
        value = str(case).split(';')
        interface = '/customer/customer/list'
        url = host + interface
        payload = {
            "rows": value[0],
            "page": value[1],
            "keyWord": value[2],
            "audit_status": value[3],
            "on_blackList": value[4],
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def customercustomeraudit(self, case):
        # u'客户管理审核'
        value = str(case).split(';')
        interface = '/customer/customer/audit'
        url = host + interface
        payload = {
            "customerid": value[0],
            "audit_status": value[1],
            "reason": value[2],
            "license_number": value[3],
            "license_type": value[4],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def customercustomerupdate(self, case):
        # u'客户管理更新'
        value = str(case).split(';')
        interface = '/customer/customer/update'
        url = host + interface
        payload = {
            "customerid": value[0],
            "on_blackList": value[1],
            "memo": value[2],
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########运营管理##########

    def runrunlist(self):
        # u'运营管理列表'
        interface = '/run/run/list'
        url = host + interface
        payload = {
        }
        json = self.req_get(url, payload)
        return json["result"]["resultCode"], json["result"]

    def runrunset(self, case):
        # u'运营管理设置'
        value = str(case).split(';')
        interface = '/run/run/set'
        url = host + interface
        payload = {
            "settingID":  value[0],
            "params": value[1]
        }
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########订单管理##########

    def orderorderlist(self):
        # u'订单管理列表'
        interface = '/order/order/list'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def orderorderdetail(self):
        # u'订单管理详情'
        interface = '/order/order/detail'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def orderordercancel(self):
        # u'订单管理取消'
        interface = '/order/order/cancel'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    # ##########报表管理##########

    def statisticcustomerlist(self):
        # u'报表用户租车统计'
        interface = '/statistic/customer/list'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def statisticvehiclelist(self):
        # u'报表车辆出租统计'
        interface = '/statistic/vehicle/list'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]

    def statisticincomelist(self):
        # u'报表收支列表'
        interface = '/statistic/income/list'
        url = host + interface
        payload = {
        }
        
        json = self.req_post(url, payload)
        return json["result"]["resultCode"], json["result"]


appsession = requests.Session()
websession = requests.Session()

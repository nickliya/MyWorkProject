#coding=utf-8
#create by 15025463191 2017/07/10
# _metaclass_ = type
import requests

s = requests.Session()

def setHost(x):
    global host
    host = x

def isSucc():
    if json["result"]["resultCode"]==0:
        print 'pass'
        try:
            print 'authCode:'+json["option"]["authCode"]
        except:pass
    else:
        print "resultCode:"+str(json["result"]["resultCode"])+'\t'+"resultMessage:"+json["result"]["resultMessage"]

def req_get(url,payload):
    r=s.get(url, params=payload)
    return r.json()

def req_post(url,payload):
    r = s.post(url, data=payload)
    return r.json()

class Customer:
    '''客户模块'''
    def authcode(self,phone):
        u'获取验证码'
        interface = '/provider/testProvide/sendAuthCode'
        url = host+interface
        # phone=random.choice(['139','188','185','136','158','151'])+''.join(random.choice("0123456789") for i in range(8))
        payload = {
            "phone":phone
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def reg(self,phone,authcode,pawword):
        u'注册'
        interface = '/customer/reg'
        url = host+interface
        payload = {
            "phone": phone,
            "authcode": authcode,
            "pawword": pawword
        }
        global json
        json=req_post(url, payload)
        isSucc()
    def postAuthenticationData(self,name,idNumber,frontOfIDCard,backOfIDCard,frontOfDL,backOfDL):
        u'提交客户认证资料'
        interface = '/customer/postAuthenticationData'
        url = host+interface
        payload = {
            "name": name,
            "idNumber": idNumber,
            "frontOfIDCard": frontOfIDCard,
            "backOfIDCard": backOfIDCard,
            "frontOfDL": frontOfDL,
            "backOfDL": backOfDL
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def modifyPass(self,oldPassword,newPassword,authcode):
        u'修改密码'
        interface='/customer/modifyPass'
        url=host+interface
        payload={
            "oldPassword": oldPassword,
            "newPassword": newPassword,
            "authcode": authcode
        }
        global json
        json=req_post(url, payload)
        isSucc()
    def forgetPassword(self, phone, idNumber, authcode, newPassword):
        u'忘记密码'
        interface='/customer/forgetPassword'
        url=host+interface
        payload={
            "phone": phone,
            "idNumber": idNumber,
            "authcode": authcode,
            "newPassword": newPassword,
        }
        global json
        json=req_post(url, payload)
        isSucc()
    def login(self,phone,password):
        u'登陆'
        interface='/customer/login'
        url=host+interface
        payload={
            "phone": phone,
            "password": password,
        }
        global json
        json=req_post(url, payload)
        isSucc()
    def detail(self,phone,password):
        u'查询客户信息'
        interface='/customer/detail'
        url=host+interface
        payload={
            "phone": phone,
            "password": password,
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def detailDepositPayInfo(self):
        u'获取押金缴纳信息'
        interface='/customer/detailDepositPayInfo'
        url=host+interface
        payload = {
        }
        global json
        json = req_post(url, payload)
        isSucc()

class Car:
    '''租车用车模块'''
    def list(self):
        u'查询可租车辆'
        interface = '/car/list'
        url = host+interface
        payload = {
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def detail(self,vehicleid):
        u'查询车辆详情'
        interface = '/car/detail'
        url = host+interface
        payload = {
            "vehicleid": vehicleid
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def rent(self,vehicleid):
        u'预约租用车辆'
        interface = '/car/detail'
        url = host+interface
        payload = {
            "vehicleid": vehicleid
        }
        global json
        json = req_post(url, payload)
        isSucc()
    def control(self,vehicleid,command):
        u'车辆控制'
        interface = '/car/detail'
        url = host+interface
        payload = {
            "vehicleid": vehicleid,
            "command": command
        }
        global json
        json = req_post(url, payload)
        isSucc()


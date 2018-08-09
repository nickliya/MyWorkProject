# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from Yq_Djago import models
import json
import MySQLdb
from django.http import QueryDict
import time


def login(request):
    return render(request, 'loginsys/login.html')


def homepage(request):
    request.encoding = 'utf-8'
    res = request.POST
    if res["user"] == u'的':
        return render(request, 'trip/hello.html')
    else:
        return render(request, 'loginsys/login.html')


def returndata(request):
    info = models.Interface.objects.get(payload=23321)
    response_data = {}
    isdict = model_to_dict(info)
    response_data["resultcode"] = 0
    response_data["message"] = isdict
    return HttpResponse(JsonResponse(response_data), content_type="application/json")


# def returndata(request):
#     info = models.Interface.objects.all().values("interfaceName")
#     isdict = serializers.serialize('json', info)
#     return HttpResponse(isdict, content_type="application/json")


def getinterface(request):
    conn = MySQLdb.connect(host='192.168.6.235', user='root', passwd='123456')
    cur = conn.cursor()
    # sql = "SHOW TABLES FROM yangqing"
    sql = "SELECT interfaceName FROM yangqing.interface;"
    cur.execute(sql)
    info = cur.fetchall()
    listinfo = []
    for i in info:
        listinfo.append(i[0])
    response_data = {}
    response_data["resultcode"] = 0
    response_data["message"] = listinfo
    return HttpResponse(JsonResponse(response_data), content_type="application/json")


def getinterfacepayload(request):
    request.encoding = 'utf-8'
    res = request.POST
    name = res.values()
    info = models.Interface.objects.filter(interfaceName=name[0])
    isdict = info.values("payload").get()
    isdict["payload"] = eval(isdict["payload"])
    response_data = {}
    response_data["resultcode"] = 0
    response_data["message"] = isdict
    return HttpResponse(JsonResponse(response_data), content_type="application/json")


@accept_websocket
def socket(request):
    if not request.is_websocket():  # 判断是不是websocket连接
        try:  # 如果是普通的http方法
            message = request.POST['message']
            return HttpResponse(message)
        except:
            return render(request, 'loginsys/login.html')
    else:
        response = request.websocket
        # msg = response.wait()
        for i in response:
            response.send()
        # request.websocket.send(response.read())  # 发送消息到客户端
        request.websocket.close()

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from Yq_Djago import models
import json
import MySQLdb

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
    conn = MySQLdb.connect(host='192.168.6.237', user='root', passwd='123456')
    cur = conn.cursor()
    sql = "SHOW TABLES FROM yangqing"
    cur.execute(sql)
    info = cur.fetchall()
    listinfo = []
    for i in info:
        listinfo.append(i[0])
    response_data = {}
    response_data["resultcode"] = 0
    response_data["message"] = listinfo
    return HttpResponse(JsonResponse(response_data), content_type="application/json")

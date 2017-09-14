# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

#
# def hello(request):
#     return HttpResponse("Hello world ! ")


def hello(request):
    context = {'hello': 'Hello World!'}
    return render(request, 'trip/hello.html')


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
# Create your models here.


class Interface(models.Model):
    interfaceName = models.CharField(max_length=64)
    payload = models.CharField(max_length=512)

    class Meta:
        db_table = "interface"  # 自定义表的名称
        app_label = "Yq_Djago"  # 定义是哪个app


class Interface2(models.Model):
    interfaceName = models.CharField(max_length=64)
    payload = models.CharField(max_length=512)

    class Meta:
        db_table = "interface2"
        app_label = "Yq_Djago"

admin.site.register(Interface)
admin.site.register(Interface2)

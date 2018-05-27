#!/usr/bin/dev python
# -*- coding:utf-8 -*-
# __author__ = "guoxing"
# Date:2018/5/26

from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    # url(r'^test.html$', views.test),
    url(r'^serverlist',views.server_list),
    url(r'^serveradd',views.server_add),
]
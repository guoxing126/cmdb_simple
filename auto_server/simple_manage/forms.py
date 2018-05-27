#!/usr/bin/dev python
# -*- coding:utf-8 -*-
# __author__ = "guoxing"
# Date:2018/5/26

from django import forms

class ServerForm(forms.Form):
    hostname = forms.CharField(max_length=128)
    sn = forms.CharField(max_length=128,)
    manufacturer = forms.CharField(max_length=64)
    model = forms.CharField(max_length=64)

    manage_ip = forms.GenericIPAddressField()

    os_platform = forms.CharField(max_length=16)
    os_version = forms.CharField(max_length=128)

    cpu_count = forms.IntegerField()
    cpu_physical_count = forms.IntegerField()
    cpu_model = forms.CharField(max_length=128)

    create_at = forms.DateTimeField()

    latest_date = forms.DateTimeField()
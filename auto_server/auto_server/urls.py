"""auto_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from repository import urls
from django.shortcuts import render, HttpResponse,redirect
from django.urls import reverse
from smart_admin.service import service

# def index(request):
#     test_url=reverse('xx',kwargs={'a1':'a1'})
#     return redirect(test_url)
#
# def test(request,*args,**kwargs):
#     return HttpResponse('test')

urlpatterns = [
    # url(r'^index/',index),
    # url(r'^test/asdf/(?P<a1>\w+)/asdwfv/',test,name='xx'),
    # url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    # url(r'^smartadmin/', ([
    #                           url(r'^repository/', ([
    #                                                     url(r'^userinfo/', index),
    #                                                     url(r'^userinfo/add', index),
    #                                                     url(r'^userinfo/(\d+)/delete', index),
    #                                                     url(r'^userinfo/(\d+)/change', index),
    #                                                 ], 'xx', 'xx'))
    #                       ], 'xx', 'xx')),
    url(r'^smartadmin/', service.site.urls),
    url(r'^', include('web.urls')),
    # 上面那条路由给js—curd专用
]

from django.shortcuts import render,HttpResponse
from django import forms
from repository.models import Server,Disk,Memory,NIC
from .forms import ServerForm

def server_list(request):
    serverlist = Server.objects.all()
    # print(serverlist)
    return render(request,'serverlist.html',{'serverlist':serverlist})

def server_add(request):
    if request.method == 'GET':
        obj = ServerForm()
        return render(request,'serveradd.html',{'obj':obj})
    else:
        obj = ServerForm(data=request.POST)
        if obj.is_valid():
            return HttpResponse('ok')
        else:
            return render(request,'serveradd.html',{'obj':obj})
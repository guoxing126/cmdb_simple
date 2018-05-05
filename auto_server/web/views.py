from django.shortcuts import render, HttpResponse
from repository import models
from django.http import JsonResponse
import json
from .service.server import ServerService
from .service.disk import DiskService


# Create your views here.
def server(request):
    service_url='/server_json.html'
    return render(request, 'service.html',{'service_url':service_url})


def server_json(request):
    server_service = ServerService(request)

    if request.method == 'GET':
        response = server_service.fetch()
        return HttpResponse(json.dumps(response))

    elif request.method == 'DELETE':
        response = server_service.delete()
        return HttpResponse(json.dumps(response))

    elif request.method == "PUT":
        response = server_service.update()
        return HttpResponse(json.dumps(response))

def test_server(request):
    data_list = models.Server.objects.all().values('hostname', 'server_status_id')

    def dis_choices(data_list):
        for row in data_list:
            for item in models.Server.server_status_choices:
                if item[0] == row['server_status_id']:
                    row['server_status_id_name'] = item[1]
                    break
            yield row

    return render(request, 'test_server.html', {'server_list': dis_choices(data_list)})

def disk(request):
    service_url = '/disk_json.html'
    return render(request, 'service.html', {'service_url': service_url})

def disk_json(request):
    disk_service=DiskService(request)

    if request.method == 'GET':
        response = disk_service.fetch()
        return HttpResponse(json.dumps(response))

    elif request.method == 'DELETE':
        response = disk_service.delete()
        return HttpResponse(json.dumps(response))

    elif request.method == "PUT":
        response = disk_service.update()
        return HttpResponse(json.dumps(response))
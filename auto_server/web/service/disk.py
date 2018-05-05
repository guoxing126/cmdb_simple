import json
from repository import models
from utils.page import Pagination
from .base import BasiceService
from ..service_config import disk as disk_config

class DiskService(BasiceService):
    def __init__(self,request):
        self.request=request
        self.table_config=disk_config.table_config
        self.search_config=disk_config.search_config
    def fetch(self):
        current_page = self.request.GET.get('pageNum')
        total_item_count = models.Disk.objects.filter(self.conditions()).count()
        page_obj = Pagination(current_page, total_item_count, per_page_count=5)

        server_list = models.Disk.objects.filter(self.conditions()).values(*self.values())[page_obj.start:page_obj.end]
        server_list = list(server_list)

        response = {
            # 'status':True,
            'table_name':disk_config.table_name,
            'search_config': disk_config.search_config,
            'data_list': server_list,
            'table_config': disk_config.table_config,
            'global_choices_dict': {
                'server_status_choices': models.Server.server_status_choices,
            },
            'page_html': page_obj.page_html_js(),
        }
        return response

    def delete(self):
        response = {'status': True, 'msg': None}
        id_list = json.loads(self.request.body.decode('utf-8'))

        for id in id_list:
            try:
                # models.Server.objects.filter(id=id).delete()
                pass
            except Exception as e:
                response['status'] = False
                response['msg'] = str(e)
        return response

    def update(self):
        response = {'status': True, 'msg': []}
        update_dict = json.loads(self.request.body.decode('utf-8'))
        # [
        #     {'id': '2', 'hostname': 'c1.com123'},
        #     {'id': '3', 'sn': 'c2cwevfwvw'}
        # ]
        for item in update_dict:
            try:
                server_id = item['id']
                item.pop('id')
                models.Server.objects.filter(id=server_id).update(**item)
            except Exception as e:
                response['status'] = False
                response['msg'].append(str(e))
        return response
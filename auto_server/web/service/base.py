import json
from django.db.models import Q

class BasiceService(object):
    def values(self):
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    # 获取搜索条件
    def conditions(self):
        conditions_dict = json.loads(self.request.GET.get('conditions'))
        con = Q()
        for k, v in conditions_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item))
            con.add(temp, 'AND')
        return con
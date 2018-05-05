table_name="服务器列表"

search_config=[
            {'name':'hostname__contains','title':'主机名','type':'input',},
            {'name':'sn', 'title': '序列号','type':'input',},
            {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select','choices_name':'server_status_choices',},
        ]

table_config=[
            {
                'q': None,
                'title': '选择',
                'display':True,
                'text':{'tpl':'<input type="checkbox" value="{id}" />','kwargs':{'id':'@id'},},
                'attr':{'class':'c1','id':'@id',},
            },
            {
                'q': 'id',
                'title': 'ID',
                'display':False,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'},},
                'attr': {},
            },
            {
                'q':'hostname',
                'title':'主机名',
                'display':True,
                'text':{'tpl':'{a1}','kwargs':{'a1':'@hostname'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@hostname',
                    'name':'hostname',
                },
            },
            {
                'q':'sn',
                'title': '序列号',
                'display':True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@sn',
                    'name': 'sn',
                },
            },
            {
                'q': 'os_platform',
                'title': '操作系统',
                'display': True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_platform'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@os_platform',
                    'name': 'os_platform',
                },
            },
            {
                'q': 'server_status_id',
                'title': '服务器状态',
                'display':True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@server_status_choices'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'select',
                    'choices-key':'server_status_choices',
                    'origin':'@server_status_id',
                    'name': 'server_status_id',
                },
            },
            {
                'q': None,
                'title': '操作',
                'display':True,
                'text': {'tpl': '<a href="/edit/{eid}">编辑</a> | <a href="/del/{did}">删除</a>', 'kwargs': {'eid': '@id','did': '@id'},},
                'attr': {'class':'c1',},
            },
        ]
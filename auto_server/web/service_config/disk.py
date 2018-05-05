table_name="硬盘列表"

search_config=[
            {'name':'model__contains','title':'硬盘型号','type':'input',},
            {'name':'slot', 'title': '槽位','type':'input',},
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
                'q':'slot',
                'title':'槽位',
                'display':True,
                'text':{'tpl':'{a1}','kwargs':{'a1':'@slot'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@slot',
                    'name':'slot',
                },
            },
            {
                'q':'model',
                'title': '硬盘型号',
                'display':True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@model'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@model',
                    'name': 'model',
                },
            },
            {
                'q': 'capacity',
                'title': '容量',
                'display': True,
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@capacity'},},
                'attr': {
                    'class':'c1',
                    'edit':'true',
                    'edit-type':'input',
                    'origin':'@capacity',
                    'name': 'capacity',
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
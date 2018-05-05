from smart_admin.service import service
from . import models
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from django.forms import widgets as form_widgets

# class ServerInfoModelForm(ModelForm):
#     class Meta:
#         model=models.Server
#         fields="__all__"
#         widgets={
#             'hostname':form_widgets.TextInput(attrs={'class':'form_control',}),
#             'os_platform':form_widgets.TextInput(attrs={'class':'form_control',}),
#         }

class PermissionConfig(object):
    def get_show_btn(self):
        return True
    def get_list_display(self):
        return super().get_list_display()
    def get_actions(self):
        return super().get_actions()

# ############# 服务器相关配置 ###############
class ServerInfoConfig(PermissionConfig,service.ModelSm):
    def xxxx(self, ojb=None, is_header=False):
        if is_header:
            return '列名称'
        return '自定义列'

    list_display = ['id', 'hostname', xxxx]

    # model_form = ServerInfoModelForm

service.site.register(models.Server, ServerInfoConfig)

# ############# 硬盘相关配置 ###############
class DiskInfoConfig(service.ModelSm):
    list_display = ['id','model','capacity',]
    # list_filter=['server_obj','slot',]
    list_filter=[
        service.OptionConfig('server_obj',True),
        service.OptionConfig('slot', False),
    ]

service.site.register(models.Disk,DiskInfoConfig)

# ############# 内存相关配置 ###############
service.site.register(models.Memory)

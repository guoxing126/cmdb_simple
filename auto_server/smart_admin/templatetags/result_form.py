from django.template.library import Library
from types import FunctionType,MethodType
from django.forms.models import ModelChoiceField,ModelMultipleChoiceField
from django.urls import reverse
from smart_admin.service.service import site

register=Library()

def add_model(model_form_obj):
    for item in model_form_obj:
        tpl={'has_popup':False,'item':item,'popup_url':None,}
        if (isinstance(item.field,ModelChoiceField) or isinstance(item.field,ModelMultipleChoiceField)) and item.field.queryset.model in site._registry:
            tpl['has_popup']=True
            field_class=item.field.queryset.model
            app_label=field_class._meta.app_label
            model_name=field_class._meta.model_name
            url=reverse('%s:%s_%s_add'%(site.namespace,app_label,model_name))
            url='%s?_popup=%s'%(url,item.auto_id)
            tpl['popup_url']=url
        yield tpl

@register.inclusion_tag('smart_admin/change_form.html')
def show_form(model_form_obj):
    return {'form':add_model(model_form_obj)}

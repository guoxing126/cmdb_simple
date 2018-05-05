from django.template.library import Library
from types import FunctionType,MethodType

register=Library()

@register.inclusion_tag('smart_admin/change_list_table.html')
def show_result_list(cl):
    # 定制表头
    def headers():
        if not cl.list_display:
            yield cl.model_config_obj.model_class._meta.model_name
        else:
            for v in cl.list_display:
                if isinstance(v, FunctionType):
                    yield v(cl.model_config_obj,is_header=True)
                else:
                    yield cl.model_config_obj.model_class._meta.get_field(v).verbose_name
                    # yield v(self,True) if isinstance(v, FunctionType) else self.model_class._meta.get_field(v).verbose_name

    # 填充表格内容
    def body():
        for row in cl.data_list:
            if not cl.list_display:
                yield [str(row), ]
            else:
                row_data = []
                for name in cl.list_display:
                    if isinstance(name, FunctionType):
                        row_data.append(name(cl.model_config_obj,row))
                    else:
                        row_data.append(getattr(row, name))
                yield row_data
    return {
        'headers': headers(),
        'body': body(),
    }

@register.inclusion_tag('smart_admin/change_list_actions.html')
def show_actions(cl):
    def yield_actions(cl):
        for item in cl.actions:
            yield (item.__name__,item.short_desc,)
    return {'yield_actions':yield_actions(cl)}
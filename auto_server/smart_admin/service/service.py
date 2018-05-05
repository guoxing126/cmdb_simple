from django.shortcuts import HttpResponse, render, redirect
from types import FunctionType
from django.urls import reverse
from django.utils.safestring import mark_safe
from utils.page import Pagination
from django.http import QueryDict
from django.forms import ModelForm
import copy


class OptionConfig(object):
    def __init__(self, name_or_func, is_multi=False):
        self.name_or_func = name_or_func
        self.is_multi = is_multi

    @property
    def is_func(self):
        if isinstance(self.name_or_func, FunctionType):
            return True

    @property
    def name(self):
        if isinstance(self.name_or_func, FunctionType):
            return self.name_or_func.__name__
        else:
            return self.name_or_func


class RowItems(object):
    def __init__(self, option, data_list, params):
        self.option = option
        self.data_list = data_list
        self.params = copy.deepcopy(params)
        self.params._mutable = True

    def __iter__(self):
        if self.option.is_multi:
            current_pk_or_list = self.params.getlist(self.option.name)
        else:
            current_pk_or_list = self.params.get(self.option.name)

        if self.params.get(self.option.name):
            # 如果name在，才在‘全部’按钮中取出该项，否则会报错
            self.params.pop(self.option.name)
            url = self.params.urlencode()
            yield mark_safe("<a href='?%s'>全部</a>" % (url,))
        else:
            url = self.params.urlencode()
            yield mark_safe("<a class='active' href='?%s'>全部</a>" % (url,))

        for obj in self.data_list:
            pk = str(obj.pk)
            text = str(obj)
            # print('pk',pk)
            # print('text',text)

            # print('原来的',self.params)
            if self.option.is_multi:
                if pk not in current_pk_or_list:
                    temp = []
                    temp.extend(current_pk_or_list)
                    temp.append(pk)
                    # self.params[self.option.name] = temp
                    self.params.setlist(self.option.name,temp)
            else:
                self.params[self.option.name] = pk

            url = self.params.urlencode()
            # print('修改的',self.params,url)
            if not self.option.is_multi:
                if current_pk_or_list == pk:
                    tpl = "<a class='active' href='?%s'>%s</a>" % (url, text)
                else:
                    tpl = "<a href='?%s'>%s</a>" % (url, text)
            else:
                if pk in current_pk_or_list:
                    tpl = "<a class='active' href='?%s'>%s</a>" % (url, text)
                else:
                    tpl = "<a href='?%s'>%s</a>" % (url, text)
            yield mark_safe(tpl)


class ChangeList(object):
    def __init__(self, data_list, model_config_obj):
        self.list_display = model_config_obj.get_list_display()
        self.actions = model_config_obj.get_actions()
        self.list_filter = model_config_obj.get_list_filter()

        self.model_config_obj = model_config_obj
        request_get = copy.deepcopy(model_config_obj.request.GET)
        request_get._mutable = True

        page = Pagination(
            current_page=model_config_obj.request.GET.get('page'),
            total_item_count=data_list.count(),
            base_url=model_config_obj.request.path_info,
            per_page_count=5,
            request_params=request_get,
        )

        self.data_list = data_list[page.start:page.end]
        self.page_html = page.page_html()

    def add_html(self):
        '''
        在changelist页面生产添加按钮
        :return:
        '''
        app_model_label = self.model_config_obj.model_class._meta.app_label, self.model_config_obj.model_class._meta.model_name
        add_url = reverse('sm:%s_%s_add' % app_model_label)

        query_dict = QueryDict(mutable=True)
        query_dict['_qwertyu'] = self.model_config_obj.request.GET.urlencode()

        add_html = mark_safe('<a class="btn btn-primary" href="%s?%s">增加</a>' % (add_url, query_dict.urlencode(),))
        return add_html

    def gen_list_filter(self):
        '''
        在changelist页面生成组合搜索的过滤条件
        :return:
        '''
        model_class = self.model_config_obj.model_class
        params = self.model_config_obj.request.GET
        # request是IO对象，不能直接复制，只能复制其GET等方法的返回值
        for option in self.list_filter:
            field_obj = model_class._meta.get_field(option.name)
            from django.db.models.fields.related import RelatedField
            if isinstance(field_obj, RelatedField):
                field_related_class = field_obj.rel.to
                # data_list = field_related_class.objects.all()
                row_items = RowItems(option, field_related_class.objects.all(), params)
            else:
                # data_list = model_class.objects.all()
                row_items = RowItems(option, model_class.objects.all(), params)
            yield row_items


class ModelSm(object):
    def __init__(self, model_class, site):
        self.model_class = model_class
        self.site = site
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    def xxxx(self, obj=None, is_header=False):
        if is_header:
            return '列名称'
        return '自定义列'

    '''定制显示'''
    list_display = []

    def cbox(self, obj=None, is_header=False):
        if is_header:
            return '选择'
        else:
            tpl = '<input type="checkbox" name="pk" value="%s">' % (obj.pk)
            return mark_safe(tpl)

    def option(self, obj=None, is_header=False):
        if is_header:
            return '操作'
        else:
            app_model_label = self.model_class._meta.app_label, self.model_class._meta.model_name
            edit_url = reverse('sm:%s_%s_change' % app_model_label, args=(obj.pk,))
            del_url = reverse('sm:%s_%s_delete' % app_model_label, args=(obj.pk,))
            query_dict = QueryDict(mutable=True)
            query_dict['_qwertyu'] = self.request.GET.urlencode()
            tpl = '<a href="%s?%s">编辑</a>|<a href="%s?%s">删除</a>' % (
                edit_url, query_dict.urlencode(), del_url, query_dict.urlencode(),)
            return mark_safe(tpl)

    def get_list_display(self):
        result = []
        if self.list_display:
            result.extend(self.list_display)
            result.insert(0, ModelSm.cbox)
            # result_list.py会对传入的对象进行判断，因为判断标准是函数，所以要传入类的函数
            result.append(ModelSm.option)
        return result

    show_add_btn = True

    '''定制actions'''

    def mulit_del(self):
        pk_list = self.request.POST.getlist('pk')
        # self.model_class.objects.filter(pk__in=pk_list).delete()

    mulit_del.short_desc = '批量删除'

    def init_actions(self):
        pass

    init_actions.short_desc = '初始化'

    actions = []

    def get_actions(self):
        result = []
        result.extend(self.actions)
        result.append(ModelSm.mulit_del)
        result.append(ModelSm.init_actions)
        return result

    '''定制modelform'''
    model_form = None

    def get_model_form_class(self):
        result = self.model_form
        if not result:
            class DefaultModelForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = "__all__"

            result = DefaultModelForm
        return result

    def get_show_btn(self):
        return self.show_add_btn

    '''定制组合筛选'''
    list_filter = []

    def get_list_filter(self):
        result = []
        result.extend(self.list_filter)
        return result

    def changelist_view(self, request, *args, **kwargs):
        '''
        查看列表页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        self.request = request
        if request.method == "POST":
            action_name = request.POST.get('action')
            action_method = getattr(self, action_name, None)
            # 反射会在优先自己的名称空间内取值，如果取到，这里不是函数，而是方法，执行方法不用传self
            if action_method:
                action_method()
        # elif request.method=="GET":
        data_list = self.model_class.objects.all()

        cl = ChangeList(data_list, self)

        context = {
            # 'data_list': data_list,
            # 'list_display':self.list_display,
            'cl': cl,
        }
        return render(request, 'smart_admin/changelist.html', context)

    def add_view(self, request, *args, **kwargs):
        '''
        查看添加页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        self.request = request
        popup = request.GET.get('_popup')
        if request.method == "GET":
            form = self.get_model_form_class()()
            context = {
                'form': form,
            }
            if popup:
                return render(request, 'smart_admin/add_popup.html', context)
            else:
                return render(request, 'smart_admin/add.html', context)
        elif request.method == "POST":
            form = self.get_model_form_class()(data=request.POST)
            if form.is_valid():
                obj = form.save()
                if popup:
                    result = {
                        'id': obj.pk,
                        'text': str(obj),
                        'popup_id': popup,
                    }
                    return render(request, 'smart_admin/popup_response.html', result)
                else:
                    # 添加成功后，跳转到原浏览页面，否则还停留在添加页面并显示错误
                    change_list_url_params = request.GET.get('_qwertyu')
                    base_url = self.reverse_change_list_url()
                    back_url = '%s?%s' % (base_url, change_list_url_params)
                    return redirect(back_url)
            context = {
                'form': form,
            }
            return render(request, 'smart_admin/add.html', context)

    def delete_view(self, request, *args, **kwargs):
        return HttpResponse('删除页面')

    def change_view(self, request, pk, *args, **kwargs):
        '''
        修改页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        # 获取对象
        self.request = request
        obj = self.model_class.objects.filter(pk=pk).first()
        if request.method == "GET":
            form = self.get_model_form_class()(instance=obj)
            context = {
                'form': form,
            }
            return render(request, 'smart_admin/change.html', context)
        elif request.method == "POST":
            form = self.get_model_form_class()(data=request.POST, instance=obj)
            if form.is_valid:
                form.save()
                change_list_url_params = request.GET.get('_qwertyu')
                base_url = self.reverse_change_list_url()
                back_url = '%s?%s' % (base_url, change_list_url_params)
                return redirect(back_url)
            context = {
                'form': form,
            }
            return render(request, 'smart_admin/change.html', context)

    def reverse_change_list_url(self):
        url = reverse('%s:%s_%s_changelist' % (self.site.namespace, self.app_label, self.model_name))
        return url

    def get_urls(self):
        from django.conf.urls import url

        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        patterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % app_model_name),
            url(r'^add/$', self.add_view, name='%s_%s_add' % app_model_name),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % app_model_name),
        ]

        return patterns

    @property
    def urls(self):
        return self.get_urls(), None, None


class SmartAdminSite(object):
    def __init__(self):
        self.name = 'sm'
        self.namespace = 'sm'
        self._registry = {}

    def register(self, model, model_sm=None):
        if not model_sm:
            model_sm = ModelSm
        self._registry[model] = model_sm(model, self)
        # print(self._registry)

    def login(self, request):
        return HttpResponse('登录页面')

    def logout(self, request):
        return HttpResponse('退出页面')

    def get_urls(self):
        patterns = []

        from django.conf.urls import url, include
        patterns += [
            url(r'^login/', self.login),
            url(r'^logout', self.logout),
        ]

        for model_class, model_sm_obj in self._registry.items():
            patterns += [
                url(r'^%s/%s/' % (model_class._meta.app_label, model_class._meta.model_name,), model_sm_obj.urls),
            ]

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.name, self.namespace


site = SmartAdminSite()

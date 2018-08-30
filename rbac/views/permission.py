from django.shortcuts import render, redirect
from django import forms
from django.forms.models import model_to_dict
from collections import OrderedDict

from rbac import models
from rbac.forms import permission   # 引入自定义forms模块
from rbac.service.routes import get_all_url_dict


def permission_list(request):

    user_list = models.UserInfo.objects.all()
    role_list = models.Role.objects.all()
    menu_list = models.Menu.objects.all()
    permission_list = models.Permission.objects.all()
    return render(request, 'rbac/permission_list.html', locals())


def permission_add(request):
    if request.method == "GET":
        form = permission.Permission()    # get时生成空表单 并渲染到前端
    else:
        form = permission.Permission(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/permission/list/')

    return render(request, 'rbac/permission_edit.html', {'form': form})


def permission_edit(request, id):
    if request.method == "GET":
        permission_obj = models.Permission.objects.filter(id=id).first()
        form = permission.Permission(
            instance=permission_obj)    # get时生成空表单 并渲染到前端
    else:
        form = permission.Permission(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/permission/list/')
    return render(request, 'rbac/permission_edit.html', {'form': form})


def permission_del(request, id):
    pass


def permission_multi(request):
    # get_all_urls(urlpatterns, pre_fix='/', is_firt_time=True)

    # 1. 生成formset对象，关键词‘extra’决定生成form时默认填充的数据之外，再生成几个空form。
    PermissionFormSet = forms.formset_factory(
        permission.MultiPermission, extra=0)
    generate_formset = ''

    # POST请求：
    if request.method == "POST":
        request_type = request.GET.get('type')
        if request_type == 'update':
            permission_formset = PermissionFormSet(
                request.POST)    # post时：1. 接收传值

            # ret = permission_formset
            # print('permission_formset', type(ret), ret)
            if permission_formset.is_valid():    # 2. 校验前端数据是否合法 若通过验证

                # ret = permission_formset.cleaned_data
                # print('formset.cleaned_data', type(ret), ret)
                for item in permission_formset.cleaned_data:
                    id = item['id']
                    models.Permission.objects.filter(
                        id=id).update(**item)
        if request_type == 'generate':
            generate_formset = PermissionFormSet(
                request.POST)    # post时：1. 接收传值
            # ret = generate_formset
            # print('generate generate_formset 《-----', type(ret), ret)
            if generate_formset.is_valid():    # 2. 校验前端数据是否合法 若通过验证
                for item in generate_formset.cleaned_data:
                    ret = item
                    print('item -----》', type(ret), ret)
                    id = item['id']
                    models.Permission.objects.create(**item)

                # ret = generate_formset.cleaned_data
                # print('generate cleaned_data -----》', type(ret), ret)
                return redirect('rbac:permission_multi')
        if request_type == 'destroy':
            pass

    # GET请求：
    # 1. 获取permission表中左右url ----------
    permission_queryset = models.Permission.objects.all()
    permission_dict = OrderedDict()
    permission_list = []
    for x in permission_queryset:
        # 使用model_to_dict 将单个queryset转dict
        permission_list.append(model_to_dict(x))
        permission_dict[x.name] = model_to_dict(x)
    permission_name_set = set(permission_dict.keys())

    # ret = permission_list
    # print('permission_list', type(ret), ret)

    permission_formset = PermissionFormSet(
        initial=permission_list  # 将数据填充到formset中 供前端渲染
    )

    # 2. 获取路由中所有routes ----------
    route_dict = get_all_url_dict(ignore_namespace_list=['admin'])

    for row in permission_dict.values():
        name = row['name']
        if name in route_dict:
            route_dict[name].update(row)    # 将路由中获得的每条route 补全字段
    route_name_set = set(route_dict.keys())

    # ret = permission_list
    # print('permission_list', type(ret), ret)
    # ret = route_dict
    # print('route_dict', type(ret), ret)
    # ret = permission_dict
    # print('permission_dict', type(ret), ret)

    # ret = route_name_set
    # print('route_dict', type(ret), ret)
    # ret = permission_name_set
    # print('permission_dict', type(ret), ret)

    # 3. 差集 db有 route无 待删除 ----------
    destroy_name_list = permission_name_set - route_name_set
    # ret = generate_name_list
    # print('generate_name_list', type(ret), ret)
    destroy_list = [permission_dict[name] for name in destroy_name_list]
    # ret = destroy_list
    # print('destroy_list', type(ret), ret)
    destroy_formset = PermissionFormSet(
        initial=destroy_list  # 将数据填充到formset中 供前端渲染
    )
    # ret = destroy_formset
    # print('destroy_formset', type(ret), ret)

    # 4. 差集 db无 route有 待添加 ----------
    generate_name_list = route_name_set - permission_name_set
    # ret = generate_name_list
    # print('generate_name_list', type(ret), ret)
    generate_list = [route_dict[name] for name in generate_name_list]
    # ret = generate_list
    # print('generate_list', type(ret), ret)
    if not generate_formset:
        generate_formset = PermissionFormSet(
            initial=generate_list  # 将数据填充到formset中 供前端渲染
        )
    # ret = generate_formset
    # print('generate_formset', type(ret), ret)

    return render(request, 'rbac/permission_multi.html', locals())

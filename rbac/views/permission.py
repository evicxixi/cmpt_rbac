from django.shortcuts import render, redirect
from django import forms
from django.forms.models import model_to_dict
from collections import OrderedDict

from rbac import models
import rbac.forms
from rbac.service.routes import get_all_url_dict

from rbac.utils import decorator


def permission_list(request):
    '''权限列表

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    '''
    user_list = models.UserInfo.objects.all()
    role_list = models.Role.objects.all()
    menu_list = models.Menu.objects.all()
    permission_list = models.Permission.objects.all()
    return render(request, 'rbac/permission_list.html', locals())


def permission_add(request):
    '''添加权限

    Arguments:
        request {[type]} -- [description]

    Returns:
        [type] -- [description]
    '''
    if request.method == "GET":
        form = rbac.forms.permission.Permission()    # get时生成空表单 并渲染到前端
    else:
        form = rbac.forms.permission.Permission(
            request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/permission/list/')

    return render(request, 'rbac/permission_edit.html', {'form': form})


def permission_edit(request, id):
    '''编辑权限

    Arguments:
        request {[type]} -- [description]
        id {[type]} -- [description]

    Returns:
        [type] -- [description]
    '''
    if request.method == "GET":
        permission_obj = models.Permission.objects.filter(id=id).first()
        form = rbac.forms.permission.Permission(
            instance=permission_obj)    # get时生成空表单 并渲染到前端
    else:
        form = rbac.forms.permission.Permission(
            request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/permission/list/')
    return render(request, 'rbac/permission_edit.html', {'form': form})


def permission_del(request, id):
    pass


@decorator.timekeep
def permission_multi(request):
    '''权限批量管理

    GET: 生成以下3个formset
        generate_formset,
        destroy_formset,
        permission_formset

    POST: 根据request_type进行删除或更改的动作

    Decorators:
        decorator.timekeep

    Arguments:
        request {[type]} -- [description]
    '''
    # get_all_urls(urlpatterns, pre_fix='/', is_firt_time=True)

    # 1. 生成formset对象 'extra'决定生成form时默认填充的数据之外，再生成几个空form。
    PermissionFormSet = forms.formset_factory(
        rbac.forms.permission.MultiPermission, extra=0)

    # POST请求：
    if request.method == "POST":
        request_type = request.GET.get('type')
        # print('POST', request_type, request.POST)

        # 删除权限 待完善
        if request_type == 'destroy':
            pass

        # 1. post时接收传值
        formset = PermissionFormSet(request.POST)
        print('is_valid', formset.is_valid(), formset.errors,)
        # print('formset.cleaned_data', type(
        #     formset.cleaned_data), formset.cleaned_data)
        # 2. 校验前端数据是否合法 若通过验证
        if formset.is_valid():
            # print('formset.cleaned_data', type(
                # formset.cleaned_data), formset.cleaned_data)
            if request_type == 'update':
                for item in formset.cleaned_data:
                    models.Permission.objects.filter(
                        id=item['id']).update(**item)
            if request_type == 'generate':
                print('generate', )
                # for item in formset.cleaned_data:
                #     print('item', type(item), item)
                #     models.Permission.objects.create(**item)

                object_list = []
                has_error = False
                for item in formset.cleaned_data:
                    print('item', item)
                    try:
                        new_object = models.Permission.objects.create(**item)
                        # new_object = models.Permission(**item)
                        # print('new_object', type(new_object),
                        #       new_object.__dict__)
                        new_object.validate_unique()
                        object_list.append(new_object)
                    except Exception as e:
                        formset.errors.append(e)
                        generate_formset = formset
                        has_error = True
                        print('e', formset.errors)
                if not has_error:
                    models.Permission.objects.bulk_create(
                        object_list, batch_size=100)
            else:
                generate_formset = formset

                return redirect('rbac:permission_multi')

    # GET请求：
    # 1. 生成permission_formset

    # 获取permission表中所有url
    # 并构造字典 {name: {'id': 1, 'title': '查看客户列表', 'url': '/customer/list/', 'name': 'customer_list', 'parent': None, 'menu': 2},}
    permission_queryset = models.Permission.objects.all()
    permission_dict = {d.name: model_to_dict(d)
                       for d in permission_queryset}
    # print('permission_dict', len(permission_dict),
    #       permission_dict)

    permission_formset = PermissionFormSet(
        initial=list(permission_dict.values())  # 将数据填充到formset中 供前端渲染
    )

    # 2. 获取路由中所有routes
    route_dict = get_all_url_dict(ignore_namespace_list=['admin'])

    # 补全route_dict中每个item中的字段
    for row in permission_dict.values():
        if row['name'] in route_dict:
            route_dict[row['name']].update(row)    # 将路由中获得的每条route 补全字段

    # print('route_dict', type(route_dict), route_dict.keys())
    # print('permission_dict', type(permission_dict), permission_dict)

    # 3. 生成destroy_formset
    # 差集 db有 route无 待删除
    destroy_name_list = set(permission_dict.keys()) - set(route_dict.keys())
    # print('destroy_name_list', type(destroy_name_list), destroy_name_list)
    destroy_list = [permission_dict[name] for name in destroy_name_list]
    # print('destroy_list', type(destroy_list), destroy_list)
    destroy_formset = PermissionFormSet(
        initial=destroy_list  # 将数据填充到formset中 供前端渲染
    )
    # print('destroy_formset', type(destroy_formset), destroy_formset)

    # 4. 生成generate_formset
    # 差集 db无 route有 待添加
    generate_name_list = set(route_dict.keys()) - set(permission_dict.keys())
    # print('generate_name_list', type(generate_name_list), generate_name_list)
    generate_list = [route_dict[name] for name in generate_name_list]
    # print('generate_list', type(generate_list), generate_list)
    generate_formset = PermissionFormSet(
        initial=generate_list  # 将数据填充到formset中 供前端渲染
    )
    # print('generate_formset', type(generate_formset), generate_formset)

    response = {
        'generate_formset': generate_formset,
        'destroy_formset': destroy_formset,
        'permission_formset': permission_formset
    }
    return render(request, 'rbac/permission_multi.html', response)

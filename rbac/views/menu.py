from django.shortcuts import render, redirect
from rbac import models
from rbac.forms import menu   # 引入自定义forms模块
from django.db.models import Q


def menu_list(request):
    '''菜单和权限列表

    Returns:
        [dict] -- [权限二级数据结构]
        {
          1:
          {
            'id': 1,
            'title': '查看客户列表',
            'url': '/customer/list/',
            'name': 'customer_list',
            'children': [
            {
              'id': 2,
              'title': '添加客户',
              'url': '/customer/add/',
              'name': 'customer_add'
            },
            ...
            ]
          },
          ...
        }
    '''

    id = int(request.GET.get('id', 0))
    # ret = id
    # print('id', type(ret), ret)

    menu_queryset = models.Menu.objects.all()
    # ret = menu_list
    # print('ret', type(ret), ret)

    # 获取指定menu.id的permission.id
    if not id:   # 获取所有menu(包括二级、三级菜单)
        permission_queryset = models.Permission.objects.all().values()
        # print('permission_queryset', type(
        #     permission_queryset), permission_queryset)
    else:   # 获取指定menu.id的1个二级菜单、和parent是二级菜单的三级菜单
        parent_id = models.Permission.objects.filter(menu_id=id).first().id
        permission_queryset = models.Permission.objects.filter(
            Q(menu_id=id) | Q(parent_id=parent_id)).values()
        # print('parent_id', type(parent_id), parent_id, permission_queryset)

    # 构造权限二级数据结构
    permission_dict = {}
    for item in permission_queryset:
        if not item['parent_id']:
            permission_dict[item['id']] = {
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'name': item['name'],
                'children': [],
            }
    for item in permission_queryset:
        if item['parent_id']:
            permission_dict[item['parent_id']]['children'].append({
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'name': item['name'],
            })

    # print('permission_dict', type(permission_dict), permission_dict)

    return render(request, 'rbac/menu_list.html', locals())


def menu_add(request):
    '''添加菜单
    '''
    if request.method == "GET":
        form = menu.Menu()    # get时生成空表单 并渲染到前端
    else:
        form = menu.Menu(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/menu/list/')

    return render(request, 'rbac/menu_edit.html', {'form': form})


def menu_edit(request, id):
    '''编辑菜单
    '''
    if request.method == "GET":
        menu_obj = models.Menu.objects.filter(id=id).first()
        form = menu.Menu(instance=menu_obj)    # get时生成空表单 并渲染到前端
    else:
        form = menu.Menu(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/menu/list/')
    return render(request, 'rbac/menu_edit.html', {'form': form})

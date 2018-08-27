from django.shortcuts import render, redirect
from rbac import models
from rbac.forms import permission   # 引入自定义forms模块


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

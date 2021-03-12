from django.shortcuts import render, redirect
from rbac import models
from rbac.forms import role   # 引入自定义forms模块

import json
from django.core import serializers


def role_list(request):
    role_list = models.Role.objects.all()

    # 将m2m字段聚合成list 避免每一个m2m字段的值单独一条
    role_list = serializers.serialize("json", role_list)
    role_list = json.loads(role_list)
    # print(type(role_list), role_list)
    return render(request, 'rbac/role_list.html', locals())


def role_add(request):
    if request.method == "GET":
        form = role.Role()    # get时生成空表单 并渲染到前端
    else:
        form = role.Role(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/role/list/')

    return render(request, 'rbac/role_edit.html', {'form': form})


def role_edit(request, id):
    if request.method == "GET":
        role_obj = models.Role.objects.filter(id=id).first()
        form = role.Role(instance=role_obj)    # get时生成空表单 并渲染到前端
    else:
        form = role.Role(request.POST)    # post时：1. 校验前端数据是否合法
        if form.is_valid():    # 2. 通过验证
            print('通过验证')
            form.save()    # 3. 存库
            return redirect('/role/list/')
    return render(request, 'rbac/role_edit.html', {'form': form})

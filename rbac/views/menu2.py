from django.shortcuts import render, redirect
from rbac import models
from rbac.forms import menu   # 引入自定义forms模块


def menu_list(request):
    menu_queryset = models.Menu.objects.all()
    permission_queryset = models.Permission.objects.all()

    return render(request, 'rbac/menu_list.html', locals())


def menu_add(request):
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

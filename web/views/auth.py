from django.shortcuts import redirect, HttpResponse, render

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response

from rbac import models as rbac_models
from web import models as web_models
from rbac.service.init_permission import init_permission    # 自定义的权限初始化模块
# from web.utlis.response import BaseResponse


class AuthView(ViewSetMixin, APIView):

    authentication_classes = []  # drf的认证组件已设置全局后 此字段设置空 意味此视图类不走认证模块

    def login(self, request, *args, **kwargs):
        """
        get请求时返回登录页面
        """
        return render(request, 'auth.html')

    def auth(self, request, *args, **kwargs):
        """
        用户登陆认证，登陆成功后调用自定义的权限初始化模块，将当前用户（权限url、权限menu）存入session
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        action = request.data.get('action')

        # 登出
        if action == 'logout':
            request.session.flush()
            return render(request, 'auth.html')

        # 1. 校验用户登录
        username = request.data.get('username')
        password = request.data.get('password')

        user_obj = rbac_models.UserInfo.objects.filter(
            name=username, password=password).first()

        # 如果用户未登录
        if not user_obj:
            return HttpResponse('登录失败！')

        # 2. 如果用户已登录 调用自定义的权限初始化模块 将当前用户权限url、权限menu存入session
        init_permission(request, user_obj)

        return redirect('/customer/list')

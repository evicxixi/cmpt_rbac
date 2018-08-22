import re

from django.shortcuts import HttpResponse, render, redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class RbacMD(MiddlewareMixin):
    """
    url权限验证中间件
    """

    def process_request(self, request):

        # print('RbacMD-----')

        # 1. 取值 当前用户权限url、权限menu
        pms_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        # menu_list = request.session.get('menu_list')

        # 2. 当前url若在白名单 直接返回None放行
        for url in settings.VALID_URL:
            # print(request.path_info, re.match(url, request.path_info))
            if re.match(url, request.path_info):
                # print(111, request.path_info)
                return None

        # 3. 当前url若在pms_list中 返回None放行
        for url in pms_list:
            # print('url', url)
            if re.match(url, request.path_info):
                return None

        return HttpResponse('no permission')

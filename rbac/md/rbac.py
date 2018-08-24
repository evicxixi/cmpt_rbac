import re

from django.shortcuts import HttpResponse, render, redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


def get_permission_dict(permission_dict, id):
    '''
    从权限url（permission_dict）中构造menu_list字段
    模板：{'title': '查看客户列表', 'url': '/customer/list/'}
    '''
    for item in permission_dict.values():
        print(item['id'], item['title'], item['url'])
        if id == item['id']:
            return {
                'title': item['title'],
                'url': item['url']
            }


def get_root_menu_title(menu_dict, pid):
    '''
    从权限菜单（menu_dict）中构造menu_list的根菜单字段
    模板：{'title': '客户管理', 'url': '/'}
    '''
    for item in menu_dict.values():
        for children in item['children']:
            if pid == children['id']:
                return {
                    'title': item['title'],
                    'url': '/'
                }


class RbacMD(MiddlewareMixin):
    """
    url权限验证中间件
    """

    def process_request(self, request):

        # print('RbacMD-----')

        # 1. 取值 当前用户权限url、权限menu
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        # ret = permission_dict
        # print('permission_dict', len(ret), type(ret), ret)
        menu_dict = request.session.get(settings.MENU_SESSION_KEY)

        # ret = menu_dict
        # print('menu_dict', len(ret), type(ret), ret)
        # 2. 当前url若在白名单 直接返回None放行
        for url in settings.VALID_URL:
            if re.match(url, request.path_info):
                # print(111, request.path_info)
                return None

        # 3. 当前url若在permission_dict中 返回None放行
        for item in permission_dict.values():
            # ret = item
            # print('permission_dict > item', len(ret), type(ret), ret)
            if re.match(item['url'], request.path_info):
                # 4. 构造breadcrumb_list 并存入session
                breadcrumb_list = [
                    {'title': '首页', 'url': '/'},
                ]
                if item['pid']:
                    breadcrumb_list.extend([
                        get_root_menu_title(menu_dict, item['pid']),
                        get_permission_dict(permission_dict, item['pid']),
                        {
                            'title': item['title'],
                            'url':item['url']
                        }
                    ])
                else:
                    breadcrumb_list.extend([
                        get_root_menu_title(menu_dict, item['id']),
                        {
                            'title': item['title'],
                            'url': item['url']
                        }])
                # print('breadcrumb_list', breadcrumb_list)
                request.session['breadcrumb_list'] = breadcrumb_list
                return None
        return HttpResponse('no permission')

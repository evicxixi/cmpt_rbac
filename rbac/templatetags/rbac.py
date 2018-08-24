from django.template import Library
from django.conf import settings
import re

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)

    # 为当前的一级、二级菜单标记class = 'active'
    for item in menu_dict.values():
        for children in item['children']:
            if re.match(children['url'], request.path_info):
                item['class'] = 'active'
                children['class'] = 'active'
                break

    # ret = menu_dict
    # print('templatetags > menu_dict', type(ret), ret)
    return {settings.MENU_SESSION_KEY: menu_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    breadcrumb_list = request.session.get('breadcrumb_list')
    return {'breadcrumb_list': breadcrumb_list}

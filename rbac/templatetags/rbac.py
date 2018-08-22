from django.template import Library
from django.conf import settings
import re

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_list = request.session.get(settings.MENU_SESSION_KEY)
    for item in menu_list:
        if re.match(item['url'], request.path_info):
            item['class'] = 'active'

    # print('menu_list', menu_list)
    return {settings.MENU_SESSION_KEY: menu_list}

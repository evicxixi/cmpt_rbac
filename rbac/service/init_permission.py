from django.conf import settings


def init_permission(request, user_obj):
    """
    权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
    :param request:
    :param user:
    :return:
    """
    # 2. 如果用户已登录 构建将要存入session的当前用户权限url、权限menu
    # 2.1 获取当前用户所有的权限信息并去重 存入queryset
    queryset = user_obj.roles.filter(
        permissions__url__isnull=False).values(
        'permissions__id',
        'permissions__title',
        'permissions__url',
        # 'permissions__name',
        'permissions__parent_id',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    ).distinct()

    # ret = queryset
    # print('ret', type(ret), ret)

    # ret = list(queryset)
    # print('pms_list2', type(ret), len(ret), ret)

    # 2.2 构建将要存入session的当前用户权限url、权限menu

# permission_dict = {
#     'name': {'id': '', 'title': '', 'url': '', 'pid': ''},
#     'name': {'id': '', 'title': '', 'url': '', 'pid': ''},
# }
# menu_dict = {
#     'id': {
#         'title': '',
#         'icon': '',
#         'children': [
#             {
#                 'id': '',
#                 ...
#             }
#         ]
#     }
# }
    permission_dict = {}
    menu_dict = {}
    for item in queryset:
        # print(item)
        permission_dict[item['permissions__title']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__parent_id'],
            'mid': item['permissions__menu_id'],
            'menu_title': item['permissions__menu__title'],
        }

        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [{
                    'id': item['permissions__id'],
                    'title': item['permissions__title'],
                    'url': item['permissions__url'],
                }],
            }
        else:
            # print(type(item['permissions__menu_id']))
            menu_dict[menu_id]['children'].append({
                'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url'],
            })

    # ret = permission_dict
    # print('ret', len(ret), type(ret), ret)
    # ret = menu_dict
    # print('ret', type(ret), ret)

    # pms_list = []
    # menu_list = []
    # for item in queryset:
    #     # 2.2.1 当前用户权限url存入pms_list
    #     pms_list.append(item['permissions__url'])

    #     # 2.2.2 若是菜单 将当前用户权限menu信息存入menu_list
    #     if item['permissions__is_menu']:
    #         menu_list.append({
    #             'title': item['permissions__title'],
    #             'url': item['permissions__url'],
    #             'is_menu': item['permissions__is_menu'],
    #             'icon': item['permissions__icon'],
    # })

    # 3. 存库session
    # 3.1 将当前用户权限url、权限menu 存入session
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict

    # 3.2 最后在session存入用户信息
    request.session['username'] = {
        'id': user_obj.id, 'username': user_obj.name}

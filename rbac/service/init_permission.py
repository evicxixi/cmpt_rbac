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
        permissions__url__isnull=False).values('permissions__title', 'permissions__url', 'permissions__is_menu', 'permissions__icon').distinct()

    # ret = list(queryset)
    # print('pms_list2', type(ret), len(ret), ret)

    # 2.2 构建将要存入session的当前用户权限url、权限menu
    pms_list = []
    menu_list = []
    for item in queryset:
        # 2.2.1 当前用户权限url存入pms_list
        pms_list.append(item['permissions__url'])

        # 2.2.2 若是菜单 将当前用户权限menu信息存入menu_list
        if item['permissions__is_menu']:
            menu_list.append({
                'title': item['permissions__title'],
                'url': item['permissions__url'],
                'is_menu': item['permissions__is_menu'],
                'icon': item['permissions__icon'],
            })
    # print('pms_list', type(pms_list), len(pms_list), pms_list)
    # print('menu_list', type(menu_list), len(menu_list), menu_list)

    # 3. 存库session
    # 3.1 将当前用户权限url、权限menu 存入session
    request.session[settings.MENU_SESSION_KEY] = menu_list
    request.session[settings.PERMISSION_SESSION_KEY] = pms_list

    # 3.2 最后在session存入用户信息
    request.session['username'] = {
        'id': user_obj.id, 'username': user_obj.name}

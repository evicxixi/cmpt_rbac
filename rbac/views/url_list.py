from django.shortcuts import render, redirect
from rbac import models
# from rbac.forms import menu   # 引入自定义forms模块

# from urls import urlpatterns
from django.urls import RegexURLPattern


def get_all_urls(patterns, pre_fix, is_firt_time=False, result=[]):
    if is_firt_time:
        result.clear()

    for item in patterns:
        print('item', item, type(item))
        part = item._regex.strip('^$')
        if isinstance(item, RegexURLPattern):
            result.append(pre_fix + part)
        else:
            get_all_urls(item.urlconf_name, pre_fix + part)

    return result


def url_list(request):

    id = request.GET.get('id', 0)
    id = int(id)
    # ret = id
    # print('id', type(ret), ret)

    url_queryset = models.Permission.objects.all().values(
        'id', 'title', 'url', 'parent', 'name')

    # 构造权限二级数据结构
    url_dict = {}
    for item in url_queryset:
        url_dict[item['url']] = {
            'id': item['id'],
            'title': item['title'],
            'url': item['url'],
            'name': item['name'],
            'children': [],
        }

    # ret = url_dict
    # print('url_dict', type(ret), ret)

    ret = set(url_dict)
    print('url_dict', type(ret), ret)

    all_url = get_all_urls(urlpatterns, pre_fix='/',
                           is_firt_time=True, result=[])

    ret = set(all_url)
    print('all_url', type(ret), ret)

    return render(request, 'rbac/url_list.html', locals())

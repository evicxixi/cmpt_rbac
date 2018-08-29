from django.conf.urls import url
from rbac.views import role, menu, permission

urlpatterns = [
    url(r'^role/list/$', role.role_list, name='role_list'),
    url(r'^role/add/$', role.role_add, name='role_add'),
    url(r'^role/edit/(?P<id>\d+)/$', role.role_edit, name='role_edit'),
    # url(r'^role/del/(?P<pid>\d+)/$', role.role_del),

    url(r'^menu/list/$', menu.menu_list, name='menu_list'),
    url(r'^menu/add/$', menu.menu_add, name='menu_add'),
    url(r'^menu/edit/(?P<id>\d+)/$', menu.menu_edit, name='menu_edit'),

    url(r'^permission/list/$', permission.permission_list, name='permission_list'),
    url(r'^permission/add/$', permission.permission_add, name='permission_add'),
    url(r'^permission/edit/(?P<id>\d+)/$',
        permission.permission_edit, name='permission_edit'),
    url(r'^permission/multi/$', permission.permission_multi, name='permission_multi'),
]

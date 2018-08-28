from django.conf.urls import url
from web.views import customer, payment, auth
from rbac.views import role, menu, permission, url_list

urlpatterns = [
    url(r'^auth/$', auth.AuthView.as_view({'get': 'login', 'post': 'auth'})),

    url(r'^customer/list/$', customer.customer_list),
    url(r'^customer/add/$', customer.customer_add),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del),
    url(r'^customer/import/$', customer.customer_import),
    url(r'^customer/tpl/$', customer.customer_tpl),

    url(r'^payment/list/$', payment.payment_list),
    url(r'^payment/add/$', payment.payment_add),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del),

    url(r'^role/list/$', role.role_list),
    url(r'^role/add/$', role.role_add),
    url(r'^role/edit/(?P<id>\d+)/$', role.role_edit),
    # url(r'^role/del/(?P<pid>\d+)/$', role.role_del),

    url(r'^menu/list/$', menu.menu_list),
    url(r'^menu/add/$', menu.menu_add),
    url(r'^menu/edit/(?P<id>\d+)/$', menu.menu_edit),

    url(r'^permission/list/$', permission.permission_list),
    url(r'^permission/add/$', permission.permission_add),
    url(r'^permission/edit/(?P<id>\d+)/$', permission.permission_edit),
    url(r'^permission/multi/$', permission.permission_multi),

    url(r'^url/list/$', url_list.url_list),
    # url(r'^menu/add/$', menu.menu_add),
    # url(r'^menu/edit/(?P<id>\d+)/$', menu.menu_edit),
]

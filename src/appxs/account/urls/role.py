# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.role import list_role, edit_role, add_role, del_role
from ..apps import app_name

urlpatterns = [

    url(r'^add/$', add_role, name='add'),
    url(r'^list/$', list_role, name='list'),
    # url(r'^detail/(?P<role_id>\d+)/$', profile_role, name='detail'),
    url(r'^edit/(?P<role_id>\d+)/$', edit_role, name='edit'),
    url(r'^del/(?P<role_id>\d+)/$', del_role, name='del'),
]

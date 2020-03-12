# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.group import list_group, edit_group, add_group, del_group
from ..apps import app_name

urlpatterns = [

    url(r'^add/$', add_group, name='add'),
    url(r'^list/$', list_group, name='list'),
    # url(r'^detail/(?P<group_id>\d+)/$', profile_group, name='detail'),
    url(r'^edit/(?P<group_id>\d+)/$', edit_group, name='edit'),
    url(r'^del/(?P<group_id>\d+)/$', del_group, name='del'),
]

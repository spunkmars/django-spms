# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.user import login, logout, signup, profile_user, list_user, edit_user, change_info, \
    change_password, add_user, del_user
from ..apps import app_name

urlpatterns = [

    url(r'^add/$', add_user, name='add'),
    url(r'^list/$', list_user, name='list'),
    url(r'^detail/(?P<user_id>\d+)/$', profile_user, name='detail'),
    url(r'^edit/(?P<user_id>\d+)/$', edit_user, name='edit'),
    url(r'^del/(?P<user_id>\d+)/$', del_user, name='del'),
]

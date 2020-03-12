# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.user import login, logout, signup, profile_user, list_user, edit_user, change_info, \
    change_password, add_user, del_user, add_avatar
from ..apps import app_name

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^login_rbac/$', login, name='login_rbac'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^profile/$', profile_user, name='profile'),
    # url(r'^profile/(?P<user_id>\d+)/$', profile_user, name='profile'),
    url(r'^change_password/$', change_password, name='change_password'),
    # url(r'^change_info/(?P<user_id>\d+)/$', change_info, name='change_info'),
    url(r'^change_info/$', change_info, name='change_info'),
    url(r'^add_avatar/$', add_avatar, name='add_avatar'),

]

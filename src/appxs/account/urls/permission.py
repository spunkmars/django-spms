# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.permission import index, get_resource_tree, save_resource_tree, add_resource, edit_resource, \
    del_resource, get_perm_tree, save_perm_tree, grant_perm, grant_perm_min, show_user_perm, get_user_perm_tree, \
    update_resource_position
from ..apps import app_name

urlpatterns = [
    url(r'^index/$', index, name='index'),
    url(r'^add_resource/(?P<resource_pid>\d+)/$', add_resource, name='add_resource'),
    # url(r'^list_resource/$', list_resource, name='list_resource'),
    url(r'^edit_resource/(?P<resource_id>\d+)/$', edit_resource, name='edit_resource'),
    url(r'^del_resource/(?P<resource_id>\d+)/$', del_resource, name='del_resource'),
    url(r'^get_resource_tree/$', get_resource_tree, name='get_resource_tree'),
    url(r'^save_resource_tree/$', save_resource_tree, name='save_resource_tree'),
    url(r'^grant_perm/(?P<role_id>\d+)/$', grant_perm, name='grant_perm'),
    url(r'^grant_perm_min/(?P<role_id>\d+)/$', grant_perm_min, name='grant_perm_min'),
    url(r'^get_perm_tree/(?P<role_id>\d+)/$', get_perm_tree, name='get_perm_tree'),
    url(r'^save_perm_tree/(?P<role_id>\d+)/$', save_perm_tree, name='save_perm_tree'),
    url(r'^show_user_perm/(?P<user_id>\d+)/$', show_user_perm, name='show_user_perm'),
    url(r'^get_user_perm_tree/(?P<user_id>\d+)/$', get_user_perm_tree, name='get_user_perm_tree'),
    url(r'^update_resource_position/$', update_resource_position, name='update_resource_position'),

]

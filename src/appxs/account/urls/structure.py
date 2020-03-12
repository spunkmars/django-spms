# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include

from appxs.account.views.structure import list_structure, edit_structure, add_structure, del_structure
from ..apps import app_name

urlpatterns = [

    url(r'^add/$', add_structure, name='add'),
    url(r'^list/$', list_structure, name='list'),
    # url(r'^detail/(?P<structure_id>\d+)/$', profile_structure, name='detail'),
    url(r'^edit/(?P<structure_id>\d+)/$', edit_structure, name='edit'),
    url(r'^del/(?P<structure_id>\d+)/$', del_structure, name='del'),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from django.urls import reverse
# from ..apps import app_name

urlpatterns = [
    url(r'manage/user/', include('appxs.account.urls.m_user', namespace='manage_user')),
    url(r'user/', include('appxs.account.urls.user', namespace='user')),
    url(r'role/', include('appxs.account.urls.role', namespace='role')),
    url(r'structure/', include('appxs.account.urls.structure', namespace='structure')),
    url(r'group/', include('appxs.account.urls.group', namespace='group')),
    url(r'permission/', include('appxs.account.urls.permission', namespace='permission')),
    url(r'^login/$', lambda x: HttpResponseRedirect(reverse('account:user:login')), name='login'),
    url(r'^login_rbac/$', lambda x: HttpResponseRedirect(reverse('account:user:login_rbac')), name='login_rbac'),
    url(r'^logout/$', lambda x: HttpResponseRedirect(reverse('account:user:logout')), name='logout'),
]

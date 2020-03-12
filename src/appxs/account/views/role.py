# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

if sys.version_info >= (3, 0, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
import json

from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from guardian.decorators import permission_required, permission_required_or_403
from django.utils.decorators import method_decorator

from spmo.common import Common
from spmo.data_serialize import DataSerialize
from spcc.views.common import list_data, del_model_items, display_confirm_msg
from spcc.models.common import del_model_data

from spcc.views.common import Ajax

from appxs.account.models.user import Role
from appxs.account.forms.role import AddRoleForm


co = Common()


def app_info():
    app = {
        "name": "account",
        "fun": "role",
        "edit_url": 'account:role:edit',
        "del_url": 'account:role:del',
    }
    return app


@csrf_exempt  # 禁用csrf
@login_required
def index(request, ):
    app = app_info()
    app['location'] = 'index'
    return render(request, 'account/role.html',
                  {'app': app})


@login_required
def edit_role(request, role_id):
    role = get_object_or_404(Role, pk=role_id)
    # print 'is_active=%s' % role.is_active
    if request.method == 'POST':
        ds = DataSerialize()
        form = AddRoleForm(model=Role, instance=role, data=request.POST)
        if form.is_valid():
            new_role = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = AddRoleForm(model=Role, instance=role)

    app = app_info()
    app['name'] = "m_role"
    app['location'] = 'edit'
    return render(request, 'edit_data2_not_nav.html',
                  {'form': form, 'app': app})


@login_required
def add_role(request):
    if request.method == 'POST':
        ds = DataSerialize()
        form = AddRoleForm(model=Role, data=request.POST)
        if form.is_valid():
            new_role = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = AddRoleForm(model=Role)

    app = app_info()
    app['name'] = "m_role"
    app['location'] = 'add'
    return render(request, 'add_data2_not_nav.html',
                  {'form': form, 'app': app})


@login_required
def list_role(request):
    model_object = Role
    template_file = 'account/role.html'
    show_field_list = ['id',
                       'name',
                       'comment',
                       'create_time',
                       'update_time',
                       ]
    filter_field = 'name'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['name'] = "m_role"
    app['location'] = 'list'
    app['extra_urls'] = []
    app['extra_urls'].append({'title': '授权', 'url': 'account:permission:grant_perm_min'})

    render_context = list_data(app=app, request=request, model_object=model_object, each_page_items=each_page_items,
                               filter_field=filter_field, template_file=template_file, show_field_list=show_field_list,
                               is_frontend_paging=True)
    return render_context


@csrf_exempt  # 禁用csrf
@login_required
def del_role(request, role_id):
    del_res = {}
    if request.method == "POST":
        del_res = del_model_data(model=Role, id=role_id)

    html = json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")

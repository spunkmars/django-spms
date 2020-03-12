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

from appxs.account.models.user import Structure
from appxs.account.forms.structure import AddStructureForm

co = Common()


def app_info():
    app = {
        "name": "account",
        "fun": "structure",
        "edit_url": 'account:structure:edit',
        "del_url": 'account:structure:del',
    }
    return app


@csrf_exempt  # 禁用csrf
@login_required
def index(request, ):
    app = app_info()
    app['location'] = 'index'
    return render(request, 'account/structure.html',
                  {'app': app})


@login_required
def edit_structure(request, structure_id):
    structure = get_object_or_404(Structure, pk=structure_id)
    # print 'is_active=%s' % structure.is_active
    if request.method == 'POST':
        ds = DataSerialize()
        form = AddStructureForm(model=Structure, instance=structure, data=request.POST)
        if form.is_valid():
            new_structure = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = AddStructureForm(model=Structure, instance=structure)

    app = app_info()
    app['name'] = "m_structure"
    app['location'] = 'edit'
    return render(request, 'edit_data2_not_nav.html',
                  {'form': form, 'app': app})


@login_required
def add_structure(request):
    if request.method == 'POST':
        ds = DataSerialize()
        form = AddStructureForm(model=Structure, data=request.POST)
        if form.is_valid():
            new_structure = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = AddStructureForm(model=Structure)

    app = app_info()
    app['name'] = "m_structure"
    app['location'] = 'add'
    return render(request, 'add_data2_not_nav.html',
                  {'form': form, 'app': app})


@login_required
def list_structure(request):
    model_object = Structure
    template_file = 'account/structure.html'
    show_field_list = ['id',
                       'name',
                       'type',
                       'parent',
                       'comment',
                       'create_time',
                       'update_time',
                       ]
    filter_field = 'name'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['name'] = "m_structure"
    app['location'] = 'list'
    app['extra_urls'] = []

    render_context = list_data(app=app, request=request, model_object=model_object, each_page_items=each_page_items,
                               filter_field=filter_field, template_file=template_file, show_field_list=show_field_list,
                               is_frontend_paging=True)
    return render_context


@csrf_exempt  # 禁用csrf
@login_required
def del_structure(request, structure_id):
    del_res = {}
    if request.method == "POST":
        del_res = del_model_data(model=Structure, id=structure_id)

    html = json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")

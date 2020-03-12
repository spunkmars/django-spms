# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

if sys.version_info >= (3, 0, 0):
    from io import BytesIO
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
    import cStringIO

from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from spcc.views.common import Ajax
from libs.common import create_uuid
from spmo.data_serialize import DataSerialize


def get_check_code_image(request, ):
    from spcc.libs.security import create_validate_code
    (im, rand_str) = create_validate_code()
    # from libs.security import get_check_code
    # (im, rand_str) = get_check_code()
    request.session['checkcode'] = rand_str
    if sys.version_info >= (3, 0, 0):
        buf = BytesIO()
    else:
        buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    return HttpResponse(buf.getvalue(), 'image/gif')


@csrf_exempt  # 禁用csrf
def get_uuid(request):
    ajax_ins = Ajax(request=request, s_method=['GET', 'POST'])
    in_data = ajax_ins.get_ds_input_data()
    d_type = in_data['d_type']
    da = {}
    if d_type == 'NULL':
        da = {'val': ''}
    else:
        da = {'val': create_uuid()}
    ajax_ins.load_data(da)
    return ajax_ins.make_response()


@csrf_exempt  # 禁用csrf
def convert_view_name_to_url(request):
    ajax_ins = Ajax(request=request, s_method=['GET', 'POST'])
    ds = DataSerialize()
    in_data = ajax_ins.get_ds_input_data()
    data = {k: in_data.getlist(k) if len(in_data.getlist(k)) > 1 else v for k, v in in_data.items()}
    data['view_param'] = ds.deserialize(data['view_param'])
    view_name = data['view_name']
    id = None
    if 'id' in data['view_param']:
        id = int(data['view_param']['id'])
    da = {}
    if view_name is None or view_name == '':
        da = {'url': ''}
    else:
        if id is None or id == '':
            da = {'url': reverse(view_name)}
        else:
            da = {'url': reverse(view_name, args=(id,))}
    ajax_ins.DD(da)
    return ajax_ins.make_response()

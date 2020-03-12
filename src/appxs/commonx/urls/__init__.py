# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..views.common import get_check_code_image
from ..views.common import get_uuid
from ..views.common import convert_view_name_to_url
from ..apps import app_name

urlpatterns = [
    url(r'language/', include('appxs.commonx.urls.language')),  # 每添加一个url.py文件时，都在此加一行
    url(r'^get_uuid/$', get_uuid, name='get_uuid'),
    url(r'^get_check_code_image/$', get_check_code_image, name='get_checkcode_image'),
    url(r'^convert_view_name_to_url/$', convert_view_name_to_url, name='convert_view_name_to_url'),

]

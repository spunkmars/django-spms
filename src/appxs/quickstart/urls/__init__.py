# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from django.urls import reverse

from appxs.quickstart.views import index

app_name = 'quickstart'

urlpatterns = [
    url(r'^$', index, name='index'),
]

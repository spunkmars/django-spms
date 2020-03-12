# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


def app_info():
    app = {
        "name": "quickstart",
        "fun": "common",
        "edit_url": 'quickstart:index',
        "del_url": 'quickstart:index'
    }
    return app


def index(request,):
    app = app_info()
    app['location'] = 'index'
    return render(request, 'quickstart/index.html',
                  {'app': app})

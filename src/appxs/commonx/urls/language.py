# coding=utf-8
from django.conf.urls import url, include

from ..views import language
from ..apps import app_name

urlpatterns = [
    url(r'^$', language.list_language, name='all_lang'),
    url(r'list/$', language.list_language, name='list_lang'),
    url(r'select/$', language.select_language, name='select_lang'),
]

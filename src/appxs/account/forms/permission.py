# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import Resouce
from django.contrib.auth import get_user_model

Resouce = get_user_model()

from django import forms

from spcc.forms.field import newDateTimeInput, AutoGetVal
from spcc.forms.common import newModelForm, newChoiceField


class AddResourceForm(newModelForm):
    name = forms.CharField(max_length=255, label=_('名称'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = newChoiceField(choices=(), label=_('资源类型'), required=True,
                          widget=forms.Select(
                              attrs={'class': 'form-control'}))
    parent = newChoiceField(choices=(), label=_('父资源'), required=False,
                            widget=forms.Select(attrs={'class': 'form-control'}))

    icon = forms.CharField(max_length=255, label=_('图标'), required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    code = forms.CharField(max_length=255, label=_('编码'), required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    url = forms.CharField(max_length=255, label=_('URL'), required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    url_target = newChoiceField(choices=(), label=_('URL打开方式'), required=False,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    # order = forms.CharField(max_length=255, label=_('菜单排序'), required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    # seq = forms.FloatField(label=_('排序'), required=False,
    #                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    view_name = forms.CharField(max_length=255, label=_('显示名称'),
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    # level = forms.IntegerField(label=_('层级'), required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    desc = forms.CharField(max_length=255, label=_('描述'), required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.CharField(max_length=255, label=_('标题'), required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    comment = forms.CharField(max_length=255, label=_('备注'), required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

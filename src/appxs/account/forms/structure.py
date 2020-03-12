# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import Resouce
from django.contrib.auth import get_user_model

from django import forms

from spcc.forms.field import newDateTimeInput, AutoGetVal
from spcc.forms.common import newModelForm, newChoiceField


class AddStructureForm(newModelForm):
    name = forms.CharField(max_length=255, label=_('名称'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = newChoiceField(choices=(), label=_('组织类型'), required=True,
                          widget=forms.Select(
                              attrs={'class': 'form-control'}))
    parent = newChoiceField(choices=(), label=_('上级组织'), required=False,
                            widget=forms.Select(attrs={'class': 'form-control'}))
    comment = forms.CharField(max_length=255, label=_('备注'), required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

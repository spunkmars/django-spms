# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from django import forms

from spcc.forms.field import newDateTimeInput, AutoGetVal
from spcc.forms.common import newModelForm, newChoiceField


class AddRoleForm(newModelForm):
    name = forms.CharField(max_length=255, label=_('名称'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    comment = forms.CharField(max_length=255, label=_('备注'), required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

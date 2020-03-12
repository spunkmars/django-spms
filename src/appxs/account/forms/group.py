# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import Resouce
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from django import forms

from spcc.forms.field import newDateTimeInput, AutoGetVal
from spcc.forms.common import newModelForm, newChoiceField


class AddGroupForm(newModelForm):
    name = forms.CharField(max_length=255, label=_('组名'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), label=_('用户组权限（Django自带）'),
                                            required=False,
                                            widget=forms.SelectMultiple(attrs={'class': 'form-control'}))


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

from django import forms
from django.conf import settings
from django.contrib.auth.hashers import make_password

TBOOLEAN_CHOICES = getattr(settings, 'TBOOLEAN_CHOICES')
from spcc.forms.field import newDateTimeInput, ForeignKeyWidget, ManyToManyWidget
from spcc.forms.common import newModelForm, newChoiceField
from spmo.common import Common
from ..models.user import Role
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import update_session_auth_hash

co = Common()


class SignupForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Username') + ' :')
    email = forms.EmailField(label=_('e-Mail') + ' :')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                                label=_('Password') + ' :')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                                label=_('Type Password again') + ' :')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("This username is already in use.Please choose another."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        return new_user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label=_('Username') + ' :')
    password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                               label=_('Password') + ' :')


class AddUserAvatarForm(forms.Form):
    image = forms.ImageField(required=False, max_length=100, label=_('头像'), )


class UserForm(newModelForm):
    name = forms.CharField(max_length=255, label=_('姓名'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=255, label=_('First Name'), required=False,
    #                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=255, label=_('Last Name'), required=False,
    #                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, label=_('邮箱'), required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    birthday = forms.CharField(max_length=255, label=_('出生日期'), required=False,
                               widget=newDateTimeInput(d_type='onlydate', attrs={'class': 'form-control'}))
    gender = newChoiceField(choices=(("male", "男"), ("female", "女")), label=_('性别'), required=True,
                            widget=forms.Select(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=25, label=_('手机号码'), required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))


class ManageBaseUserForm(newModelForm):
    username = forms.CharField(max_length=255, label=_('账户名（登录所用）'),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=255, label=_('姓名'),
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    # first_name = forms.CharField(max_length=255, label=_('First Name'), required=False,
    #                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    # last_name = forms.CharField(max_length=255, label=_('Last Name'), required=False,
    #                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, label=_('邮箱'), required=False,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=255, label=_('密码'), required=True,
                               widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control'}))
    birthday = forms.CharField(max_length=255, label=_('出生日期'), required=False,
                               widget=newDateTimeInput(d_type='onlydate', attrs={'class': 'form-control'}))
    gender = newChoiceField(choices=(("male", "男"), ("female", "女")), label=_('性别'), required=True,
                            widget=forms.Select(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=25, label=_('手机号码'), required=False,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = newChoiceField(choices=(), label=_('部门'), required=False,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    position = forms.CharField(max_length=50, label=_('职位'), required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    superior = newChoiceField(choices=(), label=_('直属上级'), required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label=_('角色'),
                                           required=False,
                                           widget=ManyToManyWidget(url_prefix='/manage/account/user',
                                                                   attrs={'class': 'form-control'}))
    is_superuser = newChoiceField(choices=TBOOLEAN_CHOICES, label=_('是否超级用户'), required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    is_staff = newChoiceField(choices=TBOOLEAN_CHOICES, label=_('是否可登陆admin后台'), required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    is_active = newChoiceField(choices=TBOOLEAN_CHOICES, label=_('是否激活'), required=False,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), label=_('用户组'),
                                            required=False,
                                            widget=ManyToManyWidget(url_prefix='/manage/account/group',
                                                                    attrs={'class': 'form-control'}))
    # user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), label=_('用户权限（Django自带）'),
    #                                                   required=False,
    #                                                   widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), label=_('用户权限（Django自带）'),
                                                      required=False,
                                                      widget=ManyToManyWidget(url_prefix='/manage/account/perm',
                                                                              attrs={'class': 'form-control'}))


class ManageAddUserForm(ManageBaseUserForm):

    def get_save_data(self, model=None):
        s_dict = super(ManageAddUserForm, self).get_save_data(model_cls=model)
        if 'password' in self.cleaned_data.keys():
            if self.cleaned_data['password'] is not None and self.cleaned_data['password'] != '' \
                    and self.cleaned_data['password'].lower() != 'none':
                s_dict['password'] = (make_password(self.cleaned_data['password']))
            else:
                raise Exception('password can not be null，Please input again！')
        return s_dict

    # def save(self):
    #     new_user = User.objects.create_user(username=self.cleaned_data['username'],
    #                                         password=self.cleaned_data['password'],
    #                                         is_superuser=self.cleaned_data['is_superuser'],
    #                                         is_staff=self.cleaned_data['is_staff'],
    #                                         is_active=self.cleaned_data['is_active'],
    #                                         )
    #     return new_user


class ManageEditUserForm(ManageBaseUserForm):
    password = forms.CharField(max_length=255, label=_('密码'), required=False,
                               widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control'}))

    def get_save_data(self, model=None):
        s_dict = super(ManageEditUserForm, self).get_save_data(model_cls=model)
        if 'password' in self.cleaned_data.keys():
            if self.cleaned_data['password'] is not None and self.cleaned_data['password'] != '' \
                    and self.cleaned_data['password'].lower() != 'none':
                s_dict['password'] = (make_password(self.cleaned_data['password']))
            else:
                s_dict['password'] = getattr(self.instance, 'password')
        return s_dict


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                                   label=_('OldPassword') + ' :')
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                                label=_('Password') + ' :')
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False),
                                label=_('Type Password again') + ' :')

    def clean(self):
        if 'old_password' in self.cleaned_data:
            if self.cleaned_data['old_password'] == '' or self.cleaned_data['old_password'].lower() == 'none':
                raise forms.ValidationError("You must type the old password !")
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("You must type the same password each time!")

        return self.cleaned_data

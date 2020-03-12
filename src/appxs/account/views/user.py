# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import os
import datetime

if sys.version_info >= (3, 0, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse
import json

from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from guardian.decorators import permission_required, permission_required_or_403
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.conf import settings

from spmo.common import Common
from spmo.data_serialize import DataSerialize
from spcc.views.common import list_data, del_model_items, display_confirm_msg
from spcc.models.common import del_model_data

from appxs.account.forms.account import SignupForm, LoginForm, UserForm, ManageEditUserForm, ManageAddUserForm, \
    ChangePasswordForm, AddUserAvatarForm

# from appxs.account.utils.permission import init_permission

User = get_user_model()

from spmo.common import Common

co = Common()

ASSET_DIR = getattr(settings, 'ASSET_DIR')
AVATAR_PRE_DIR = getattr(settings, 'AVATAR_PRE_DIR')


def app_info():
    app = {
        "name": "account",
        "fun": "user",
        "edit_url": 'account:manage_user:edit',
        "del_url": 'account:manage_user:del'
    }
    return app


def parse_uri(uri=None):
    if sys.version_info >= (2, 5, 0):
        url_h = urlparse(uri)
        url_scheme = url_h.scheme
        url_hostname = url_h.hostname
        url_port = url_h.port
        url_path = url_h.path
    else:
        url_h = urlparse(uri)
        url_scheme = url_h[0]
        host_a = url_h[1].split(':')
        url_hostname = host_a[0]
        if len(host_a) == 2:
            url_port = host_a[1]
        else:
            url_port = None
        url_path = url_h[2]

    uri_h = {'scheme': url_scheme, 'hostname': url_hostname, 'port': url_port, 'path': url_path}
    return uri_h


@login_required
def profile_user(request):
    user = get_object_or_404(User, pk=request.user.id)
    # print 'is_active=%s' % user.is_active
    if request.method == 'POST':
        form = UserForm(model=User, instance=user, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('account:user:profile'))

    app = app_info()
    app['location'] = 'profile'
    return render(request, 'account/user_profile.html',
                  {'info': user, 'app': app})


@login_required
def change_info(request):
    # 这里需要修改，限定能修改的字段，防止用户非法提权
    user = get_object_or_404(User, pk=request.user.id)
    # print 'is_active=%s' % user.is_active
    if request.method == 'POST':
        form = UserForm(model=User, instance=user, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('account:user:profile'))
    else:
        form = UserForm(model=User, instance=user)

    app = app_info()
    app['location'] = 'change_info'
    return render(request, 'edit_data2.html',
                  {'form': form, 'app': app})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # print 'is_active=%s' % user.is_active
    if request.method == 'POST':
        ds = DataSerialize()
        form = ManageEditUserForm(model=User, instance=user, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = ManageEditUserForm(model=User, instance=user, )

    m2m_fs = User._meta.many_to_many
    m2m_list = []
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    app = app_info()
    app['name'] = "m_account"
    app['location'] = 'edit'
    return render(request, 'edit_data2_not_nav.html',
                  {'form': form, 'app': app, 'm2m_list': m2m_list})


@login_required
def add_user(request):
    if request.method == 'POST':
        ds = DataSerialize()
        form = ManageAddUserForm(model=User, data=request.POST)
        if form.is_valid():
            new_user = form.save()
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = ManageAddUserForm(model=User)

    m2m_fs = User._meta.many_to_many
    m2m_list = []
    for m2m_f in m2m_fs:
        if m2m_f.name in form.fields.keys():
            m2m_list.append(m2m_f.name)
    app = app_info()
    app['name'] = "m_account"
    app['location'] = 'add'
    return render(request, 'add_data2_not_nav.html',
                  {'form': form, 'app': app, 'm2m_list': m2m_list})


def write_file(f_obj, w_file):
    with open(w_file, 'wb+') as destination:
        for chunk in f_obj.chunks():
            destination.write(chunk)


@csrf_exempt  # 禁用csrf
@login_required
def add_avatar(request, ):
    '''
    上传头像
    :param request:
    :return:
    '''
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.id)
            USER_AVATAR_PRE_DIR = os.path.join(AVATAR_PRE_DIR, str(user.id))
            avatar_file_obj = request.FILES['avatar_file']
            avatar_file_path = os.path.join(USER_AVATAR_PRE_DIR,
                                            datetime.datetime.now().strftime('avatar_%Y%m%d%H%M%S.jpg'))
            avatar_file_fullpath = os.path.join(ASSET_DIR, avatar_file_path)
            USER_AVATAR_DIR = os.path.dirname(avatar_file_fullpath)
            if os.path.exists(USER_AVATAR_DIR) is False:
                os.makedirs(USER_AVATAR_DIR)
            if os.path.exists(avatar_file_fullpath):
                try:
                    os.remove(avatar_file_fullpath)
                except(OSError, e):
                    print("Error: %s - %s." % (e.filename, e.strerror))

            write_file(avatar_file_obj, avatar_file_fullpath)
            if os.path.exists(avatar_file_fullpath):
                user.image = avatar_file_path
                user.save()
        else:
            return HttpResponseRedirect(reverse('site_index'))

    app = app_info()
    app['name'] = "account"
    app['location'] = 'add_avatar'
    return render(request, 'account/add_avatar.html',
                  {'app': app, })


@csrf_exempt  # 禁用csrf
@login_required
def del_user(request, user_id):
    del_res = {}
    if request.method == "POST":
        del_res = del_model_data(model=User, id=user_id)
        USER_AVATAR_PRE_DIR = os.path.join(AVATAR_PRE_DIR, str(user_id))
        USER_AVATAR_DIR = os.path.join(ASSET_DIR, USER_AVATAR_PRE_DIR)
        if os.path.exists(USER_AVATAR_DIR):
            try:
                os.rmdir(USER_AVATAR_DIR)
            except(OSError, e):
                print("Error: %s - %s." % (e.filename, e.strerror))

    html = json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


@login_required
def list_user(request):
    model_object = User
    template_file = 'account/user.html'
    show_field_list = ['id',
                       'name',
                       'username',
                       'email',
                       'department',
                       'position',
                       'superior',
                       'roles',
                       'is_staff',
                       'is_superuser',
                       'is_active',
                       'date_joined',
                       'last_login',
                       ]
    filter_field = 'username'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['name'] = "m_account"
    app['location'] = 'list'
    ex_field_list = {
        'Role_m2m': {
            'fields': {
                'role_name': 'host_record',
            }
        }
    }

    render_context = list_data(app=app, request=request, model_object=model_object, each_page_items=each_page_items,
                               filter_field=filter_field, template_file=template_file, show_field_list=show_field_list,
                               is_frontend_paging=True)
    return render_context


def signup(request):
    # return HttpResponseRedirect(reverse('site_index'))
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        checkcod_s = request.session.get('checkcode', '').upper()
        checkcod_q = request.POST.get('checkcode', '').upper()
        if checkcod_s == checkcod_q and form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('account:user:login'))
    else:
        form = SignupForm()
    app = app_info()
    app['location'] = 'signup'
    return render(request, 'account/signup2.html',
                  {'form': form, 'app': app},
                  )


@never_cache
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            checkcod_s = request.session.get('checkcode', '').upper()
            checkcod_q = request.POST.get('checkcode', '').upper()
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            x_next = request.GET.get('next', None)

            if x_next is None:
                s_next = request.POST.get('next', reverse('site_index'))
            else:
                s_next = x_next

            if parse_uri(s_next)['path'] in [reverse('account:user:login'), reverse('account:user:logout'),
                                             reverse('account:user:signup')]:
                next = reverse('site_index')
            else:
                next = s_next

            user = auth.authenticate(username=username, password=password)
            if checkcod_s == checkcod_q and user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                ruser = User.objects.get(username=username)
                # init_permission(request, ruser)
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('account:user:login'))
        else:
            form = LoginForm()
            s_next = request.GET.get('next', None)
            next = s_next
            if next is None:
                next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return render(request, 'account/login2.html',
                      {'form': form, 'next': next})
    else:
        next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return HttpResponseRedirect(next)


@never_cache
def login_rbac(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            checkcod_s = request.session.get('checkcode', '').upper()
            checkcod_q = request.POST.get('checkcode', '').upper()
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            x_next = request.GET.get('next', None)

            if x_next is None:
                s_next = request.POST.get('next', reverse('site_index'))
            else:
                s_next = x_next

            if parse_uri(s_next)['path'] in [reverse('account:user:login_rbac'), reverse('account:user:logout'),
                                             reverse('account:user:signup')]:
                next = reverse('site_index')
            else:
                next = s_next

            user = auth.authenticate(username=username, password=password)
            if checkcod_s == checkcod_q and user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                # init_permission(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('account:user:login_rbac'))
        else:
            form = LoginForm()
            s_next = request.GET.get('next', None)
            next = s_next
            if next is None:
                next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return render(request, 'account/login2.html',
                      {'form': form, 'next': next})
    else:
        next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return HttpResponseRedirect(next)


@login_required
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('site_index'))


@login_required
def change_password(request):
    if request.user.is_authenticated:
        app = app_info()
        app['name'] = "account"
        app['location'] = 'change_password'
        if request.method == 'POST':
            old_password = request.POST.get('old_password').strip()
            password1 = request.POST.get('password1', '').strip()
            password2 = request.POST.get('password2', '').strip()
            is_success = 'false'
            if password1 != '' and password2 != '' and password1 == password2:
                user = get_object_or_404(User, pk=request.user.id)
                if user.check_password(old_password):
                    user.set_password(password1)
                    user.save()
                    update_session_auth_hash(request, user)  # 更新session，避免重新登录。
                    msg = '修改密码成功！'
                    is_success = 'true'
                else:
                    msg = '旧密码错误，请重新输入正确的旧密码！'
            else:
                msg = '两次密码输入不一致，请重新输入！'
            return render(request, 'account/change_password.html',
                          {'app': app, 'msg': msg, 'is_success': is_success})
        else:
            return render(request, 'account/change_password.html',
                          {'app': app})
    else:
        return HttpResponseRedirect(reverse('site_index'))

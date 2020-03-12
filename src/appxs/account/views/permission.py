# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

if sys.version_info >= (3, 0, 0):
    from urllib.parse import urlparse
else:
    from urlparse import urlparse

if sys.version_info >= (3, 5, 0):
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
else:
    from math import isclose
import json

from django.shortcuts import render, get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from guardian.decorators import permission_required, permission_required_or_403
from django.utils.decorators import method_decorator

from spmo.common import Common
from spmo.data_serialize import DataSerialize
from spcc.views.common import list_data, del_model_items, display_confirm_msg
from spcc.models.common import del_model_data

from spcc.views.common import Ajax

from appxs.account.models.user import Menu, Role
from appxs.account.forms.permission import AddResourceForm

co = Common()


def app_info():
    app = {
        "name": "account",
        "fun": "permission",
        "edit_url": 'account:edit_permission',
        "del_url": 'account:del_permission'
    }
    return app


def get_all_resource(r_type='all'):
    resources = list(Menu.objects.values(
        'id',
        'name',
        'url',
        'url_target',
        'icon',
        'code',
        'parent',
        'type',
        'level',
        'view_name',
        'desc',
        'order',
    ).distinct())

    # 按order字段重新排序
    resources = sorted(resources, key=lambda y: str(y['order']))
    if r_type == 'menu':
        r_menu = [r for r in resources if r['permissions__type'] == 'menu']
    else:
        r_menu = resources
    return r_menu


def get_resource_from_role(role_id=None, r_type='all'):
    # try:
    resources = list(Role.objects.get(id=role_id).permissions.values(
        'id',
        'name',
        'url',
        'url_target',
        'icon',
        'code',
        'parent',
        'type',
        'level',
        'view_name',
        'desc',
        'order',
    ).distinct())

    resources = sorted(resources, key=lambda y: str(y['order']))

    if r_type == 'menu':
        r_menu = [r for r in resources if r['permissions__type'] == 'menu']
    else:
        r_menu = resources
    return r_menu


def get_resource_by_user(user=None):
    if isinstance(user, User) is False:
        user = get_object_or_404(User, pk=user)

    resources = list(user.roles.values(
        'permissions__id',
        'permissions__name',
        'permissions__url',
        'permissions__url_target',
        'permissions__icon',
        'permissions__code',
        'permissions__parent',
        'permissions__type',
        'permissions__level',
        'permissions__view_name',
        'permissions__desc',
        'permissions__order',

    ).distinct())
    resources = sorted(resources, key=lambda y: str(y['permissions__order']))
    o_resources = []

    for item in resources:
        resource = {
            'id': item['permissions__id'],
            'name': item['permissions__name'],
            'url': item['permissions__url'],
            'url_target': item['permissions__url_target'],
            'icon': item['permissions__icon'],
            'code': item['permissions__code'],
            'type': item['permissions__type'],
            'parent': item['permissions__parent'],
            'level': item['permissions__level'],
            'view_name': item['permissions__view_name'],
            'desc': item['permissions__desc'],
            'order': item['permissions__order'],
        }
        o_resources.append(resource)
    return o_resources


@csrf_exempt  # 禁用csrf
@login_required
def index(request, ):
    app = app_info()
    app['location'] = 'index'
    return render(request, 'account/permission.html',
                  {'app': app})


@csrf_exempt  # 禁用csrf
@login_required
def grant_perm(request, role_id):
    app = app_info()
    app['location'] = 'grant_perm'
    role_ins = get_object_or_404(Role, pk=role_id)
    return render(request, 'account/grant_permission.html',
                  {'app': app, 'role_id': role_ins.id, 'role_name': role_ins.name}, )


@csrf_exempt  # 禁用csrf
@login_required
def grant_perm_min(request, role_id):
    app = app_info()
    app['location'] = 'grant_perm_min'
    role_ins = get_object_or_404(Role, pk=role_id)
    return render(request, 'account/grant_perm_min.html',
                  {'app': app, 'role_id': role_ins.id, 'role_name': role_ins.name}, )


@csrf_exempt  # 禁用csrf
@login_required
def show_user_perm(request, user_id):
    app = app_info()
    app['location'] = 'show_user_perm'
    user_ins = get_object_or_404(User, pk=user_id)
    return render(request, 'account/show_user_perm.html',
                  {'app': app, 'user_id': user_ins.id, 'user_name': user_ins.__str__}, )


@csrf_exempt  # 禁用csrf
@login_required
def get_user_perm_tree(request, user_id):
    perm_data = []

    user_ins = get_object_or_404(User, pk=user_id)
    all_roles_ins = list(user_ins.roles.all())

    perm_rolenames = {}
    for role_ins in all_roles_ins:
        all_resources = get_resource_from_role(role_id=role_ins.id)
        for a_resource in all_resources:
            pid = a_resource['parent']
            r_id = a_resource['id']
            checked = "true"
            if pid is None:
                pid = 0
            if r_id in perm_rolenames:
                role_name = '%s, %s' % (perm_rolenames[r_id], role_ins.name)
            else:
                role_name = role_ins.name
                perm_rolenames[r_id] = role_name

            perm_i = {'id': r_id, 'pId': pid,
                      'name': '%s[%s]<-[%s]' % (a_resource['view_name'], a_resource['type'], role_name),
                      'checked': checked}
            perm_data.append(perm_i)
    if request.method == "GET":
        tree_res = {'data': perm_data}

    html = json.dumps(tree_res)
    return HttpResponse(html, content_type="application/json")


@csrf_exempt  # 禁用csrf
@login_required
def get_resource_tree(request, ):
    perm_data = []

    all_resources = get_all_resource()
    for a_resource in all_resources:
        pid = a_resource['parent']
        if pid is None:
            pid = 0
        perm_i = {'id': a_resource['id'], 'pId': pid, 'name': '%s[%s]' % (a_resource['view_name'], a_resource['type']),
                  'order': a_resource['order'], }
        perm_data.append(perm_i)
    if request.method == "GET":
        tree_res = {'data': perm_data}

    html = json.dumps(tree_res)
    return HttpResponse(html, content_type="application/json")


def sort_nodes(nodes=[], is_recursion=True):
    '''
    更新所有节点的位置、排序、层级信息
    :param nodes:
    :param is_recursion:
    :return:
    '''
    has_done = {}
    nodes_count = len(nodes)
    init_max_order_num = 2.0
    init_min_order_num = 1.0
    node_order_step = 0.0
    if nodes_count > 0:
        node_order_step = round((init_max_order_num - init_min_order_num) / nodes_count, 5)  # 保留5位小数
    curr_order_num = 0.0
    curr_node_num = 0
    for node in nodes:
        if is_recursion and node['isParent']:
            sort_nodes(nodes=node['children'], is_recursion=True)
        if node['id'] not in has_done:
            n_ins = get_object_or_404(Menu, pk=node['id'])
            curr_order_num = init_min_order_num + node_order_step * curr_node_num
            if curr_node_num == nodes_count - 1:
                t_order = init_max_order_num
            elif curr_node_num == 0:
                t_order = init_min_order_num
            else:
                t_order = curr_order_num
            n_ins.level = node['level']
            n_ins.order = t_order
            is_update_pid = False
            if n_ins.parent is not None:  # 非根节点
                if node['pId'] is None:  # 非根节点 --> 根节点
                    n_ins.parent = None
                elif n_ins.parent.id != node['pId']:  # 非根节点 --> 非根节点（父节点有变化）
                    is_update_pid = True
            elif node['pId'] is not None and n_ins.parent is None:  # 根节点 --> 非根节点
                is_update_pid = True
            else:
                is_update_pid = False
            if is_update_pid:
                n_ins.parent = get_object_or_404(Menu, pk=node['pId'])
            n_ins.save()
            curr_node_num = curr_node_num + 1

        has_done[node['id']] = 'done'

        del n_ins


def sort_subnodes(parent_ins):
    '''
    更新父节点下的所有子节点排序
    :param parent_ins: Menu instance
    :return: nothing
    '''
    nodes = Menu.objects.filter(parent=parent_ins)
    nodes_count = len(nodes)
    init_max_order_num = 2.0
    init_min_order_num = 1.0
    node_order_step = 0.0
    curr_order_num = 0.0
    curr_node_num = 0
    if nodes_count > 0:
        node_order_step = round((init_max_order_num - init_min_order_num) / nodes_count, 5)  # 保留5位小数
    for n_ins in nodes:
        curr_order_num = init_min_order_num + node_order_step * curr_node_num
        if curr_node_num == nodes_count - 1:
            t_order = init_max_order_num
        elif curr_node_num == 0:
            t_order = init_min_order_num
        else:
            t_order = curr_order_num
        # print('n_ins_name: %s, n_ins_view_name: %s, t_order: %s' % (n_ins.name, n_ins.view_name, t_order))
        n_ins.order = t_order

        # 更新节点的level
        if n_ins.parent is None:
            n_ins.level = 0
        else:
            n_ins.level = n_ins.parent.level + 1
        n_ins.save()
        curr_node_num = curr_node_num + 1
        # del n_ins


@csrf_exempt  # 禁用csrf
@login_required
def save_resource_tree(request):
    '''
    保存所有节点的位置、排序、层级信息
    :param request:
    :return:
    '''
    if request.method == "POST":
        ds = DataSerialize()
        tree_data = request.POST.get('tree_data')
        tree_data = ds.deserialize(tree_data)
        sort_nodes(nodes=tree_data)
        rs_data = {'timestamp': ds.get_create_date()}
        html = json.dumps(rs_data)
        return HttpResponse(html, content_type="application/json")


@csrf_exempt  # 禁用csrf
@login_required
def update_resource_position(request):
    '''
    更新资源节点的位置、排序、层级信息
    :param request:
    :return:
    '''
    if request.method == "POST":
        ds = DataSerialize()
        node_data = request.POST.get('node_data')
        node_data = ds.deserialize(node_data)
        # co.DD(node_data)
        node = node_data['curr_node']
        pre_node = node_data['pre_node']
        next_node = node_data['next_node']
        n_ins = get_object_or_404(Menu, pk=node['id'])
        old_parent_ins = n_ins.parent
        init_max_order_num = 2.0
        init_min_order_num = 1.0

        is_update_pid = False
        if n_ins.parent is not None:  # 非根节点
            if node['pId'] is None:  # 非根节点 --> 根节点
                n_ins.parent = None
            elif n_ins.parent.id != node['pId']:  # 非根节点 --> 非根节点（父节点有变化）
                is_update_pid = True
        elif node['pId'] is not None and n_ins.parent is None:  # 根节点 --> 非根节点
            is_update_pid = True
        else:
            is_update_pid = False
        if is_update_pid:
            n_ins.parent = get_object_or_404(Menu, pk=node['pId'])
            # 更新节点的level
            if n_ins.parent is None:
                n_ins.level = 0
            else:
                n_ins.level = n_ins.parent.level + 1
        else:
            n_ins.level = node['level']
        if pre_node is not None and next_node is not None:  # 夹在中间位
            t_order = round((pre_node['order'] + next_node['order']) / 2, 5)
        elif pre_node is None and next_node is None:  # 第一位或最后一位(有且只有一个元素)
            t_order = init_min_order_num
        elif pre_node is None and next_node is not None:  # 第一位
            t_order = round(next_node['order'] / 2, 5)
        elif pre_node is not None and next_node is None:  # 最后一位
            t_order = round((pre_node['order'] + 1), 5)
        n_ins.order = t_order
        n_ins.save()

        # 重新整理同级所有节点排序，使得序号范围在init_min_order_num -- init_max_order_num之间，
        # 同级的序号间距也重新规整为：round(init_max_order_num-init_min_order_num/subnodes_count, 5)
        new_parent_ins = n_ins.parent
        if new_parent_ins != old_parent_ins:
            sort_subnodes(parent_ins=new_parent_ins)
        sort_subnodes(parent_ins=old_parent_ins)

        rs_data = {'timestamp': ds.get_create_date()}
        html = json.dumps(rs_data)
        return HttpResponse(html, content_type="application/json")


@csrf_exempt  # 禁用csrf
@login_required
def get_perm_tree(request, role_id):
    perm_data = []
    role_perm = {}
    role_resources = get_resource_from_role(role_id=role_id)
    for r_resource in role_resources:
        role_perm[r_resource['id']] = r_resource

    all_resources = get_all_resource()
    for a_resource in all_resources:
        pid = a_resource['parent']
        checked = "false"
        if pid is None:
            pid = 0
        if a_resource['id'] in role_perm.keys():
            checked = "true"
        perm_i = {'id': a_resource['id'], 'pId': pid, 'name': '%s[%s]' % (a_resource['view_name'], a_resource['type']),
                  'checked': checked}
        perm_data.append(perm_i)
    if request.method == "GET":
        tree_res = {'data': perm_data}

    html = json.dumps(tree_res)
    return HttpResponse(html, content_type="application/json")


@csrf_exempt  # 禁用csrf
@login_required
def save_perm_tree(request, role_id):
    if request.method == "POST":
        ds = DataSerialize()
        tree_data = request.POST.get('tree_data')
        tree_data = ds.deserialize(tree_data)
        role_id = request.POST.get('role_id')
        rs_data = {'timestamp': ds.get_create_date()}
        role_ins = get_object_or_404(Role, pk=role_id)
        for td in tree_data:
            if td['checked'] is True and td['checkedOld'] is False:
                role_ins.permissions.add(Menu.objects.get(pk=td['id']))
            elif td['checked'] is False and td['checkedOld'] is True:
                role_ins.permissions.remove(Menu.objects.get(pk=td['id']))
        role_ins.save()
        html = json.dumps(rs_data)
        return HttpResponse(html, content_type="application/json")


@csrf_exempt  # 禁用csrf
@login_required
def add_resource(request, resource_pid=None):
    if request.method == 'POST':
        ds = DataSerialize()
        form = AddResourceForm(model=Menu, data=request.POST)
        if form.is_valid():
            new_resource = form.save()
            r_parent = new_resource.parent
            if r_parent is not None:
                new_resource.level = new_resource.parent.level - 1
            elif r_parent is None:
                new_resource.level = 0
            new_resource.save()

            sort_subnodes(parent_ins=r_parent)
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        if resource_pid is None or resource_pid == '' or int(resource_pid) == 0:
            form = AddResourceForm(model=Menu, )
        else:
            form = AddResourceForm(model=Menu, instance=Menu(parent_id=resource_pid))

    app = app_info()
    app['name'] = "permission"
    app['location'] = 'add'
    return render(request, 'add_data2_not_nav.html',
                  {'form': form, 'app': app})


@csrf_exempt  # 禁用csrf
@login_required
def edit_resource(request, resource_id):
    resource = get_object_or_404(Menu, pk=resource_id)
    ds = DataSerialize()
    if request.method == 'POST':
        form = AddResourceForm(model=Menu, instance=resource, data=request.POST)
        if form.is_valid():
            new_resource = form.save()
            r_parent = new_resource.parent
            sort_subnodes(parent_ins=r_parent)
            rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
            html = json.dumps(rs_data)
            return HttpResponse(html, content_type="application/json")
    else:
        form = AddResourceForm(model=Menu, instance=resource)

    app = app_info()
    app['name'] = "m_account"
    app['location'] = 'edit'
    return render(request, 'edit_data2_not_nav.html',
                  {'form': form, 'app': app})


@csrf_exempt  # 禁用csrf
@login_required
def del_resource(request, resource_id):
    ds = DataSerialize()
    if request.method == "POST":
        new_resource = get_object_or_404(Menu, pk=resource_id)
        r_parent = new_resource.parent

        sub_menus = Menu.objects.filter(parent=new_resource)
        for sm in sub_menus:
            sm.parent = r_parent
            sm.save()
        del_res = del_model_data(model=Menu, id=resource_id)
        sort_subnodes(parent_ins=r_parent)
        rs_data = {'timestamp': ds.get_create_date(), 'result': 'success'}
        html = json.dumps(rs_data)
        return HttpResponse(html, content_type="application/json")

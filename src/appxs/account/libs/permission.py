# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

import functools


def perm_required(perms=[], allow_method=[]):
    def check_perm(request, perms=[]):
        # 如未定义，默认放行
        if len(perms) < 1:
            return True
        has_perm = False
        if not hasattr(request, 'permission_codes') or len(request.permission_codes) < 1:
            return False
        for perm in perms:
            if perm is None or perm == '':
                has_perm = False
                break
            else:
                if perm in request.permission_codes:
                    has_perm = True
                else:
                    has_perm = False
                    break
        return has_perm

    def check_method(request, allow_method):
        # 如未定义，默认所有方法都放行
        if len(allow_method) < 1:
            return True
        if request.method.upper() in allow_method:
            return True
        else:
            return False

    def wpp(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            is_denied = False
            if request.user.is_authenticated:
                if check_method(request, allow_method) is False or check_perm(request, perms) is False:
                    is_denied = True
            if is_denied:
                return HttpResponseForbidden()
            return func(request, *args, **kwargs)

        return wrapper

    return wpp


def is_inter(la, lb):
    '''
    判断两个列表元素是否有交集
    :param la: list
    :param lb: list
    :return: True/False
    '''
    result = list(set(la) & set(lb))
    if result:
        return True
    else:
        return False


def get_user(request):
    return request.user


def get_resource_from_role(request, user=None, r_type='menu'):
    if user is None:
        user = get_user(request)
    try:
        menus = user.roles.values(
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
        ).distinct()

        if r_type == 'menu':
            r_menu = [menu for menu in menus if menu['permissions__type'] == 'menu']
        else:
            r_menu = menus

        return r_menu

    except AttributeError:
        return None


def get_permission_code(request, user=None):
    role_menus = get_resource_from_role(request, user=user, r_type='all')
    if role_menus is not None:
        permission_code_list = [menu['permissions__code'] for menu in role_menus]
        return permission_code_list
    else:
        return []


def get_permission_url(request):
    role_menus = get_resource_from_role(request, r_type='permission')
    if role_menus is not None:
        permission_url_list = [menu['permissions__url'] for menu in role_menus]
        return permission_url_list
    else:
        return []


def get_permission_menu(request):
    permission_menu_list = []
    hk = {}

    def get_lorder(level):
        '''
        获取lorder值
        :param level:
        :return:

        正常工作条件：
            L1，L2，L3分别为第一层级，第二层级，第三层级
            L1_level为第一层级的level值,  0
            L2_level为第二层级的level值， 1
            L3_level为第二层级的level值， 2

            L1层级的元素总个数 小于  pow(10, （L2_level + 3) 。

            例如：
                第一层级：l1元素数量 < pow(10, (1 + 3)) = 10000个
                第二层级：l2元素数量 < pow(10, (2 + 3)) = 100000个
                第三层级：l3元素数量 < pow(10, (3 + 3)) = 1000000个
                .
                .
                .
        '''
        if isinstance(level, (int, float)):
            if level in hk:
                hk[level] = hk[level] + 1
            else:
                if level == 0:
                    hk[level] = 1
                else:
                    hk[level] = pow(10, level + 3)
            lorder = hk[level]
        else:
            lorder = 1
        return lorder

    role_menus = get_resource_from_role(request, r_type='menu')
    if role_menus is not None:
        for item in role_menus:
            menu = {
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
                'lorder': get_lorder(item['permissions__level']),
                'active': False,
                'sub_menu': [],
            }
            permission_menu_list.append(menu)
        return sorted(permission_menu_list, key=lambda y: y['lorder'], reverse=True)  # 按lorder 反向排序


def get_reveal_menu(request):
    permission_menu_dict = {}
    request_url = request.path_info
    permission_menu_list = get_permission_menu(request)
    if permission_menu_list is not None:
        p_menu_active_id_list = []
        top_menu_sub_ids = {}
        for menu in permission_menu_list:
            url = menu['url']

            if url and re.match(url, request_url):
                p_menu_active_id_list.insert(0, menu['id'])
                menu['active'] = True

            if menu['parent'] is None:
                if menu['id'] not in top_menu_sub_ids.keys() or isinstance(top_menu_sub_ids[menu['id']],
                                                                           list) is False:
                    top_menu_sub_ids[menu['id']] = []

            permission_menu_dict[menu['id']] = menu

        menu_data = []
        top_menu_ids_map = {}

        for i in permission_menu_dict:
            if permission_menu_dict[i]['parent']:
                pid = permission_menu_dict[i]['parent']
                if pid in top_menu_sub_ids.keys():
                    top_menu_sub_ids[pid].append(i)
                if pid in permission_menu_dict.keys():
                    parent_menu = permission_menu_dict[pid]
                    parent_menu['sub_menu'].append(permission_menu_dict[i])
                    # 子菜单排序
                    parent_menu['sub_menu'] = sorted(parent_menu['sub_menu'], key=lambda y: y['order'])
                    '''
                    设置父菜单中的active参数
                    '''
                    if permission_menu_dict[i]['id'] in p_menu_active_id_list:
                        parent_menu['active'] = True
                        p_menu_active_id_list.append(parent_menu['id'])
            else:
                menu_data.append(permission_menu_dict[i])
                top_menu_ids_map[len(menu_data)] = i

        '''
        搜寻根菜单，设置active参数
        '''
        for k in top_menu_ids_map.keys():
            # 返回父id为k的所有子菜单id列表
            # sub_ids = list(Menu.objects.filter(parent=top_menu_ids_map[k]).values_list('id', flat=True))
            sub_ids = top_menu_sub_ids[top_menu_ids_map[k]]
            if is_inter(p_menu_active_id_list, sub_ids):
                menu_data[k - 1]['active'] = True

        '''
        根菜单依据order字段排序
        '''
        menu_data = sorted(menu_data, key=lambda y: y['order'])

        reveal_menu = menu_data
        return reveal_menu

    else:
        return []


def get_role(user):
    return ['aa', 'bb', 'cc']


def cas_user_perm_attributes(user, service):
    """
    Return site user perm and role
    """
    attributes = {}
    attributes['permission'] = get_permission_code(request=None, user=user)
    attributes['role'] = get_role(user=user)
    return attributes

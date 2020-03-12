# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission, DjangoModelPermissions

from spmo.common import Common

co = Common()


class CustomBasePermissions(BasePermission):

    def __init__(self, perms=[]):
        self.perms = perms

    def get_custom_perms(self, view, method):  # 接收请求的视图，以及请求方法
        if hasattr(view, 'extra_perms'):
            if isinstance(view.extra_perms, dict):
                if hasattr(view, 'name'):
                    if view.name is None:
                        view_name = view.action_map.get(method.lower(), '').lower()
                    else:
                        view_name = view.name.lower()
                else:
                    view_name = method.lower()
                return view.extra_perms.get(view_name, [])
        return []

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        # 忽略用户验证（如果DRF全局也配置不需要登录可访问，则访客也可通过验证）
        if getattr(view, '_ignore_verify_auth', False):
            return True

        # 验证是否登录
        if not request.user or not request.user.is_authenticated:
            return False

        # 忽略权限验证
        if getattr(view, '_ignore_verify_permission', False):
            return True

        perms = self.get_custom_perms(view, request.method)

        # 如果没有定义相关权限，默认是拒绝访问！每个访问都需要明确定义权限
        if len(perms) < 1:
            return False

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


class CustomModelPermissions(DjangoModelPermissions):

    # def __init__(self):
    #     self.perms_map = copy.deepcopy(self.perms_map)  # you need deepcopy when you inherit a dictionary type
    #     self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def get_custom_perms(self, view, method):  # 接收请求的视图，以及请求方法
        if hasattr(view, 'extra_perm_map'):  # 判断视图是否定义了extra_perm_map
            if isinstance(view.extra_perm_map, dict):  # 判断extra_perm_map属性必须是一个dict
                return view.extra_perm_map.get(method, [])  # 返回extra_perm_map里定义的参数，默认为空list
        return []

    def has_permission(self, request, view):
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if not request.user or (
                not request.user.is_authenticated and self.authenticated_users_only):
            return False

        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        perms.extend(self.get_custom_perms(view, request.method))  # 两个列表相加，将请求方法加入DjangoModelPermissions里的perms_map中.
        return request.user.has_perms(perms)


def jwt_response_payload_handler(token, user=None, request=None):
    """为返回的结果添加用户相关信息"""

    return {
        'token': token,
        # 'user_id': user.id,
        # 'username': user.username,
    }

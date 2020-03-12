# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.conf import settings
# from django.contrib.auth import get_user_model
#
# # from appxs.account.models.user import User as RbacUser
#
# User = get_user_model()
#
# from spmo.common import Common
#
# co = Common()
#
# def init_permission(request, user):
#     """
#     用户权限信息初始化，获取当前用户所有权限信息，并保存到Session中
#     此处的request以及user参数均为对象，user为登陆成功时在数据库中查询到的user对象
#     :param request:
#     :param user:
#     :return:
#     """
#     # 去空去重
#     user = User.objects.get(pk=user.id)
#     permission_list = user.roles.filter(permissions__id__isnull=False).values(
#         'permissions__id',
#         'permissions__title',  # 用户列表
#         'permissions__url',
#         'permissions__code',
#         'permissions__menu_gp_id',  # 组内菜单ID，Null表示是菜单
#         'permissions__group_id',  # 权限的组ID
#         'permissions__group__menu_id',  # 当前权限所在组的菜单ID
#         'permissions__group__menu__title',  # 当前权限所在组的菜单名称
#     ).distinct()
#
#     co.DD(permission_list)
#     # 菜单相关配置，在inclusion_tag中使用
#     menu_permission_list = []
#     for item in permission_list:
#         tpl = {
#             'id': item['permissions__id'],
#             'title': item['permissions__title'],
#             'url': item['permissions__url'],
#             'menu_gp_id': item['permissions__menu_gp_id'],
#             'menu_id': item['permissions__group__menu_id'],
#             'menu_title': item['permissions__group__menu__title']
#         }
#         menu_permission_list.append(tpl)
#         request.session[settings.PERMISSION_MENU_KEY] = menu_permission_list
#         # 形如
#         """
#         {"url": "/host/","menu_title": "主机管理","title": "主机列表","id": 1,"menu_gp_id": null,"menu_id": 1},
#         {"url": "/host/add/","menu_title": "主机管理","title": "添加主机","id": 2,"menu_gp_id": 1,"menu_id": 1},
#         {"url": "/host/(\\d+)/delete/","menu_title": "主机管理","title": "删除主机","id": 3,"menu_gp_id": 1,"menu_id": 1},
#         {"url": "/host/(\\d+)/change/","menu_title": "主机管理","title": "修改主机","id": 4,"menu_gp_id": 1,"menu_id": 1}
#         {"url": "/userinfo/","menu_title": "用户管理","title": "用户列表","id": 5,"menu_gp_id": null,"menu_id": 2},
#         {"url": "/userinfo/add/","menu_title": "用户管理","title": "添加用户","id": 6,"menu_gp_id": 5,"menu_id": 2},
#         ......
#         """
#
#     # 权限相关，中间件使用
#     permission_dict = {}
#     for item in permission_list:
#         group_id = item['permissions__group_id']
#         code = item['permissions__code']
#         url = item['permissions__url']
#         if group_id in permission_dict:
#             permission_dict[group_id]['codes'].append(code)
#             permission_dict[group_id]['urls'].append(url)
#         else:
#             permission_dict[group_id] = {"codes": [code, ], "urls": [url, ]}
#     request.session[settings.PERMISSION_URL_DICT_KEY] = permission_dict
#     # 形如
#     """
#     {
#         "1": {
#             "codes": ["list","add","delete","edit"],
#             "urls": ["/host/","/host/add/","/host/(\\d+)/delete/","/host/(\\d+)/change/"]
#          },
#         "2": {
#             "codes": ["list","add","delete","change"],
#             "urls": ["/userinfo/","/userinfo/add/","/userinfo/(\\d+)/delete/","/userinfo/(\\d+)/change/"]
#          }
#     }
#     """

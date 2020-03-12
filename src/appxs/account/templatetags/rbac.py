# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.conf import settings
# from django.template import Library
# import re
# import json
#
# from spmo.common import Common
#
# co = Common()
# register = Library()
#
#
# @register.inclusion_tag('menu_tpl.html')
# def menu_html(request):
#     """
#     获取session中的菜单信息，匹配当前URL，生成菜单
#     :param request: 请求的requst对象
#     :return:
#     """
#     menu_list = request.session.get(settings.PERMISSION_MENU_KEY)
#     # 当前请求URL
#     current_url = request.path_info
#     print('current_url:%s' % current_url)
#     co.DD(menu_list)
#     menu_dict = {}
#     # menu_gp_id为空则是菜单
#     for item in menu_list:
#         if not item['menu_gp_id']:
#             menu_dict[item['id']] = item
#     print('vvvv')
#     co.DD(menu_dict)
#     print('kkkkk')
#     for item in menu_list:
#         regax = "^{0}$".format(item['url'])
#         if re.match(regax, current_url):
#             menu_gp_id = item['menu_gp_id']
#             if menu_gp_id:
#                 #menu_dict[menu_gp_id] = {}
#                 menu_dict[menu_gp_id]['active'] = True
#             else:
#                 #menu_dict[item['id']] = {}
#                 menu_dict[item['id']]['active'] = True
#
#     co.DD(menu_dict)
#     result = {}
#     for item in menu_dict.values():
#         active = item.get('active')
#         menu_id = item['menu_id']
#         if menu_id in result:
#             result[menu_id]['children'].append({'title': item['title'], 'url': item['url'], 'active': active})
#             if active:
#                 result[menu_id]['active'] = True
#         else:
#             result[menu_id] = {
#                 'menu_id': item['menu_id'],
#                 'menu_title': item['menu_title'],
#                 'active': active,
#                 'children': [
#                     {'title': item['title'], 'url': item['url'], 'active': active}
#                 ]
#             }
#     print(json.dumps(result, indent=4, ensure_ascii=False))
#     return {'menu_dict': result}

# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# import re
#
# from django.shortcuts import redirect, HttpResponse
# from django.conf import settings
# from django.utils.deprecation import MiddlewareMixin
#
#
# class RbacMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # 1. 当前请求URL
#         current_request_url = request.path_info
#
#         # 2. 处理白名单,如login及admin页面需开放访问权限，根据实际情况而定
#         for url in settings.VALID_URL_LIST:
#             if re.match(url, current_request_url):
#                 return None
#
#         if request.user.is_superuser:
#             return None
#
#         # 3. 获取session中保存的权限信息
#         permission_dict = request.session.get(settings.PERMISSION_MENU_LIST)
#         if not permission_dict:
#             # 登陆页面
#             return redirect(settings.RBAC_LOGIN_URL)
#
#         flag = False
#         for group_id, values in permission_dict.items():
#             for url in values['urls']:
#                 regex = settings.URL_FORMAT.format(url)
#                 if re.match(regex, current_request_url):
#                     flag = True
#                     break
#             if flag:
#                 break
#         if not flag:
#             # 无权访问页面，可以直接redirect
#             return HttpResponse('无权访问')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.deprecation import MiddlewareMixin
from jwt import InvalidSignatureError
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from spmo.common import Common

from appxs.account.libs.permission import get_permission_code

co = Common()


class ValidJwtTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
        if jwt_token is not None and jwt_token != '':
            data = {
                'token': request.META['HTTP_AUTHORIZATION'].split(' ')[1],
            }
            user = None
            try:
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                request.user = user
                # 注入用户拥有的权限码
                request.permission_codes = get_permission_code(request, user)
            except (InvalidSignatureError, ValidationError):
                return None

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404, HttpResponse

from appxs.account.libs.permission import get_permission_code, get_reveal_menu, get_permission_url
from spmo.common import Common

co = Common()


class MenuCollection(MiddlewareMixin):

    def process_request(self, request):
        reveal_menu = get_reveal_menu(request)
        if len(reveal_menu) >= 0:
            request.reveal_menu = reveal_menu
            request.permission_url_list = get_permission_url(request)
            request.permission_codes = get_permission_code(request)


class RbacMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if hasattr(request, 'permission_url_list'):
            request_url = request.path_info
            permission_url = request.permission_url_list
            # print('url=%s' % request_url)
            # return None

            for url in settings.SAFE_URL:
                # print('url=%s' % url)
                if re.match(url, request_url):
                    return None

            for p_url in permission_url:
                # print('p_url=%s' % p_url)
                if p_url is not None and re.match(p_url, request_url):
                    return None
            else:
                if request.user.is_authenticated:
                    return render(request, '403.html')
                else:
                    if request_url.startswith('/api') and request_url.startswith('/api/jwt/') is False:
                        print('redirect jwt auth ...')
                        # return HttpResponseRedirect('/api/jwt/api-token-auth/')
                        return HttpResponse(status=401)
                    else:
                        return HttpResponseRedirect(reverse('account:user:login'))

                    # if request_url in permission_url:
            #     return None
            # else:
            #     return render(request, '404.html')

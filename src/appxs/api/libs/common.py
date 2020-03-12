# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

    def get_paginated_response(self, data):
        # page_size = int(self.request.query_params.get(self.page_size_query_param, self.page_size))
        # if page_size > self.max_page_size:
        #     page_size = self.max_page_size

        page_size = self.get_page_size(self.request)
        current_page = int(self.request.query_params.get(self.page_query_param, 1))
        count = self.page.paginator.count
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': count,
            'page_size': page_size,
            'current_page': current_page,
            'total_page': math.ceil(count / page_size),
            'results': data,
        })

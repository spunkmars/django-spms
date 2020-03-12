# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import copy
import json

from django.http import HttpResponse
from rest_framework.response import Response
from spmo.common import Common
from libs.common import create_uuid


def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class APIResponse(Common):
    def __init__(self, *args, **kwargs):
        self.response_id = create_uuid()
        self.data = {}
        self.message = ''
        self.status_code = 0
        self.doc_url = ''
        self.errors = {}
        super(APIResponse, self).__init__(*args, **kwargs)

    # @property
    # def m_data(self):
    #     return self.data
    #
    # @m_data.setter
    # def data(self, value):
    #     if isinstance(value, dict):
    #         self.data = value

    # @property
    # def message(self):
    #     return self.message
    #
    # @message.setter
    # def message(self, value):
    #     if isinstance(value, dict):
    #         self.message = value

    def m_response(self, b_rd={}):
        r_d = {
            'results': self.data,
            'status_code': self.status_code,  # 不等于0有错误，0正常
            'message': self.message,  # 如果调用api有错误产生，将错误信息写入这里。
            'create_at': get_timestamp(),  # 返回结果的时间戳。
            'response_id': self.response_id,
            'doc_url': self.doc_url,  # 此API的接口文档地址
            'errors': self.errors,  # 更详细的报错细节 ，可以是一个复杂的数据结构
        }
        r_d.update(b_rd)
        return Response(r_d)


def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)

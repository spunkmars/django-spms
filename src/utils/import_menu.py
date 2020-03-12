# coding=utf-8


import os
import sys
import datetime
import time
import argparse
import os
import datetime
import threading
import re
import xlrd
import django

B_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT_LIBS_PATH = B_DIR
if EXT_LIBS_PATH == '':
    EXT_LIBS_PATH = './'
sys.path.append(EXT_LIBS_PATH)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spmo.common import Common
from appxs.account.models.user import Menu

co = Common()


def import_m(app, module, verbose_name):
    def get_menu_url(v):
        return '/%s/%s/%s/' % (app, module, v)

    def get_menu_code(v):
        return '%s-%s-%s' % (app, module, v)

    def get_menu_name(v):
        return '%s-%s-%s' % (app, module, v)

    def get_menu_view(v):
        return '%s:%s:%s' % (app, module, v)

    def get_menu_view_name(temp, action, name):
        return temp.replace('$ACTION$', action).replace('$NAME$', name)

    def import_menu(app, module, verbose_name):
        l_views = [
            # {'index':
            #     {
            #         'type': 'memu',
            #         'view_name_temp': '$NAME$$ACTION$',
            #         'parent': None,
            #         'action': 'index',
            #         'action_v_name': '首页'
            #     },
            # },
            {
                'type': 'menu',
                'view_name_temp': '$NAME$$ACTION$',
                'parent': None,
                'action': 'list',
                'action_v_name': ''
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'add',
                'action_v_name': '添加'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'edit',
                'action_v_name': '编辑'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'del',
                'action_v_name': '删除'
            },
            {
                'type': 'page',
                'view_name_temp': '$NAME$$ACTION$',
                'parent': 'list',
                'action': 'detail',
                'action_v_name': '详情'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'query',
                'action_v_name': '查找'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'filter',
                'action_v_name': '过滤'
            },
            {
                'type': 'button',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'mult_do',
                'action_v_name': '多项操作'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'import',
                'action_v_name': '导入'
            },
            {
                'type': 'page',
                'view_name_temp': '$ACTION$$NAME$',
                'parent': 'list',
                'action': 'export',
                'action_v_name': '导出'
            },

        ]
        i = 1

        d_views = {}
        for vv in l_views:
            d_views[vv['action']] = vv
        for v in l_views:
            parent_ins = None
            parent = v['parent']
            if parent is not None and parent in d_views:
                parent_ins, _ = Menu.objects.get_or_create(name=get_menu_name(parent))
                parent_ins.type = d_views[parent]['type']
                parent_ins.url = get_menu_url(parent)
                parent_ins.code = get_menu_code(parent)
                parent_ins.view_name = get_menu_view_name(d_views[parent]['view_name_temp'],
                                                          d_views[parent]['action_v_name'], verbose_name)
                parent_ins.order = i
                parent_ins.save()
            menu, _ = Menu.objects.get_or_create(name=get_menu_name(v['action']))
            menu.type = v['type']
            menu.url = get_menu_url(v['action'])
            menu.code = get_menu_code(v['action'])
            menu.parent = parent_ins
            menu.view_name = get_menu_view_name(v['view_name_temp'], v['action_v_name'], verbose_name)
            menu.order = i
            menu.save()
        i = i + 0.1

    import_menu(app, module, verbose_name)


menu_config = [
    {
        'app': 'quickstart',
        'module': 'qstart',
        'verbose_name': '示例',
    },

]

for mc in menu_config:
    print('do %s ...' % mc['verbose_name'])
    import_m(mc['app'], mc['module'], mc['verbose_name'])

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template

from spmo.common import Common

co = Common()

register = template.Library()


def do_sidebar_nav(parser, token):
    try:
        tag_name, menu_data = token.split_contents()
    except:
        raise (template.TemplateSyntaxError, "%r tags error" % token.split_contents()[0])

    return SidebarNav(menu_data)


def show_menu(m_data=[]):
    res_str = ''
    for m in m_data:
        m_url = m['url']
        m_url_target = m['url_target']
        m_active = m['active']
        m_icon = m['icon']
        m_view_name = m['view_name']
        m_sub = m['sub_menu']
        m_code = m['code']
        r_str = ''
        if m_active is True:
            m_active_str = 'active'
        else:
            m_active_str = ''
        if m_url is None or m_url == '':
            m_type = 'parent'
            m_icon_str = 'fa fa-circle-o'
        else:
            m_type = 'sub'
            m_icon_str = 'fa fa-caret-right'

        if m_icon is not None and m_icon != '':
            m_icon_str = m_icon

        if m_type == 'parent':
            if isinstance(m_sub, list) and len(m_sub) > 0:
                r_str = '''
                <li class="treeview %s" id="%s">
                        <a href="">
                            <i class="%s"></i><span>%s</span>
                            <span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i>
                        </span>
                        </a>
                        <ul class="treeview-menu">
                        %s
                        </ul>
                </li>
                ''' % (m_active_str, m_code, m_icon_str, m_view_name, show_menu(m_sub))
            else:
                r_str = '''
                <li class="treeview %s" id="%s">
                        <a href="">
                            <i class="%s"></i><span>%s</span>
                            <span class="pull-right-container"><i class="fa fa-angle-left pull-right"></i>
                        </span>
                        </a>
                </li>
                ''' % (m_active_str, m_code, m_icon_str, m_view_name)

        elif m_type == 'sub':
            r_str = '''
                <li id="%s" class="%s">
                    <a href="%s" TARGET="%s"><i
                            class="%s"></i>
                        <span>%s</span>
                    </a>
                </li>

            ''' % (m_code, m_active_str, m_url, m_url_target, m_icon_str, m_view_name)

        res_str = res_str + r_str

    return res_str


class SidebarNav(template.Node):
    def __init__(self, menu_data):
        self.menu_data = template.Variable(menu_data)

    def render(self, context):
        menu_data = self.menu_data.resolve(context)

        return show_menu(m_data=menu_data)


register.tag('sidebar_nav', do_sidebar_nav)

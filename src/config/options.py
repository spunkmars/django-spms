# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

if sys.version_info >= (3, 6, 0):
    import configparser as ConfigParser
else:
    import ConfigParser

from django.utils.translation import ugettext_lazy
from django.utils.translation import ugettext

from spmo.common import Common


def get_conf_obj(config_file=None):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


def get_conf_to_dict(config_file=None):
    c_dict = {}
    config = get_conf_obj(config_file=config_file)
    sections = config.sections()
    for sect in sections:
        c_dict[sect] = config.items(sect)
    return c_dict


def get_option_val(conf_obj=None, section=None, c_k={}):
    if conf_obj.has_option(section, c_k['name']):
        if c_k['type'] == 'boolean':
            return conf_obj.getboolean(section, c_k['name'])
        elif c_k['type'] == 'int':
            return conf_obj.getint(section, c_k['name'])
        elif c_k['type'] == 'float':
            return conf_obj.getfloat(section, c_k['name'])
        elif c_k['type'] == 'list':
            cl = []
            cl_str = conf_obj.get(section, c_k['name'])
            cl = cl_str.split(',')
            cl = [l.strip() for l in cl]
            return cl
        elif c_k['type'] == 'text':
            return conf_obj.get(section, c_k['name'])
        else:
            return conf_obj.get(section, c_k['name'])
    elif 'has_default' in c_k and c_k['has_default'] is True and 'default' in c_k:
        return c_k['default']
    else:
        raise Exception('Can not find option, and has not defualt !')


def get_section_val(conf_obj=None, section=None, c_ks={}):
    c_args = {}
    if not conf_obj.has_section(section):
        raise Exception('Can not find section: [%s] !' % section)
    for k in c_ks:
        if k['require'] is True:
            if not conf_obj.has_option(section, k['name']):
                raise Exception('Can not find section: [%s] option: [%s] !' % (section, k['name']))
        c_args[k['name']] = get_option_val(conf_obj=conf_obj, section=section, c_k=k)
    return c_args


def get_common_conf(config_file=None):
    config = get_conf_obj(config_file=config_file)
    sections = {}
    c_args = {}
    c_keys = {
        'common':
            [
                {'name': 'site_name', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'site_desc', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'site_version', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'site_copyright_year', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'secret_key', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'debug', 'type': 'boolean', 'default': False, 'require': False,
                 'has_default': True},
                {'name': 'time_zone', 'type': 'text', 'default': 'Asia/Shanghai', 'require': False,
                 'has_default': True},
                {'name': 'language_code', 'type': 'text', 'default': 'en-us', 'require': False,
                 'has_default': True},
            ],
        'cors':
            [
                {'name': 'cors_allow_credentials', 'type': 'boolean', 'default': True, 'require': False,
                 'has_default': True},
                {'name': 'cors_origin_allow_all', 'type': 'boolean', 'default': True, 'require': False,
                 'has_default': True},
                {'name': 'cors_origin_whitelist', 'type': 'list', 'default': [], 'require': False,
                 'has_default': True},
            ]

    }

    sections['common'] = get_section_val(conf_obj=config, section='common', c_ks=c_keys['common'])
    sections['cors'] = get_section_val(conf_obj=config, section='cors', c_ks=c_keys['cors'])
    c_args = sections
    return c_args


def get_db_conf(config_file=None):
    config = get_conf_obj(config_file=config_file)
    sections = {}
    c_args = {}
    c_keys = {
        'common':
            [
                {'name': 'db_type', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
            ],
        'sqlite':
            [
                {'name': 'db_name', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False}, ],
        'mysql':
            [
                {'name': 'host', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'port', 'type': 'int', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'user', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'passwd', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'db', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
            ],
        'redis':
            [
                {'name': 'type', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'host', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'port', 'type': 'int', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'user', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'passwd', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'db', 'type': 'int', 'default': None, 'require': True,
                 'has_default': False},
            ],
    }

    sections['common'] = get_section_val(conf_obj=config, section='common', c_ks=c_keys['common'])
    if sections['common']['db_type'] == 'sqlite':
        sections['sqlite'] = get_section_val(conf_obj=config, section='sqlite', c_ks=c_keys['sqlite'])
    elif sections['common']['db_type'] == 'mysql':
        sections['mysql'] = get_section_val(conf_obj=config, section='mysql', c_ks=c_keys['mysql'])
    sections['redis'] = get_section_val(conf_obj=config, section='redis', c_ks=c_keys['redis'])

    c_args = sections
    return c_args


def get_cas_conf(config_file=None):
    config = get_conf_obj(config_file=config_file)
    sections = {}
    c_args = {}
    c_keys = {
        'common':
            [
                {'name': 'mama_cas_enable_single_sign_out', 'type': 'boolean', 'default': True, 'require': False,
                 'has_default': True},
                {'name': 'allow_sites', 'type': 'list', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'deny_sites', 'type': 'list', 'default': None, 'require': True,
                 'has_default': False},
            ],
        'site':
            [
                {'name': 'service', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'callbacks', 'type': 'list', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'logout_allow', 'type': 'boolean', 'default': None, 'require': True,
                 'has_default': False},
                {'name': 'logout_url', 'type': 'text', 'default': None, 'require': True,
                 'has_default': False},
            ],
    }

    sections['common'] = get_section_val(conf_obj=config, section='common', c_ks=c_keys['common'])
    allow_sites = []
    if 'allow_sites' in sections['common']:
        a_sites = sections['common']['allow_sites']
        if 'deny_sites' in sections['common']:
            d_sites = sections['common']['deny_sites']
            allow_sites = list(set(a_sites) - set(d_sites))
        else:
            allow_sites = a_sites
    for s in allow_sites:
        sections[s] = get_section_val(conf_obj=config, section=s, c_ks=c_keys['site'])

    c_args = sections
    return c_args


class GoballOptions(Common):
    def __init__(self, *args, **kwargs):
        self.trans_type = kwargs.get('trans_type', 'lazy')
        self.OPTIONS = {}
        self.set_trans(trans_type=self.trans_type)
        super(GoballOptions, self).__init__(*args, **kwargs)

    def original_output(self, var_s=''):
        return var_s

    def set_trans(self, **kwargs):
        self.trans_type = kwargs.get('trans_type', self.trans_type)
        if self.trans_type == 'lazy':
            self.trans = ugettext_lazy
        elif self.trans_type == 'original':
            self.trans = self.original_output
        elif self.trans_type == 'immediate':
            self.trans = ugettext
        else:
            self.trans = self.original_output

        self.set_options()

    def set_option(self, var_name, val):
        setattr(self, var_name, val)
        self.OPTIONS[var_name] = val

    def set_options(self):
        self.set_option('INT_CHOICES',
                        (
                            (0, self.trans('True')),
                            (1, self.trans('False')),
                        )
                        )

        self.set_option('STATUS_CHOICES',
                        (
                            (0, self.trans('Valid')),
                            (1, self.trans('Spare')),
                            (2, self.trans('Invalid')),
                        )
                        )

        self.set_option('BOOLEAN_CHOICES',
                        (
                            ('true', self.trans('true')),
                            ('false', self.trans('false')),
                        )
                        )
        self.set_option('TBOOLEAN_CHOICES',
                        (
                            (True, self.trans('true')),
                            (False, self.trans('false')),
                        )
                        )

        self.set_option('TF_CHOICES',
                        (
                            (True, self.trans('True')),
                            (False, self.trans('False')),
                        )
                        )

    def trans_tuple_to_dict(self, v_tuple):
        n_dict = {}
        for vv in v_tuple:
            n_dict[vv[1]] = vv[0]
        return n_dict

    def reverse_dict(self, dict={}):
        n_dict = {}
        for key in dict:
            n_dict[dict[key]] = key
        return n_dict

    def get_option(self, var_name=None):
        return getattr(self, var_name)

    def get_dict_option(self, var_name=None):
        var = getattr(self, var_name)
        return self.trans_tuple_to_dict(var)

    def get_reverse_dict_option(self, var_name=None):
        c_dict = self.get_dict_option(var_name)
        n_dict = self.reverse_dict(c_dict)
        return n_dict


def declare_goball_options(trans_type='lazy'):
    GB_OP = GoballOptions(trans_type=trans_type)
    for option in GB_OP.OPTIONS:
        exec('global  %s' % option)
        exec('%s = GB_OP.get_option("%s")' % (option, option))


# 声明变量
declare_goball_options()

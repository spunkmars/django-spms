# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
spunkmars（spunkmars#gmail.com) http://github.com/spunkmars  http://www.spunkmars.com

"""

import os
import sys
import re
import datetime

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
from pyecharts.globals import NotebookType
from pyecharts.globals import CurrentConfig

is_in_docker = False

if 'DOCKER_CONTAINER' in os.environ:
    if os.environ['DOCKER_CONTAINER'] == "1":
        is_in_docker = True

from ..options import GoballOptions, get_common_conf, get_db_conf, get_cas_conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(BASE_DIR)
sys.path.append(BASE_DIR)
APPXS_DIR = os.path.join(BASE_DIR, 'appxs')  # app目录
sys.path.insert(0, APPXS_DIR)
# sys.path.append(APPS_DIR)

STATIC_DIR = os.path.join(BASE_DIR, 'static')  # 静态文件存储目录
COMMON_STATIC_DIR = os.path.join(STATIC_DIR, 'common')
COMMON_FONTS_DIR = os.path.join(COMMON_STATIC_DIR, 'fonts')
COMMON_IMG_DIR = os.path.join(COMMON_STATIC_DIR, 'img')
COMMON_CSS_DIR = os.path.join(COMMON_STATIC_DIR, 'css')
COMMON_JS_DIR = os.path.join(COMMON_STATIC_DIR, 'js')

DATA_DIR = os.path.join(BASE_DIR, 'data')  # 数据目录
CONF_DIR = os.path.join(DATA_DIR, 'conf')  # 配置文件目录
ASSET_DIR = os.path.join(DATA_DIR, 'asset')  # 应用产生的数据（可对外提供）
COMMON_LOCALE_DIR = os.path.join(DATA_DIR, 'locale')  # 存放公共的翻译文件目录

SQLITE_DB_PATH = os.path.join(DATA_DIR, 'db')  # sqlite 文件存储路径
RUNTIME_DIR = os.path.join(BASE_DIR, 'runtime')  # 应用运行产生的临时数据
LOG_DIR = os.path.join(RUNTIME_DIR, 'log')  # 应用运行时产生的日志目录
TEMP_DIR = os.path.join(RUNTIME_DIR, 'tmp')  # 应用运行时使用的临时目录
PID_DIR = os.path.join(RUNTIME_DIR, 'pid')  # 应用运行时产生的pid记录文件储存路径
GLOBAL_TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')  # 全局模板目录

# print 'BASE_DIR: %s，APPXS_DIR:%s,  SQLITE_PATH: %s' % (BASE_DIR, APPXS_DIR, SQLITE_DB_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/


common_i = get_common_conf(config_file=os.path.join(CONF_DIR, 'common.ini'))
site_i = common_i['common']
SITE_NAME = site_i['site_name']
SITE_DESC = site_i['site_desc']
SITE_VERSION = site_i['site_version']
SITE_COPYRIGHT_YEAR = site_i['site_copyright_year']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', site_i['secret_key'])

DEBUG = site_i['debug'] if "True" in os.environ.get("DEBUG_MODE", "False") else False

ALLOWED_HOSTS = []

# Custom Var definition
GB_OP = GoballOptions(trans_type='lazy')
for option in GB_OP.OPTIONS:
    exec('%s = GB_OP.get_option("%s")' % (option, option))

# Application definition

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_PANELS += ['django_uwsgi.panels.UwsgiPanel', ]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,  # 关闭debug_toolbar 截取 302跳转
}

DJANGO_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'guardian',
    'corsheaders',
    'mama_cas',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_docs',
    'django_celery_results',
    'django_celery_beat',
    'drf_yasg',
    'django_filters',
    'django_uwsgi',
    'debug_toolbar',
    'spcc',
    'ckeditor',
    'ckeditor_uploader',
    'mdeditor',
]

LOCAL_APPS = [
    'appxs.commonx.apps.CommonxConfig',
    'appxs.account.apps.AccountConfig',
    'appxs.quickstart.apps.QuickStartConfig',
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'appxs.account.middleware.permission.MenuCollection',
    'appxs.api.libs.middleware.ValidJwtTokenMiddleware',
    'appxs.account.middleware.permission.RbacMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [GLOBAL_TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'appxs.commonx.views.site.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

db_i = get_db_conf(os.path.join(CONF_DIR, 'db.ini'))

if db_i['common']['db_type'] == 'mysql':
    if is_in_docker and 'MYSQL_HOST' in os.environ:
        mysql_host = os.environ['MYSQL_HOST']
    else:
        mysql_host = db_i['mysql']['host']

    if is_in_docker and 'MYSQL_PORT' in os.environ:
        mysql_port = os.environ['MYSQL_PORT']
    else:
        mysql_port = db_i['mysql']['port']

    if is_in_docker and 'MYSQL_DATABASE' in os.environ:
        mysql_db = os.environ['MYSQL_DATABASE']
    else:
        mysql_db = db_i['mysql']['db']

    if is_in_docker and 'MYSQL_USER' in os.environ:
        mysql_user = os.environ['MYSQL_USER']
    else:
        mysql_user = db_i['mysql']['user']

    if is_in_docker and 'MYSQL_PASSWORD' in os.environ:
        mysql_passwd = os.environ['MYSQL_PASSWORD']
    else:
        mysql_passwd = db_i['mysql']['passwd']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': mysql_db,
            'USER': mysql_user,
            'PASSWORD': mysql_passwd,
            'HOST': mysql_host,
            'PORT': mysql_port,
            'default-character-set': 'utf8',
            'OPTION': {'init_command': 'SET storage_engine=INNODB;'},
            'OPTIONS': {'charset': 'utf8'},
        }
    }

elif db_i['common']['db_type'] == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(SQLITE_DB_PATH, db_i['sqlite']['db_name']),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = site_i['language_code']

TIME_ZONE = site_i['time_zone']

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

LOCALE_PATHS = [COMMON_LOCALE_DIR, ]
MEDIA_ROOT = ASSET_DIR  # 用户上传数据目录
MEDIA_URL = '/asset/'  # 用户数据uri

STATIC_ROOT = 'resource/static'
STATIC_URL = '/static/'
STATICFILES_DIRS = ('static',)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# print('STATIC_ROOT=%s' % STATIC_ROOT)
# STATICFILES_DIRS = []


# STATIC_URL = '/static/'
# STATICFILES_DIRS = ('static/',)


# LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DATA_UPLOAD_MAX_MEMORY_SIZE = 262144000  # 250Mb
FILE_UPLOAD_MAX_MEMORY_SIZE = 262144000  # 250Mb

LANGUAGES = (('en-us', u'English'), ('zh-cn', u'简体中文'), ('zh-tw', u'繁體中文'))

# ck编辑器配置
CKEDITOR_UPLOAD_PATH = 'ck_upload/'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

CKEDITOR_RESTRICT_BY_DATE = True  # ck上传文件按日期目录(yy/mm/dd)存储

# ck 编辑器默认配置
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width': 'auto',
        'height': '250px',
        # tab键转换空格数
        'tabSpaces': 4,
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_Full': [
            # ['Source', '-', 'Save', 'NewPage', 'DocProps', 'Preview', 'Print', '-', 'Templates'],
            ['Source', '-', 'DocProps', 'Preview', 'Print', '-', 'Templates'],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'],

            ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker', 'Scayt'],
            ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
            '/',
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],
            ['CodeSnippet'],  # 代码段按钮
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'],
            '/',
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', '-', 'About'],

        ],
        'toolbar': 'Full',
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet']),
    }
}

# mdeditor markdown编辑器配置
MDEDITOR_CONFIGS = {
    'default': {
        'width': '90%',  # 自定义编辑框宽度
        'heigth': 500,  # 自定义编辑框高度
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型
        'image_floder': 'editor',  # 图片保存文件夹名称
        'theme': 'default',  # 编辑框主题 ，dark / default
        'preview_theme': 'default',  # 预览区域主题， dark / default
        'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default
        'toolbar_autofixed': True,  # 工具栏是否吸顶
        'search_replace': True,  # 是否开启查找替换
        'emoji': True,  # 是否开启表情功能
        'tex': True,  # 是否开启 tex 图表功能
        'flow_chart': True,  # 是否开启流程图功能
        'sequence': True  # 是否开启序列图功能
    },

    'form_config': {
        'width': '70%',  # 自定义编辑框宽度
        'heigth': 500,  # 自定义编辑框高度
        'toolbar': ["undo", "redo", "|", "link", "reference-link", "image", "code", "preformatted-text", "code-block",
                    "table",
                    "emoji", "|",
                    "help", "info", "preview", "watch", "fullscreen"],  # 自定义编辑框工具栏
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # 图片上传格式类型
        'image_floder': 'editor',  # 图片保存文件夹名称
        'theme': 'dark',  # 编辑框主题 ，dark / default
        'preview_theme': 'default',  # 预览区域主题， dark / default
        'editor_theme': 'default',  # edit区域主题，pastel-on-dark / default
        'toolbar_autofixed': True,  # 工具栏是否吸顶
        'search_replace': True,  # 是否开启查找替换
        'emoji': True,  # 是否开启表情功能
        'tex': True,  # 是否开启 tex 图表功能
        'flow_chart': True,  # 是否开启流程图功能
        'sequence': True  # 是否开启序列图功能
    },

}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s : %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(module)s %(process)d %(thread)d : %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': os.path.join(LOG_DIR, 'sys.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'appxs.api.libs.common.CustomPagination',
    'PAGE_SIZE': int(os.getenv('DJANGO_PAGINATION_LIMIT', 10)),
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'appxs.api.libs.permission.CustomBasePermissions',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

}

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY_EXPIRATION': True,
    # 'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=20),
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(minutes=5),
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'appxs.api.libs.permission.jwt_response_payload_handler',
}

cas_i = get_cas_conf(config_file=os.path.join(CONF_DIR, 'cas.ini'))
# 允许退出登录，可选项
MAMA_CAS_ENABLE_SINGLE_SIGN_OUT = cas_i['common']['mama_cas_enable_single_sign_out']

# 重要！，service是client的IP，是个数组，可以在后面添加SERVICE的HOST:PORT。
MAMA_CAS_SERVICES = []

if 'common' in cas_i:
    del cas_i['common']
for cik in cas_i:
    MAMA_CAS_SERVICES.append({
        'SERVICE': cas_i[cik]['service'],
        'CALLBACKS': cas_i[cik]['callbacks'],
        'LOGOUT_ALLOW': cas_i[cik]['logout_allow'],
        'LOGOUT_URL': cas_i[cik]['logout_url'],
    })

cors_i = common_i['cors']
CORS_ALLOW_CREDENTIALS = cors_i['cors_allow_credentials']
CORS_ORIGIN_ALLOW_ALL = cors_i['cors_origin_allow_all']
CORS_ORIGIN_WHITELIST = cors_i['cors_origin_whitelist']

CELERY_APPLICATION_PATH = 'config.celery.app'

AVATAR_PRE_DIR = 'img/account/avatar'

AUTH_USER_MODEL = 'account.UserProfile'

PERMISSION_MENU_KEY = "ppppppooooo"
PERMISSION_URL_DICT_KEY = "99988yyttt"
PERMISSION_MENU_LIST = "hello"
# RBAC_LOGIN_URL='/accounts/user/login_rbac/'
RBAC_LOGIN_URL = '/accounts/user/login/'


class UrlFormatCls(object):
    @classmethod
    def format(cls, url):
        return re.compile(url)


URL_FORMAT = UrlFormatCls

SAFE_URL = [
    # r'*', #开放所有访问权限
    r'^/$',
    r'^/index/',
    r'^/accounts/user/login/',
    r'^/accounts/user/logout/',
    # r'^/accounts/login/*',
    # r'^/accounts/logout/*',
    r'^/api/*',  # 放行api，drf使用自身的jwt登录，以及自定义的验证模块
    r'/api/jwt/*',  # api 的jwt验证接口
    r'/api/auth/login/*',  # api 的普通验证接口
    r'/api/auth/logout/*',  # api 的普通验证接口
    r'/cas/*',  # cas 验证接口
    # r'^/accounts/user/signup/',  # 开放注册
    r'^/commonx/get_check_code_image/',  # 验证码
    r'^/commonx/get_uuid/',  # 获取UUID
    r'^/commonx/language/list/',  # 语言列表
    # r'^/commonx/convert_view_name_to_url/', # 转换view_name 为实际的url
    r'^/media/',  # 媒体文件访问
    r'^/asset/',  # 上传文件访问
    r'^/admin/uwsgi/*',  # django_uwsgi
    # r'^/admin/', # 后台管理
    r'^/health/',  # 应用健康检查
    r'^/__debug__/*',  # debug_toolbar
    # r'^/quickstart/*',

]

# pyecharts配置
s_reg = re.compile('/$')
N_STATIC_URL = s_reg.sub('', STATIC_URL)  # 去除结尾的 '/'

custom_jinja2_env = Environment(
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(
        os.path.join(
            GLOBAL_TEMPLATES_DIR, "pyecharts"
        )
    ),
)


class CustomCurrentConfig:
    PAGE_TITLE = "Awesome-pyecharts"
    # ONLINE_HOST = "https://assets.pyecharts.org/assets/"
    ONLINE_HOST = "%s/pyecharts/" % N_STATIC_URL
    NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK
    GLOBAL_ENV = custom_jinja2_env


ccc = CustomCurrentConfig()
CurrentConfig.ONLINE_HOST = ccc.ONLINE_HOST
CurrentConfig.GLOBAL_ENV = ccc.GLOBAL_ENV

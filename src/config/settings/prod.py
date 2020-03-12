# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_AGE = 60 * 60 * 24  # 24小时
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

if is_in_docker and 'REDIS_HOST' in os.environ:
    REDIS_HOST = os.environ['REDIS_HOST']
else:
    REDIS_HOST = "localhost"

if is_in_docker and 'REDIS_PORT' in os.environ:
    REDIS_PORT = os.environ['REDIS_PORT']
else:
    REDIS_PORT = 6379

BROKER_BACKEND = "redis"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True
CELERY_TRACK_STARTED = True
# CELERY_TASK_RESULT_EXPIRES = 10
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
# CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
BROKER_URL = 'redis://%s:%s' % (REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://%s:%s' % (REDIS_HOST, REDIS_PORT)
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

# CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_IGNORE_RESULT = True
# CELERYD_MAX_TASKS_PER_CHILD = 50  # worker的某个进程如果累计执行了50个任务后就会被重启，以防某些内存泄漏问题。
# CELERYD_POOL_RESTARTS = True  # 重启pool里的进程，使得worker加载最新代码。


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # email后端

if is_in_docker and 'EMAIL_USE_TLS' in os.environ:
    if os.environ['EMAIL_USE_TLS'].lower() == 'false':
        EMAIL_USE_TLS = False
    else:
        EMAIL_USE_TLS = True
else:
    EMAIL_USE_TLS = False  # 是否使用TLS安全传输协议

if is_in_docker and 'EMAIL_USE_SSL' in os.environ:
    if os.environ['EMAIL_USE_SSL'].lower() == 'false':
        EMAIL_USE_SSL = False
    else:
        EMAIL_USE_SSL = True
else:
    EMAIL_USE_SSL = True  # 是否使用SSL加密，qq企业邮箱要求使用

if is_in_docker and 'EMAIL_HOST' in os.environ:
    EMAIL_HOST = os.environ['EMAIL_HOST']
else:
    EMAIL_HOST = 'smtp.exmail.qq.com'  # 发送邮件的邮箱 的 SMTP服务器，这里用了qq企业邮箱

if is_in_docker and 'EMAIL_PORT' in os.environ:
    EMAIL_PORT = int(os.environ['EMAIL_PORT'])
else:
    EMAIL_PORT = 465

if is_in_docker and 'EMAIL_HOST_USER' in os.environ:
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
else:
    EMAIL_HOST_USER = 'alert@spunkmars.com'  # 发送邮件的邮箱地址

if is_in_docker and 'EMAIL_HOST_PASSWORD' in os.environ:
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
else:
    EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxx'  # 发送邮件的邮箱密码

if is_in_docker and 'DEFAULT_FROM_EMAIL' in os.environ:
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
else:
    DEFAULT_FROM_EMAIL = '%s <alert@spunkmars.com>' % common_i['common']['site_name'].upper()

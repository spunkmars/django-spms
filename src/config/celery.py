# coding=utf-8

from __future__ import absolute_import
import os
import time
from datetime import timedelta

from celery import Celery, shared_task, Task
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from django.apps import apps
from django.conf import settings

from spmo.common import Common

co = Common()
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

site = getattr(settings, 'SITE_NAME').lower()
TEMP_DIR = getattr(settings, 'TEMP_DIR')
app = Celery(site, ignore_result=False)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.control.broadcast('pool_restart', arguments={'reload': True})

app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'


class BaseTask(Task):
    # queue = 'router'

    def __init__(self, *args, **kwargs):
        self.logger = get_task_logger(__name__)
        super(BaseTask, self).__init__(*args, **kwargs)

    def log_info(self, msg=None):
        self.logger.info('%s' % msg)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


class DebugTask(BaseTask):
    '''
    用于debug都task基类
    '''

    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)


# app.Task = BaseTask #设定默认的任务都继承于BaseTask


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def debug_add(self, x, y):
    z = 0
    z = x + y
    print('%s + %s = %s' % (x, y, z))
    return z


@app.task(bind=True)
def progress_test(self, a, b):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    return 'hello world: %i' % (a + b)


@shared_task
def wfile_test(vstr):
    w_file = os.path.join(TEMP_DIR, "output.txt")
    with open(w_file, "a") as f:
        f.write("hello world: %s --> %s" % (co.get_create_date(), vstr))
        f.write("\n")


@shared_task
def print_test(vstr):
    print(vstr)
    return vstr


@shared_task
def longtime_task_test():
    for i in range(1, 1000):
        print('longtime_task: %d ...' % i)
        time.sleep(1)

# 设置定时任务、间隔任务。 如果启用django-celery-beat 请使用django-celery-beat接口添加定时任务
#
# app.conf.update(
#     beat_schedule={
#         "progress_test": {
#             "task": "config.celery.progress_test",
#             "schedule": crontab(minute=0, hour=7),
#             "args": (1, 2)
#         },
#
#         "wfile_test": {
#             "task": "config.celery.wfile_test",
#             "schedule": timedelta(seconds=3),
#             "args": ('vvvvvvvH',)
#         },
#         "print_test": {
#             "task": "config.celery.print_test",
#             "schedule": timedelta(seconds=3),
#             "args": ('uuuuuuu',)
#         },
#     }
# )

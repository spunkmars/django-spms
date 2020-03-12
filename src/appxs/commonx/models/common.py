# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class BaseModel(models.Model):
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from appxs.account.models.user import UserProfile, Structure, Menu, Role

admin.site.register(Structure)
admin.site.register(UserProfile)
admin.site.register(Menu)
admin.site.register(Role)

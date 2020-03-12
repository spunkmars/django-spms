# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
from rest_framework import routers
# from appxs.api.base.router import CustomReadOnlyRouter

from .views.account import UserViewSet, GroupViewSet

router = routers.DefaultRouter()
# router = CustomReadOnlyRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

api_urlpatterns = router.urls

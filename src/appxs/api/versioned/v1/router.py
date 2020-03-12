# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers
from appxs.api.versioned.v1.views.account import user

router = routers.DefaultRouter()
# router = CustomReadOnlyRouter()
router.register(r'userx', user.UserListView)

api_urlpatterns = router.urls

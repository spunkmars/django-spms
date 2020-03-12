from spmo.common import Common

from django.conf.urls import url, include
from rest_framework import routers
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import routers

from appxs.api.base.router import reg_api_uri

router = routers.DefaultRouter()
api_router = router

api_version = ''
api_app = 'spms'
api_uri_prefix = api_app

urlpatterns = [

]
api_v1 = api_router.urls

api_v1 = api_v1 + urlpatterns

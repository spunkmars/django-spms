from spmo.common import Common

from django.conf.urls import url, include
from rest_framework import routers
from django.http import HttpResponseRedirect
from django.urls import reverse as reverse2
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse

from appxs.api.versioned.v1.urls import api_v1

app_name = 'api'

urlpatterns = [
    url(r'^v1/', include((api_v1, app_name), namespace='v1', ), ),  # 版本v1
]


class ApiGlobalRootView(APIView):
    # APIView中 key为requet.method 小写. (get/post/put/delete/patch)
    extra_perms = {
        'get': ['api', ],
    }

    def get(self, request, format=None, *args, **kwargs):
        '''
        API Global Root.
        所有API的总入口
        '''
        return Response({
            'v1': '%s://%s%s' % (
                request.META['wsgi.url_scheme'], request.META['HTTP_HOST'], reverse2('api:v1:api-root')),
        })


urlpatterns.insert(0, url(r'^$', ApiGlobalRootView.as_view(), name='api_global_root'), )

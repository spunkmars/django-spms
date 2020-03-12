# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import routers
# from rest_framework.routers import Route, DynamicDetailRoute, SimpleRouter
#
#
# class CustomReadOnlyRouter(SimpleRouter):
#     '''
#     A router for read-only API
#     '''
#
#     routes = [
#         Route(
#             url=r'^{prefix}$',
#             mapping={'get': 'list'},
#             name='{basename}-list',
#             initkwargs={'suffix': 'List'}
#         ),
#         Route(
#             url=r'^{prefix}/{lookup}$',
#             mapping={'get': 'retrieve'},
#             name='{basename}-detail',
#             initkwargs={'suffix': 'Detail'}
#         ),
#         DynamicDetailRoute(
#             url=r'^{prefix}/{lookup}/{methodnamehyphen}$',
#             name='{basename}-{methodnamehyphen}',
#             initkwargs={}
#         )
#     ]


from appxs.api.base import views

# router = routers.DefaultRouter()
# router = CustomReadOnlyRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# api_router = router


def reg_api_uri(a_router, uri_prefix, basename, viewset):
    a_router.register(r'%s/%s' % (uri_prefix, basename), viewset, basename=basename)

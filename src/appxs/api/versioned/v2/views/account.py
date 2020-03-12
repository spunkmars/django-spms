# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from appxs.api.base.views import *
# from appxs.api.base import views as base_views
# from . import serializers as v2_serializers
#
#
# class UserViewSet(base_views.UserViewSet):
#     serializer_class = v2_serializers.UserSerializer


from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

from ..serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited..
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

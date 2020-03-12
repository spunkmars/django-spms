# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group

from django.contrib.auth import get_user_model

User = get_user_model()
from rest_framework import viewsets

from appxs.api.base.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited..
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer

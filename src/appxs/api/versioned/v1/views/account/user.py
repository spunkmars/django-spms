# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

User = get_user_model()
from django.contrib.auth.models import Group
from appxs.api.base.serializers import UserSerializer, GroupSerializer

from rest_framework import filters
from rest_framework import generics


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    # search_fields = ('username', 'email')
    search_fields = ('id', 'username', 'email', 'groups__name')
    ordering_fields = ('id', 'username', 'email')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from appxs.api.base import serializers as base_serializers
# from appxs.api.base.serializers import *
#
#
# class UserSerializer(base_serializers.UserSerializer):
#     full_name = serializers.SerializerMethodField()
#
#     class Meta(base_serializers.UserSerializer.Meta):
#         fields = ('url', 'id', 'email', 'full_name')
#
#     def get_full_name(self, obj):
#         return '{0} {1}'.format(obj.first_name, obj.last_name)


from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)
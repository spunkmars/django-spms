# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from django.conf import settings

AVATAR_PRE_DIR = getattr(settings, 'AVATAR_PRE_DIR')


class Menu(models.Model):
    """
    菜单/页面
    """
    type_choices = (("menu", "菜单"), ("page", "页面"), ("button", "按钮"), ("only_permission", "仅仅是权限"))
    url_target_choices = (("_blank", "新窗口"), ("_self", "当前窗口"), ("_parent", "父窗口"), ("_top", "整个窗口"))
    name = models.CharField(max_length=128, unique=True, verbose_name="菜单名", null=True,
                            blank=True, )
    type = models.CharField(max_length=20, choices=type_choices, default="menu", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")
    icon = models.CharField(max_length=128, null=True, blank=True, verbose_name="图标")
    code = models.CharField(max_length=128, null=True, blank=True, verbose_name="编码")
    url = models.CharField(max_length=128, null=True, blank=True)
    url_target = models.CharField(max_length=20, choices=url_target_choices, default="_self", verbose_name="URL打开方式")
    order = models.FloatField(max_length=50, null=True, blank=True, default=0.00, verbose_name="菜单排序")
    seq = models.FloatField(max_length=50, null=True, blank=True, default=0.00, verbose_name="排序")
    view_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="菜单显示的名称")
    level = models.IntegerField(null=True, blank=True, verbose_name="菜单层级")
    desc = models.CharField(max_length=255, blank=True, null=True, verbose_name="菜单描述")
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name="页面标题")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['-level', 'order']

    @classmethod
    def get_all_p_url(cls):
        try:
            return dict(menu=Menu.objects.all())
        except:
            None

    @classmethod
    def get_sub_ids(cls, pid=None):
        try:
            return Menu.filter(parent=pid).values_list('id', flat=True)
        except:
            None

    @classmethod
    def get_menu(cls):
        try:
            return dict(menu=Menu.objects.get(type='menu'))
        except:
            None

    def __str__(self):
        return '%s[%s]' % (self.view_name, self.type)

    def __unicode__(self):
        return '%s[%s]' % (self.view_name, self.type)

    def search_name(self):
        return '%s:  %s # %s' % (self.__class__.__name__, self.name, self.type)

    # 为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        return reverse('account:permission:edit_resource', args=[self.id])

    def delete(self, *args, **kwargs):
        super(self.__class__, self).delete(*args, **kwargs)


class Role(models.Model):
    """
    角色：用于权限绑定
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="名称")
    permissions = models.ManyToManyField("menu", blank=True, verbose_name="授权")
    comment = models.CharField(max_length=120, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def search_name(self):
        return '%s:  %s ' % (self.__class__.__name__, self.name)

    # 为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        return reverse('account:role:edit', args=[self.id])

    def delete(self, *args, **kwargs):
        super(self.__class__, self).delete(*args, **kwargs)


class Structure(models.Model):
    """
    组织架构
    """
    type_choices = (("company", "公司"), ("department", "部门"))
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类架构")
    comment = models.CharField(max_length=120, blank=True, null=True, verbose_name="备注")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.parent:
            return '%s-%s' % (self.parent, self.name)
        else:
            return self.name

    def __unicode__(self):
        if self.parent:
            return '%s-%s' % (self.parent, self.name)
        else:
            return self.name

    def search_name(self):
        return '%s:  %s ' % (self.__class__.__name__, self.name)

    # # 为了在模板标签中可以使用items方法
    # def items(self):
    #     return [(field, field.value_to_string(self)) for field in self.__class__._meta.fields]
    # def items(self):
    #     r_data = []
    #     for field in self.__class__._meta.fields:
    #         if hasattr(field, 'choices') and len(field.choices) > 0:
    #             f_value = getattr(self, 'get_%s_display' % field.name)()
    #         else:
    #             f_value = field.value_to_string(self)
    #         r_data.append((field, f_value))
    #     return r_data

    def get_absolute_url(self):
        return reverse('account:structure:edit', args=[self.id])

    def delete(self, *args, **kwargs):
        super(self.__class__, self).delete(*args, **kwargs)


def upload_to(instance, fielname):
    return os.path.join(AVATAR_PRE_DIR, str(instance.id))


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生日期")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")),
                              default="male", verbose_name="性别")
    mobile = models.CharField(max_length=15, null=True, blank=True, verbose_name="手机号码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    image = models.ImageField(upload_to=upload_to, default=os.path.join(AVATAR_PRE_DIR, 'default.jpg'),
                              max_length=100, null=True, blank=True)
    department = models.ForeignKey("Structure", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="部门")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="职位")
    superior = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级主管")
    roles = models.ManyToManyField("Role", verbose_name="角色", blank=True)

    # create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        if self.name and self.department:
            return '%s-%s<%s>' % (self.department, self.name, self.username)
        else:
            return self.username

    def __unicode__(self):
        if self.name and self.department:
            return '%s-%s<%s>' % (self.department, self.name, self.username)
        else:
            return self.username

    def search_name(self):
        return '%s:  %s # %s' % (self.__class__.__name__, self.name, self.department)

    # 为了在模板标签中可以使用items方法
    def items(self):
        return [(field, field.value_to_string(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        return reverse('account:manage_user:edit', args=[self.id])

    def delete(self, *args, **kwargs):
        super(self.__class__, self).delete(*args, **kwargs)

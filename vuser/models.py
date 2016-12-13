#!encoding: utf8
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class User(models.Model):
    user_sex = (
        (0, '男'),
        (1, '女'),
        (2, '保密'),
    )
    username = models.CharField(max_length=100, default='', verbose_name='用户名', null=True, blank=True)
    userid = models.CharField(max_length=128, verbose_name='用户唯一ID', unique=True)
    sex = models.IntegerField(choices=user_sex, default=2, verbose_name='性别')
    nickname = models.CharField(max_length=50, verbose_name='用户昵称', null=True, blank=True)
    birthday = models.DateField(default='', verbose_name='生日', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='邮箱')
    password = models.CharField(max_length=50, verbose_name='密码')

    def __unicode__(self):
        return self.nickname
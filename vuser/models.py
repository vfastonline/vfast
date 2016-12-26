#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from vcourse.models import *

# Create your models here.
class User(models.Model):
    statuses = (
        (0, '已激活'),
        (1, '未激活'),
    )
    rolestatus = (
        (0, 'SP'),
        (1, 'NO'),
    )
    username = models.CharField('用户名', max_length=20, null=True, blank=True, default='')
    email = models.EmailField('邮箱', unique=True)
    password = models.CharField('密码', max_length=20)
    token = models.CharField('账号激活码', max_length=50, unique=False)
    status = models.SmallIntegerField('激活状态', choices=statuses, default=1)
    regtime = models.IntegerField('注册时间')
    uuid = models.CharField('UUID', max_length=50)
    role = models.IntegerField('用户角色', choices=rolestatus, default=1)
    sumtime = models.IntegerField('学习总时间', default=0)
    sumscore = models.IntegerField('学习总得分', default=0)

    def __unicode__(self):
        return self.email

    class Meta:
        db_table = 'user'

#!encoding:utf-8
from __future__ import unicode_literals
from django.db import models
from vcourse.models import Section, SectionType, Course
# Create your models here.

class User(models.Model):

    statuses = (
        (0, '已激活'),
        (1, '未激活'),
    )
    rolestatus = (
        (0, 'Super'),
        (1, 'Normal'),
    )
    level = (
        (1, '初级'),
        (2, '中级'),
        (3, '高级'),
    )
    username = models.CharField('用户名', max_length=20, null=True, blank=True, default='')
    fullname = models.CharField('真实姓名', max_length=20, default='', null=True, blank=True)
    email = models.EmailField('邮箱', unique=True)
    password = models.CharField('密码', max_length=64)
    token = models.CharField('账号激活码', max_length=50, unique=False)
    status = models.SmallIntegerField('激活状态', choices=statuses, default=1)
    regtime = models.IntegerField('注册时间')
    uuid = models.CharField('UUID', max_length=50)
    role = models.IntegerField('用户角色', choices=rolestatus, default=1)
    sumtime = models.IntegerField('学习总时间', default=0)
    sumscore = models.IntegerField('学习总得分', default=0)
    headimg = models.ImageField('个人头像', upload_to='headimg/%Y/%m', null=True, blank=True)
    address = models.CharField('当前位置', default='城市', max_length=20)
    birthday = models.DateField('生日', null=True, blank=True)
    resume = models.FileField('简历', upload_to='resume/%Y/%m', null=True, blank=True)
    description = models.TextField('个人描述', null=True, blank=True)
    exceptlevel = models.IntegerField('期望工作级别', choices=level, default=3)
    exceptjob = models.CharField('期望工作', max_length=100, null=True, blank=True)
    company = models.CharField('现在所在的公司', max_length=30, null=True, default=' ', blank=True)
    companylocal = models.CharField('所在公司地址', max_length=50, null=True, default=' ', blank=True)
    stackoverflow = models.IntegerField('是否激活stackoverflow', choices=statuses, default=1)
    linkin = models.IntegerField('是否关联linkin', choices=statuses, default=1)
    homepage = models.CharField('个人主页', max_length=100, default=' ', null=True, blank=True)
    github = models.IntegerField('是否激活github', choices=statuses, default=1)

    def __unicode__(self):
        return self.email


class UserCourse(models.Model):
    course_status = (
        (0, '未观看'),
        (1, '未看完'),
        (2, '已看完'),
    )
    userid = models.ForeignKey(User, verbose_name='用户ID')
    courseid = models.ForeignKey(Course, verbose_name='课时ID')
    sectionid = models.ForeignKey(Section, verbose_name='课程ID')
    status = models.SmallIntegerField('是否看完视频', choices=course_status)
    coursetime = models.IntegerField('观看视频的位置')

    def __unicode__(self):
        return  '%s  %s'  % (self.userid.username, self.courseid.coursename)


class Medal(models.Model):
    name = models.CharField('勋章名称', max_length=20)
    imgurl = models.CharField('勋章图片位置', max_length=50, null=True, default='img/a.gif')

    def __unicode__(self):
        return self.name


class Points(models.Model):
    userid = models.ForeignKey(User)
    timeday = models.DateField('获得积分时间,天')
    point = models.IntegerField('获得分数')

    def __unicode__(self):
        return self.timeday
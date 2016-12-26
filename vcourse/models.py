#!encoding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class  SectionType(models.Model):
    color = models.CharField('颜色', db_column='color', max_length=10)
    sectiontype = models.CharField('课程类型', db_column='sectiontype', max_length=50)

    def __unicode__(self):
        return self.sectiontype


class Section(models.Model):
    pub = (
        (0, '已发布'),
        (1, '未发布'),
        (2, '即将发布')
    )
    name = models.CharField(verbose_name='课程标题', max_length=50, default=' ')
    stypeid = models.ForeignKey(SectionType, db_column='stypeid', verbose_name='课程类型')
    tag = models.TextField(verbose_name='课程tag,供检索', db_column='tag')
    sumtime = models.CharField(verbose_name='课程总时间', db_column='sumtime', max_length=10)
    description = models.TextField(verbose_name='课程描述', db_column='description')
    pubstype = models.IntegerField('发布状态', choices=pub, default=1)

    def __unicode__(self):
        return self.name


class Course(models.Model):
    coursename = models.CharField(db_column='coursename', max_length=150, verbose_name='课时名称')
    uptime = models.DateField(db_column='uptime', verbose_name='视频上传时间')
    videolocal = models.FileField(db_column='videolocal', verbose_name='视频上传位置', upload_to='./video')
    courseware = models.FileField(db_column='courseware', verbose_name='课件上传位置', upload_to='./courseware')
    sectionid = models.ForeignKey(Section)
    lengtime = models.DecimalField(db_column='lengtime', verbose_name='视频时长', max_digits=4, decimal_places=2,)  #12:12
    description = models.TextField(verbose_name='课时简介', db_column='description')


    def __unicode__(self):
        return self.coursename


class Path(models.Model):
    name = models.CharField(max_length=20, db_column='name', verbose_name='职业路径名称')
    description = models.TextField(verbose_name='职业路径简介', db_column='description')
    sections = models.ManyToManyField(Section, verbose_name='职业路径包含的课程')

    def __unicode__(self):
        return self.name

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 03:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vuser', '0010_auto_20161226_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='\u57ce\u5e02', max_length=20, verbose_name='\u5f53\u524d\u4f4d\u7f6e'),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='\u751f\u65e5'),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.CharField(blank=True, default=' ', max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='companylocl',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.TextField(default=' ', verbose_name='\u4e2a\u4eba\u63cf\u8ff0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='exceptjob',
            field=models.CharField(default=' ', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='exceptlevel',
            field=models.IntegerField(choices=[(1, '\u521d\u7ea7'), (2, '\u4e2d\u7ea7'), (3, '\u9ad8\u7ea7')], default=3),
        ),
        migrations.AddField(
            model_name='user',
            name='fullname',
            field=models.CharField(default='', max_length=20, verbose_name='\u771f\u5b9e\u59d3\u540d'),
        ),
        migrations.AddField(
            model_name='user',
            name='headimg',
            field=models.CharField(default=' ', max_length=50, verbose_name='\u4e2a\u4eba\u5934\u50cf'),
        ),
        migrations.AddField(
            model_name='user',
            name='homepage',
            field=models.IntegerField(choices=[(0, '\u5df2\u6fc0\u6d3b'), (1, '\u672a\u6fc0\u6d3b')], default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='linkin',
            field=models.IntegerField(choices=[(0, '\u5df2\u6fc0\u6d3b'), (1, '\u672a\u6fc0\u6d3b')], default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='resume',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u7b80\u5386'),
        ),
        migrations.AddField(
            model_name='user',
            name='stackoverflow',
            field=models.IntegerField(choices=[(0, '\u5df2\u6fc0\u6d3b'), (1, '\u672a\u6fc0\u6d3b')], default=1),
        ),
    ]

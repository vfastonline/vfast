# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vuser', '0012_auto_20161227_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='\u4e2a\u4eba\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='user',
            name='exceptjob',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u671f\u671b\u5de5\u4f5c'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='\u771f\u5b9e\u59d3\u540d'),
        ),
        migrations.AlterField(
            model_name='user',
            name='headimg',
            field=models.CharField(blank=True, default=' ', max_length=50, null=True, verbose_name='\u4e2a\u4eba\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64, verbose_name='\u5bc6\u7801'),
        ),
    ]

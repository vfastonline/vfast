# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-22 07:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vuser', '0003_auto_20161222_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=50, unique=False, verbose_name='\u8d26\u53f7\u6fc0\u6d3b\u7801'),
        ),
    ]

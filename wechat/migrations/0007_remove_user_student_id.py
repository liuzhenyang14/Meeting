# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-07 13:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0006_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='student_id',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-29 04:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0007_remove_user_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlogin',
            name='confid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wechat.ConfBasic'),
        ),
    ]

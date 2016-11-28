# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-28 14:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('study_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='write_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
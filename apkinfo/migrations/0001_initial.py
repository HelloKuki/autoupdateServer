# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-08 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApkInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=128)),
                ('apk_size', models.CharField(max_length=64)),
                ('icon', models.CharField(max_length=128)),
                ('package_name', models.CharField(max_length=128)),
                ('version_code', models.CharField(max_length=64)),
                ('version_name', models.CharField(max_length=64)),
                ('min_sdk_version', models.CharField(max_length=64)),
                ('target_sdk_version', models.CharField(max_length=64)),
                ('app_key', models.CharField(max_length=128)),
                ('create_time', models.CharField(max_length=128)),
                ('update_time', models.CharField(max_length=128)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-11 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apkinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UpdateRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(max_length=128)),
                ('level', models.IntegerField()),
                ('download_url', models.CharField(max_length=256)),
                ('version_code', models.CharField(max_length=64)),
                ('version_name', models.CharField(max_length=64)),
                ('min_sdk_version', models.CharField(max_length=64)),
                ('target_sdk_version', models.CharField(max_length=64)),
                ('apk_size', models.CharField(max_length=64)),
                ('update_content', models.CharField(max_length=512)),
                ('is_mandatory', models.BooleanField()),
                ('create_time', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='apkinfo',
            name='apk_size',
        ),
        migrations.RemoveField(
            model_name='apkinfo',
            name='min_sdk_version',
        ),
        migrations.RemoveField(
            model_name='apkinfo',
            name='target_sdk_version',
        ),
        migrations.RemoveField(
            model_name='apkinfo',
            name='version_code',
        ),
        migrations.RemoveField(
            model_name='apkinfo',
            name='version_name',
        ),
    ]

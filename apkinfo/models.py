# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class ApkInfo(models.Model):
    _id = models.IntegerField()
    app_name = models.CharField(max_length=128)
    icon = models.CharField(max_length=128)
    package_name = models.CharField(max_length=128)
    app_key = models.CharField(max_length=128)
    create_time = models.CharField(max_length=128)
    update_time = models.CharField(max_length=128)
    progress_notify_type = models.IntegerField()


class UpdateRecord(models.Model):
    app_id = models.CharField(max_length=128)
    level = models.IntegerField()
    app_name = models.CharField(max_length=128)
    package_name = models.CharField(max_length=128)
    download_url = models.CharField(max_length=256)
    version_code = models.CharField(max_length=64)
    version_name = models.CharField(max_length=64)
    min_sdk_version = models.CharField(max_length=64)
    target_sdk_version = models.CharField(max_length=64)
    apk_size = models.CharField(max_length=64)
    update_content = models.CharField(max_length=512)
    update_type = models.IntegerField()
    create_time = models.CharField(max_length=128)

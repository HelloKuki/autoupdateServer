# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class User(models.Model):
    phone = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    nickname = models.CharField(max_length=64)
    age = models.IntegerField()
    token = models.CharField(max_length=256)
    create_time = models.CharField(max_length=128)
    update_time = models.CharField(max_length=128)

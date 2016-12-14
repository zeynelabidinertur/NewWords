from __future__ import unicode_literals

from django.db import models


class MyEntry(models.Model):
    header = models.CharField(max_length=15)
    body = models.CharField(max_length=300)

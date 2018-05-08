from __future__ import unicode_literals

from django.db import models
from tags.models import Tag
from django.contrib.auth.models import User


class MyEntry(models.Model):
    header = models.CharField(max_length=15)
    body = models.CharField(max_length=300)
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, default=None, blank=True, null=True)

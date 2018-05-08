from __future__ import unicode_literals

from django.contrib.auth.models import User
from tags.models import Tag
from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=220)
    description = models.CharField(max_length=400)
    owner = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)

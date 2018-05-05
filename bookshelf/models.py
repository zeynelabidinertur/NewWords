from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Book(models.Model):
    id          = models.CharField(max_length=520)
    name        = models.CharField(max_length=220)
    description = models.CharField(max_length=400)
    size        = models.IntegerField()
    owner       = models.ManyToOneRel()


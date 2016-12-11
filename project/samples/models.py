from __future__ import unicode_literals
from django.db import models
from sysadmin.models import User

class SampleTask(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    sample = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return sample



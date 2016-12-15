from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
from guardian.mixins import GuardianUserMixin

class User(AbstractUser, GuardianUserMixin):
    gender = models.CharField(max_length=1, blank=True)
    mb = models.CharField(max_length=32, blank=True)
    qq = models.CharField(max_length=32, blank=True)
    address = models.CharField(max_length=64, blank=True)
    avatar = models.FileField()

# Operation log table
class Operation(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    logtype = models.IntegerField()
    message = models.CharField(max_length=1024)
    logtime = models.DateTimeField()

    def __unicode__(self):
        return self.message

    def save_log(self):
        self.logtime = timezone.now()
        self.save()

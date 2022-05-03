from django.db import models
from accounts.models import *
from tag.models import *
# Create your models here.

class UserLog(models.Model):
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag          = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    start_time   = models.DateTimeField(auto_now_add=False, null=True)
    end_time     = models.DateTimeField(auto_now_add=False, null=True)
    abnomal_time = models.DateTimeField(auto_now_add=False, null=True)

class TimeLog(models.Model):
    user_log    = models.ForeignKey(User_log, on_delete=models.SET_NULL, null=True)
    occur_time  = models.DateTimeField(auto_now_add=False)
    tag_name    = models.IntegerField()
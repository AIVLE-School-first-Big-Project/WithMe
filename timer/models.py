from django.db import models
from accounts.models import *
from tag.models import *
# Create your models here.

class UserLog(models.Model):
    user         = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag          = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True)
    start_time   = models.DateTimeField(auto_now_add=True, null=True)
    end_time     = models.DateTimeField(auto_now_add=False, null=True)
    abnormal_time= models.IntegerField(default=0)
    textneck_point = models.IntegerField(default=0)

class TimeLog(models.Model):
    user_log    = models.ForeignKey(UserLog, on_delete=models.SET_NULL, null=True)
    time        = models.DateTimeField(auto_now_add=True)
    event_type  = models.IntegerField()

    class Meta:
        ordering = ['-time']
from django.db import models
from accounts.models import *
from tag.models import *
# Create your models here.



class User_log(models.Model):
    user_log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tag_name = models.CharField(max_length=50)
    start_time = models.DateTimeField(auto_now_add=True)
    pause = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    abnomal_time = models.DateTimeField(auto_now_add=False)

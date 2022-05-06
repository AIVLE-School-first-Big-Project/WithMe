# from django.db import models

# # Create your models here.

from django.db import models
from psutil import users
from sqlalchemy import null
# from log_sign.models import User
# Create your models here.

# 게시판 피드 객체
class BulletinFeed(models.Model):
#    id = models.IntegerField(primary_key=True)
    title       = models.CharField(max_length=255,  null=True)
    upload_time = models.DateTimeField( null=True)    
    #txt_path로 바꿀지 확인
    content     = models.TextField(max_length=255,  null=True)    
    img_path    = models.CharField(max_length=255,  null=True)
    # user        = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
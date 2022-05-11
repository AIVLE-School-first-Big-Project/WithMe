from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserType(models.Model):
    Type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.Type_name


class User(AbstractUser):
    User_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, null=True)
    Deleted_at = models.DateTimeField(null=True)

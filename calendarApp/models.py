from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Todolist(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    confirm = models.BooleanField(default=False)
    description = models.CharField(max_length=50)
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    register_date = models.DateTimeField(auto_now=True)

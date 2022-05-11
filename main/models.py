from django.db import models


# Create your models here.
class Intro(models.Model):
    intro_text = models.TextField()

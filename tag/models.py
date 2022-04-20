from django.db import models


class Tag(models.Model):
    Tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.Tag_name}'

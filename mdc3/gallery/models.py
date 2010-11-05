
from django.contrib.auth.models import User
from django.db import models

class Image(models.Model):
    uploader    = models.ForeignKey(User)
    title       = models.CharField(max_length=160)
    description = models.TextField(null=True,blank=True)
    url         = models.URLField()
    image_hash  = models.CharField(max_length=64)
    delete_hash = models.CharField(max_length=64)


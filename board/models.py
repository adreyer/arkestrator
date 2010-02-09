from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

import datetime

class Thread(models.Model):
    subject = models.CharField(max_length=60, blank=False)
    creator = models.ForeignKey(User,null=False,related_name='user')
    
    last_post_by = models.ForeignKey(User,null=False,
        related_name='last_post_by')
    last_post = models.DateTimeField('Last Post',
        default=datetime.datetime.now()) # w00t denormalization
    site = models.ForeignKey(Site, null=False)
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.subject

class Post(models.Model):
    thread = models.ForeignKey(Thread, null=False)
    creator = models.ForeignKey(User,null=False)
    body = models.TextField(blank=False)
    updated_at = models.DateTimeField('Created at',
        default=datetime.datetime.now())

    def __str__(self):
        return "%s: %s"%(str(self.thread),self.body[:20])
    

def update_thread(sender, instance, signal, *args, **kwargs):
    if instance.updated_at > instance.thread.last_post:
        instance.thread.last_post = instance.updated_at
        instance.thread.last_post_by = instance.creator
        instance.thread.save()

post_save.connect(update_thread,sender=Post)


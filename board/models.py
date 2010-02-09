from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

import datetime

class Thread(models.Model):
    title = models.CharField(max_length=60, blank=False)
    last_post = models.DateTimeField('Last Post',
        default=datetime.datetime.now()) # w00t denormalization
    site = models.ForeignKey(Site, null=False)
    on_site = CurrentSiteManager()

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, null=False)
    
    body = models.TextField(blank=False)
    updated_at = models.DateTimeField('Created at',
        default=datetime.datetime.now())

    def __str__(self):
        return "%s: %s"%(str(self.thread),self.body[:20])
    
    def update_thread(self,**kwargs):
        if self.thread.last_post < self.updated_at:
            self.thread.last_post = self.updated_at
            self.thread.save()

post_save.connect(Post.update_thread,sender=Post)


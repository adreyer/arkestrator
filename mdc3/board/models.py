from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.cache import cache

from mdc3.decorators import instance_memcache

import datetime

class Thread(models.Model):
    subject = models.CharField(max_length=60, blank=False)
    creator = models.ForeignKey(User,null=False,related_name='threads')
    
    last_post_by = models.ForeignKey(User,null=False,
        related_name='last_post_by')
    last_post = models.DateTimeField('Last Post',
        default=datetime.datetime.now) # w00t denormalization
    site = models.ForeignKey(Site, null=False)
    
    last_read = models.ManyToManyField(User,
        through = 'LastRead',
        related_name='last_read')

    on_site = CurrentSiteManager()

    def __str__(self):
        return self.subject

    @instance_memcache('default-posts-list')
    def default_post_list(self):
        post_list = self.post_set.select_related('creator').order_by("id")
        post_list = post_list[max(0,post_list.count()-25):]
        return post_list

class Post(models.Model):
    thread = models.ForeignKey(Thread, null=False)
    creator = models.ForeignKey(User,null=False)
    body = models.TextField(blank=False)
    updated_at = models.DateTimeField('Created at',
        default=datetime.datetime.now)

    def __str__(self):
        return "%s: %s"%(str(self.thread),self.body[:20])
    
class LastRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    timestamp = models.DateTimeField(default = datetime.datetime.now)
    post = models.ForeignKey(Post)
    read_count = models.IntegerField(default=0)

def update_thread(sender, instance, signal, *args, **kwargs):
    if instance.updated_at > instance.thread.last_post:
        instance.thread.last_post = instance.updated_at
        instance.thread.last_post_by = instance.creator
        instance.thread.save()

def invalidate_front_page(sender, instance, signal, *args, **kwargs):
    cache_key = "thread-list-page:%d:1"%Site.objects.get_current().id
    cache.delete(cache_key)
    del instance.default_post_list

post_save.connect(update_thread,sender=Post)
post_save.connect(invalidate_front_page,sender=Thread)


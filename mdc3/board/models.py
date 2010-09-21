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
        default = datetime.datetime.now,
        db_index = True) # w00t denormalization
    site = models.ForeignKey(Site, null=False)
    
    last_read = models.ManyToManyField(User,
        through = 'LastRead',
        related_name='last_read')

    on_site = CurrentSiteManager()

    def __str__(self):
        return self.subject

    @instance_memcache('default-posts-list', 1800)
    def default_post_list(self):
        post_list = self.post_set.select_related('creator').order_by("id")
        post_list = post_list[max(0,post_list.count()-25):]
        return post_list

    @instance_memcache('total-posts', 1800)
    def total_posts(self):
        if getattr(self, 'post__count', None):
            return self.post__count
        return self.post_set.count()

    @instance_memcache('total-views', 1800)
    def total_views(self):
        if getattr(self, 'lastread__read_count__sum', None):
            return self.lastread__read_count__sum
        queryset = LastRead.objects.filter(thread=self)
        agg = queryset.aggregate(models.Sum('read_count'))
        total = agg['read_count__sum']
        if not total:
            return 0
        return total

class Post(models.Model):
    thread = models.ForeignKey(Thread, null=False)
    creator = models.ForeignKey(User,null=False)
    body = models.TextField(blank=False)
    updated_at = models.DateTimeField('Created at',
        default = datetime.datetime.now, 
        db_index = True)

    def __str__(self):
        return "%s: %s"%(str(self.thread),self.body[:20])
    
class LastRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    timestamp = models.DateTimeField(default = datetime.datetime.now,
        db_index = True)
    read_count = models.IntegerField(default=0)

def update_thread(sender, instance, signal, *args, **kwargs):
    if instance.updated_at > instance.thread.last_post:
        instance.thread.last_post = instance.updated_at
        instance.thread.last_post_by = instance.creator
        instance.thread.save()

        try:
            lastread = LastRead.objects.get(
                user = instance.creator,
                thread = instance.thread
            )
            lastread.timestamp = instance.updated_at
            lastread.save()
        except LastRead.DoesNotExist:
            lastread = LastRead.objects.create(
                user = instance.creator,
                thread = instance.thread,
                timestamp = instance.updated_at,
            )

def invalidate_front_page(sender, instance, signal, *args, **kwargs):
    cache_key = "thread-list-page:%d:1"%Site.objects.get_current().id
    cache.delete(cache_key)
    del instance.default_post_list
    del instance.total_posts

post_save.connect(update_thread,sender=Post)
post_save.connect(invalidate_front_page,sender=Thread)


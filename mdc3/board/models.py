from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.cache import cache

from mdc3.decorators import instance_memcache
from bbking.fields import BBCodeField

import datetime


class Thread(models.Model):
    class Meta:
        permissions=(
            ('can_sticky', 'Can sticky threads'),
            ('can_lock', 'Can lock threads'),
            )
    
    subject = models.CharField(max_length=160, blank=False)
    creator = models.ForeignKey(User,null=False,related_name='threads')
    last_post = models.ForeignKey("board.Post", null=True, 
        related_name='last_post_on')
    stuck = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)
    site = models.ForeignKey(Site, null=False)
    last_read = models.ManyToManyField(User,
        through = 'LastRead',
        related_name='last_read')

    objects = CurrentSiteManager()

    def __unicode__(self):
        return self.subject

    @instance_memcache('default-posts-list', 1800)
    def default_post_list(self):
        post_list = self.post_set.select_related('creator').order_by("id")
        post_list = post_list[max(0,post_list.count()-10):]
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
    bbhash = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField('Created at',
        default = datetime.datetime.now, 
        db_index = True)

    bbcode = BBCodeField('body', 'bbhash')

    def __unicode__(self):
        return "%s: %s"%(unicode(self.thread),self.body[:20])
    
class LastRead(models.Model):
    user = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)
    post = models.ForeignKey(Post, null=True, blank=True)
    timestamp = models.DateTimeField(default = datetime.datetime.now,
        db_index = True)
    read_count = models.IntegerField(default=0)

def update_thread(sender, instance, signal, *args, **kwargs):
    if instance.id > instance.thread.last_post_id:

        instance.thread.last_post = instance
        instance.thread.save()

        try:
            lastread = LastRead.objects.get(
                user = instance.creator,
                thread = instance.thread
            )
            lastread.timestamp = instance.created_at
            lastread.post = instance
            lastread.save()
        except LastRead.DoesNotExist:
            lastread = LastRead.objects.create(
                user = instance.creator,
                thread = instance.thread,
                timestamp = instance.created_at,
                post = instance,
            )

def invalidate_front_page(sender, instance, signal, *args, **kwargs):
    cache_key = "thread-list-page:%d:1"%Site.objects.get_current().id
    cache.delete(cache_key)
    del instance.default_post_list
    del instance.total_posts

post_save.connect(update_thread,sender=Post)
post_save.connect(invalidate_front_page,sender=Thread)


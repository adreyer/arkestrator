from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db.models.signals import post_save
from django.db.models import Q,F

from mdc3.board.models import Thread, LastRead

def posting_users(request):
    return { 'posting_users': len(request.posting_users) }

def _thread_count_key(site):
    return "thread-count:%d"%site.id

def thread_count(request):
    key = _thread_count_key(Site.objects.get_current())

    count = cache.get(key, None)
    if count is None:
        count = Thread.objects.filter(recipient__isnull=True).count()
        cache.set(key, count)
    
    return { 'thread_count': count }

def _invalidate_thread_count(sender, instance, signal, *args, **kwargs):
    cache.delete(_thread_count_key(Site.objects.get_current()))

post_save.connect(_invalidate_thread_count, sender=Thread)

def pm_count(request):
    if request.user.is_authenticated():
        cache_key = "pm-count:%d:%d"%(
            Site.objects.get_current().id,
            request.user.id,
        )
        pm_count = cache.get(cache_key, None)
        if pm_count is None:
            pm_count = LastRead.objects.exclude(thread__recipient__isnull=True
                ).exclude(thread__deleted_by = request.user
                ).filter(user=request.user
                ).filter(Q(thread__creator=request.user)|Q(
                    thread__recipient=request.user)
                ).filter(post__id__lt=F('thread__last_post__id')
                ).count()
        return { 'new_pms' : pm_count }
    else:
        return { 'new_pms' : 0 }

def _invalidate_pm_count_on_read(sender, instance, signal, *args, **kwargs):
    if instance.thread.is_private:
        cache_key = "pm-count:%d:%d"%(
            Site.objects.get_current().id,
            instance.user.id,
        )
        cache.delete(cache_key)

def _invalidate_pm_count_on_post(sender, instance, signal, *args, **kwargs):
    if instance.is_private:
        cache_keys = [
            "pm-count:%d:%d"%(
                Site.objects.get_current().id,
                instance.creator.id),
            "pm-count:%d:%d"%(
                Site.objects.get_current().id,
                instance.recipient.id),
        ]
        cache.delete_many(cache_keys)

post_save.connect(_invalidate_pm_count_on_read, sender=LastRead)
post_save.connect(_invalidate_pm_count_on_post, sender=Thread)


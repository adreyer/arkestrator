from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db.models.signals import post_save

from mdc3.board.models import Thread

def posting_users(request):
    return { 'posting_users': len(request.posting_users) }

def _thread_count_key(site):
    return "thread-count:%d"%site.id

def thread_count(request):
    key = _thread_count_key(Site.objects.get_current())

    count = cache.get(key, None)
    if count is None:
        count = Thread.objects.count()
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
            pm_count = Recipient.objects.filter(
                recipient=request.user,read=False).count()
            cache.set(cache_key, pm_count)
        return { 'new_pms' : pm_count }
    else:
        return { 'new_pms' : 0 }

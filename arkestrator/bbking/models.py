from django.core.cache import cache
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save, post_delete

class WordFilter(models.Model):
    name = models.CharField(max_length=40)
    base_re = models.CharField(max_length=500)
    base_replace = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    ignore_case = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.name

def clear_regex_cache(sender, instance, signal, *args, **kwargs):
    cache_key = 'wordfilter-regexes:%d' % Site.objects.get_current().id
    cache.delete(cache_key)

post_save.connect(clear_regex_cache, sender=WordFilter)
post_delete.connect(clear_regex_cache, sender=WordFilter)


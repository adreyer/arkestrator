import re
from django import template
from django.core.cache import cache
from django.contrib.sites.models import Site

from ..models import WordFilter

register = template.Library()

@register.filter
def wordfilter(value):
    
    cache_key = 'wordfilter-regexes:%d' % Site.objects.get_current().id
    regexes = cache.get(cache_key)
    #try to cache regexes and recover them
    if regexes is None:
        filters = WordFilter.objects.filter(
                    active=True).order_by('-priority')
        regexes = []
        for filter in filters:
            if filter.ignore_case:
                regex = re.compile(filter.base_re, re.IGNORECASE)
            else: 
                regex = re.compile(filter.base_re)
            regexes.append((regex,filter.base_replace))
        cache.set(cache_key, regexes)

    for regex, rep in regexes:
        value = regex.sub(rep,value)
    return value

from django.core.cache import cache
from django.contrib.sites.models import Site

from arkestrator.pms.models import Recipient

def new_pm(request):
    """ the number of new pms a user has """

    if request.user.is_authenticated():
        cache_key = "pm-count:%d" %request.user.id
        pm_count = cache.get(cache_key, None)
        if pm_count is None:
            pm_count = Recipient.objects.filter(
                recipient=request.user,read=False).count()
            cache.set(cache_key, pm_count)
        return { 'new_pms' : pm_count }
    else:
        return { 'new_pms' : 0 }

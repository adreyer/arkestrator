from django.core.cache import cache
from django.contrib.sites.models import Site

from mdc3.invites.models import Invite

def new_invites(request):
    cache_key = "inv-count:%d"%(
        Site.objects.get_current().id,
    )
    inv_count = cache.get(cache_key, None)
    if inv_count is None:
        inv_count = Invite.objects.filter(
            approved=False,rejected=False).count()
        cache.set(cache_key, inv_count)
    return { 'new_invites' : inv_count }

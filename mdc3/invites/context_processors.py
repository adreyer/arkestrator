from django.core.cache import cache
from django.contrib.sites.models import Site

from mdc3.invites.models import Invite

def new_invites(request):
    """ how many unapproved or rejected invites are there """
    inv_count = cache.get('inv_count', None)
    if inv_count is None:
        inv_count = Invite.objects.filter(
                approved=False,rejected=False).count()
        cache.set('inv_count', inv_count)
    return { 'new_invites' : inv_count }

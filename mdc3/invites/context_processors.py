from django.core.cache import cache
from django.contrib.sites.models import Site

from mdc3.invites.models import Invite

def new_invites(request):
    inv_count = Invite.objects.filter(
            approved=False,rejected=False).count()
    return { 'new_invites' : inv_count }

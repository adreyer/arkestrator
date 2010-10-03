import datetime

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.core.cache import cache

from mdc3.pms.models import Recipient

def site_name(request):

    Site.objects.clear_cache()
    current_site = Site.objects.get_current()
    return { 'site_name' : current_site.name }


def new_pm(request):

    if request.user.is_authenticated():
        pm_count = Recipient.objects.filter(recipient=request.user,read=False).count()
        return { 'new_pms' : pm_count }
    else:
        return { 'new_pms' : 0 }

def online_users(request):
    return { 'online_users' : len(request.online_users) }



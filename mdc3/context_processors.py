
def site_name(request):
    from django.contrib.sites.models import Site

    Site.objects.clear_cache()
    current_site = Site.objects.get_current()
    return { 'site_name' : current_site.name }


def new_pm(request):
    from django.contrib.auth.models import User
    from mdc3.pms.models import Recipient 

    pm_count = Recipient.objects.filter(recipient=request.user,read=False).count()
    return { 'new_pms' : pm_count }



def site_name(request):
    from django.contrib.sites.models import Site

    Site.objects.clear_cache()
    current_site = Site.objects.get_current()
    return { 'site_name' : current_site.name }


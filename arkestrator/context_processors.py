from django.contrib.sites.models import Site

def site_name(request):

    Site.objects.clear_cache()
    current_site = Site.objects.get_current()
    return { 'site_name' : current_site.name }

def online_users(request):
    """ the number of users online recently see arkestrator.middleware """
    return { 'online_users' : len(request.online_users) }



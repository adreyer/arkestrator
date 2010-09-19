from django.conf.urls.defaults import *

urlpatterns = patterns('mdc3.profiles.views',
        url(r"^(?P<user_id>\d+)/$", 'view_profile', name='view-profile'),
        url(r"", 'list_profiles', name='list-profiles'),
)

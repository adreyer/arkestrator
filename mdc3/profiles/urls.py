from django.conf.urls.defaults import *
from django.contrib.auth.views import password_change
import views

urlpatterns = patterns('',
        url(r"^(?P<user_id>\d+)/$", views.view_profile, name='view-profile'),
        url(r"^edit_info/$", views.edit_info, name='edit-info'),
        url(r"^edit_prefs/$", views.edit_prefs, name='edit-prefs'),
        url(r"^passwd/$", password_change, name='passwd'),
        (r'^password/done/$',
             'django.contrib.auth.views.password_change_done'),
        url(r"^list_profiles/$", views.list_profiles, name='list-profiles'),
)

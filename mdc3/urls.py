from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import bbcode
bbcode.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)/$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/accounts/login/'}),
    (r'^themes/', include('mdc3.themes.urls')),
    (r'', include('mdc3.board.urls')),
    (r'^profiles/', include('mdc3.profiles.urls')),
    (r'^invites/', include('mdc3.invites.urls')),
    url(r'^active/$', 'mdc3.util.views.active_users',
        name='active-users'),
    url(r'^quote/(?P<id>\d+)/$', 'mdc3.board.views.get_quote', name='get-quote'),
)

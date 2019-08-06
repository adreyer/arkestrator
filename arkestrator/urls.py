from django.conf.urls import include, url
from django.conf import settings
import django.views.static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from arkestrator.board.views import get_quote
from arkestrator.util.views import active_users

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)/$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^themes/', include('arkestrator.themes.urls')),
    url(r'', include('arkestrator.board.urls')),
    url(r'^profiles/', include('arkestrator.profiles.urls')),
    url(r'^invites/', include('arkestrator.invites.urls')),
    url(r'^pms/', include('arkestrator.pms.urls')),
    url(r'^events/', include('arkestrator.events.urls')),
    url(r'^gallery/', include('arkestrator.gallery.urls')),
    url(r'^mod/', include('arkestrator.moderation.urls')),
    url(r'^active/$', active_users, name='active-users'),
    url(r'^quote/(?P<id>\d+)/$', get_quote, name='get-quote'),
]

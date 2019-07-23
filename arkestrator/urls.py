from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)/$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^themes/', include('arkestrator.themes.urls')),
    (r'', include('arkestrator.board.urls')),
    (r'^profiles/', include('arkestrator.profiles.urls')),
    (r'^invites/', include('arkestrator.invites.urls')),
    (r'^pms/', include('arkestrator.pms.urls')),
    (r'^events/', include('arkestrator.events.urls')),
    (r'^gallery/', include('arkestrator.gallery.urls')),
    (r'^mod/', include('arkestrator.moderation.urls')),
    url(r'^active/$', 'arkestrator.util.views.active_users',
        name='active-users'),
    url(r'^quote/(?P<id>\d+)/$', 'arkestrator.board.views.get_quote', name='get-quote'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('arkestrator.moderation.views',
        url(r"^ban/$", 'ban_user', name='ban'),
        url(r"^ban/list/$", 'ban_list', name='ban-list'),
        url(r"^$", 'mod_panel', name='mod-panel'),
)

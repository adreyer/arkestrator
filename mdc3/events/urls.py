from django.conf.urls.defaults import *


urlpatterns = patterns('mdc3.events',
    url(r"^new/$",'views.new_event',name='new-event'),
    url(r"^(?P<ev_id>\d+)/$", 'views.view_event',name='view-event'),
                       )

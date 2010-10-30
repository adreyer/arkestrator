from django.conf.urls.defaults import *


urlpatterns = patterns('mdc3.events',
    url(r"^new/$",'views.new_event',name='new-event'),
    url(r"^(?P<ev_id>\d+)/$", 'views.view_event',name='view-event'),
    url(r'^list/$','views.list_events',name='list-events'),
    url(r'^list/past/$','views.list_events',
        {'upcoming' : False},
        name='list-past-events'
        ),
    url(r'^list/past/ew/$','views.list_events',
        {'upcoming' : False, 'local': False },
        name='list-past-ew-events'
        ),
    url(r'^list/ew/$','views.list_events',
        {'local': False },
        name='list-ew-events'
        ),
                       )

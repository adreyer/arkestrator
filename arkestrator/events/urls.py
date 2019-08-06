from django.conf.urls import url

from arkestrator.events.views import EventListView

from arkestrator.events import views


urlpatterns = [
    url(r"^new/$",views.new_event, name='new-event'),
    url(r"^(?P<ev_id>\d+)/$", views.view_event, name='view-event'),
    url(r"^(?P<ev_id>\d+)/edit/$", views.edit_event, name='edit-event'),
    url(r"^(?P<ev_id>\d+)/rsvp/$", views.update_rsvp, name='update-rsvp'),
    url(r'^list/$', EventListView.as_view(), name='list-events'),
    url(r'^list/past/$', EventListView.as_view(), {'upcoming' : False}, name='list-past-events'),
    url(r'^list/past/ew/$', EventListView.as_view(), {'upcoming' : False, 'local': False }, name='list-past-ew-events'),
    url(r'^list/ew/$', EventListView.as_view(), {'local': False }, name='list-ew-events'),
]

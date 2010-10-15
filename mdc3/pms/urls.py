from django.conf.urls.defaults import *


urlpatterns = patterns('mdc3.pms',
    url(r"^new_pm/$", 'views.new_pm', name='new-pm'),
    url(r"^new_pm/(?P<rec_id>\d+)/$", 'views.new_pm', name='new-pm'),
    url(r"^inbox/$", 'views.inbox', name='inbox'),
    url(r"^outbox/$", 'views.outbox', name='outbox'),
    url(r"^mark_read/$", 'views.mark_read', name='mark-read'),
    url(r"^(?P<pm_id>\d+)/$", 'views.view_pm',name='view-pm'),
    url(r"^(?P<pm_id>\d+)/show_thread/$", 'views.pm_thread',name='pm-thread'),
    url(r"^del/(?P<pm_id>\d+)/$", 'views.del_pm',name='del-pm'),
    url(r"^quote/(?P<id>\d+)/$", 'views.get_quote', name='get-pm-quote'),
)

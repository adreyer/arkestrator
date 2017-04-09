from django.conf.urls.defaults import *
import views


urlpatterns = patterns('arkestrator.pms',
    url(r"^new_pm/$", views.NewPM.as_view(), name='new-pm'),
    url(r"^inbox/$", views.Inbox.as_view(), name='inbox'),
    url(r"^outbox/$", views.Outbox.as_view(), name='outbox'),
    url(r"^mark_read/$", views.MarkRead.as_view(), name='mark-read'),
    url(r"^(?P<pm_id>\d+)/$", views.PMDetail.as_view(), name='view-pm'),
    url(r"^(?P<pm_id>\d+)/show_thread/$", views.PMThread.as_view(), name='pm-thread'),
    url(r"^del/(?P<pm_id>\d+)/$", views.DeletePM.as_view(), name='del-pm'),
    url(r"^quote/(?P<pm_id>\d+)/$", views.PMQuote.as_view(), name='get-pm-quote'),
)

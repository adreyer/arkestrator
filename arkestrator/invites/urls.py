from django.conf.urls import patterns, url

from arkestrator.invites.views import InviteListView

urlpatterns = patterns('arkestrator.invites.views',
        url(r"^(?P<code>\w+)/$", 'register', name='register'),
        url(r"^$", InviteListView.as_view(), name='invite-list'),
        url(r"^approve_invite/(?P<id>\w+)/$", 'approve_invite',
                name='approve-invite'),
        url(r"^reject_invite/(?P<id>\w+)/$", 'reject_invite',
                name='reject-invite'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('mdc3.invites.views',
        url(r"^(?P<code>\w+)/$", 'register', name='register'),
        url(r"^$", 'invite_list', name='invite-list'),
        url(r"^approve_invite/(?P<id>\w+)/$", 'approve_invite',
                name='approve-invite'),
        url(r"^reject_invite/(?P<id>\w+)/$", 'reject_invite',
                name='reject-invite'),
)

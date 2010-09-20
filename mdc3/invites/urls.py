from django.conf.urls.defaults import *

urlpatterns = patterns('mdc3.invites.views',
        url(r"^new_invite/$", 'new_invite', name='new-invite'),
        url(r"^(?P<code>\w+)/$", 'register', name='register'),
)

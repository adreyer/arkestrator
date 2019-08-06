from django.conf.urls import url

from arkestrator.invites.views import InviteListView

from arkestrator.invites import views

urlpatterns = [
        url(r"^(?P<code>\w+)/$", views.register, name='register'),
        url(r"^$", InviteListView.as_view(), name='invite-list'),
        url(r"^approve_invite/(?P<id>\w+)/$", views.approve_invite,
                name='approve-invite'),
        url(r"^reject_invite/(?P<id>\w+)/$", views.reject_invite,
                name='reject-invite'),
]

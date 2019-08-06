from django.conf.urls import url

from arkestrator.moderation import views

urlpatterns = [
        url(r"^ban/$", views.ban_user, name='ban'),
        url(r"^ban/list/$", views.ban_list, name='ban-list'),
        url(r"^$", views.mod_panel, name='mod-panel'),
]

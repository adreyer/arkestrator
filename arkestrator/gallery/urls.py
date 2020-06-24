from django.conf.urls import url

from arkestrator.gallery import views


urlpatterns = [
    url(r"^upload/$", views.upload_image, name='upload-image'),
    url(r"^image/(?P<id>\d+)/$", views.view_image, name='view-image'),
]

from django.conf.urls import patterns, url


urlpatterns = patterns('arkestrator.gallery',
    url(r"^upload/$", 'views.upload_image',name='upload-image'),
    url(r"^image/(?P<id>\d+)/$", 'views.view_image',name='view-image'),
)

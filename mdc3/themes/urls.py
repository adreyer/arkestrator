from django.conf.urls.defaults import *

from models import Theme

urlpatterns = patterns('',
    url(r"^theme/(?P<object_id>\d+)/$", 
        "django.views.generic.list_detail.object_detail",{
            'queryset' : Theme.objects ,
            'template_name' : 'themes/theme.css',
            'mimetype' : 'text/css',
        }, name = 'theme-css'),
)

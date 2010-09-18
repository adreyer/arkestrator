from django.conf.urls.defaults import *

from models import Theme
from views import edit_theme

urlpatterns = patterns('',
    url(r"^(?P<object_id>\d+)/$", 
        "django.views.generic.list_detail.object_detail",{
            'queryset' : Theme.objects ,
            'template_name' : 'themes/theme.css',
            'mimetype' : 'text/css',
        }, name = 'theme-css'),
    url(r"^edit/$", edit_theme, name="edit-theme"),
)

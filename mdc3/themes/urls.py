from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_detail

from models import Theme
from views import edit_theme

urlpatterns = patterns('',
    url(r"^(?P<object_id>\d+)/$", 
        cache_page(600)(object_detail), {
            'queryset' : Theme.objects ,
            'template_name' : 'themes/theme.css',
            'mimetype' : 'text/css',
        }, name = 'theme-css'),
    url(r"^default/$", 
        "django.views.generic.simple.direct_to_template",{
            'template' : 'themes/theme.css',
            'mimetype': 'text/css',
            'extra_context': {
                'object': Theme(),
            },
        }, name = 'default-theme-css'),
    url(r"^edit/$", edit_theme, name="edit-theme"),
    url(r"^edit/(?P<theme_id>\d+)/$", edit_theme, name="edit-existing-theme"),
)

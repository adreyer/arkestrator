from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template
from django.db.models.signals import post_save

from models import Theme
from views import edit_theme
from mdc3.decorators import better_cache

theme_css = better_cache('theme-css', 600)(object_detail)
def invalidate_theme(sender, instance, signal, *args, **kwargs):
    theme_css.invalidate(instance.id)
post_save.connect(invalidate_theme, sender = Theme)

urlpatterns = patterns('',
    url(r"^(?P<object_id>\d+)/$", 
        theme_css, {
            'queryset' : Theme.objects ,
            'template_name' : 'themes/theme.css',
            'mimetype' : 'text/css',
        }, name = 'theme-css'),
    url(r"^default/$", 
        cache_page(direct_to_template, 600), {
            'template' : 'themes/theme.css',
            'mimetype': 'text/css',
            'extra_context': {
                'object': Theme(),
            },
        }, name = 'default-theme-css'),
    url(r"^edit/$", edit_theme, name="edit-theme"),
    url(r"^edit/(?P<theme_id>\d+)/$", edit_theme, name="edit-existing-theme"),
)

from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page, cache_control
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.db.models.signals import post_save

from models import Theme
from views import edit_theme
from arkestrator.decorators import better_cache


class DefaultThemeView(TemplateView):
    template_name = 'themes/theme.css'
    content_type = 'text/css'

    def get_context_data(self, **kwargs):
        context = super(DefaultThemeView, self).get_context_data(**kwargs)
        context['object'] = Theme()
        return context


class ThemeView(DetailView):
    template_name = 'themes/theme.css'
    content_type = 'text/css'
    model = Theme


default_cache_control = cache_control(
    max_age=604800,
    must_revalidate = False,
)


urlpatterns = patterns('',
    url(r"^(?P<pk>\d+)/$", ThemeView.as_view(), name='theme-css'),
    url(r"^default/$", 
        default_cache_control(cache_page(DefaultThemeView.as_view(), 600)), name='default-theme-css'),
    url(r"^edit/$", edit_theme, name="edit-theme"),
    url(r"^edit/(?P<theme_id>\d+)/$", edit_theme, name="edit-existing-theme"),
)

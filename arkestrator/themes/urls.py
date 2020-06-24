from django.conf.urls import url
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.db.models.signals import post_save

from arkestrator.themes.models import Theme
from arkestrator.themes.views import edit_theme


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


urlpatterns = [
    url(r"^(?P<pk>\d+)/$", ThemeView.as_view(), name='theme-css'),
    url(r"^default/$", DefaultThemeView.as_view(), name='default-theme-css'),
    url(r"^edit/$", edit_theme, name="edit-theme"),
    url(r"^edit/(?P<theme_id>\d+)/$", edit_theme, name="edit-existing-theme"),
]

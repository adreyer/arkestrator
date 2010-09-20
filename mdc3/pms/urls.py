from django.conf.urls.defaults import *


urlpatterns = patterns('mdc3.pms',
    url(r"^new_pm/$", 'views.new_pm', name='new-pm'),
    url(r"^inbox/$", 'views.inbox', name='inbox'),
)

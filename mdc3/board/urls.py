from django.conf.urls.defaults import *

from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list

import views
import models

threads_dict = {
    'queryset': models.Thread.on_site.order_by('-last_post').
        select_related(),
    'paginate_by': 50,
}

urlpatterns = patterns('',
    url(r"^$",login_required(object_list),
        threads_dict,name='list-threads'),
    url(r"^threads/(?P<id>\d+)/$",views.view_thread,name='view-thread'),
)


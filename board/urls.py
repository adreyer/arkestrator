from django.conf.urls.defaults import *

import views
import models

threads_dict = {
    'queryset': models.Thread.on_site.order_by('-last_post').
        select_related().all(),
    'paginate_by': 50,
}

urlpatterns = patterns('',
    url(r"^$",
        'django.views.generic.list_detail.object_list',
        threads_dict,
        name='list-threads'),
)



from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic import list_detail

import models

def view_thread(request,id=None):
    thread = get_object_or_404(models.Thread,pk=id,
        site=Site.objects.get_current())

    page = request.GET.get('page','1')
    
    return list_detail.object_list(
        request,
        queryset=thread.post_set.order_by("updated_at").select_related(),
        paginate_by = 25,
        page = page,
        extra_context = {
            "thread" : thread,
        }
    )


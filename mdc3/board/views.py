
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import list_detail

import models
import forms

@login_required
def view_thread(request,id=None):
    thread = get_object_or_404(models.Thread,pk=id,
        site=Site.objects.get_current())

    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            form.save(thread, request.user)
            return HttpResponseRedirect("/")
    else:
        form = forms.PostForm()

    page = request.GET.get('page','1')

    return list_detail.object_list(
        request,
        queryset=thread.post_set.order_by("updated_at").select_related(),
        paginate_by = 25,
        page = page,
        extra_context = {
            "thread" : thread,
            "form" : form,
        }
    )

@login_required
def new_thread(request):
    if request.method == 'POST':
        form = forms.ThreadForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect("/")
    else:
        form = forms.ThreadForm()
    return render_to_response("board/new_thread.html",
        { 'form' : form },
        context_instance = RequestContext(request))

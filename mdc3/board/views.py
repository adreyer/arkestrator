
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.db.models.signals import post_save
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage

from models import Thread
import forms

@login_required
def view_thread(request,id=None):
    thread = get_object_or_404(Thread,pk=id)

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

@login_required
def list_threads(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    cache_key = "thread-list-page:%d:%d"%(Site.objects.get_current().id, page)
    page_obj = cache.get(cache_key, None)
    if page_obj is None:
        queryset = Thread.on_site.order_by("-last_post").select_related(
            "creator","last_post_by")
        paginator = Paginator(queryset, 50, allow_empty_first_page=True)
        page_obj = paginator.page(page)
        cache.set(cache_key, page_obj)

    thread_list = page_obj.object_list

    return render_to_response("board/thread_list.html", {
        'thread_list' : thread_list,
        'page_obj' : page_obj
    }, context_instance = RequestContext(request))


import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.db.models.signals import post_save
from django.db.models import Sum, Count, Max, F
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage

from models import Thread, Post, LastRead
import forms

@login_required
def view_thread(request,id=None,expand=False):
    thread = get_object_or_404(Thread,pk=id)

    if request.method == 'POST':
        post = Post(
            thread = thread,
            creator = request.user
        )
        form = forms.PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = forms.PostForm()

    queryset=thread.post_set.order_by("updated_at").select_related(
        'creator')

    try:
        lastread = LastRead.objects.get(
            user = request.user,
            thread = thread
        )
        if not expand:
            queryset = queryset.filter(updated_at__gte=lastread.timestamp)
    except LastRead.DoesNotExist:
        lastread = LastRead(user = request.user,
            thread = thread,
            read_count = 0,
        )

    lastread.timestamp = datetime.datetime.now()
    lastread.read_count += 1
    lastread.save()
    del thread.total_views

    if not expand and queryset.count() < 25:
        queryset = thread.default_post_list

    return list_detail.object_list(
        request,
        queryset = queryset,
        extra_context = {
            "thread" : thread,
            "form" : form,
        }
    )

@login_required
def new_thread(request):
    if request.method == 'POST':
        thread = Thread(
            creator = request.user,
            last_post_by = request.user,
            site = Site.objects.get_current(),
        )
        post = Post(
            thread = thread,
            creator = request.user
        )
        thread_form = forms.ThreadForm(request.POST, instance = thread)
        post_form = forms.PostForm(request.POST, instance = post)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save()
            post.thread = thread
            post_form = forms.PostForm(request.POST, instance = post)
            post_form.save()
            return HttpResponseRedirect("/")
    else:
        thread_form = forms.ThreadForm()
        post_form = forms.PostForm()
    return render_to_response("board/new_thread.html",{
            'thread_form' : thread_form,
            'post_form' : post_form,
        }, context_instance = RequestContext(request))

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
        paginator = Paginator(queryset, 3, allow_empty_first_page=True)
        page_obj = paginator.page(page)
        cache.set(cache_key, page_obj)

    page_list = range(1,paginator.num_pages+1)
    print paginator.num_pages
    print page_list

    thread_list = page_obj.object_list

    last_read = LastRead.objects.filter(
        thread__in=[t.id for t in thread_list],
        user = request.user,
    ).values('thread__id', 'timestamp')
    last_viewed = dict((lr['thread__id'], lr['timestamp']) for lr in last_read)
    for t in thread_list:
        if t.id in last_viewed:
            t.unread = last_viewed[t.id] < t.last_post
        else:
            t.unread = True

    return render_to_response("board/thread_list.html", {
        'thread_list' : thread_list,
        'page_obj' : page_obj,
        'page_list' : page_list,
    }, context_instance = RequestContext(request))

@login_required
def thread_history(request,id=None,expand=False):
    thread = get_object_or_404(Thread,pk=id)

    queryset = LastRead.objects.filter(thread = thread).order_by("-timestamp")
    queryset = queryset.select_related('user')

    return render_to_response("board/thread_history.html", {
        'thread' : thread,
        'read_list' : queryset.all(),
    }, context_instance = RequestContext(request))


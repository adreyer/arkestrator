import datetime
import random
import sys
import string

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.db.models.signals import post_save
from django.db.models import Sum, Count, Max, F
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User

from mdc3.profiles.models import Profile
from models import Thread, Post, LastRead
import forms

from mdc3.decorators import super_no_cache

@login_required
def view_thread(request,id=None,expand=False):
    thread = get_object_or_404(Thread,pk=id)
    
    if request.method == 'POST':
        if thread.locked:
            return HttpResponseRedirect("/")  
        post = Post(
            thread = thread,
            creator = request.user
        )
        form = forms.PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            request.posting_users.add_to_set(request.user.id)
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

    if not expand and queryset.count() < 10:
        queryset = thread.default_post_list

    post_list = list(queryset)
    #this is a hack to hide images
    try:
        if not request.user.get_profile().show_images:
            for post in post_list:
                post.body = post.body.replace('[img','(img)[url')
                post.body = post.body.replace('[/img]','[/url]')
    except ObjectDoesNotExist:
        pass

    lastread.timestamp = datetime.datetime.now()
    lastread.read_count += 1
    lastread.post = post_list[-1]
    lastread.save()
    del thread.total_views

    if len(post_list)< 10:
        expand = True
        
    return render_to_response("board/post_list.html", {
        'object_list' : post_list,
        'thread' : thread,
        'form' : form,
        'expand': expand,
        },
        context_instance = RequestContext(request))

@login_required
def new_thread(request):
    if request.method == 'POST':
        thread = Thread(
            creator = request.user,
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
            request.posting_users.add_to_set(request.user.id)
            return HttpResponseRedirect("/")
    else:
        thread_form = forms.ThreadForm()
        post_form = forms.PostForm()
    return render_to_response("board/new_thread.html",{
            'thread_form' : thread_form,
            'post_form' : post_form,
        }, context_instance = RequestContext(request))

@super_no_cache
@login_required
def list_threads(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    
    cache_key = "thread-list-page:%d:%d"%(Site.objects.get_current().id, page)
    page_obj = cache.get(cache_key, None)
    if page_obj is None:
        queryset = Thread.objects.order_by("-stuck","-last_post__id"
            ).select_related("creator","last_post","last_post__creator")
        paginator = Paginator(queryset, 25, allow_empty_first_page=True)
        page_obj = paginator.page(page)
        cache.set(cache_key, page_obj)

    thread_list = page_obj.object_list

    last_read = LastRead.objects.filter(
        thread__in=[t.id for t in thread_list],
        user = request.user,
    ).values('thread__id', 'post__id')
    last_viewed = dict((lr['thread__id'], lr) for lr in last_read)
    for t in thread_list:
        if t.id in last_viewed:
            t.unread = last_viewed[t.id]['post__id'] < t.last_post_id
            t.last_post_read = last_viewed[t.id]['post__id']
        else:
            t.unread = True

    return render_to_response("board/thread_list.html", {
        'thread_list' : thread_list,
        'page_obj' : page_obj,
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

@login_required
def toggle_sticky(request,id):
    thread = get_object_or_404(Thread,pk=id)
    if thread.stuck:
        thread.stuck = False
    else:
        thread.stuck = True
    thread.save()
    return HttpResponseRedirect("/")

@login_required
def mark_read(request):
    thread_list = Thread.on_site.order_by("-stuck","-last_post")[0:50]
    lr_list = LastRead.objects.filter(
        thread__in=[t.id for t in thread_list],
        user = request.user,
    ).select_related('thread__id', 'timestamp')
    last_read = lr_list.values('thread__id', 'timestamp')
    last_viewed = dict((lr['thread__id'], lr['timestamp']) for lr in last_read)
    for t in thread_list:
        if t.id in last_viewed and last_viewed[t.id] < t.last_post:
            lr = lr_list.get(thread__id=t.id)
            lr.timestamp = datetime.datetime.now()
            lr.save()
        else:
            try:
                lr = LastRead.objects.get(
                    user = request.user,thread = t)
            except LastRead.DoesNotExist:
                lr = LastRead(user = request.user,
                    thread = t, read_count = 0)
            lr.timestamp = datetime.datetime.now()
            lr.save()
    return HttpResponseRedirect("/")

@login_required
def threads_by(request, id):
    poster = get_object_or_404(User,pk=id)
    queryset = Thread.on_site.filter(creator=id).order_by(
        '-last_post').select_related('last_post', 'last_post__creator')

    return list_detail.object_list(
            request,
            queryset = queryset,
            paginate_by = 50,
            template_name = "board/threads_by.html",
            extra_context = {"poster" : poster.username}
            )

@login_required
def posts_by(request, id):
    poster = get_object_or_404(User,pk=id)
    queryset = Post.objects.filter(creator=poster).order_by(
        '-updated_at').select_related('thread__subject')

    return list_detail.object_list(
            request,
            queryset = queryset,
            paginate_by = 50,
            template_name = "board/posts_by.html",
            extra_context = {"poster" : poster.username}
            )

@login_required
def get_quote(request, id):
    post = get_object_or_404(Post, pk=id)
    user = get_object_or_404(User, pk=post.creator.id)
    return render_to_response("board/get_quote.html", {
            'post': post,
            'user': user,
    })

@login_required
@permission_required('board.can_lock','/')
def lock_thread(request, id):
    thread = get_object_or_404(Thread,pk=id)
    thread.locked = not thread.locked
    thread.save()
    return HttpResponseRedirect("/")
    

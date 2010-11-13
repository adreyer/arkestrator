import datetime
import random
import sys
import string
import re

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
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
from mdc3.events.models import Event
from mdc3.events.forms import RSVPForm
from models import Thread, Post, LastRead
import forms

from mdc3.decorators import super_no_cache


@login_required
def view_thread(request,id=None,start=False,expand=False,hide=None):
    thread = get_object_or_404(Thread,pk=id)
    try:
        event = Event.objects.get(thread=thread)
    except Event.DoesNotExist:
        event = None
                                  
    
    if request.method == 'POST':
        if thread.locked:
            return HttpResponseRedirect(reverse('list-threads'))
        post = Post(
            thread = thread,
            creator = request.user
        )
        form = forms.PostForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            request.posting_users.add_to_set(request.user.id)
            return HttpResponseRedirect(reverse('list-threads'))
    else:
        form = forms.PostForm()

    queryset=thread.post_set.order_by(
        "id").select_related('creator')

    try:
        lastread = LastRead.objects.get(
            user = request.user,
            thread = thread
        )
        if not expand:
            coll_size = request.user.get_profile().collapse_size
            if start:
                tset = queryset.filter(pk__lte=start).reverse()
            else:
                tset = queryset.filter(
                    created_at__lte=lastread.timestamp).reverse()
            if tset.count() >coll_size:
                tstart = tset[coll_size].id
                queryset = queryset.filter(pk__gte=tstart)
            else:
                expand = True
    except LastRead.DoesNotExist:
        lastread = LastRead(user = request.user,
            thread = thread,
            read_count = 0,
        )
        if event:
            cache.delete('event-count:%d'%(request.user.id))

    if not expand and not start and queryset.count() < 10:
        queryset = thread.default_post_list
        queryset = queryset=thread.post_set.order_by(
            "created_at").select_related('creator')
        queryset = queryset[max(0,queryset.count()-10):]
 
            
    post_list = list(queryset)
    try:
        if (not hide is False) and (hide or not request.user.get_profile().show_images):
            hide = True
            for post in post_list:
                img_start = re.compile('\[img', re.IGNORECASE)
                img_end = re.compile('\[/img\]', re.IGNORECASE)
                post.body = img_start.sub('(img)[url',post.body)
                post.body = img_end.sub('[/url]',post.body)
    except ObjectDoesNotExist:
        pass

    lastread.timestamp = datetime.datetime.now()
    lastread.read_count += 1
    lastread.post = post_list[-1]
    lastread.save()
    del thread.total_views

    fav = False
    if thread.favorite.filter(id=request.user.id):
        fav = True
    
    if len(post_list)< 10:
        expand = True

    if not start and post_list:
        start = post_list[0].id


    if event:
        event = Event.objects.get(thread=thread)
        return render_to_response("events/view_event.html", {
        'object_list' : post_list,
        'thread' : thread,
        'form' : form,
        'expand': expand,
        'hide': hide,
        'start': start,
        'fav' : fav,
        'event' : event,
        'rsvp_form' : RSVPForm(),
        'rsvp_list' : event.rsvp_list(),
        },
        context_instance = RequestContext(request))

    
    return render_to_response("board/post_list.html", {
        'object_list' : post_list,
        'thread' : thread,
        'form' : form,
        'expand': expand,
        'hide': hide,
        'start': start,
        'fav' : fav,
        },
        context_instance = RequestContext(request))

@login_required
def view_post(request, id):
    post = get_object_or_404(Post, pk=id)
    return view_thread(request, id=post.thread.id,start=id)
    

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
            return HttpResponseRedirect(reverse('list-threads'))
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
        paginator = Paginator(queryset, 50, allow_empty_first_page=True)
        page_obj = paginator.page(page)
        cache.set(cache_key, page_obj)

    thread_list = list(page_obj.object_list)

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

    #pull unread favorites to the top if favs_first
    if request.user.get_profile().favs_first:
        fav_indexes = []
        stickies = -1
        for i, t in zip(range(len(thread_list)), thread_list):
            if t.favorite.filter(id = request.user.id):
                t.fav = True
                if t.unread:
                    fav_indexes.append(i) 
            else:
                t.fav = False
            if t.stuck:
                stickies=i
            
        favs = []
        for i in fav_indexes:
            favs.append(thread_list.pop(i))
        if stickies != -1:
            thread_list = thread_list[0:stickies+1] + favs + thread_list[stickies+1:]
        else:
            thread_list = favs + thread_list
        
    #otherwise just figure out what's favorited
    else:
        for t in thread_list:
            if t.favorite.filter(id = request.user.id):
                t.fav = True
            else:
                t.fav = False

    return render_to_response("board/thread_list.html", {
        'thread_list' : thread_list,
        'page_obj' : page_obj,
    }, context_instance = RequestContext(request))

@login_required
def favorite_list(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    
    queryset = request.user.favorites.all().order_by(
        '-last_post__id').select_related(
        "creator","last_post","last_post__creator")
    
    paginator = Paginator(queryset, 50, allow_empty_first_page=True)
    page_obj = paginator.page(page)

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

@super_no_cache
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
@permission_required('board.can_sticky')
def sticky(request,id):
    thread = get_object_or_404(Thread,pk=id)
    thread.stuck = True
    thread.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
@permission_required('board.can_sticky')
def unsticky(request,id):
    thread = get_object_or_404(Thread,pk=id)
    thread.stuck = False
    thread.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
def mark_read(request):
    thread_list = Thread.objects.order_by("-stuck","-last_post")[0:50]
    lr_list = LastRead.objects.filter(
        thread__in=[t.id for t in thread_list],
        user = request.user,
    ).select_related('thread__id', 'timestamp')
    last_read = lr_list.values('thread__id', 'post')
    last_viewed = dict((lr['thread__id'], lr['post']) for lr in last_read)
    for t in thread_list:
        if t.id in last_viewed and last_viewed[t.id] < t.last_post:
            lr = lr_list.get(thread__id=t.id)
            lr.timestamp = datetime.datetime.now()
            lr.post = t.last_post
            lr.save()
        else:
            try:
                lr = LastRead.objects.get(
                    user = request.user,thread = t)
            except LastRead.DoesNotExist:
                lr = LastRead(user = request.user,
                    thread = t,
                    post = t.last_post,
                    read_count = 0)
            lr.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
def threads_by(request, id):
    poster = get_object_or_404(User,pk=id)
    queryset = Thread.objects.filter(creator=id).order_by(
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
    queryset = Post.objects.filter(creator = poster).order_by(
        '-created_at').select_related('thread__subject')

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
@permission_required('board.can_lock')
def lock_thread(request, id):
    thread = get_object_or_404(Thread,pk=id)
    thread.locked = True
    thread.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
@permission_required('board.can_lock')
def unlock_thread(request, id):
    thread = get_object_or_404(Thread,pk=id)
    thread.locked = False
    thread.save()
    return HttpResponseRedirect(reverse('list-threads'))
    
@login_required
def favorite_thread(request, id):
    thread = get_object_or_404(Thread,pk=id)
    thread.favorite.add(request.user)
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
def unfavorite_thread(request,id):
    thread = get_object_or_404(Thread,pk=id)
    thread.favorite.remove(request.user)
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
def ghetto_search(request):
    'fuck this shit is ghetto'

    query = request.GET.get('query', 'rev is the best')
    
    queryset = Thread.objects.filter(subject__icontains=query).order_by(
        '-last_post__id')
    
    return list_detail.object_list(
        request,
        queryset = queryset,
        template_object_name = 'thread',
        paginate_by = 50,
        template_name = "board/thread_list.html",
        extra_context = { 'search_query' : query },
    )


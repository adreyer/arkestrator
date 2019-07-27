import datetime
import random
import sys
import string
import re
import urllib

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic.list import ListView
from django.db.models.signals import post_save
from django.db.models import Sum, Count, Max, F
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from arkestrator.profiles.models import Profile
from arkestrator.events.models import Event
from arkestrator.events.forms import RSVPForm
from arkestrator.util import get_client_ip
from arkestrator.views import LoginRequiredMixin
from models import Thread, Post, LastRead, Favorite
import forms

from arkestrator.decorators import super_no_cache

THREADS_PER_PAGE = 101

class ThreadList(LoginRequiredMixin, ListView):

    template_name = "board/thread_list.html"
    paginate_by = THREADS_PER_PAGE
    queryset = Thread.objects.order_by(
            "-stuck","-last_post__id").select_related(
            "creator","last_post","last_post__creator","favorite")

    def get_context_data(self, **kwargs):
        """ set up extra context data """
        context = super(ThreadList, self).get_context_data(**kwargs)
        context['object_list'] = self.last_reads(context['object_list'],
                                                self.request.user)
        context['object_list'] = self.favorites(context['object_list'],
                                                self.request.user)

        return context

    def last_reads(self, thread_list, user):
        """ Annotate a queryset of threads with the last read status for a user.
            Add an unread boolean to each thread
            if it was read before add a last_post_read id
            :param: thread_list the list of threads to annotate
            :param: user the user who should be looked up.
        """

        last_read = LastRead.objects.filter(
                thread__in=thread_list,
                user = user).values('thread__id', 'post__id')
        last_viewed = dict((lr['thread__id'], lr['post__id']) for lr in last_read)
        for t in thread_list:
            try:
                t.unread = last_viewed[t.id] < t.last_post_id
                t.last_post_read = last_viewed[t.id]
            except KeyError:
                t.unread = True

        return thread_list

    def favorites(self, thread_list, user):
        """ annotate a queryset of threads with a users favorites """
        favs = Favorite.objects.filter(
                                thread__in=thread_list,
                                user=user).values('thread__id')

        for thread in thread_list:
            thread.fav = thread.id in favs
        return thread_list

class FavoritesList(ThreadList):
    """ subclass of ThreadList that displays the current users favorites """

    def get_queryset(self):
        return Thread.objects.filter(favorite=self.request.user)

class ThreadsByList(ThreadList):
    """ Thread list takes a single argument the user id of the user """

    def get_queryset(self):
        return Thread.objects.filter(creator_id = self.kwargs['by'])

@login_required
def view_thread(request,id,start=False,expand=False,hide=None):
    """ display thread  id for a user

        args:
        id: the thread id
        start:  the first post to show otherwise prefs and collapsing are used
        expand: show all posts in the thread
        hide:  hide images in the thread

    """
    thread = get_object_or_404(Thread,pk=id)
    try:
        event = Event.objects.get(thread=thread)
    except Event.DoesNotExist:
        event = None

    #try to make a new post in the thread
    if request.method == 'POST':
        if thread.locked:
            return HttpResponseRedirect(reverse('list-threads'))
        post = Post(
            thread = thread,
            creator = request.user,
            posted_from = get_client_ip(request)
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

    #try to collapse the thread appriately
    try:
        lastread = LastRead.objects.get(
            user = request.user,
            thread = thread
        )
        if not expand:
            coll_size = request.user.profile.collapse_size
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

    #hide images in the thread if appropriate
    try:
        if (not hide is False) and (hide or not request.user.profile.show_images):
            hide = True
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

    #if this is an event display it as such
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
    """  view a thread starting with post num post id """
    post = get_object_or_404(Post, pk=id)
    return view_thread(request, id=post.thread.id,start=id)
    

@login_required
@transaction.commit_on_success
def new_thread(request):
    """ create a new thead """
    if request.method == 'POST':
        thread = Thread(
            creator = request.user,
            site = Site.objects.get_current(),
        )
        post = Post(
            thread = thread,
            creator = request.user,
            posted_from = get_client_ip(request)
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
def thread_history(request,id=None):
    """ show who has read a thread and when they last did """
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
    """ if the user has permissions sticky thread id """
    thread = get_object_or_404(Thread,pk=id)
    if request.method == 'POST':
        if request.POST['sticky'] == 'sticky':
            thread.stuck = True
        elif request.POST['sticky'] == 'unsticky':
            thread.stuck = False
        thread.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
def mark_read(request):
    """ mark all threads on the first page read """
    if request.method == 'POST' and request.POST['confirm'] == 'true':
        queryset = Thread.objects.order_by("-stuck","-last_post")
        count = queryset.count()
        if count > THREADS_PER_PAGE:
            thread_list = queryset[0:THREADS_PER_PAGE]
        else:
            thread_list = queryset[0:count]
        for t in thread_list:
            try:
                lr = LastRead.objects.get(
                        user = request.user,thread = t)
                lr.timestamp = datetime.datetime.now()
                lr.post = t.last_post
            except LastRead.DoesNotExist:
                lr = LastRead(user = request.user,
                        thread = t,
                        post = t.last_post,
                        read_count = 0)
            lr.save()
    return HttpResponseRedirect(reverse('list-threads'))

class PostsByListView(LoginRequiredMixin, ListView):
    template_name = 'board/posts_by.html'
    paginate_by = 49

    @property
    def poster(self):
        return get_object_or_404(User, pk=self.kwargs['id'])

    def get_queryset(self):
        queryset = Post.objects.filter(creator=self.poster).order_by(
            '-created_at').select_related('thread__subject')
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(PostsByListView, self).get_context_data(**kwargs)
        ctx['poster'] = self.poster.username
        return ctx


@login_required
def get_quote(request, id):
    """ get a quote of post id """
    post = get_object_or_404(Post, pk=id)
    user = get_object_or_404(User, pk=post.creator.id)

    return render_to_response("board/get_quote.html", {
            'post': post,
            'user': user,
    })

@login_required
@permission_required('board.can_lock')
def lock_thread(request, id):
    """ lock thread id if the requester has perms"""
    thread = get_object_or_404(Thread,pk=id)
    if request.method == 'POST':
        if request.POST['lock'] == 'lock':
            thread.locked = True
        elif request.POST['lock'] == 'unlock':
            thread.locked = False
    thread.save()
    return HttpResponseRedirect(reverse('list-threads'))


@login_required
def favorite_thread(request, id):
    """ add thread id to the users favorited """
    thread = get_object_or_404(Thread,pk=id)
    if request.method == 'POST':
        if request.POST['fav'] == 'add':
            thread.favorite.add(request.user)
        elif request.POST['fav'] == 'remove':
            thread.favorite.remove(request.user)
    return HttpResponseRedirect(reverse('list-threads'))


class ThreadTitleSearchView(ListView):
    "lol search"

    paginate_by = 49
    template_name = 'board/thread_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadTitleSearchView, self).dispatch(*args, **kwargs)

    @property
    def query(self):
        return self.request.GET.get('query', 'rev is the best')

    def get_queryset(self):
        return Thread.objects.filter(subject__icontains=self.query).order_by('-last_post__id')

    def get_context_data(self, **kwargs):
        ctx = super(ThreadTitleSearchView, self).get_context_data(**kwargs)
        ctx['search_query'] = self.query
        ctx['paginator_query'] = urllib.urlencode({'query': self.query})
        return ctx

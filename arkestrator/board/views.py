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
from django.shortcuts import render_to_response,get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View
from django.db.models.signals import post_save
from django.db.models import Sum, Count, Max, F
from django.core.cache import cache
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User

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
        return Thread.objects.filter(favorite__user=self.request.user)

class ThreadsByList(ThreadList):
    """ Thread list takes a single argument the user id of the user """

    def get_queryset(self):
        return Thread.objects.filter(creator_id = self.args[0])

class PostList(LoginRequiredMixin, TemplateView):
    template_name = 'board/post_list.html'

    def get_context_data(self, **kwargs):
        thread_id = kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        start = kwargs.get('start', 0)
        expand = kwargs.get('expand', False)
        hide = kwargs.get('hide')

        posts = thread.post_set.order_by('id').select_related('creator')
        # TODO REGRESSION we broke re-collapsing; threads are collapsed correctly
        # and can then be "show all"'d but you can't collapse again. all of
        # that should be ported to query paramters, anyway, and this can be
        # fixed then.

        # TODO REGRESSION handle events

        # TODO get or create, yo
        lastread = LastRead(
            user=self.request.user,
            thread=thread,
            read_count=0)
        try:
            lastread = LastRead.objects.get(
                user=self.request.user,
                thread=thread)
        except LastRead.DoesNotExist:
            if event:
                cache.delete('event-count:%d'%(self.request.user.id))

        if not expand:
            collapse_size = self.request.user.get_profile().collapse_size
            # TODO we're literally fetching all the posts we *do not* want to display
            if start:
                temp_posts = posts.filter(pk__lte=start).reverse()
            else:
                temp_posts = posts.filter(created_at__lte=lastread.timestamp).reverse()
            if temp_posts.count() > collapse_size:
                post_start = temp_posts[collapse_size].id
                posts = posts.filter(pk__gte=post_start)
            else:
                expand = True

        posts = list(posts)

        try:
            # TODO clean this up
            if (not hide is False) and (hide or not self.request.user.get_profile().show_images):
                hide = True
        except ObjectDoesNotExist:
            pass

        lastread.timestamp = datetime.datetime.now()
        lastread.read_count += 1
        lastread.post = posts[-1]
        lastread.save()
        # This del is confusing; seems to interact with the instance_memcache
        # decorator.
        del thread.total_views

        fav = False
        if thread.favorite.filter(id=self.request.user.id):
            fav = True

        if len(posts)< 10:
            expand = True

        if not start and posts:
            start = posts[0].id

        ctx = {
            'object_list': posts,
            'thread': thread,
            'form': forms.PostForm(),
            'expand': expand,
            'hide': hide,
            'start': start,
            'fav': fav,
        }
        return ctx

    @transaction.commit_on_success
    def post(self, request, **kwargs):
        thread_id = kwargs['thread_id']
        thread = get_object_or_404(Thread, pk=thread_id)
        if thread.locked:
            return redirect(reverse('list-threads'))
        post = Post(
            thread = thread,
            creator = request.user,
            posted_from = get_client_ip(request)
        )
        form = forms.PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            request.posting_users.add_to_set(request.user.id)
            return redirect(reverse('list-threads'))
        return redirect(reverse('view-thread', args=[thread_id]))

class PostView(PostList):
    def get_context_data(self, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        kwargs['start'] = post.id
        kwargs['thread_id'] = post.thread.id
        return super(PostView, self).get_context_data(**kwargs)


class NewThreadView(LoginRequiredMixin, TemplateView):
    template_name ="board/new_thread.html"

    @transaction.commit_on_success
    def post(self, request, **kwargs):
        thread = Thread(
            creator=request.user,
            site=Site.objects.get_current(),
        )
        post = Post(
            thread=thread,
            creator=request.user,
            posted_from=get_client_ip(request)
        )
        thread_form = forms.ThreadForm(request.POST, instance=thread)
        post_form = forms.PostForm(request.POST, instance = post)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save()
            post.thread = thread
            post_form = forms.PostForm(request.POST, instance=post)
            post_form.save()
            request.posting_users.add_to_set(request.user.id)
            return redirect(reverse('list-threads'))
        else:
            return redirect(reverse('new-thread'))

    def get_context_data(self, **kwargs):
        return {
            'thread_form': forms.ThreadForm(),
            'post_form': forms.PostForm(),
        }


class ThreadHistoryView(LoginRequiredMixin, TemplateView):
    template_name='board/thread_history.html'

    def get_context_data(self, **kwargs):
        thread = get_object_or_404(Thread,pk=kwargs['thread_id'])

        queryset = LastRead.objects.filter(thread = thread).order_by("-timestamp")
        queryset = queryset.select_related('user')
        return {
            'thread': thread,
            'read_list': queryset.all(),
        }

class StickyView(LoginRequiredMixin, View):
    # TODO REGRESSION adapt permission_required for class view
    # @permission_required('board.can_sticky')
    def post(self, request, **kwargs):
        thread = get_object_or_404(Thread,pk=kwargs['thread_id'])
        if request.POST['sticky'] == 'sticky':
            thread.stuck = True
        elif request.POST['sticky'] == 'unsticky':
            thread.stuck = False
        thread.save()
        return redirect(reverse('list-threads'))


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


@login_required
def posts_by(request, id):
    """ list all posts by user id """
    poster = get_object_or_404(User,pk=id)
    queryset = Post.objects.filter(creator = poster).order_by(
        '-created_at').select_related('thread__subject')

    return list_detail.object_list(
            request,
            queryset = queryset,
            paginate_by = 49,
            template_name = "board/posts_by.html",
            extra_context = {"poster" : poster.username}
            )

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


@login_required
def lol_search(request):
    'lol search'

    query = request.GET.get('query', 'rev is the best')
    
    queryset = Thread.objects.filter(subject__icontains=query).order_by(
        '-last_post__id')
    
    return list_detail.object_list(
        request,
        queryset = queryset,
        template_object_name = 'thread',
        paginate_by = 49,
        template_name = "board/thread_list.html",
        extra_context = { 
            'search_query' : query,
            'paginator_query' : urllib.urlencode({ 'query' : query })
        },
    )


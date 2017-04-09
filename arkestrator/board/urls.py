from django.conf.urls.defaults import *


import views
import models

urlpatterns = patterns('',
    url(r"^$",views.ThreadList.as_view(), name='list-threads'),
    url(r"^threads/(?P<thread_id>\d+)/$",views.PostList.as_view(), name='view-thread'),

    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/$",
        views.PostList.as_view(),
        name='view-thread-start'),
    url(r"^threads/(?P<thread_id>\d+)/full/$",
        views.PostList.as_view(),{
        'expand' : True,
    }, name='view-thread-full'),
    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/full/$",views.PostList.as_view(),{
        'expand' : True,
    }, name='view-thread-full-start'),
    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/full/show/$",views.PostList.as_view(),{
        'expand' : True, 'hide' : False,
    }, name='view-thread-full-show'),
    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/full/hide/$",views.PostList.as_view(),{
        'expand' : True, 'hide' : True,
    }, name='view-thread-full-hide'),
    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/hide/$",views.PostList.as_view(),{
        'expand' : False, 'hide' : True,
    }, name='view-thread-hide'),
    url(r"^threads/(?P<thread_id>\d+)/(?P<start>\d+)/show/$",views.PostList.as_view(),{
        'expand' : False, 'hide' : False,
    }, name='view-thread-show'),

    url(r"^threads/(?P<thread_id>\d+)/sticky/$",
        views.StickyView.as_view(),
        name='sticky'),

    url(r"^threads/(?P<id>\d+)/lock/$",views.lock_thread,
        name='lock-thread'),

    url(r"^threads/(?P<thread_id>\d+)/history/$",
        views.ThreadHistoryView.as_view(),
        name='thread-history'),

    url(r"^threads/new/$",
        views.NewThreadView.as_view(),
        name='new-thread'),

    url(r"^threads/mark_read/$",
        views.MarkReadView.as_view(),
        name='mark-threads-read'),

    url(r"^profiles/(?P<by>\d+)/threads/$", views.ThreadsByList.as_view(),
            name='threads-by'),
    url(r"^profiles/(?P<id>\d+)/posts/$", views.posts_by,
            name='posts-by'),
    url(r"^posts/(?P<post_id>\d+)/$",views.PostView.as_view(), name='view-post'),
    url(r"^quote/(?P<id>\d+)/$", views.get_quote, name='get-quote'),
    url(r"^threads/(?P<id>\d+)/favorite/$", views.favorite_thread,
        name='favorite'),
    url(r"^threads/favorites/$", views.FavoritesList.as_view(),
            { 'fav' : True }, name='favorite-list'),
    url(r"^threads/search/$", views.lol_search, name='search-threads'),
)

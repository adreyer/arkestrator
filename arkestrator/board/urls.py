from django.conf.urls import patterns, url


import views
import models

urlpatterns = patterns('',
    url(r"^$",views.ThreadList.as_view(), name='list-threads'),
    url(r"^threads/(?P<id>\d+)/$",views.view_thread,name='view-thread'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/$",views.view_thread,
        name='view-thread-start'),
    url(r"^threads/(?P<id>\d+)/full/$",views.view_thread,{
        'expand' : True,
    }, name='view-thread-full'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/full/$",views.view_thread,{
        'expand' : True,
    }, name='view-thread-full-start'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/full/show/$",views.view_thread,{
        'expand' : True, 'hide' : False,
    }, name='view-thread-full-show'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/full/hide/$",views.view_thread,{
        'expand' : True, 'hide' : True,
    }, name='view-thread-full-hide'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/hide/$",views.view_thread,{
        'expand' : False, 'hide' : True,
    }, name='view-thread-hide'),
    url(r"^threads/(?P<id>\d+)/(?P<start>\d+)/show/$",views.view_thread,{
        'expand' : False, 'hide' : False,
    }, name='view-thread-show'),
    url(r"^threads/(?P<id>\d+)/sticky/$",views.sticky,
        name='sticky'),
    url(r"^threads/(?P<id>\d+)/lock/$",views.lock_thread,
        name='lock-thread'),
    url(r"^threads/(?P<id>\d+)/history/$",views.thread_history,
        name='thread-history'),
    url(r"^threads/new/$",views.new_thread,name='new-thread'),
    url(r"^threads/mark_read/$",views.mark_read,name='mark-threads-read'),
    url(r"^profiles/(?P<by>\d+)/threads/$", views.ThreadsByList.as_view(),
            name='threads-by'),
    url(r"^profiles/(?P<id>\d+)/posts/$", views.PostsByListView.as_view(),
            name='posts-by'),
    url(r"^posts/(?P<id>\d+)/$",views.view_post,name='view-post'),
    url(r"^quote/(?P<id>\d+)/$", views.get_quote, name='get-quote'),
    url(r"^threads/(?P<id>\d+)/favorite/$", views.favorite_thread,
        name='favorite'),
    url(r"^threads/favorites/$", views.FavoritesList.as_view(),
            { 'fav' : True }, name='favorite-list'),
    url(r"^threads/search/$", views.ThreadTitleSearchView.as_view(), name='search-threads'),
)

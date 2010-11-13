import datetime
import calendar

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User

from mdc3.board.views import view_thread

from models import Event, Market
import forms


@login_required
def view_event(request, ev_id):
    """ view event ev_id """
    event = get_object_or_404(Event,pk=ev_id)
    return view_thread(request,event.thread.id)

@login_required
def list_events(request, upcoming=True, local=True):
    """ list events 
         
        args:
        upcoming: if true only future events will be listed
        local:    if true only events in the users market or
                   events where all_markets are true will be 
                   shown
    """

    queryset = Event.objects.all()
    if upcoming:
        queryset = queryset.filter(time__gte=datetime.datetime.now)
        
    usr_mrk = request.user.get_profile().market
    if usr_mrk:
        if local:
            queryset = queryset.filter(Q(
                Q(market=usr_mrk) | Q(all_markets=True)))
    queryset = queryset.order_by('time')

    request.user.get_profile().last_events_view = datetime.datetime.now()
    request.user.get_profile().save()
    cache.delete('event-count:%d'%(request.user.id))
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 50,
        extra_context={
            'upcoming' : upcoming,
            'local' : local,
            }
        )


@login_required
def new_event(request):
    """ 
        create a new event

    """

    if request.method =='POST':
        form = forms.NewEventForm(request.POST)
        if form.is_valid():
            event = form.save(request.user)
            return HttpResponseRedirect(reverse('list-threads'))
    else:
        form = forms.NewEventForm()
    return render_to_response('events/new_event.html',
        {
            'form': form,
        },
        context_instance = RequestContext(request))

@login_required
def edit_event(request, ev_id):
    """   edit event ev_id

          only available to the events creator or
          users with the events.can_edit permissions
    """
    event = get_object_or_404(Event,pk=ev_id)
    if not request.user.has_perm('events.can_edit'):
        if not event.creator == request.user:
            return Http404
    if request.method =='POST':
        form = forms.EditEventForm(request.POST,
                    instance = event)
        if form.is_valid():
            form.save()
            if event.thread.subject != event.title:
                event.thread.subject = event.title
                event.thread.save()
        return HttpResponseRedirect(reverse('view-thread',
                        args=[event.thread.id]))
    else:
        form = forms.EditEventForm(instance = event)
    return render_to_response('events/edit_event.html',
                { 'form' : form ,
                  'event' : event},
                context_instance = RequestContext(request))                      
    
@login_required
def update_rsvp(request, ev_id):
    """ update a users rsvp for ev_id  
        
        should be called from submit with RSVPForm
    """
    event = get_object_or_404(Event,pk=ev_id)
    if request.method == 'POST':
        form = forms.RSVPForm(request.POST)
        if form.is_valid():
            form.save(request.user,event)
            return HttpResponseRedirect(reverse('view-thread',
                        args=[event.thread.id]))
    return view_thread(request, event.thread.id, rsvp_form=form)

    
    
def calendar(request, mstring=None, local=True):
    """     NOT FULLY IMPLEMENTED
            display a months events in calendar format
            

            args:
            mstring = a string of the month  mm-yy
                        if not included the current month will be displayed
            local =   if True only events from the users 
                      market will be displayed
    """

    month = None
    year = None
    date = datetime.date.today()
    if mstring is None:
        month = tday.month
        year = tday.year
    else:
        try:
            month, year = date.split('-')
            month = int(month)
            year = int(year)
            date = datetime.date(year, month, 1)
        except ValueError:
            return Http404
    cal = calendar.monthcalendar(year,month)
    events = Event.objects.filter(time__year=year,
                time__month=month)
    usr_mrk = request.user.get_profile().market
    if usr_mrk:
        if local:
            events = events.filter(Q(
                Q(market=usr_mrk) | Q(all_markets=True)))
    events = events.order_by('time')
    ecounter = 0
    for week in cal:
        for day in week:
            if day == 0:
                day = [0,[]]
            else:
                evs = []
                while ecounter < events.count() and day == events[ecounter].time.day:
                    evs.append(events[ecounter])
                day = [day,evs]
    
    return render_to_response('events/calendar.html',
                { 'cal' : cal,
                  'month' : month,
                  'year' : year,
                },
                context_instance = RequestContext(request))
    
    
   

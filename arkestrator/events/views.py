import datetime
import calendar
import pytz

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.views.generic.list import ListView
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from arkestrator.board.views import view_thread

from models import Event, Market
import forms

class EventListView(ListView):
    paginate_by=50

    @property
    def upcoming(self):
        return self.kwargs.get('upcoming', True)

    @property
    def local(self):
        return self.kwargs.get('local', True)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        request = self.request
        queryset = Event.objects.all()
        if self.upcoming:
            queryset = queryset.filter(time__gte=datetime.datetime.now())

        usr_mrk = request.user.profile.market
        if usr_mrk:
            if self.local:
                queryset = queryset.filter(Q(
                    Q(market=usr_mrk) | Q(all_markets=True)))
        queryset = queryset.order_by('time')

        request.user.profile.last_events_view = datetime.datetime.now()
        request.user.profile.save()
        cache.delete('event-count:%d'%(request.user.id))
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(EventListView, self).get_context_data(**kwargs)
        ctx['upcoming'] = self.upcoming
        ctx['local'] = self.local
        return ctx


@login_required
def view_event(request, ev_id):
    """ view event ev_id """
    event = get_object_or_404(Event,pk=ev_id)
    return view_thread(request,event.thread.id)

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
    return render(request, 'events/new_event.html',
        {'form': form})

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
            form.save(event)
        return HttpResponseRedirect(reverse('view-thread',
                        args=[event.thread.id]))
    else:
        utc = pytz.timezone('UTC')
        ltz = pytz.timezone(event.market.timezone)
        local_time = utc.localize(event.time)
        local_time = local_time.astimezone(ltz)
        form = forms.EditEventForm(
            initial={ 'time' : local_time,
                        'title' : event.thread.subject, },
            instance = event)
    return render(request, 'events/edit_event.html',
                { 'form' : form ,
                  'event' : event})
    
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
    return view_thread(request, event.thread.id)

    
    
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
    usr_mrk = request.user.profile.market
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
    
    return render(request, 'events/calendar.html',
                { 'cal' : cal,
                  'month' : month,
                  'year' : year,
                })
    
    
   

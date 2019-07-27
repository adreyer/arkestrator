import datetime
from django.core.cache import cache

from arkestrator.board.models import LastRead, Thread
from arkestrator.profiles.models import Profile
from models import Event

def new_events(request):
    """ returns the number of new events
        
        The number of new events since the last time the user visited
        the events list with the exception of events whose thread
        they have read.

        new events don't show up immediately
    """
        
    if request.user.is_authenticated():
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return{ 'new_events' : 0 }
        cache_key = 'event-count:%d'%(request.user.id)
        event_count =  cache.get(cache_key, None)
        if event_count is None:
            event_count = 0
            new_events = Event.objects.filter(
                created_at__gte=profile.last_events_view,
                time__gte=datetime.datetime.now()
                ).select_related('thread')
            for event in new_events:
                try:
                    LastRead.objects.get(user=request.user,thread=event.thread)

                except LastRead.DoesNotExist:
                    event_count += 1
            cache.set(cache_key, event_count)
        return{ 'new_events' : event_count }
    return{ 'new_events' : 0 }

import datetime
from django.core.cache import cache

from mdc3.board.models import LastRead, Thread
from models import Event

def new_events(request):
##    print 'context processor'
##    if request.user.is_authenticated():
##        cache_key = 'event-count:%d'%(request.user.id)
##        event_count =  cache.get(cache_key, None)
##        if event_count is None:
##            event_count = 0
##            new_events = Event.objects.filter(
##                created_at__gte=request.user.get_profile().last_events_view,
##                time__gte=datetime.datetime.now()
##                ).select_related('thread')
##                
##            for event in new_events:
##                try:
##                    LastRead.objects.get(user=request.user,thread=event.thread)
##                except LastRead.DoesNotExist:
##                    event_count += 1
##            cache.set(cache_key, event_count)
##        return{ 'new_events' : event_count }
    return{ 'new_events' : 0 }

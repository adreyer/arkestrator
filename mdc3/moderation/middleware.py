import datetime
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from models import Ban

class BanMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        banned = Ban.objects.filter(user=request.user,
                                end__gte=datetime.datetime.now,
                                start__lte=datetime.datetime.now)
        if banned:
            return HttpResponseRedirect(reverse('ban-page'))
            

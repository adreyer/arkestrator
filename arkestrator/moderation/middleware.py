import datetime
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .models import Ban
from .views import ban_page

class BanMiddleware(object):
    def process_view(self, request, view, args, kwargs):
        if request.user.is_authenticated():
            banned = Ban.objects.filter(user=request.user,
                                end__gte=datetime.datetime.now(),
                                start__lte=datetime.datetime.now())
            if banned:
                return ban_page(request,banned)
            

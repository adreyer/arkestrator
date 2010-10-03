from django.contrib.sites.models import Site

from mdc3.util.cache_set import TimedCacheSet

class OnlineUsersMiddleware(object):
    def process_request(self, request):
        cache_key_base = "users-online:%d"%Site.objects.get_current().id
        tcs = TimedCacheSet(cache_key_base)

        if not request.user.is_anonymous():
            tcs.add_to_set(request.user.id)

        request.online_users = tcs.full_set


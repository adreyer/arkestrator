from django.contrib.sites.models import Site

from mdc3.util.cache_set import TimedCacheSet

class OnlineUsersMiddleware(object):
    def process_request(self, request):
        tcs = TimedCacheSet("online-users")

        if not request.user.is_anonymous():
            tcs.add_to_set(request.user.id)

        request.online_users = tcs


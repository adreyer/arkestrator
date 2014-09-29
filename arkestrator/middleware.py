from django.contrib.sites.models import Site

from arkestrator.util.cache_set import TimedCacheSet

class OnlineUsersMiddleware(object):
    """ update the cache with the number of users online """
    def process_request(self, request):
        tcs = TimedCacheSet("online-users")

        if not request.user.is_anonymous():
            tcs.add_to_set(request.user.id)

        request.online_users = tcs


import datetime

from django.contrib.sites.models import Site
from django.core.cache import cache

class OnlineUsersMiddleware(object):
    def process_request(self, request):
        curr = datetime.datetime.now()
        prev = curr - datetime.timedelta(seconds = 60)

        cache_key_base = "users-online:%d:%%s"%Site.objects.get_current().id

        curr_key = cache_key_base % curr.strftime("%H:%M")
        prev_key = cache_key_base % prev.strftime("%H:%M")

        curr_set = cache.get(curr_key, set())
        prev_set = cache.get(prev_key, set())

        if not request.user.is_anonymous() and request.user.id not in curr_set:
            curr_set |= set([request.user.id])
            cache.set(curr_key, curr_set, 60)

        user_set = prev_set | curr_set

        request.online_users = user_set


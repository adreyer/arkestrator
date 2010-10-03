from mdc3.util.cache_set import TimedCacheSet

class PostingUsersMiddleware(object):
    def process_request(self, request):
        request.posting_users = TimedCacheSet("posting-users")


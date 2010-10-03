from mdc3.util.cache_set import TimedCacheSet

class PostingUsersMiddleware(object):
    def process_request(self, request):
        tcs = TimedCacheSet("posting-users")

        request.posting_users = tcs.full_set
        

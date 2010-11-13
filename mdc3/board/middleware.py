from mdc3.util.cache_set import TimedCacheSet

class PostingUsersMiddleware(object):
    """ the users who are currently posting """
    def process_request(self, request):
        request.posting_users = TimedCacheSet("posting-users")


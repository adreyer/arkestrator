from django.core.cache import cache
from django.core.urlresolvers import reverse

class BetterCacher(object):
    def __init__(self, urlname, duration, fn):
        self.urlname = urlname
        self.duration = duration
        self.fn = fn

    def __call__(self, request, *args, **kwargs):
        if request.method != 'GET':
            return self.fn(request,*args, **kwargs)

        key = request.path
        response = cache.get(key, None)
        if response is None:
            response = self.fn(request, *args, **kwargs)
            cache.set(key, response, self.duration)
        return response

    def invalidate(self, *args, **kwargs):
        cache.delete(reverse(self.urlname, args=args, kwargs=kwargs))

def better_cache(urlname, duration):
    def _better_cache(fn):
        return BetterCacher(urlname, duration, fn)
    return _better_cache


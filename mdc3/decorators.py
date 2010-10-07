from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test
from mdc3.profiles.models import Profile

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

class InstanceMethodCache(property):
    def __init__(self, key, fn, timeout=None):
        self.key = key
        self.fn = fn
        self.timeout = timeout

    def __get__(self,instance,owner):
        instance_cache = getattr(instance, '_instance_cache', {})
        result = instance_cache.get(self.key)
        if result is None:
            key = "%s:%d"%(self.key, instance.id)
            result = cache.get(key, None)
            if result is None:
                result = self.fn(instance)
                if self.timeout:
                    cache.set(key, result, self.timeout)
                else:
                    cache.set(key, result)
        instance_cache[self.key] = result
        instance._instance_cache = instance_cache

        return result

    def __delete__(self, instance): # epic haxx
        key = "%s:%d"%(self.key, instance.id)
        cache.delete(key)
        instance_cache = getattr(instance, '_instance_cache', {})

        try:
            del instance_cache[self.key]
        except KeyError:
            pass

def instance_memcache(key, timeout=None):
    """This decorator takes a key and expects to be used on an instance method
    with no parameters.  It sticks the id of the instance at the end of the
    key and uses that as a cache key for getting/setting data in memcache.

    It overrides the del statement to clear the cache.
    """
    def _instance_memcache(fn):
        return InstanceMethodCache(key, fn, timeout)
    return _instance_memcache

def super_no_cache(fn):
    def _super_no_cache(*args, **kwargs):
        response = fn(*args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        return response
    return _super_no_cache

def moderator_required(redirect_field='/'):
    lamd

from django.core.cache import cache

from mdc3.profiles.models import Profile


def is_mod(request):
    if request.user.is_authenticated():
        cache_key = "is-mod:%d"%(
            request.user.id,
        )
        is_mod = cache.get(cache_key, None)
        if is_mod is None:
            is_mod = Profile.objects.get(user=request.user).moderator
            cache.set(cache_key, is_mod)
            return { 'is_mod': is_mod }
    else:
        return { 'is_mod': False }

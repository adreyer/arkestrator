from django.core.cache import cache

from mdc3.profiles.models import Profile


def is_mod(request):
    if request.user.is_authenticated():
        is_mod = Profile.objects.get(user=request.user).moderator
        return { 'is_mod': is_mod }
    else:
        return { 'is_mod': False }

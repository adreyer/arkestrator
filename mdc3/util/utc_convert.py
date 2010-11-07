from datetime import timedelta

from django.contrib.auth.models import User
from mdc3.board.models import Post, LastRead
from mdc3.pms.models import PM
from mdc3.profiles.models import Profile
from mdc3.themes.models import Theme

def utc_convert(delta_num=4):
    delta = timedelta(delta_num)
    themes = Theme.objects.all()
    for theme in themes:
        theme.updated += delta
        theme.save()

    profs = Profile.objects.all()
    for prof in profs:
        prof.last_login += delta
        prof.last_view += delta
        prof.last_post += delta
        prof.last_profile_update += delta
        prof.save()

    pms = PM.objects.all()
    for pm in pms:
        pm.created_at += delta
        pm.save()

    posts = Post.objects.all()
    for post in posts:
        post.created_at += delta
        post.save()

    lrs = LastRead.objects.all()
    for lr in lrs:
        lr.timestamp += delta
        lr.save()

    users = User.objects.all()
    for user in users:
        user.date_joined += delta
        user.save()
        

from datetime import timedelta, datetime

from django.contrib.auth.models import User
from arkestrator.board.models import Post, LastRead
from arkestrator.pms.models import PM
from arkestrator.profiles.models import Profile
from arkestrator.themes.models import Theme



def utc_convert():
    delta1 = timedelta(5)
    delta2 = timedelta(4)
    cutoff = datetime(2010,11,7,1)
    
    print('converting themes')
    themes = Theme.objects.all()
    for theme in themes:
        theme.updated += delta2
        theme.save()

    print('converting profiles')
    profs = Profile.objects.all()
    for prof in profs:
        prof.last_login += delta2
        prof.last_view += delta2
        prof.last_post += delta2
        prof.last_profile_update += delta2
        prof.save()

    print('converting dst pms')
    pms = PM.objects.filter(created_at__lte=cutoff)
    for pm in pms:
        pm.created_at += delta1
        pm.save()

    print('converting std pms')
    pms = PM.objects.filter(created_at__gte=cutoff)
    for pm in pms:
        pm.created_at += delta2
        pm.save()

    print('converting dst posts')
    posts = Post.objects.filter(created_at__lte=cutoff)
    for post in posts:
        post.created_at += delta1
        post.save()

    print('converting std posts')
    posts = Post.objects.filter(created_at__lte=cutoff)
    for post in posts:
        post.created_at += delta2
        post.save()

    print('converting last reads')
    lrs = LastRead.objects.all()
    for lr in lrs:
        lr.timestamp += delta2
        lr.save()

    print('converting users')
    users = User.objects.all()
    for user in users:
        user.date_joined += delta1
        user.save()
        

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.base import RequestContext

@login_required
def active_users(request):
    posting = getattr(request, 'posting_users', set())
    online = getattr(request, 'online_users', set())

    user_list = User.objects.filter(id__in=online).all()
    for user in user_list:
        if user.id in posting:
            user.is_posting = True
        else:
            user.is_posting = False

    return render(request, "util/active_users.html", {
        'user_list' : user_list,
        })
        

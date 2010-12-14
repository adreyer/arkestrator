from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

#using can_lock is temporary till moderation has some models
@permission_required('board.can_lock')
def ban_user(request, id=None):
    """ display a list of users to ban or ban/unban user id """
    if id:
        user = get_object_or_404(User,pk=id)
        if request.method == 'POST':
            if request.POST['ban'] == 'ban':
                user.is_active = False
                user.save()
            elif request.POST['ban'] == 'unban':
                user.is_active = True
                user.save()
            return HttpResponseRedirect(reverse('ban'))

    queryset = User.objects.user_list = User.objects.exclude(
            profile__isnull=True).order_by('is_active','username')

    return render_to_response("moderation/ban.html",
            { 'user_list' : queryset },
            context_instance = RequestContext(request))

@permission_required('board.can_lock')
def mod_panel(request):
    return render_to_response("moderation/mod_panel",
        context_instance = RequestContext(request))

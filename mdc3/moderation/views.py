from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from forms import BanForm
from models import Ban

#using can_lock is temporary till moderation has some models
@permission_required('moderation.can_ban')
def ban_user(request):
    """ display a list of users to ban or ban/unban user id """
    if request.method == 'POST':
        ban = Ban(creator=request.user)
        form = BanForm(request.POST,instance=ban)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ban-list'))

    else:
        form = BanForm()

    return render_to_response("moderation/ban.html",
            { 'form' : form, },
            context_instance = RequestContext(request))


@permission_required('moderation.can_ban')
def ban_list(request):
    queryset = Ban.objects.all()
    return render_to_response('moderation/ban_list.html',
        { 'object_list' : queryset,},
        context_instance = RequestContext(request))

@permission_required('moderation.can_ban')
def mod_panel(request):
    return render_to_response("moderation/mod_panel",
        context_instance = RequestContext(request))

def ban_page(request, bans):
    return render_to_response("moderation/ban_page.html",
            { 'ban' : bans[0] },
            context_instance = RequestContext(request))

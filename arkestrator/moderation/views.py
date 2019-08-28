from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

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

    return render(request, "moderation/ban.html",
            { 'form' : form, })


@permission_required('moderation.can_ban')
def ban_list(request):
    queryset = Ban.objects.all()
    return render(request, 'moderation/ban_list.html',
        { 'object_list' : queryset,})

@permission_required('moderation.can_ban')
def mod_panel(request):
    return render(request, "moderation/mod_panel")

def ban_page(request, bans):
    return render(request, "moderation/ban_page.html",
            { 'ban' : bans[0] })

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from mdc3.invites.models import Invite

import forms

@login_required
def new_invite(request):
    if request.method == 'POST':
        form = forms.NewInviteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect("/")
    else:
        form = forms.NewInviteForm()
        return render_to_response("invites/new_invite.html",
            { 'form' : form },
            context_instance = RequestContext(request))
    

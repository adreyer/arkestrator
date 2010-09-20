from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from mdc3.invites.models import Invite
from mdc3.profiles.models import Profile

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


def register(request,code):
    invite = get_object_or_404(Invite,invite_code=code)
    if invite.used:
        return HttpResponse("THIS INVITE IS USED OR EXPIRED")
    temp_profile = Profile(
            ip_signup = request.META['REMOTE_ADDR'],
            invite_used = invite)
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        profile_form = forms.ProfileRegistrationForm(request.POST,
                instance=temp_profile)
        if user_form.is_valid():
            if profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                temp_profile.user = user
                profile_form = forms.ProfileRegistrationForm(request.POST,
                instance=temp_profile)
                profile_form.save(user)
##                invite.used = True
##                invite.save()
                return HttpResponseRedirect("/")

    user_form = forms.UserRegistrationForm()
    profile_form = forms.ProfileRegistrationForm(
            instance = temp_profile)
    return render_to_response ("invites/register.html",
        { 'user_form' : user_form,
          'profile_form' : profile_form,
          'code' : code },
         context_instance = RequestContext(request))
    

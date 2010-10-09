from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.views.generic import list_detail
from django.core.cache import cache

import datetime
import time

from mdc3.invites.models import Invite
from mdc3.profiles.models import Profile
from mdc3.decorators import moderator_required
import forms

@login_required
def new_invite(request):
    if request.method == 'POST':
        form = forms.NewInviteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            cache.delete('inv_count')
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
        if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                #this is really ugly at the least add a
                #password feild not attached to the model
                #then clean them and set
                user.set_password(user_form.cleaned_data["pass2"])
                user.groups.add(2)
                user.save()
                temp_profile.user = user
                profile_form = forms.ProfileRegistrationForm(request.POST,
                instance=temp_profile)
                profile_form.save(user)
                invite.used = True
                invite.save()
                return HttpResponseRedirect("/")
    else:
        user_form = forms.UserRegistrationForm()
        profile_form = forms.ProfileRegistrationForm(
                instance = temp_profile)
    return render_to_response ("invites/register.html",
        { 'user_form' : user_form,
          'profile_form' : profile_form,
          'code' : code },
         context_instance = RequestContext(request))
    

@login_required
@permission_required('invites.can_approve','/')
def invite_list(request):
    queryset = Invite.objects.filter(rejected=False,
            approved=False).order_by('-created_on')
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 10)

@login_required
@permission_required('invites.can_approve','/')
def approve_invite(request, id):
    inv = get_object_or_404(Invite,id=id)
    if not inv.approved:
        inv.approved = True
        if inv.rejected:
            inv.rejected=False
        inv.approved_on = datetime.datetime.now()
        inv.approved_by = request.user
        inv.invite_code = str(abs(hash(time.time())))
        invite_url = 'http://mdc3.mdc2.org/invites/' + inv.invite_code
        send_mail(subject='Welcome to MDC',
                message="""
Welcome to MDC. Use the link below to create your account
<a href=\"""" + invite_url + '\">' + invite_url + '</a>',
                from_email = 'cmr@mdc2.org',
                recipient_list = [inv.invitee],
                fail_silently=False)
        cache.delete('inv_count')
        inv.save()
    return HttpResponseRedirect("/invites/")

@login_required
@permission_required('invites.can_approve','/')
def reject_invite(request, id):
    inv = get_object_or_404(Invite,id=id)
    if not inv.rejected:
        inv.rejected = True
        inv.approved_on = datetime.datetime.now()
        inv.approved_by = request.user
        cache.delete('inv_count')
        inv.save()
    return HttpResponseRedirect("/invites/")

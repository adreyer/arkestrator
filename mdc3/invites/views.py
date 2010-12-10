import datetime
import time
import hashlib

from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.views.generic import list_detail
from django.core.cache import cache
from django.core.urlresolvers import reverse

from mdc3.invites.models import Invite
from mdc3.profiles.models import Profile
from mdc3.decorators import moderator_required
import forms

@login_required
def invite_list(request):
    """ if the user has perms list all open invites """
    if request.method == 'POST':
        form = forms.NewInviteForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            cache.delete('inv_count')
            return HttpResponseRedirect(reverse('list-threads'))
    else:
        form = forms.NewInviteForm()

    queryset = Invite.objects.filter(rejected=False,
        approved=False).order_by('-created_on')
    return list_detail.object_list(
        request,
        queryset = queryset,
        paginate_by = 10,
        extra_context={
            'form':form,
        })



def register(request,code):
    """ register a new user with invite_code code 404 bad codes """
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
                user.set_password(user_form.cleaned_data["pass2"])
                user.groups.add(Group.objects.get(name='everyone').id)
                user.save()
                temp_profile.user = user
                profile_form = forms.ProfileRegistrationForm(request.POST,
                instance=temp_profile)
                profile_form.save(user)
                invite.used = True
                invite.save()
                return HttpResponseRedirect(reverse('list-threads'))
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
def approve_invite(request, id):
    """ approve and invite if the requester has perms """
    inv = get_object_or_404(Invite,id=id)
    if request.method == 'POST' and request.POST['confirm'] == 'true':
        if not inv.approved:
            inv.approved = True
            if inv.rejected:
                inv.rejected=False
            inv.approved_on = datetime.datetime.now()
            inv.approved_by = request.user
            inv.invite_code = hashlib.sha224(str(time.time())).hexdigest()[:16]
            invite_url = 'http://board.mdc2.org/invites/' + inv.invite_code
            send_mail(subject='Welcome to MDC',
                    message="""
Welcome to MDC. Use the link below to create your account
""" + invite_url,
                    from_email = 'cmr@mdc2.org',
                    recipient_list = [inv.invitee],
                    fail_silently=False)
            cache.delete('inv_count')
            inv.save()
    return HttpResponseRedirect(reverse('list-threads'))

@login_required
@permission_required('invites.can_approve','/')
def reject_invite(request, id):
    """ reject and invite if the requester has perms """
    if request.method =='POST' and request.POST['confirm'] == 'true':
        inv = get_object_or_404(Invite,id=id)
        if not inv.rejected:
            inv.rejected = True
            inv.approved_on = datetime.datetime.now()
            inv.approved_by = request.user
            cache.delete('inv_count')
            inv.save()
    return HttpResponseRedirect(reverse("list-threads"))

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import Profile
from mdc3.board.models import LastRead

import forms


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    profile = get_object_or_404(Profile,user=user)
    if request.user != user:
        profile.profile_views += 1
        profile.save()
    last_seen = LastRead.objects.filter(user=user).order_by(
            '-timestamp')[0].timestamp
    return render_to_response("profiles/view_profile.html",
        {   'view_user' : user,
            'view_profile' : profile,
            'last_seen' : last_seen},
        context_instance = RequestContext(request))


@login_required
def list_profiles(request):
    profile_list = User.objects.all().order_by('date_joined')
    return render_to_response("profiles/list_profiles.html",
        { 'profile_list' : profile_list }, 
        context_instance = RequestContext(request))

@login_required
def edit_info(request):
    if request.method == 'POST':
        profile_form = forms.InfoProfileForm(request.POST,
                instance=Profile.objects.get(user=request.user))
        if profile_form.is_valid(): 
            profile_form.save()
            return HttpResponseRedirect("/")
    else:
        profile_form = forms.InfoProfileForm(
                    instance=Profile.objects.get(user=request.user))
        
    return render_to_response("profiles/edit_info.html",
                { 'profile_form' : profile_form },
                context_instance = RequestContext(request))
    
    
@login_required
def edit_prefs(request):
    if request.method == 'POST':
        prefs_form = forms.PrefsForm(request.POST,
                instance=Profile.objects.get(user=request.user))
        if prefs_form.is_valid(): 
            prefs_form.save()
            return HttpResponseRedirect("/")
    else:
        prefs_form = forms.PrefsForm(
                    instance=Profile.objects.get(user=request.user))
        
    return render_to_response("profiles/edit_prefs.html",
                { 'prefs_form' : prefs_form },
                context_instance = RequestContext(request))
    

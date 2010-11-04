from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from mdc3.themes.models import Theme
from models import Profile
import forms


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User,pk=user_id)
    profile = get_object_or_404(Profile,user=user)
    if request.user != user:
        profile.profile_views += 1
        profile.save()
    return render_to_response("profiles/view_profile.html",
        {   'view_user' : user,
            'view_profile' : profile,
        },
        context_instance = RequestContext(request))


@login_required
def list_users(request):
    user_list = User.objects.exclude(
        profile__isnull=True).order_by('date_joined')
    return render_to_response("profiles/list_users.html",
        { 'user_list' : user_list }, 
        context_instance = RequestContext(request))

@login_required
def edit_info(request):
    prof = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile_form = forms.InfoProfileForm(request.POST,
                instance=prof)
        if profile_form.is_valid(): 
            profile_form.save()
            #there must be a better way to do this
            purl = '/profiles/' + str(request.user.id)
            return HttpResponseRedirect(prof.get_absolute_url())
    else:
        profile_form = forms.InfoProfileForm(
                    instance=prof)
        
    return render_to_response("profiles/edit_info.html",
                { 'profile_form' : profile_form },
                context_instance = RequestContext(request))
    
    
@login_required
def edit_prefs(request):
    prof = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        prefs_form = forms.PrefsForm(request.POST,
                instance=prof)
        if prefs_form.is_valid(): 
            prefs_form.save()
            return HttpResponseRedirect(prof.get_absolute_url())
    else:
        prefs_form = forms.PrefsForm(instance=prof)
        
    return render_to_response("profiles/edit_prefs.html",
                {   
                    'prefs_form' : prefs_form },
            context_instance = RequestContext(request))
    

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect,  HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
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
        {   'user' : user,
            'profile' : profile },
        context_instance = RequestContext(request))


@login_required
def list_profiles(request):
    profile_list = User.objects.all()
    return render_to_response("profiles/list_profiles.html",
        { 'profile_list' : profile_list }, 
        context_instance = RequestContext(request))

@login_required
def edit_info(request):
    if request.method == 'POST':
        user_form = forms.InfoUserForm(request.POST, instance=request.user)
        profile_form = forms.InfoProfileForm(request.POST,
                instance=Profile.objects.get(user=request.user))
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect("/")  
        
    else:
        user_form = forms.InfoUserForm(instance=request.user)
        profile_form = forms.InfoProfileForm(
                    instance=Profile.objects.get(user=request.user))
 
    return render_to_response("profiles/edit_info.html",
                { 'user_form' : user_form,
                  'profile_form' : profile_form},
                context_instance = RequestContext(request))
    
    

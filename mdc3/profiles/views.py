from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
##from mdc3.profiles.models import Profile



def view_profile(request, user_id):
    profile = get_object_or_404(User,pk=user_id)
    return render_to_response("profiles/view_profile.html",
        { 'profile' : profile },
        context_instance = RequestContext(request))

def list_profiles(request):
    profile_list = User.objects.all()
    return render_to_response("profiles/list_profiles.html",
        { 'profile_list' : profile_list }, 
        context_instance = RequestContext(request))

##def edit_prefs(request):
##    if request.method == 'POST':
##        form = forms.PrefForm(request.POST)
##        if form.is_valid():
##            form.save(request.user)
##            return HttpResponseRedirect("/")
##        else:
##            form = forms.ThreadForm()
##        #does this get the users profile and user models?
##        #is there a better way to pre-populate the form
##        profile = get_object_or_404(models.Profile,pk=request.user)
##        user = get_object_or_404(models.User,pk=request.user)
##        return render_to_response("profiles/edit_prefs.html",
##            { 'profile' : profile, 'user' : User },
##            context_instance = RequestContext(request))
    

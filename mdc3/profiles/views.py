from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


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

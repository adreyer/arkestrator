from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail

from models import PM, Recipient
from django.contrib.auth.models import User
import forms

@login_required
def new_pm(request):
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect("/pms/inbox")
    else:
        form =forms.NewPMForm()
    return render_to_response('pms/new_pm.html',
            { 'form' : form },
            context_instance = RequestContext(request))


@login_required
def outbox(request):
    pm_list = PM.objects.filter(sender=request.user).order_by('-created_on')
    return render_to_response('pms/box.html',
            { 'pm_list' : pm_list,
              'box_type' : 'outbox' },
            context_instance = RequestContext(request))

@login_required
def inbox(request):
    pm_list = PM.objects.filter(recipients=request.user).order_by('-created_on')
    read_list = []
    for pm in pm_list:
        read_list.append(Recipient.objects.get(
                recipient=request.user,
                message=pm).read) 
    return render_to_response('pms/inbox.html',
            { 'pm_list' : pm_list,
              'read_list' : read_list,
              'box_type' : 'inbox' },
            context_instance = RequestContext(request))

@login_required
def mark_all_read(request):
    unread_list = Recipients.objects.filter(user=request.user,read=false)
    for rec in unread_list:
        rec.read = True
        rec.save()
    return HttpResponseRedirect("/pms/inbox")

@login_required
def view_pm(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)
    if pm.sender != request.user:
        read = get_object_or_404(Recipient,message=pm,recipient=request.user)
        print 'verified shit'
        if not read.read:
            print unread
            read.read = True
            read.save()
    form =forms.NewPMForm()
    return render_to_response("pms/view_pm.html",
            { 'pm' : pm ,
              'form' : form },
            context_instance = RequestContext(request))
        
            
        

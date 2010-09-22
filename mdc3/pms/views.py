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
    pm_rec_list = []
    for pm in pm_list:
        rec_list = Recipient.objects.filter(message=pm)
        read_list = []
        for rec in rec_list:
            read_list.append([rec,rec.read])
        pm_rec_list.append([pm , read_list])
        
    print pm_rec_list
    return render_to_response('pms/box.html',
            { 'pm_rec_list' : pm_rec_list },
            context_instance = RequestContext(request))

@login_required
def inbox(request):
    pm_list = PM.objects.filter(recipients=request.user).order_by('-created_on')
    read_list = []
    #can be made more efficient
    for pm in pm_list:
        read_list.append(Recipient.objects.get(
                recipient=request.user,
                message=pm).read)
    pm_read = zip(pm_list, read_list)
    return render_to_response('pms/inbox.html',
            { 'pm_read' : pm_read},
            context_instance = RequestContext(request))

@login_required
def mark_read(request):
    unread_list = Recipient.objects.filter(recipient=request.user,read=False)
    for rec in unread_list:
        rec.read = True
        rec.save()
    return HttpResponseRedirect("/pms/inbox")

@login_required
def view_pm(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)
    if pm.sender != request.user:
        read = get_object_or_404(Recipient,message=pm,recipient=request.user)
        if not read.read:
            read.read = True
            read.save()
    #this else is to make sure pms sent to oneself get marked read
    else:
        try:
            recip = Recipient.objects.get(message=pm,
                    recipient=request.user, read=False)
            recip.read=True
            recip.save()
        except Recipient.DoesNotExist:
            pass
    ## Moving this higher will probably improve performance
    ## think about security before doing so though
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.parent = pm
            new_pm.save()
            return HttpResponseRedirect("/pms/inbox")
    else:
        rec_str = pm.get_rec_str()
        form =forms.NewPMForm()
    return render_to_response("pms/view_pm.html",
            { 'pm' : pm ,
              'rec_str' : rec_str,
              'form' : form },
            context_instance = RequestContext(request))
        

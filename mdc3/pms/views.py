from copy import copy
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic import list_detail
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User
from django.db.models import Q



from models import PM, Recipient
from mdc3.profiles.models import Profile
import forms

@login_required
def new_pm(request, rec_id=0):    
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST)
        if form.is_valid():
            pm = form.save(request.user)
            pm.parent = pm
            pm.save()
            return HttpResponseRedirect("/pms/inbox")
    else:
        rec=''
        if rec_id:
            try:
                rec= User.objects.get(pk=rec_id)
            except User.DoesNotExist:
                pass
        form =forms.NewPMForm(initial={ 'recs':rec })
    return render_to_response('pms/new_pm.html',
            { 'form' : form },
            context_instance = RequestContext(request))


@login_required
def outbox(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    queryset = PM.objects.filter(sender=request.user,
                deleted=False).order_by('-created_on')

    paginator = Paginator(queryset, 25, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list

    rec_list = list(Recipient.objects.filter(message__in=pm_list).order_by(
        '-message__created_on').select_related('recipient'))

    for pm in pm_list:
        pm_rec_list = []
        while rec_list and pm.id == rec_list[0].message_id:
            pm_rec_list.append(rec_list[0])
            rec_list = rec_list[1:]
        pm.rec_list = pm_rec_list
        if pm.parent != pm:
            pm.reply = 'Re: '

    return render_to_response('pms/outbox.html',
            { 'pm_rec_list' : pm_list,
              'page_obj' : page_obj },
            context_instance = RequestContext(request))

@login_required
def inbox(request):
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    queryset = Recipient.objects.filter(recipient=request.user,
        deleted=False).order_by("-message__created_on").select_related(
        'message', 'message__sender')

    paginator = Paginator(queryset, 25, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list
    for pm in pm_list:
        if pm.message.parent != pm.message:
            pm.reply = 'Re: '
    
    return render_to_response('pms/inbox.html',
            { 'pm_list' : pm_list,
              'page_obj' : page_obj },
            context_instance = RequestContext(request))

@login_required
def mark_read(request):
    unread_list = Recipient.objects.filter(
        recipient=request.user,read=False).update(
            read=True)
    return HttpResponseRedirect("/pms/inbox")

@login_required
def view_pm(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)
    #make sure only the sender and recipients can read it
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
    
    reply = copy(pm)
    reply.body = ''
    reply.parent = pm.parent
    if not Profile.objects.get(user=request.user).show_images:
        pm.body = pm.body.replace('[img','(img)[url')
        pm.body = pm.body.replace('[/img]','[/url]')
        
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.parent = pm.parent
            new_pm.save()
            return HttpResponseRedirect("/pms/inbox")
    else:
        form =forms.NewPMForm(instance=reply,
                initial={'recs' : pm.sender.username })
    rec_str = pm.get_rec_str()
    return render_to_response("pms/view_pm.html",
            { 'pm' : pm ,
              'rec_str' : rec_str,
              'form' : form ,
              'reply_all' : pm.get_reply_all(request.user),
               'rec_str': rec_str},
            context_instance = RequestContext(request))

def pm_thread(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)

    
    queryset = PM.objects.filter(parent=pm.parent).filter(Q(
        Q(sender=request.user) | Q(
        recipient__recipient=request.user))).order_by(
        'created_on').select_related('body', 'subject',
            'deleted','sender__username').distinct()

    
    pm_list = list(queryset)
    for i, tpm in enumerate(pm_list):
        popped = False
        if tpm.sender==request.user and tpm.deleted:
            pm_list.pop(i)
            popped=True
        try:
            recip = Recipient.objects.get(message=tpm,
                    recipient=request.user, read=False)
            if not popped and recip.deleted:
                pm_list.pop(i)
            recip.read=True
            recip.save()
        except Recipient.DoesNotExist:
            pass
        if not Profile.objects.get(user=request.user).show_images:
            tpm.body = tpm.body.replace('[img','(img)[url')
            tpm.body = tpm.body.replace('[/img]','[/url]')
        
    reply = copy(pm)
    reply.body = ''
    reply.parent = pm.parent
    reply_recs = pm.sender.username
        
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.parent = pm.parent
            new_pm.save()
            return HttpResponseRedirect("/pms/inbox")
    else:
        form =forms.NewPMForm(instance=reply,
                initial={'recs' : reply_recs})
    return render_to_response("pms/show_thread.html",
            { 'pm_list' : queryset,
              'pm' : pm,
              'form' : form,
              'thread' : True,
              'reply_all' : pm.get_reply_all(request.user), },
            context_instance = RequestContext(request))
    
        
def del_pm(request, pm_id):
    pm = get_object_or_404(PM,pk=pm_id)
    if pm.sender == request.user:
        pm.deleted = True
        pm.save()
    rec_list = Recipient.objects.filter(message=pm)
    rec_list.filter(recipient=request.user).update(deleted=True)
    if pm.deleted and not rec_list.filter(deleted=False):
        pm.delete()
        rec_list.delete()
    return HttpResponseRedirect("/pms/inbox")

@login_required
def get_quote(request, id):
    pm = get_object_or_404(PM, pk=id)
    if not pm.check_privacy(request.user):
        raise Http404
    user = pm.sender

    return render_to_response("pms/get_quote.html", {
            'pm': pm,
            'user': user,
    })

from copy import copy
import re
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, Http404
from django.template.base import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse



from models import PM, Recipient
from arkestrator.profiles.models import Profile
import forms

@login_required
def new_pm(request, rec_id=0): 
    """ create a new pm """

    if request.method == 'POST':
        form =forms.NewPMForm(request.POST)
        if form.is_valid():
            pm = form.save(request.user)
            pm.root_parent = pm
            pm.save()
            return HttpResponseRedirect(reverse('inbox'))
    else:
        rec=''
        if rec_id:
            try:
                rec= User.objects.get(pk=rec_id)
            except User.DoesNotExist:
                pass
        form =forms.NewPMForm(initial={ 'recs':rec })
    return render(request, 'pms/new_pm.html', {'form': form})


@login_required
def outbox(request):
    """ all outgoing messages """
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    queryset = PM.objects.filter(sender=request.user,
                deleted=False).order_by('-created_at')

    paginator = Paginator(queryset, 50, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list

    rec_list = list(Recipient.objects.filter(message__in=pm_list).order_by(
        '-message__created_at').select_related('recipient'))

    for pm in pm_list:
        pm_rec_list = []
        while rec_list and pm.id == rec_list[0].message_id:
            pm_rec_list.append(rec_list[0])
            rec_list = rec_list[1:]
        pm.rec_list = pm_rec_list
        if pm.root_parent != pm:
            pm.reply = 'Re: '

    return render(request, 'pms/outbox.html',
            { 'pm_rec_list' : pm_list,
              'page_obj' : page_obj })

@login_required
def inbox(request):
    """ all incoming messages """
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404

    queryset = Recipient.objects.filter(recipient=request.user,
        deleted=False).order_by("-message__created_at").select_related(
        'message', 'message__sender')

    paginator = Paginator(queryset, 50, allow_empty_first_page=True)
    page_obj = paginator.page(page)

    pm_list = page_obj.object_list
    for pm in pm_list:
        if pm.message.root_parent != pm.message:
            pm.reply = 'Re: '
    
    return render(request, 'pms/inbox.html',
            { 'pm_list' : pm_list,
              'page_obj' : page_obj })

@login_required
def mark_read(request):
    """ mark all recipients the user has read """
    if request.method == 'POST' and request.POST['confirm'] == 'true':
        unread_list = Recipient.objects.filter(
                        recipient=request.user,
                        read=False).update(read=True)
    return HttpResponseRedirect(reverse('inbox'))

@login_required
def view_pm(request, pm_id):
    """ display pm pm_id and if appropriate it's parent """
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
    
        
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.root_parent = pm.root_parent
            new_pm.parent = pm
            new_pm.save()
            return HttpResponseRedirect(reverse('inbox'))
    else:
        form =forms.NewPMForm(instance=reply,
                initial={'recs' : pm.sender.username })
    rec_str = pm.get_rec_str()
    parent = pm.parent
    parent_rec_str = ''
    if parent:
        if parent.check_privacy(request.user) and parent.not_deleted(request.user):
            parent_rec_str = parent.get_rec_str()
        else:
            parent=None
    hide=False
    if not Profile.objects.get(user=request.user).show_images:
        hide=True
    return render(request, "pms/view_pm.html",
            { 'pm' : pm ,
              'parent' : parent,
              'rec_str' : rec_str,
              'parent_rec_str' : parent_rec_str,
              'form' : form ,
              'reply_all' : pm.get_reply_all(request.user),
               'rec_str': rec_str,
               'hide' : hide, })

def pm_thread(request, pm_id):
    """ view all appropriate pms with the same root_parent as pm_id """
    pm = get_object_or_404(PM,pk=pm_id)

    
    queryset = PM.objects.filter(root_parent=pm.root_parent).filter(Q(
        Q(sender=request.user) | Q(
        recipient__recipient=request.user))).order_by(
        'created_at').select_related('body',
            'deleted','sender__username').distinct()

    
    pm_list = list(queryset)
    img_start = re.compile('\[img', re.IGNORECASE)
    img_end = re.compile('\[/img\]', re.IGNORECASE)
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
        
    reply = copy(pm)
    reply.body = ''
    reply.root_parent = pm.root_parent
    reply_recs = pm.sender.username
        
    if request.method == 'POST':
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.root_parent = pm.root_parent
            new_pm.save()
            return HttpResponseRedirect(reverse('inbox'))
    else:
        form =forms.NewPMForm(instance=reply,
                initial={'recs' : reply_recs})
    hide = False
    if not request.user.profile.show_images:
        hide=True
    return render(request, "pms/show_thread.html",
            { 'pm_list' : queryset,
              'pm' : pm,
              'form' : form,
              'thread' : True,
              'reply_all' : pm.get_reply_all(request.user), 
              'hide' : hide, })
    
        
def del_pm(request, pm_id):
    """ delete pm pm_id for a user """
    pm = get_object_or_404(PM,pk=pm_id)
    if request.method == 'POST' and request.POST['confirm'] == 'true':
        if pm.sender == request.user:
            pm.deleted = True
            pm.save()
        rec_list = Recipient.objects.filter(message=pm)
        rec_list.filter(recipient=request.user).update(deleted=True)
        if pm.deleted and not rec_list.filter(deleted=False):
            pm.body = ''
            pm.subject = 'deleted'
            pm.save()
    return HttpResponseRedirect(reverse('inbox'))

@login_required
def get_quote(request, id):
    """ if allowed get a quote of pm id """
    pm = get_object_or_404(PM, pk=id)
    if not pm.check_privacy(request.user):
        raise Http404
    user = pm.sender

    return render_to_response("pms/get_quote.html", {
            'pm': pm,
            'user': user,
    })

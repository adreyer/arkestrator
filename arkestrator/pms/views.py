from copy import copy
import re

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView

import forms
from models import PM, Recipient
from arkestrator.profiles.models import Profile
from arkestrator.views import LoginRequiredMixin

class NewPM(LoginRequiredMixin, FormView):
    """ create a new pm """
    template_name = 'pms/new_pm.html'
    form_class = forms.NewPMForm

    def get_success_url(self):
        return reverse('inbox')

    def form_valid(self, form):
        pm = form.save(self.request.user)
        pm.root_parent = pm
        pm.save()
        return super(NewPM, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx =  super(NewPM, self).get_context_data(**kwargs)
        rec = self.request.GET.get('recipient')
        if rec:
            ctx['form'].initial['recs'] = rec
        #import ipdb; ipdb.set_trace()
        return ctx

class Outbox(LoginRequiredMixin, TemplateView):
    template_name = 'pms/outbox.html'

    def get_context_data(self, **kwargs):
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            raise Http404

        queryset = PM.objects.filter(sender=self.request.user,
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

        ctx = { 'pm_rec_list' : pm_list,
              'page_obj' : page_obj }
        return ctx

class Inbox(LoginRequiredMixin, TemplateView):
    template_name = 'pms/inbox.html'

    def get_context_data(self, **kwargs):
        try:
            page = int(self.request.GET.get('page', 1))
        except ValueError:
            raise Http404

        queryset = Recipient.objects.filter(recipient=self.request.user,
                deleted=False).order_by("-message__created_at").select_related(
                        'message', 'message__sender')

        paginator = Paginator(queryset, 50, allow_empty_first_page=True)
        page_obj = paginator.page(page)

        pm_list = page_obj.object_list
        for pm in pm_list:
            if pm.message.root_parent != pm.message:
                pm.reply = 'Re: '

        ctx = { 'pm_list' : pm_list,
                'page_obj' : page_obj }
        return ctx


class MarkRead(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        unread_list = Recipient.objects.filter(
                        recipient=request.user,
                        read=False).update(read=True)
        return HttpResponseRedirect(reverse('inbox'))

class PMDetail(LoginRequiredMixin, TemplateView):
    template_name = "pms/view_pm.html"

    def read_pm(self, pm_id, user):
        pm = get_object_or_404(PM,pk=pm_id)
        #make sure only the sender and recipients can read it
        if pm.sender != user:
            read = get_object_or_404(Recipient,message=pm,recipient=user)
            if not read.read:
                read.read = True
                read.save()
        #this else is to make sure pms sent to oneself get marked read
        else:
            try:
                recip = Recipient.objects.get(message=pm, recipient=user, read=False)
                recip.read = True
                recip.save()
            except Recipient.DoesNotExist:
                pass
        return pm

    def post(self, request, **kwargs):
        pm = self.read_pm(kwargs['pm_id'], request.user)
        reply = copy(pm)
        form =forms.NewPMForm(request.POST,
                instance=reply)
        if form.is_valid():
            new_pm = form.save(request.user)
            new_pm.root_parent = pm.root_parent
            new_pm.parent = pm
            new_pm.save()
            return HttpResponseRedirect(reverse('inbox'))

    def get_context_data(self, **kwargs):
        user = self.request.user
        pm = self.read_pm(kwargs['pm_id'], user)
        reply = copy(pm)
        reply.body = ''

        form =forms.NewPMForm(instance=reply,
                initial={'recs' : pm.sender.username })
        rec_str = pm.get_rec_str()
        parent = pm.parent
        parent_rec_str = ''
        if parent:
            if parent.check_privacy(user) and parent.not_deleted(user):
                parent_rec_str = parent.get_rec_str()
            else:
                parent = None
        hide = False
        if not Profile.objects.get(user=user).show_images:
            hide = True
        ctx = { 'pm' : pm ,
                'parent' : parent,
                'rec_str' : rec_str,
                'parent_rec_str' : parent_rec_str,
                'form' : form ,
                'reply_all' : pm.get_reply_all(user),
                'rec_str': rec_str,
                'hide' : hide, }
        return ctx

class PMThread(PMDetail):
    template_name = 'pms/show_thread.html'

    # TODO: take advantage of super
    def get_context_data(self, **kwargs):
        user = self.request.user
        pm = self.read_pm(kwargs['pm_id'], user)

        queryset = PM.objects.filter(root_parent=pm.root_parent).filter(Q(
            Q(sender=user) | Q(
            recipient__recipient=user))).order_by(
            'created_at').select_related('body', 'subject',
                'deleted','sender__username').distinct()

        pm_list = list(queryset)
        img_start = re.compile('\[img', re.IGNORECASE)
        img_end = re.compile('\[/img\]', re.IGNORECASE)
        for i, tpm in enumerate(pm_list):
            popped = False
            if tpm.sender == user and tpm.deleted:
                pm_list.pop(i)
                popped=True
            try:
                recip = Recipient.objects.get(message=tpm,
                        recipient=user, read=False)
                if not popped and recip.deleted:
                    pm_list.pop(i)
                recip.read=True
                recip.save()
            except Recipient.DoesNotExist:
                pass

        reply = copy(pm)
        reply.body = ''
        form =forms.NewPMForm(instance=reply,
                initial={'recs' : pm.sender.username })

        hide = False
        if not user.get_profile().show_images:
            hide=True
        ctx = { 'pm_list' : queryset,
                'pm' : pm,
                'form' : form,
                'thread' : True,
                #TODO: This isn't displayed
                'reply_all' : pm.get_reply_all(user),
                'hide' : hide, }
        return ctx

class DeletePM(LoginRequiredMixin, View):
    # Should this be a DELETE?
    def post(self, request, **kwargs):
        pm = get_object_or_404(PM,pk=kwargs['pm_id'])
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

class PMQuote(LoginRequiredMixin, TemplateView):
    template_name = "pms/get_quote.html"

    def get_context_data(self, **kwargs):
        pm = get_object_or_404(PM, pk=kwargs['pm_id'])
        if not pm.check_privacy(self.request.user):
            raise Http404
        user = pm.sender

        return { 'pm': pm, 'user': user,}

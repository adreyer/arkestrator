from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import forms
from django.db.models import Q
from bbcode.fields import BBCodeFormField
from mdc3.board.models import Thread, Post, LastRead


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('subject',)
        widgets = {
            'subject': forms.TextInput(attrs={'size': 70, 'maxlength': 160})
        }

    def clean_subject(self):
        subj = self.cleaned_data["subject"]
        subj = subj.strip()
        if subj  == '':
            raise forms.ValidationError("whitespace is not a subject")
        return subj
                    

class PostForm(forms.ModelForm):
    class Meta:
        auto_id = False
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'cols': 70, 'rows': 12})
        }

class PMForm(forms.Form):
    recipients = forms.CharField(required = True,
            label = "To:", widget = forms.TextInput(attrs = {'size': 70}))
    subject = forms.CharField(required=True, label = "Subject:",
            widget = forms.TextInput(attrs = {'size': 70, 'maxlength': 160}))
    body = BBCodeFormField(required = True,
            label = "Body:", 
            widget = forms.Textarea(attrs={'cols': 70, 'rows': 12}))

    def clean_recipients(self):
        recipient_list = self.cleaned_data['recipients'].split()
        user_list = []
        for rec in recipient_list:
            try:
                user_list.append(User.objects.get(username=rec))
            except User.DoesNotExist:
                raise forms.ValidationError(("User "+ rec +" not found"))
                                            
        self.cleaned_data['recipients_user'] = set(user_list)
        return self.cleaned_data

    def save(self, thread_factory, post_factory, poster):
        threads = []
        for user in self.cleaned_data['recipients_user']:
            try:
                thread = Thread.objects.get(Q(
                    Q(creator=poster) & Q(recipient=user) |
                    Q(creator=user) & Q(recipient=poster)))
                if thread.delete_by:
                    thread.deleted_by = None
                    thread.save()
            except Thread.DoesNotExist:                                   
                tf = ThreadForm(self.cleaned_data, 
                    instance = thread_factory(recipient = user))
                thread = tf.save()

            pf = PostForm(self.cleaned_data, 
                instance = post_factory(thread = thread))
            post = pf.save()
            threads.append(thread)
            try:
                LastRead.objects.get(
                    user = user,
                    thread = thread,
                )
            except LastRead.DoesNotExist:
                LastRead.objects.create(
                    user = user,
                    thread = thread,
                    post = None,
                )
                
        return threads

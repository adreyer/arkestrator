from django import forms
from mdc3.board.models import Thread, Post
from django.contrib.sites.models import Site

class ThreadForm(forms.Form):
    subject = forms.CharField(max_length=60, required=True)
    body = forms.CharField(widget=forms.Textarea, required=True)

    def save(self, user):
        thread = Thread.on_site.create(
            creator = user,
            last_post_by = user,
            subject = self.cleaned_data['subject'],
            site = Site.objects.get_current(),
        )
        Post.objects.create(
            thread = thread,
            creator = user,
            body = self.cleaned_data['body']
        )
        return thread

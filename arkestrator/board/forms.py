import string
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import forms
from django.db.models import Q
from arkestrator.board.models import Thread, Post, LastRead
import bbking

class ThreadForm(forms.ModelForm):
    """ a form for a new thread must be used with PostForm """
    class Meta:
        model = Thread
        fields = ('subject',)
        widgets = {
            'subject': forms.TextInput(attrs={'size': 70, 'maxlength': 160})
        }

    def clean_subject(self):
        """ remove leading and trailing whitespace from a subject """
        subj = self.cleaned_data["subject"]
        subj = subj.strip(bbking.NON_PRINTING)
        if subj  == '':
            raise forms.ValidationError("whitespace is not a subject")
        return subj

class PostForm(forms.ModelForm):
    """ a form for a new Post """
    class Meta:
        auto_id = False
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'cols': 70, 'rows': 12})
        }

    def clean_body(self):
        naked = self.cleaned_data['body'].strip(bbking.NON_PRINTING)

        if not naked: # lol
            raise forms.ValidationError("This post doesn't say enough.")

        try:
            compiled = bbking.compile(naked)
            if len(compiled) < 1:
                raise forms.ValidationError("This post doesn't say enough.")
        except bbking.CompilationError:
            pass

        return naked

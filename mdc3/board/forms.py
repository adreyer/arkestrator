from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import forms
from django.db.models import Q
from mdc3.board.models import Thread, Post, LastRead


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
        subj = subj.strip()
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

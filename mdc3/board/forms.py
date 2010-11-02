from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django import forms
from django.db.models import Q
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

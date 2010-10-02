from django import forms
from mdc3.board.models import Thread, Post
from django.contrib.sites.models import Site

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ('subject',)

    def clean_subject(self):
        self.cleaned_data["subject"] = self.cleaned_data["subject"].strip()
        if self.cleaned_data["subject"] == '':
            raise forms.ValidationError("whitespace is not a subject")
        return self.cleaned_data
                    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

